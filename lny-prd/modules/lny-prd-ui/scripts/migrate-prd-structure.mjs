#!/usr/bin/env node
/**
 * Migrate legacy ui_manifest.md (embedded PAGE/COMP bodies) into ui/PAGE-*.md
 * and ui/COMP-*.md. Unrecognized layouts exit 2 for manual migration.
 *
 * Usage:
 *   node migrate-prd-structure.mjs --root <prdRoot> [--dry-run] [--force]
 */
import fs from "node:fs";
import path from "node:path";

function parseArgs(argv) {
  let root = process.cwd();
  let dryRun = false;
  let force = false;
  for (let i = 2; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === "--dry-run") {
      dryRun = true;
    } else if (arg === "--force") {
      force = true;
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
  return { root: path.resolve(root), dryRun, force };
}

function failManual(reason) {
  console.error(`需人工迁移: ${reason}`);
  process.exit(2);
}

function extractSections(markdown) {
  const lines = markdown.split(/\r?\n/);
  const hits = [];
  for (let i = 0; i < lines.length; i += 1) {
    const match = lines[i].match(/^(#{2,3})\s+((?:PAGE-[A-Z]+-\d{3})|(?:COMP-\d{3}))\s*(.*)$/);
    if (match) {
      hits.push({
        index: i,
        level: match[1].length,
        id: match[2],
        title: match[3] ? match[3].trim() : "",
      });
    }
  }
  const sections = [];
  for (let i = 0; i < hits.length; i += 1) {
    const start = hits[i].index;
    let end = lines.length;
    for (let lineIndex = start + 1; lineIndex < lines.length; lineIndex += 1) {
      const heading = lines[lineIndex].match(/^(#+)\s+/);
      if (heading && heading[1].length <= hits[i].level) {
        end = lineIndex;
        break;
      }
    }
    sections.push({
      id: hits[i].id,
      title: hits[i].title,
      body: lines.slice(start, end).join("\n").trim() + "\n",
    });
  }
  return sections;
}

function writeTransaction(items) {
  const suffix = `.lny-prd-${process.pid}-${Date.now()}`;
  const staged = items.map((item) => ({
    ...item,
    existed: fs.existsSync(item.file),
    temp: item.file + suffix + ".tmp",
    backup: item.file + suffix + ".bak",
  }));

  try {
    for (const item of staged) {
      fs.mkdirSync(path.dirname(item.file), { recursive: true });
      fs.writeFileSync(item.temp, item.body, { encoding: "utf8", flag: "wx" });
    }
    for (const item of staged) {
      if (item.existed) {
        fs.renameSync(item.file, item.backup);
      }
    }
    for (const item of staged) {
      fs.renameSync(item.temp, item.file);
    }
    for (const item of staged) {
      if (item.existed && fs.existsSync(item.backup)) {
        fs.rmSync(item.backup);
      }
    }
  } catch (error) {
    for (const item of [...staged].reverse()) {
      if (fs.existsSync(item.backup)) {
        if (fs.existsSync(item.file)) fs.rmSync(item.file);
        fs.renameSync(item.backup, item.file);
      } else if (!item.existed && fs.existsSync(item.file)) {
        fs.rmSync(item.file);
      }
      if (fs.existsSync(item.temp)) fs.rmSync(item.temp);
    }
    throw error;
  }
}

function main() {
  const { root, dryRun, force } = parseArgs(process.argv);
  const manifestPath = path.join(root, "ui_manifest.md");
  if (!fs.existsSync(manifestPath)) {
    failManual(`missing ${manifestPath}`);
  }

  const source = fs.readFileSync(manifestPath, "utf8");
  const sections = extractSections(source);
  const pages = sections.filter((section) => section.id.startsWith("PAGE-"));
  const comps = sections.filter((section) => section.id.startsWith("COMP-"));

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

  const changed = planned.filter((item) => {
    return !fs.existsSync(item.file) || fs.readFileSync(item.file, "utf8") !== item.body;
  });
  const conflicts = changed.filter((item) => fs.existsSync(item.file));

  if (dryRun) {
    console.log(`[dry-run] would write ${changed.length} file(s):`);
    for (const item of changed) {
      const marker = fs.existsSync(item.file) ? " [would overwrite]" : "";
      console.log(`  ${path.relative(root, item.file)}${marker}`);
    }
    process.exit(0);
  }

  if (conflicts.length > 0 && !force) {
    const files = conflicts.map((item) => path.relative(root, item.file)).join(", ");
    failManual(`refusing to overwrite existing files: ${files}; inspect them or rerun with --force`);
  }

  if (changed.length === 0) {
    console.log("detail files already match the legacy manifest; nothing to write");
    process.exit(0);
  }

  writeTransaction(changed);
  for (const item of changed) {
    console.log(`wrote ${path.relative(root, item.file)}`);
  }
  console.log(
    "migration wrote detail files; trim remaining bodies from ui_manifest.md so it keeps index only",
  );
}

main();
