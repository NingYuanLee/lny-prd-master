#!/usr/bin/env node
/** Negative regression coverage for the browser-level prototype validator. */
import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { mkdtemp, mkdir, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import process from "node:process";
import { promisify } from "node:util";
import { fileURLToPath } from "node:url";

const execFileAsync = promisify(execFile);
const REPO = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const VALIDATOR = join(
  REPO,
  "lny-prd-prototype",
  "scripts",
  "verify-prototype-browser.mjs"
);

const STYLE = `
<style>
  html, body { margin: 0; min-height: 100%; font-family: Arial, sans-serif; }
  .md-mobile-page { width: 100%; min-height: 844px; color: #111827; background: #f3f4f6; }
  header { box-sizing: border-box; min-height: 88px; padding: 20px; color: white; background: #164e63; }
  h1, p { margin: 0 0 8px; }
  .grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; padding: 16px; }
  .tile { min-height: 72px; }
  .md-menu { display: none; }
  .md-menu.is-open { display: block; }
</style>`;

const TILES = [
  "#ef4444",
  "#f97316",
  "#eab308",
  "#22c55e",
  "#06b6d4",
  "#3b82f6",
  "#8b5cf6",
  "#ec4899",
  "#64748b",
]
  .map((color, index) => `<div class="tile" style="background:${color}">tile ${index + 1}</div>`)
  .join("");

function documentFor(id, { title = id, head = "", extra = "", script = "" } = {}) {
  return `<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>${title} fixture</title>${STYLE}${head}</head>
<body>
  <main class="md-mobile-page">
    <header><h1>${id}</h1><p>Browser validator regression fixture with visible content.</p></header>
    <section class="grid">${TILES}</section>
    ${extra}
  </main>
  ${script}
</body>
</html>`;
}

async function writeFixture(root) {
  const directory = join(root, "prototypes", "MP");
  await mkdir(directory, { recursive: true });
  const pages = new Map([
    ["PAGE-MP-001", documentFor("PAGE-MP-001")],
    ["PAGE-MP-002", documentFor("PAGE-MP-002", { title: "wrong-title" })],
    [
      "PAGE-MP-003",
      documentFor("PAGE-MP-003", {
        head: '<link rel="stylesheet" href="http://127.0.0.1:9/external.css">',
      }),
    ],
    [
      "PAGE-MP-004",
      documentFor("PAGE-MP-004", {
        extra: '<img src="./missing.png" alt="missing regression image">',
      }),
    ],
    [
      "PAGE-MP-005",
      documentFor("PAGE-MP-005", {
        extra: '<div style="width:800px;height:12px;background:#111">overflow</div>',
      }),
    ],
    [
      "PAGE-MP-006",
      documentFor("PAGE-MP-006", {
        extra: '<button type="button" data-menu="missingMenu">Open menu</button>',
      }),
    ],
    [
      "PAGE-MP-007",
      documentFor("PAGE-MP-007", {
        script: '<script>console.error("intentional browser regression");</script>',
      }),
    ],
    [
      "PAGE-MP-008",
      "<!doctype html><html><head><title>PAGE-MP-008 blank</title></head><body></body></html>",
    ],
  ]);
  await Promise.all(
    Array.from(pages, ([id, content]) =>
      writeFile(join(directory, `${id}.html`), content, "utf8")
    )
  );
}

async function main() {
  const root = await mkdtemp(join(tmpdir(), "lny-prd-browser-regression-"));
  try {
    await writeFixture(root);
    let output = "";
    try {
      await execFileAsync(process.execPath, [VALIDATOR, root], {
        cwd: REPO,
        encoding: "utf8",
        env: process.env,
        maxBuffer: 1024 * 1024,
      });
      assert.fail("browser validator accepted all negative fixtures");
    } catch (error) {
      if (error && error.code === "ERR_ASSERTION") throw error;
      assert.equal(error.code, 1, `unexpected browser validator exit: ${error.code}`);
      output = `${error.stdout || ""}${error.stderr || ""}`;
    }

    const expected = [
      "<title> must start with PAGE-MP-002",
      "external runtime resource breaks offline preview",
      "broken image:",
      "document overflows viewport horizontally",
      "[data-menu] references missing #missingMenu",
      "console: intentional browser regression",
      "missing or invisible md-mobile-page/md-d1 root",
    ];
    for (const fragment of expected) {
      assert.match(output, new RegExp(fragment.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")));
    }
    assert.doesNotMatch(output, /^- PAGE-MP-001$/m, "healthy fixture was rejected");
    console.log("prototype browser negative regressions ok: 7 failures detected, healthy page accepted");
  } finally {
    await rm(root, { recursive: true, force: true });
  }
}

main().catch((error) => {
  console.error(error && error.stack ? error.stack : String(error));
  process.exit(1);
});
