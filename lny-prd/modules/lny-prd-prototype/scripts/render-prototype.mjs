#!/usr/bin/env node
/** Render prototype pages and keep browser screenshots for visual review. */
import { execFile } from "node:child_process";
import { mkdir, readdir, writeFile } from "node:fs/promises";
import { promisify } from "node:util";
import { join, resolve } from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";

const execFileAsync = promisify(execFile);
const skillDirectory = resolve(join(fileURLToPath(new URL(".", import.meta.url)), ".."));
const verifyScript = join(skillDirectory, "scripts", "verify-prototype-browser.mjs");

function usage(message) {
  if (message) console.error(message);
  console.error("Usage: node render-prototype.mjs <prdRoot> [--page PAGE-...] [--output <dir>]");
  process.exit(2);
}

function parseArgs(argv) {
  if (!argv.length) usage();
  const result = { root: resolve(argv[0]), pages: [], output: null };
  for (let index = 1; index < argv.length; index += 1) {
    const arg = argv[index];
    if (arg === "--page") {
      if (!argv[index + 1]) usage("--page requires a PAGE id");
      result.pages.push(argv[++index]);
    } else if (arg === "--output") {
      if (!argv[index + 1]) usage("--output requires a directory");
      result.output = resolve(argv[++index]);
    } else {
      usage(`unknown argument: ${arg}`);
    }
  }
  result.output ||= join(result.root, "prototypes", ".visual-review");
  return result;
}

async function collectScreenshots(output) {
  const pages = [];
  for (const terminal of await readdir(output, { withFileTypes: true })) {
    if (!terminal.isDirectory()) continue;
    for (const entry of await readdir(join(output, terminal.name))) {
      if (entry.endsWith(".png")) {
        pages.push({
          terminal: terminal.name,
          page: entry.slice(0, -4),
          screenshot: join(output, terminal.name, entry),
        });
      }
    }
  }
  return pages.sort((a, b) => a.page.localeCompare(b.page));
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  await mkdir(args.output, { recursive: true });
  const verifyArgs = [verifyScript, args.root, "--artifacts", args.output, "--keep-screenshots"];
  for (const page of args.pages) verifyArgs.push("--page", page);
  try {
    const result = await execFileAsync(process.execPath, verifyArgs, {
      cwd: skillDirectory,
      encoding: "utf8",
      env: process.env,
      maxBuffer: 8 * 1024 * 1024,
    });
    if (result.stdout) process.stdout.write(result.stdout);
    if (result.stderr) process.stderr.write(result.stderr);
  } catch (error) {
    if (error.stdout) process.stdout.write(error.stdout);
    if (error.stderr) process.stderr.write(error.stderr);
    process.exit(error.code || 1);
  }
  const pages = await collectScreenshots(args.output);
  const manifest = {
    generatedAt: new Date().toISOString(),
    root: args.root,
    output: args.output,
    pages,
  };
  await writeFile(join(args.output, "render-manifest.json"), `${JSON.stringify(manifest, null, 2)}\n`, "utf8");
  console.log(`rendered ${pages.length} page screenshot(s)`);
}

main().catch((error) => {
  console.error(error && error.stack ? error.stack : String(error));
  process.exit(1);
});
