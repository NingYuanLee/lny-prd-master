#!/usr/bin/env node
/** Browser-level smoke validation for generated LNY-PRD prototype pages. */
import { createRequire } from "node:module";
import { createServer } from "node:http";
import { mkdtemp, mkdir, readFile, readdir, stat, writeFile } from "node:fs/promises";
import { existsSync } from "node:fs";
import { tmpdir } from "node:os";
import { extname, join, relative, resolve, sep } from "node:path";
import process from "node:process";

const require = createRequire(import.meta.url);
let chromium;
let PNG;
try {
  ({ chromium } = require("playwright"));
  ({ PNG } = require("pngjs"));
} catch (error) {
  console.error(
    "Playwright browser validation requires the playwright and pngjs Node packages. " +
      "Install them outside the PRD project or use the host's bundled runtime."
  );
  console.error(String(error && error.message ? error.message : error));
  process.exit(2);
}

const MOBILE_TERMINALS = new Set(["MP", "H5", "APP"]);
const MIME = new Map([
  [".css", "text/css; charset=utf-8"],
  [".html", "text/html; charset=utf-8"],
  [".js", "text/javascript; charset=utf-8"],
  [".json", "application/json; charset=utf-8"],
  [".png", "image/png"],
  [".jpg", "image/jpeg"],
  [".jpeg", "image/jpeg"],
  [".svg", "image/svg+xml"],
  [".webp", "image/webp"],
]);

function usage(message) {
  if (message) console.error(message);
  console.error(
    "Usage: node verify-prototype-browser.mjs <prdRoot> " +
      "[--page PAGE-...] [--artifacts <dir>] [--keep-screenshots]"
  );
  process.exit(2);
}

function parseArgs(argv) {
  if (!argv.length) usage();
  const result = {
    root: resolve(argv[0]),
    pages: [],
    artifacts: null,
    keepScreenshots: false,
  };
  for (let index = 1; index < argv.length; index += 1) {
    const arg = argv[index];
    if (arg === "--page") {
      if (!argv[index + 1]) usage("--page requires a PAGE id");
      result.pages.push(argv[++index]);
    } else if (arg === "--artifacts") {
      if (!argv[index + 1]) usage("--artifacts requires a directory");
      result.artifacts = resolve(argv[++index]);
    } else if (arg === "--keep-screenshots") {
      result.keepScreenshots = true;
    } else {
      usage(`unknown argument: ${arg}`);
    }
  }
  return result;
}

async function walkPages(prototypes) {
  const pages = [];
  for (const terminalEntry of await readdir(prototypes, { withFileTypes: true })) {
    if (!terminalEntry.isDirectory()) continue;
    const terminal = terminalEntry.name;
    const directory = join(prototypes, terminal);
    for (const entry of await readdir(directory, { withFileTypes: true })) {
      if (entry.isFile() && /^PAGE-[A-Z]+-\d{3}\.html$/.test(entry.name)) {
        pages.push({
          id: entry.name.slice(0, -5),
          terminal,
          path: join(directory, entry.name),
        });
      }
    }
  }
  return pages.sort((a, b) => a.id.localeCompare(b.id));
}

function safeTarget(root, url) {
  const pathname = decodeURIComponent(new URL(url, "http://localhost").pathname);
  const target = resolve(root, `.${pathname}`);
  const prefix = root.endsWith(sep) ? root : `${root}${sep}`;
  return target === root || target.startsWith(prefix) ? target : null;
}

async function startStaticServer(root) {
  const server = createServer(async (request, response) => {
    try {
      if ((request.url || "").split("?", 1)[0] === "/favicon.ico") {
        response.writeHead(204).end();
        return;
      }
      let target = safeTarget(root, request.url || "/");
      if (!target) {
        response.writeHead(403).end("forbidden");
        return;
      }
      const info = await stat(target);
      if (info.isDirectory()) target = join(target, "index.html");
      const body = await readFile(target);
      response.writeHead(200, {
        "content-type": MIME.get(extname(target).toLowerCase()) || "application/octet-stream",
        "cache-control": "no-store",
      });
      response.end(body);
    } catch {
      response.writeHead(404).end("not found");
    }
  });
  await new Promise((resolveListen, reject) => {
    server.once("error", reject);
    server.listen(0, "127.0.0.1", resolveListen);
  });
  const address = server.address();
  return {
    origin: `http://127.0.0.1:${address.port}`,
    close: () => new Promise((resolveClose) => server.close(resolveClose)),
  };
}

function browserExecutable() {
  if (process.env.LNY_PRD_BROWSER_EXECUTABLE) {
    return process.env.LNY_PRD_BROWSER_EXECUTABLE;
  }
  if (process.platform !== "win32") return undefined;
  const candidates = [
    "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
    "C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe",
    "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
  ];
  return candidates.find((candidate) => existsSync(candidate));
}

function pixelSignal(buffer) {
  const png = PNG.sync.read(buffer);
  const buckets = new Set();
  const histogram = new Map();
  let sampled = 0;
  for (let y = 0; y < png.height; y += 6) {
    for (let x = 0; x < png.width; x += 6) {
      const offset = (y * png.width + x) * 4;
      if (png.data[offset + 3] < 16) continue;
      const key = `${png.data[offset] >> 4},${png.data[offset + 1] >> 4},${png.data[offset + 2] >> 4}`;
      buckets.add(key);
      histogram.set(key, (histogram.get(key) || 0) + 1);
      sampled += 1;
    }
  }
  const dominant = sampled ? Math.max(...histogram.values()) / sampled : 1;
  return { buckets: buckets.size, dominant };
}

async function pageMetrics(page) {
  return page.evaluate(() => {
    const root = document.querySelector(".md-mobile-page, .md-d1");
    const rootRect = root ? root.getBoundingClientRect() : null;
    const brokenImages = Array.from(document.images)
      .filter((image) => image.complete && image.naturalWidth === 0)
      .map((image) => image.currentSrc || image.src || image.alt || "<img>")
      .slice(0, 5);
    const visibleElements = Array.from(document.body.querySelectorAll("*"))
      .filter((element) => {
        const style = getComputedStyle(element);
        const rect = element.getBoundingClientRect();
        return style.display !== "none" && style.visibility !== "hidden" && rect.width > 1 && rect.height > 1;
      }).length;
    return {
      title: document.title,
      textLength: (document.body.innerText || "").trim().length,
      visibleElements,
      hasRoot: Boolean(root),
      rootVisible: Boolean(
        rootRect &&
          rootRect.width > 100 &&
          rootRect.height > 100 &&
          rootRect.right > 0 &&
          rootRect.bottom > 0
      ),
      horizontalOverflow: Math.max(
        document.documentElement.scrollWidth,
        document.body.scrollWidth
      ) - window.innerWidth,
      brokenImages,
      externalResources: performance
        .getEntriesByType("resource")
        .map((entry) => entry.name)
        .filter((url) => /^https?:\/\//.test(url) && new URL(url).origin !== location.origin)
        .slice(0, 5),
    };
  });
}

async function smokeInteraction(page, selector, targetAttribute, visibleSelector) {
  const trigger = page.locator(selector).first();
  if (!(await trigger.count()) || !(await trigger.isVisible())) return null;
  const targetId = await trigger.getAttribute(targetAttribute);
  if (!targetId) return `${selector} trigger is missing ${targetAttribute}`;
  const target = page.locator(`#${targetId}`);
  if (!(await target.count())) return `${selector} references missing #${targetId}`;
  await trigger.scrollIntoViewIfNeeded();
  await page.waitForTimeout(80);
  await trigger.click({ timeout: 3000 });
  await page.waitForTimeout(80);
  const visible = await target.evaluate((element, expected) => {
    const style = getComputedStyle(element);
    const rect = element.getBoundingClientRect();
    return (
      style.display !== "none" &&
      style.visibility !== "hidden" &&
      rect.width > 1 &&
      rect.height > 1 &&
      (!expected || element.matches(expected) || element.classList.contains("is-open") || element.classList.contains("is-active"))
    );
  }, visibleSelector || "");
  await page.keyboard.press("Escape").catch(() => {});
  return visible ? null : `${selector} did not reveal #${targetId}`;
}

async function validatePage(browser, origin, prototypes, target, artifacts) {
  const mobile = MOBILE_TERMINALS.has(target.terminal);
  const context = await browser.newContext({
    viewport: mobile ? { width: 390, height: 844 } : { width: 1440, height: 1000 },
    deviceScaleFactor: 1,
    reducedMotion: "reduce",
  });
  try {
    return await validatePageInContext(context, origin, prototypes, target, artifacts);
  } finally {
    await context.close();
  }
}

async function validatePageInContext(context, origin, prototypes, target, artifacts) {
  const page = await context.newPage();
  const runtimeErrors = [];
  page.on("console", (message) => {
    if (message.type() === "error") runtimeErrors.push(`console: ${message.text()}`);
  });
  page.on("pageerror", (error) => runtimeErrors.push(`pageerror: ${error.message}`));
  page.on("requestfailed", (request) => {
    if (request.url().startsWith(origin)) {
      runtimeErrors.push(`requestfailed: ${request.url()} (${request.failure()?.errorText || "unknown"})`);
    }
  });

  const relativePath = relative(prototypes, target.path).split(sep).join("/");
  const response = await page.goto(`${origin}/${relativePath}`, {
    waitUntil: "load",
    timeout: 15000,
  });
  await page.waitForTimeout(150);
  const errors = [];
  if (!response || !response.ok()) errors.push(`HTTP status ${response ? response.status() : "missing"}`);
  const metrics = await pageMetrics(page);
  if (!metrics.title.startsWith(target.id)) errors.push(`<title> must start with ${target.id}`);
  if (!metrics.hasRoot || !metrics.rootVisible) errors.push("missing or invisible md-mobile-page/md-d1 root");
  if (metrics.textLength < 20 || metrics.visibleElements < 10) {
    errors.push(`page is visually empty (text=${metrics.textLength}, visible=${metrics.visibleElements})`);
  }
  if (metrics.horizontalOverflow > 3) {
    errors.push(`document overflows viewport horizontally by ${metrics.horizontalOverflow}px`);
  }
  for (const image of metrics.brokenImages) errors.push(`broken image: ${image}`);
  for (const resource of metrics.externalResources) {
    errors.push(`external runtime resource breaks offline preview: ${resource}`);
  }

  const interactionErrors = [];
  const tab = await smokeInteraction(page, "[data-panel]:not(.is-active)", "data-panel", ".md-tab-panel");
  if (tab) interactionErrors.push(tab);
  const menu = await smokeInteraction(page, "[data-menu]", "data-menu", ".md-menu");
  if (menu) interactionErrors.push(menu);
  const drawer = await smokeInteraction(
    page,
    "[data-filter-drawer]",
    "data-filter-drawer",
    ".md-drawer"
  );
  if (drawer) interactionErrors.push(drawer);

  const wheel = page.locator("[data-wheel]").first();
  if ((await wheel.count()) && (await wheel.isVisible())) {
    await wheel.click({ timeout: 3000 });
    await page.waitForTimeout(80);
    const wheelVisible = await page.locator("#mdWheelSheet").evaluate((element) => {
      const rect = element.getBoundingClientRect();
      return element.classList.contains("is-open") && rect.width > 1 && rect.height > 1;
    });
    if (!wheelVisible) interactionErrors.push("data-wheel did not open #mdWheelSheet");
  }

  const screenshot = await page.screenshot({ fullPage: false });
  const pixels = pixelSignal(screenshot);
  if (pixels.buckets < 8 || pixels.dominant > 0.9995) {
    errors.push(
      `screenshot lacks visual diversity (buckets=${pixels.buckets}, dominant=${pixels.dominant.toFixed(5)})`
    );
  }
  if (artifacts) {
    const terminalDir = join(artifacts, target.terminal);
    await mkdir(terminalDir, { recursive: true });
    await writeFile(join(terminalDir, `${target.id}.png`), screenshot);
  }
  errors.push(...runtimeErrors, ...interactionErrors);
  return { id: target.id, errors, metrics, pixels };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const prototypes = join(args.root, "prototypes");
  if (!existsSync(prototypes)) usage(`prototypes/ not found under ${args.root}`);
  const allPages = await walkPages(prototypes);
  const selected = args.pages.length
    ? allPages.filter((page) => args.pages.includes(page.id))
    : allPages;
  const missing = args.pages.filter((id) => !selected.some((page) => page.id === id));
  if (missing.length) usage(`PAGE file(s) not found: ${missing.join(", ")}`);
  if (!selected.length) usage("no PAGE-*.html files found");

  let artifacts = args.artifacts;
  if (!artifacts && args.keepScreenshots) {
    artifacts = await mkdtemp(join(tmpdir(), "lny-prd-browser-"));
  }
  if (artifacts) await mkdir(artifacts, { recursive: true });

  const server = await startStaticServer(prototypes);
  const executablePath = browserExecutable();
  let browser = null;
  const results = [];
  try {
    browser = await chromium.launch({
      headless: true,
      ...(executablePath ? { executablePath } : {}),
    });
    for (const target of selected) {
      try {
        results.push(await validatePage(browser, server.origin, prototypes, target, artifacts));
      } catch (error) {
        results.push({
          id: target.id,
          errors: [
            `browser validation error: ${error && error.message ? error.message : String(error)}`,
          ],
        });
      }
    }
  } finally {
    if (browser) await browser.close();
    await server.close();
  }

  const failed = results.filter((result) => result.errors.length);
  if (failed.length) {
    console.error(`prototype browser validation failed: ${failed.length}/${results.length} page(s)`);
    for (const result of failed) {
      console.error(`- ${result.id}`);
      for (const error of result.errors) console.error(`  - ${error}`);
    }
    if (artifacts) console.error(`screenshots: ${artifacts}`);
    process.exitCode = 1;
  } else {
    console.log(`prototype browser validation ok: ${results.length} page(s)`);
    if (artifacts) console.log(`screenshots: ${artifacts}`);
  }
}

main().catch((error) => {
  console.error(error && error.stack ? error.stack : String(error));
  process.exit(1);
});
