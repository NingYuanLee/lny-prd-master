#!/usr/bin/env node
/**
 * Migrate legacy ui_manifest.md (embedded PAGE/COMP bodies) into ui/PAGE-*.md
 * and ui/COMP-*.md. Unrecognized layouts exit 2 for manual migration.
 *
 * Usage:
 *   node migrate-prd-structure.mjs --root <prdRoot> [--dry-run]
 */
import fs from "node:fs";
import path from "node:path";

function parseArgs(argv) {
  let root = process.cwd();
  let dryRun = false;
  for (let i = 2; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === "--dry-run") {
      dryRun = true;
    } else if (arg === "--root") {
      root = argv[i + 1];
      i += 1;
    } else if (arg.startsWith("--root=")) {
      root = arg.slice("--root=".length);
    } else {
      console.error(`unknown argument: ${arg}`);
      process.exit(1);
    }
  }
  return { root: path.resolve(root), dryRun };
}

function failManual(reason) {
  console.error(`需人工迁移: ${reason}`);
  process.exit(2);
}

function extractSections(markdown, headingPattern) {
  const lines = markdown.split(/\r?\n/);
  const hits = [];
  for (let i = 0; i < lines.length; i += 1) {
    const match = lines[i].match(headingPattern);
    if (match) {
      hits.push({ index: i, id: match[1], title: match[2] ? match[2].trim() : "" });
    }
  }
  const sections = [];
  for (let i = 0; i < hits.length; i += 1) {
    const start = hits[i].index;
    const end = i + 1 < hits.length ? hits[i + 1].index : lines.length;
    sections.push({
      id: hits[i].id,
      title: hits[i].title,
      body: lines.slice(start, end).join("\n").trim() + "\n",
    });
  }
  return sections;
}

function main() {
  const { root, dryRun } = parseArgs(process.argv);
  const manifestPath = path.join(root, "ui_manifest.md");
  if (!fs.existsSync(manifestPath)) {
    failManual(`missing ${manifestPath}`);
  }

  const source = fs.readFileSync(manifestPath, "utf8");
  const pageHeading = /^#{2,3}\s+(PAGE-[A-Z]+-\d{3})\s*(.*)$/;
  const compHeading = /^#{2,3}\s+(COMP-\d{3})\s*(.*)$/;
  const pages = extractSections(source, pageHeading);
  const comps = extractSections(source, compHeading);

  const hasLegacyBodies =
    /##\s*[56]\.?\s*(分页面|组件|页面详述|局部自定义)/.test(source) ||
    pages.length > 0 ||
    comps.length > 0;

  if (!hasLegacyBodies) {
    console.log("no embedded PAGE/COMP bodies detected; nothing to migrate");
    process.exit(0);
  }

  if (pages.length === 0 && comps.length === 0) {
    failManual("found legacy section titles but no PAGE-*/COMP-* headings");
  }

  const uiDir = path.join(root, "ui");
  const planned = [];
  for (const page of pages) {
    planned.push({ file: path.join(uiDir, `${page.id}.md`), body: page.body });
  }
  for (const comp of comps) {
    planned.push({ file: path.join(uiDir, `${comp.id}.md`), body: comp.body });
  }

  if (dryRun) {
    console.log(`[dry-run] would write ${planned.length} file(s):`);
    for (const item of planned) {
      console.log(`  ${path.relative(root, item.file)}`);
    }
    process.exit(0);
  }

  fs.mkdirSync(uiDir, { recursive: true });
  for (const item of planned) {
    fs.writeFileSync(item.file, item.body, "utf8");
    console.log(`wrote ${path.relative(root, item.file)}`);
  }
  console.log(
    "migration wrote detail files; trim remaining bodies from ui_manifest.md so it keeps index only",
  );
}

main();
