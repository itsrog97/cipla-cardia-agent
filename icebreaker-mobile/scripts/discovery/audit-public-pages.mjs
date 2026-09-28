#!/usr/bin/env node
// Public-page discovery audit for the Icebreaker UX audit (Phase 1).
//
// What it does:
//   - Renders public pages in headless Chromium (JavaScript executed).
//   - Follows only same-origin links that appear on the pages themselves.
//   - Records title, meta description, headings, links and form controls.
//   - Measures responsive behaviour at phone / tablet / desktop widths:
//     horizontal overflow, tap targets < 44px, input font size, input labelling.
//
// What it never does:
//   - Log in, submit forms, guess URLs, or call private APIs.
//
// Usage:
//   npm i -D playwright && npx playwright install chromium
//   node scripts/discovery/audit-public-pages.mjs [--base https://joinicebreaker.com] [--screenshots]
//
// Output: scripts/discovery/out/ (gitignored). Screenshots contain third-party
// content and must not be committed to this public repository.

import { chromium } from 'playwright';
import { mkdir, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const args = process.argv.slice(2);
const BASE = (args.includes('--base') ? args[args.indexOf('--base') + 1] : 'https://joinicebreaker.com').replace(/\/$/, '');
const SCREENSHOTS = args.includes('--screenshots');
const START_PATHS = ['/', '/home', '/auth'];
const MAX_PAGES = 25;
const WIDTHS = [320, 390, 768, 1024, 1440];
const OUT_DIR = path.join(path.dirname(fileURLToPath(import.meta.url)), 'out');

const slug = (p) => p.replace(/[^a-z0-9]+/gi, '_').replace(/^_|_$/g, '') || 'root';

async function load(page, url) {
  // 'networkidle' can hang on analytics beacons; wait for load plus a settle delay.
  const response = await page.goto(url, { waitUntil: 'load', timeout: 45_000 });
  await page.waitForTimeout(2_500);
  return response;
}

async function inventory(page) {
  return page.evaluate(() => {
    const clean = (s) => (s || '').trim().replace(/\s+/g, ' ');
    return {
      title: document.title,
      description: document.querySelector('meta[name="description"]')?.content ?? null,
      headings: [...document.querySelectorAll('h1,h2,h3')].map((h) => `${h.tagName}: ${clean(h.innerText)}`),
      links: [...document.querySelectorAll('a[href]')].map((a) => ({ text: clean(a.innerText), href: a.getAttribute('href') })),
      controls: [...document.querySelectorAll('button,input,select,textarea')].map((e) => ({
        tag: e.tagName.toLowerCase(),
        type: e.getAttribute('type'),
        text: clean(e.innerText || e.value),
        placeholder: e.getAttribute('placeholder'),
      })),
      textLength: document.body.innerText.length,
    };
  });
}

async function responsiveMetrics(page) {
  return page.evaluate(() => {
    const visible = (e) => {
      const r = e.getBoundingClientRect();
      const s = getComputedStyle(e);
      return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none';
    };
    const interactive = [...document.querySelectorAll('a,button,input,select,textarea,[role=button]')].filter(visible);
    const inputs = [...document.querySelectorAll('input,select,textarea')].filter(visible);
    return {
      layoutWidth: document.documentElement.scrollWidth,
      viewportWidth: window.innerWidth,
      smallTapTargets: interactive
        .filter((e) => { const r = e.getBoundingClientRect(); return r.height < 44 || r.width < 44; })
        .map((e) => { const r = e.getBoundingClientRect(); return `${e.tagName.toLowerCase()} "${(e.innerText || e.getAttribute('aria-label') || '').trim().slice(0, 30)}" ${Math.round(r.width)}x${Math.round(r.height)}`; }),
      inputFontSizes: inputs.map((e) => `${e.type}:${getComputedStyle(e).fontSize}`),
      unlabelledInputs: inputs.filter((e) => !(e.labels && e.labels.length) && !e.getAttribute('aria-label')).length,
    };
  });
}

async function main() {
  await mkdir(OUT_DIR, { recursive: true });
  const browser = await chromium.launch();
  const report = { base: BASE, generatedAt: new Date().toISOString(), pages: [], responsive: [] };

  // 1. Inventory: breadth-first over same-origin links found on the pages.
  const context = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const page = await context.newPage();
  const queue = [...START_PATHS];
  const seen = new Set();
  while (queue.length && seen.size < MAX_PAGES) {
    const p = queue.shift();
    if (seen.has(p)) continue;
    seen.add(p);
    try {
      const response = await load(page, BASE + p);
      const record = { path: p, status: response?.status() ?? null, finalUrl: page.url(), ...(await inventory(page)) };
      report.pages.push(record);
      if (SCREENSHOTS) await page.screenshot({ path: path.join(OUT_DIR, `desktop_${slug(p)}.png`), fullPage: true });
      for (const { href } of record.links) {
        let h = href.startsWith(BASE) ? href.slice(BASE.length) : href;
        if (!h.startsWith('/') || h.startsWith('//')) continue;
        h = h.split('#')[0].split('?')[0] || '/';
        if (!seen.has(h) && !queue.includes(h)) queue.push(h);
      }
      console.log(`${record.status} ${p} -> ${record.finalUrl}`);
    } catch (error) {
      report.pages.push({ path: p, error: String(error).split('\n')[0] });
      console.log(`ERR ${p}: ${String(error).split('\n')[0]}`);
    }
  }
  await context.close();

  // 2. Responsive checks: fresh context per width so layout is not carried over.
  const publicPaths = report.pages.filter((r) => !r.error && r.finalUrl?.startsWith(BASE)).map((r) => r.path);
  for (const width of WIDTHS) {
    const mobile = width < 700;
    const ctx = await browser.newContext({ viewport: { width, height: mobile ? 844 : 1000 }, isMobile: mobile, hasTouch: width < 1100 });
    const pg = await ctx.newPage();
    for (const p of publicPaths) {
      try {
        await load(pg, BASE + p);
        const m = await responsiveMetrics(pg);
        // On a mobile viewport the browser widens the layout viewport instead of
        // scrolling, so compare the layout width with the device width.
        report.responsive.push({ width, path: p, zoomedOut: m.layoutWidth > width, ...m });
        if (SCREENSHOTS && mobile) await pg.screenshot({ path: path.join(OUT_DIR, `w${width}_${slug(p)}.png`), fullPage: true });
      } catch (error) {
        report.responsive.push({ width, path: p, error: String(error).split('\n')[0] });
      }
    }
    await ctx.close();
  }
  await browser.close();

  const file = path.join(OUT_DIR, `discovery-${report.generatedAt.slice(0, 10)}.json`);
  await writeFile(file, JSON.stringify(report, null, 2));
  for (const r of report.responsive.filter((x) => x.zoomedOut)) {
    console.log(`Layout wider than device: ${r.path} @${r.width}px -> ${r.layoutWidth}px`);
  }
  console.log(`Report written to ${file}`);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
