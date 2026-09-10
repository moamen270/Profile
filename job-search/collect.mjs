#!/usr/bin/env node
/**
 * Job collector — drives YOUR already-logged-in Chrome over CDP to gather job listings.
 * It only reads. It never applies, messages, or clicks anything outward-facing.
 *
 * ── One-time: launch Chrome with a debug port ──────────────────────────────
 *   1. Fully quit Chrome (check the tray icon).
 *   2. Run in PowerShell:
 *        & "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --profile-directory="Default"
 *      (this keeps all your logins)
 *   3. In that Chrome, make sure you're logged into LinkedIn.
 *
 * ── Run the collector ─────────────────────────────────────────────────────
 *   node collect.mjs --search "<LinkedIn jobs search URL>" --details
 *   node collect.mjs --search "<url1>" --search "<url2>" --max 120
 *
 *   --details    also open each job page and grab the full description (slower)
 *   --max N      stop after N new jobs total (default 150)
 *   --pages N    max result pages per search (default 8, ~25 jobs each)
 *   --port N     CDP port (default 9222)
 *
 * Output: job-search/jobs_raw.json  (appended, deduped by platform+id)
 */

import { chromium } from "playwright-core";
import { readFileSync, writeFileSync, existsSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const OUT = join(here, "jobs_raw.json");

// ---- args ----
const args = process.argv.slice(2);
const getAll = (f) => args.reduce((a, v, i) => (v === f ? [...a, args[i + 1]] : a), []);
const getOne = (f, d) => { const i = args.indexOf(f); return i > -1 ? args[i + 1] : d; };
const has = (f) => args.includes(f);

const searches = getAll("--search");
const withDetails = has("--details");
const MAX = +getOne("--max", 150);
const MAX_PAGES = +getOne("--pages", 8);
const PORT = +getOne("--port", 9222);

if (!searches.length) {
  console.error("Give at least one --search \"<url>\". See header of this file.");
  process.exit(1);
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const rnd = (a, b) => a + Math.random() * (b - a);
const pause = () => sleep(rnd(2800, 6000)); // human-paced

// ---- store ----
const store = existsSync(OUT) ? JSON.parse(readFileSync(OUT, "utf8")) : { collectedAt: null, jobs: [] };
const seen = new Set(store.jobs.map((j) => `${j.platform}:${j.id}`));
let added = 0;
const save = () => { store.collectedAt = new Date().toISOString(); writeFileSync(OUT, JSON.stringify(store, null, 2)); };

// ---- platform extractors ----
const linkedin = {
  match: (u) => /linkedin\.com/.test(u),
  async collect(page, url) {
    for (let p = 0; p < MAX_PAGES && added < MAX; p++) {
      const pageUrl = url + (url.includes("?") ? "&" : "?") + `start=${p * 25}`;
      await page.goto(pageUrl, { waitUntil: "domcontentloaded" });
      await pause();

      if (/\/checkpoint\/|\/authwall/.test(page.url())) {
        console.log("\n⚠  LinkedIn is showing a security check. Solve it in the Chrome window, then press Enter here.");
        await waitForEnter();
        await page.goto(pageUrl, { waitUntil: "domcontentloaded" });
        await pause();
      }

      // lazy-load the left list by scrolling it
      const listSel = ".scaffold-layout__list, .jobs-search-results-list";
      for (let s = 0; s < 6; s++) {
        await page.evaluate((sel) => {
          const el = document.querySelector(sel) || document.scrollingElement;
          el.scrollBy(0, 1200);
        }, listSel).catch(() => {});
        await sleep(rnd(600, 1200));
      }

      const cards = await page.evaluate(() => {
        const pick = (el, sels) => { for (const s of sels) { const n = el.querySelector(s); if (n?.innerText?.trim()) return n.innerText.trim(); } return ""; };
        const nodes = [...document.querySelectorAll("li[data-occludable-job-id], .job-card-container, div.job-card-list")];
        return nodes.map((el) => {
          const id = el.getAttribute("data-occludable-job-id")
            || el.querySelector("[data-job-id]")?.getAttribute("data-job-id")
            || el.querySelector("a[href*='/jobs/view/']")?.href?.match(/\/jobs\/view\/(\d+)/)?.[1] || "";
          return {
            id,
            title: pick(el, [".job-card-list__title", ".job-card-list__title--link", "a.job-card-container__link", ".artdeco-entity-lockup__title"]),
            company: pick(el, [".job-card-container__primary-description", ".artdeco-entity-lockup__subtitle", ".job-card-container__company-name"]),
            location: pick(el, [".job-card-container__metadata-item", ".artdeco-entity-lockup__caption", ".job-card-container__metadata-wrapper"]),
          };
        }).filter((c) => c.id && c.title);
      });

      if (!cards.length) { console.log(`  page ${p + 1}: no cards — stopping this search`); break; }

      let newOnPage = 0;
      for (const c of cards) {
        const key = `linkedin:${c.id}`;
        if (seen.has(key)) continue;
        seen.add(key);
        const job = {
          platform: "linkedin", id: c.id,
          title: c.title, company: c.company.replace(/\s*·.*$/, "").trim(), location: c.location,
          url: `https://www.linkedin.com/jobs/view/${c.id}`,
          jd: null, collectedAt: new Date().toISOString(), fromSearch: url,
        };
        store.jobs.push(job); added++; newOnPage++;
        console.log(`  + ${job.title} — ${job.company} — ${job.location}`);
        if (added >= MAX) break;
      }
      save();
      console.log(`  page ${p + 1}: ${newOnPage} new (total new this run: ${added})`);
      if (newOnPage === 0 && p > 0) break;
      await pause();
    }

    if (withDetails) {
      const need = store.jobs.filter((j) => j.platform === "linkedin" && !j.jd);
      console.log(`\nFetching ${need.length} job descriptions…`);
      for (const j of need) {
        try {
          await page.goto(j.url, { waitUntil: "domcontentloaded" });
          await sleep(rnd(1800, 3500));
          await page.click("button.jobs-description__footer-button, button[aria-label*='see more']", { timeout: 1500 }).catch(() => {});
          j.jd = await page.evaluate(() => {
            const el = document.querySelector(".jobs-description__content, .jobs-box__html-content, #job-details, article.jobs-description__container");
            return el ? el.innerText.trim().replace(/\n{3,}/g, "\n\n") : null;
          });
          const closed = await page.evaluate(() => /no longer accepting applications|لم نعد نقبل/i.test(document.body.innerText));
          j.closed = closed;
          console.log(`  ${closed ? "✗ closed  " : "✓ "}${j.title} — ${j.company}`);
          save();
          await pause();
        } catch (e) { console.log(`  ! ${j.title}: ${e.message}`); }
      }
    }
  },
};

const extractors = [linkedin];

// ---- enter key helper ----
function waitForEnter() {
  return new Promise((res) => {
    process.stdin.resume();
    process.stdin.once("data", () => { process.stdin.pause(); res(); });
  });
}

// ---- main ----
const browser = await chromium.connectOverCDP(`http://localhost:${PORT}`).catch((e) => {
  console.error(`\nCan't reach Chrome on port ${PORT}. Did you launch it with --remote-debugging-port=${PORT} ?\n${e.message}`);
  process.exit(1);
});
const ctx = browser.contexts()[0];
if (!ctx) { console.error("No browser context — is Chrome actually open?"); process.exit(1); }
const page = await ctx.newPage();

console.log(`Connected. ${store.jobs.length} jobs already in jobs_raw.json.\n`);
for (const url of searches) {
  const ex = extractors.find((e) => e.match(url));
  if (!ex) { console.log(`(no extractor for ${url} — skipped)`); continue; }
  console.log(`▶ ${url}`);
  await ex.collect(page, url);
  if (added >= MAX) { console.log(`\nHit --max ${MAX}.`); break; }
}

await page.close();
browser.close();
save();
console.log(`\nDone. +${added} new this run. Total: ${store.jobs.length} → job-search/jobs_raw.json`);
console.log(`Next: paste that file's contents to Claude, or tell it to read jobs_raw.json.`);
process.exit(0);
