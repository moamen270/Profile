#!/usr/bin/env node
/**
 * Regenerate the repo root README.md from job-search/applications.json + the
 * files present in each job-application/<folder>/.
 *
 *   node job-search/gen-readme.mjs
 *
 * Run it after adding an application, editing applications.json, or rebuilding CVs.
 */

import { readFileSync, writeFileSync, readdirSync, existsSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const appsDir = join(root, "job-application");
const { applications } = JSON.parse(readFileSync(join(root, "job-search", "applications.json"), "utf8"));

const enc = (p) => p.split("/").map(encodeURIComponent).join("/");
const rel = (folder, file) => `job-application/${enc(folder)}/${enc(file)}`;

const STATUS = {
  ready:      "🟢 ready to apply",
  blocked:    "🟡 blocked",
  applied:    "🔵 applied",
  assessment: "🟣 assessment",
  rejected:   "🔴 rejected",
  offer:      "🎉 offer",
  passed:     "⚪ passed",
};

function filesFor(folder) {
  const dir = join(appsDir, folder);
  if (!existsSync(dir)) return {};
  const list = readdirSync(dir);
  const cvStem = list.find((f) => /^Moamen_Basyoni_.*\.pdf$/i.test(f))?.replace(/\.pdf$/i, "")
    || list.find((f) => /^Moamen_Basyoni_.*\.docx$/i.test(f))?.replace(/\.docx$/i, "");
  const clStem = list.find((f) => /^Cover_Letter.*\.pdf$/i.test(f))?.replace(/\.pdf$/i, "")
    || list.find((f) => /^Cover_Letter.*\.docx$/i.test(f))?.replace(/\.docx$/i, "");
  const jd = list.find((f) => f.endsWith(".md") && !/^Moamen_Basyoni_|^Cover_Letter/i.test(f));
  const link = (stem, ext) => (stem && list.includes(`${stem}.${ext}`) ? `[${ext}](${rel(folder, `${stem}.${ext}`)})` : "");
  return {
    cv: cvStem ? [link(cvStem, "pdf"), link(cvStem, "docx")].filter(Boolean).join(" · ") : "—",
    cover: clStem ? [link(clStem, "pdf"), link(clStem, "docx")].filter(Boolean).join(" · ") : "—",
    jd: jd ? `[JD](${rel(folder, jd)})` : "",
  };
}

const rows = applications.map((a) => {
  const f = filesFor(a.folder);
  const jdCell = [a.jdUrl ? `[posting](${a.jdUrl})` : "", f.jd].filter(Boolean).join(" · ") || "—";
  const apply = a.applyUrl ? `**[Apply ↗](${a.applyUrl})**` : "—";
  return `| ${a.company} | ${a.role} | ${a.location || ""} | ${a.fit}% | ${STATUS[a.status] || a.status} | ${jdCell} | ${f.cv} | ${f.cover} | ${apply} |`;
});

const readySoon = applications.filter((a) => a.status === "ready");
const active = applications.filter((a) => ["ready", "blocked", "assessment"].includes(a.status));

const md = `# Moamen Basyoni — Job Search

Master profile: **[profile.md](profile.md)** · Pipeline detail: [job-search/pipeline.md](job-search/pipeline.md) · Apply checklist: [job-search/to-submit.md](job-search/to-submit.md)

Each application below links to the tailored **CV** and **cover letter** (PDF for viewing, DOCX for portals that require it) and the **job posting**.
Every folder in [\`job-application/\`](job-application/) also holds the job description and a \`Cover_Letter.md\` with a headline + selling-point map.

## Applications

| Company | Role | Location | Fit | Status | Job posting | CV | Cover letter | Apply |
|---|---|---|---:|---|---|---|---|---|
${rows.join("\n")}

**Fit %** = evidence-based match of this profile to the posting (keyword coverage + requirement alignment + seniority), not a probability of an offer.

## Next actions

${readySoon.length ? `- Apply now (no blockers): ${readySoon.map((a) => a.company).join(", ")}` : "- Nothing unblocked right now."}
- Highest priority: finish the **Crossworkers** assessment (already in the pipeline).
- Skill tasks that unblock multiple applications:
  - **React + .NET Core CRUD app** on GitHub → unblocks Raya Holding and Misr Technology Services
  - **Umbraco POC** → unblocks Significa

## How this repo is organised

| Path | Purpose |
|---|---|
| \`profile.md\` | Master professional profile + rules for generating CVs (§14), headlines & cover letters (§14b), and selling-point maps (§14c) |
| \`job-application/<Company>/\` | One folder per application: job description, tailored CV, \`Cover_Letter.md\`, and built \`.docx\` / \`.pdf\` |
| \`job-search/pipeline.md\` | Every role reviewed — fit %, status, notes |
| \`job-search/to-submit.md\` | Apply checklist with per-job blockers |
| \`job-search/collect.mjs\` | Browser collector (LinkedIn → \`jobs_raw.json\`), read-only |
| \`job-search/build-cvs.mjs\` | Markdown → \`.docx\` + \`.pdf\` (pandoc + wkhtmltopdf) |
| \`job-search/gen-readme.mjs\` | Regenerates this file from \`applications.json\` |

<sub>This README is generated — edit \`job-search/applications.json\` and run \`node job-search/gen-readme.mjs\`.</sub>
`;

writeFileSync(join(root, "README.md"), md);
console.log(`README.md regenerated — ${applications.length} applications, ${active.length} active.`);
