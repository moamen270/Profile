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
  closed:     "⚫ closed",
};

function filesFor(folder) {
  const dir = join(appsDir, folder);
  if (!existsSync(dir)) return {};
  const list = readdirSync(dir);
  const stemOf = (re) => list.find((f) => re.test(f) && /\.pdf$/i.test(f))?.replace(/\.pdf$/i, "")
    || list.find((f) => re.test(f) && /\.docx$/i.test(f))?.replace(/\.docx$/i, "");
  const cvStem = stemOf(/^Moamen_Basyoni_CV_/i) || stemOf(/^Moamen_Basyoni_(?!Cover_Letter)/i);
  const clStem = stemOf(/^Moamen_Basyoni_Cover_Letter_/i);
  const jd = list.find((f) => f.endsWith(".md") && !/^Moamen_Basyoni_/i.test(f));
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
  const canApply = !["applied", "assessment", "closed", "rejected", "passed", "offer"].includes(a.status);
  const apply = canApply && a.applyUrl ? `**[Apply ↗](${a.applyUrl})**` : "—";
  return `| ${a.company} | ${a.role} | ${a.location || ""} | ${a.fit}% | ${STATUS[a.status] || a.status} | ${jdCell} | ${f.cv} | ${f.cover} | ${apply} |`;
});

const by = (s) => applications.filter((a) => a.status === s);
const active = applications.filter((a) => ["ready", "blocked", "assessment"].includes(a.status));
const line = (a) => `- **${a.company}** — ${a.note}`;
const nextActions = [
  by("assessment").length && `**In progress:**\n${by("assessment").map(line).join("\n")}`,
  by("ready").length && `**Ready to apply:**\n${by("ready").map(line).join("\n")}`,
  by("blocked").length && `**Blocked — close the gap first:**\n${by("blocked").map(line).join("\n")}`,
  by("applied").length && `**Applied — awaiting response:** ${by("applied").map((a) => a.company).join(", ")}`,
].filter(Boolean).join("\n\n");

const md = `# Moamen Basyoni — Job Search

Master profile: **[profile.md](profile.md)** · Pipeline detail: [job-search/pipeline.md](job-search/pipeline.md) · Apply checklist: [job-search/to-submit.md](job-search/to-submit.md)

Each application below links to the tailored **CV** and **cover letter** (PDF to view, DOCX for portals that require an editable upload) and the **job posting**.
Every folder in [\`job-application/\`](job-application/) also holds the job description and \`Moamen_Basyoni_Cover_Letter_<Company>.md\` with a headline + selling-point map.

## Applications

| Company | Role | Location | Fit | Status | Job posting | CV | Cover letter | Apply |
|---|---|---|---:|---|---|---|---|---|
${rows.join("\n")}

**Fit %** = evidence-based match of this profile to the posting (keyword coverage + requirement alignment + seniority), not a probability of an offer.

## Next actions

${nextActions}

**Skill tasks that unblock multiple applications:**
- **React + .NET Core CRUD app** on GitHub → unblocks Raya Holding and Misr Technology Services
- **Umbraco POC** → unblocks Significa

## How this repo is organised

| Path | Purpose |
|---|---|
| \`profile.md\` | Master professional profile + rules for generating CVs (§14), headlines & cover letters (§14b), and selling-point maps (§14c) |
| \`job-application/<Company>/\` | Per application: \`<Company>_Job_Description.md\`, \`Moamen_Basyoni_CV_<Company>.*\`, \`Moamen_Basyoni_Cover_Letter_<Company>.*\` (md + built docx/pdf) |
| \`job-search/pipeline.md\` | Every role reviewed — fit %, status, notes |
| \`job-search/to-submit.md\` | Apply checklist with per-job blockers |
| \`job-search/collect.mjs\` | Browser collector (LinkedIn → \`jobs_raw.json\`), read-only |
| \`job-search/build-cvs.mjs\` | Markdown → \`.docx\` + \`.pdf\` (pandoc + wkhtmltopdf) |
| \`job-search/gen-readme.mjs\` | Regenerates this file from \`applications.json\` |

<sub>This README is generated — edit \`job-search/applications.json\` and run \`node job-search/gen-readme.mjs\`.</sub>
`;

writeFileSync(join(root, "README.md"), md);
console.log(`README.md regenerated — ${applications.length} applications, ${active.length} active.`);
