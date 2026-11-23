#!/usr/bin/env node
/** Compare two PNG screenshots and report pixel difference. */
import { readFile, writeFile } from "node:fs/promises";
import { createRequire } from "node:module";
import process from "node:process";

const require = createRequire(import.meta.url);
let PNG;
try {
  ({ PNG } = require("pngjs"));
} catch {
  console.error("compare-prototype-shot.mjs requires the host pngjs package");
  process.exit(2);
}

function usage(message) {
  if (message) console.error(message);
  console.error("Usage: node compare-prototype-shot.mjs <baseline.png> <current.png> [--output <file>]");
  process.exit(2);
}

async function main() {
  const argv = process.argv.slice(2);
  if (argv.length < 2) usage();
  const baselinePath = argv[0];
  const currentPath = argv[1];
  const outputIndex = argv.indexOf("--output");
  const output = outputIndex >= 0 ? argv[outputIndex + 1] : null;
  const baseline = PNG.sync.read(await readFile(baselinePath));
  const current = PNG.sync.read(await readFile(currentPath));
  const width = Math.min(baseline.width, current.width);
  const height = Math.min(baseline.height, current.height);
  let difference = 0;
  let compared = 0;
  for (let y = 0; y < height; y += 1) {
    for (let x = 0; x < width; x += 1) {
      const a = (y * baseline.width + x) * 4;
      const b = (y * current.width + x) * 4;
      difference += Math.abs(baseline.data[a] - current.data[b]);
      difference += Math.abs(baseline.data[a + 1] - current.data[b + 1]);
      difference += Math.abs(baseline.data[a + 2] - current.data[b + 2]);
      compared += 765;
    }
  }
  const result = {
    baseline: baselinePath,
    current: currentPath,
    dimensions: { baseline: [baseline.width, baseline.height], current: [current.width, current.height], compared: [width, height] },
    meanAbsoluteDifference: compared ? Number((difference / compared).toFixed(4)) : 1,
    changedRatio: compared ? Number((difference / compared).toFixed(4)) : 1,
  };
  if (output) await writeFile(output, `${JSON.stringify(result, null, 2)}\n`, "utf8");
  console.log(JSON.stringify(result, null, 2));
}

main().catch((error) => {
  console.error(error && error.stack ? error.stack : String(error));
  process.exit(1);
});
