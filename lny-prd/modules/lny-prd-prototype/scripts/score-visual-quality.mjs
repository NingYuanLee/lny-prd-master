#!/usr/bin/env node
/** Score prototype visual readiness from HTML structure and rendered screenshots. */
import { readFile, writeFile } from "node:fs/promises";
import { existsSync } from "node:fs";
import { createRequire } from "node:module";
import { join, resolve } from "node:path";
import process from "node:process";

const require = createRequire(import.meta.url);
let PNG;
try {
  ({ PNG } = require("pngjs"));
} catch {
  console.error("score-visual-quality.mjs requires the host pngjs package");
  process.exit(2);
}

function usage(message) {
  if (message) console.error(message);
  console.error("Usage: node score-visual-quality.mjs <prdRoot> [--render-dir <dir>] [--output <file>]");
  process.exit(2);
}

function parseArgs(argv) {
  if (!argv.length) usage();
  const result = { root: resolve(argv[0]), renderDir: null, output: null };
  for (let index = 1; index < argv.length; index += 1) {
    if (argv[index] === "--render-dir") result.renderDir = resolve(argv[++index] || usage("--render-dir requires a directory"));
    else if (argv[index] === "--output") result.output = resolve(argv[++index] || usage("--output requires a file"));
    else usage(`unknown argument: ${argv[index]}`);
  }
  result.renderDir ||= join(result.root, "prototypes", ".visual-review");
  result.output ||= join(result.renderDir, "visual-score.json");
  return result;
}

function count(text, pattern) {
  return (text.match(pattern) || []).length;
}

function imageSignal(path) {
  if (!existsSync(path)) return { score: 0, reason: "missing screenshot" };
  const png = PNG.sync.read(require("node:fs").readFileSync(path));
  const buckets = new Set();
  let nonWhite = 0;
  for (let offset = 0; offset < png.data.length; offset += 16) {
    const r = png.data[offset];
    const g = png.data[offset + 1];
    const b = png.data[offset + 2];
    buckets.add(`${r >> 4}-${g >> 4}-${b >> 4}`);
    if (r < 245 || g < 245 || b < 245) nonWhite += 1;
  }
  const diversity = Math.min(1, buckets.size / 24);
  const coverage = Math.min(1, nonWhite / Math.max(1, png.data.length / 16) / 0.35);
  return { score: Math.round((diversity * 0.45 + coverage * 0.55) * 100), width: png.width, height: png.height };
}

function visualSystemSignal(html) {
  const signals = {
    customTokens: /--[a-z0-9-]+\s*:/i.test(html),
    typography: /(font-family|font-size|font-weight|letter-spacing)\s*:/i.test(html),
    surfaces: /(border-radius|box-shadow|background(?:-image)?|linear-gradient)\s*:/i.test(html),
    spacing: /(padding|margin|gap)\s*:/i.test(html),
    responsive: /@media\b/i.test(html),
    brandedAsset: /<(img|svg)\b/i.test(html),
    layeredComposition: /(::before|::after|position\s*:\s*(absolute|relative|sticky)|transform\s*:)/i.test(html),
  };
  return {
    score: Math.round(Object.values(signals).filter(Boolean).length / Object.keys(signals).length * 100),
    signals,
    antiPatterns: {
      titleAccentBorder: /(?:title|heading|section)[^{}]{0,80}\{[^}]*border-left\s*:/i.test(html),
      pillOveruse: count(html, /border-radius\s*:\s*9999px/gi) > 4,
      heavyShadowUse: count(html, /box-shadow\s*:/gi) > 8,
      uniformCardPattern: count(html, /(?:card|tile|panel)/gi) > 6 && count(html, /border-radius\s*:/gi) > 8,
    },
  };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const manifestPath = join(args.renderDir, "render-manifest.json");
  if (!existsSync(manifestPath)) usage(`render manifest not found: ${manifestPath}`);
  const manifest = JSON.parse(await readFile(manifestPath, "utf8"));
  const pages = [];
  for (const item of manifest.pages || []) {
    const htmlPath = join(args.root, "prototypes", item.terminal, `${item.page}.html`);
    const html = await readFile(htmlPath, "utf8");
    const checks = {
      hasTitle: /<title\b[^>]*>\s*[^<]+<\/title>/i.test(html),
      hasVisibleText: count(html, /[\u3400-\u9fff]/g) >= 4 || count(html, /[A-Za-z]{3,}/g) >= 4,
      hasStructuredSections: count(html, /data-section=|<main\b|<section\b/gi) >= 2,
      hasInteraction: /<(a|button|input|select|textarea)\b/i.test(html),
      hasAssetReferences: /(?:src|href)=["'][^"']+\.(png|jpe?g|webp|svg|css|js)/i.test(html),
      hasStateHooks: /data-(state|comp|skel|empty)-for=/i.test(html),
    };
    const structuralScore = Math.round(Object.values(checks).filter(Boolean).length / Object.keys(checks).length * 100);
    const image = imageSignal(item.screenshot);
    const visualSystem = visualSystemSignal(html);
    // This is an implementation-readiness signal. The agent must still inspect
    // the rendered screenshots with the visual self-review protocol.
    const implementationScore = Math.round(structuralScore * 0.45 + image.score * 0.55);
    const visualReadiness = Math.round(implementationScore * 0.4 + visualSystem.score * 0.35 + image.score * 0.25);
    const score = Math.min(89, visualReadiness);
    const issues = [];
    if (!checks.hasTitle) issues.push("missing title");
    if (!checks.hasStructuredSections) issues.push("few structured sections");
    if (!checks.hasInteraction) issues.push("no interactive control detected");
    if (!checks.hasAssetReferences) issues.push("no local visual asset reference detected");
    if (!checks.hasStateHooks) issues.push("no state visual hook detected");
    if (image.score < 45) issues.push("weak rendered visual signal");
    if (visualSystem.score < 70) issues.push("limited visual-system evidence; review hierarchy and brand expression");
    if (visualSystem.antiPatterns.titleAccentBorder) issues.push("possible title accent-border pattern; verify it serves the page task");
    if (visualSystem.antiPatterns.pillOveruse) issues.push("possible pill overuse; verify labels are not replacing hierarchy");
    if (visualSystem.antiPatterns.heavyShadowUse) issues.push("heavy shadow use; verify surfaces are not compensating for weak structure");
    if (visualSystem.antiPatterns.uniformCardPattern) issues.push("uniform card pattern; verify the page is not using one template for every section");
    issues.push("automated score does not replace the agent visual self-review");
    pages.push({ page: item.page, terminal: item.terminal, score, implementationScore, visualReadiness, visualSystemScore: visualSystem.score, imageScore: image.score, checks, visualSystem, issues });
  }
  const overall = pages.length ? Math.round(pages.reduce((sum, page) => sum + page.score, 0) / pages.length) : 0;
  const report = { generatedAt: new Date().toISOString(), overall, threshold: 80, scoreMeaning: "implementation and visual-system signal; evidence-backed agent visual self-review remains required", selfReview: { required: true, status: "missing", protocol: "reference-visual-self-review.md" }, passed: pages.length > 0 && overall >= 80 && pages.every((page) => page.score >= 70), pages };
  await writeFile(args.output, `${JSON.stringify(report, null, 2)}\n`, "utf8");
  console.log(`visual score ${overall}/100 ${report.passed ? "passed" : "needs revision"}`);
  if (!report.passed) process.exitCode = 1;
}

main().catch((error) => {
  console.error(error && error.stack ? error.stack : String(error));
  process.exit(1);
});
