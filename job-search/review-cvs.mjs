#!/usr/bin/env node
/**
 * Run the bundled cv-review skill over every application package and collect
 * the scores into job-search/cv-scores.json + a markdown summary.
 *
 *   node job-search/review-cvs.mjs [--only "Company"]
 *
 * Requires the venv at .venv-cvreview (see job-search/README.md).
 */

import { readdirSync, existsSync, writeFileSync, readFileSync, statSync, mkdtempSync, rmSync } from "node:fs";
import { join, dirname } from "node:path";
import { tmpdir } from "node:os";
import { fileURLToPath } from "node:url";
import { execFileSync } from "node:child_process";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const appsDir = join(root, "job-application");
const python = join(root, ".venv-cvreview", "Scripts", "python.exe");
const script = join(root, "SKILLS", "cv-review", "scripts", "cv_review.py");

const onlyIdx = process.argv.indexOf("--only");
const only = onlyIdx > -1 ? process.argv[onlyIdx + 1] : null;

if (!existsSync(python)) { console.error(`No venv python at ${python}`); process.exit(1); }
if (!existsSync(script)) { console.error(`No cv_review.py at ${script}`); process.exit(1); }

const results = [];
const dirs = readdirSync(appsDir)
  .filter((d) => { try { return statSync(join(appsDir, d)).isDirectory(); } catch { return false; } })
  .filter((d) => !only || d.toLowerCase().includes(only.toLowerCase()));

for (const dir of dirs) {
  const full = join(appsDir, dir);
  const files = readdirSync(full);
  const cv = files.find((f) => /^Moamen_Basyoni_CV_.*\.pdf$/i.test(f));
  const jd = files.find((f) => /_Job_Description\.md$/i.test(f));
  if (!cv || !jd) { console.log(`–  ${dir}: missing ${!cv ? "CV pdf" : "JD md"}, skipped`); continue; }

  process.stdout.write(`▶  ${dir} … `);
  const tmp = mkdtempSync(join(tmpdir(), "cvr-"));
  const outFile = join(tmp, "r.json");
  try {
    execFileSync(python, [script, "--resume", join(full, cv), "--jd", join(full, jd), "--json", outFile],
      { encoding: "utf8", maxBuffer: 64 * 1024 * 1024, stdio: ["ignore", "ignore", "pipe"] });
    const data = JSON.parse(readFileSync(outFile, "utf8"));
    results.push({ company: dir, cv, jd, ...data });
    const s = data.scores || {};
    console.log(`tfidf ${fmt(s.tfidf)} · embedding ${fmt(s.embedding)} · overall ${(data.overall_score ?? NaN).toFixed?.(1) ?? "—"}`);
  } catch (e) {
    console.log(`FAILED: ${(e.stderr?.toString() || e.message).split("\n")[0]}`);
    results.push({ company: dir, cv, jd, error: e.stderr?.toString() || e.message });
  } finally {
    rmSync(tmp, { recursive: true, force: true });
  }
}

function fmt(v) {
  const n = typeof v === "number" ? v : v?.score;
  return typeof n === "number" ? n.toFixed(1) : "—";
}

writeFileSync(join(root, "job-search", "cv-scores.json"), JSON.stringify({ ranAt: new Date().toISOString(), results }, null, 2));

// ---- markdown summary ----
const rows = results.filter((r) => !r.error).map((r) => {
  const s = r.scores || {};
  const c = r.criteria || {};
  return `| ${r.company} | ${fmt(s.tfidf)} | ${fmt(s.embedding)} | **${(r.overall_score ?? 0).toFixed(1)}** | ${s.tfidf?.tier ?? "—"} / ${s.tfidf?.grade ?? "—"} | ${c.met ?? "?"} / ${c.total ?? "?"}${c.undecided ? ` (${c.undecided} undecided)` : ""} | ${r.fit_gap?.badge ?? "—"} | ${(r.parse_warnings || []).length} |`;
});

const detail = results.filter((r) => !r.error).map((r) => {
  const recs = (r.recommendations || []).map((x) => `- \`[${x.priority}]\` ${x.text}`).join("\n");
  const warns = (r.parse_warnings || []).map((w) => `- ${w}`).join("\n");
  return `### ${r.company} — ${(r.overall_score ?? 0).toFixed(1)} / 100\n\n**Parse warnings**\n${warns || "- none"}\n\n**Recommendations**\n${recs || "- none"}\n`;
}).join("\n");

const md = `# CV review scores — cv-review skill

Generated ${new Date().toISOString().slice(0, 16).replace("T", " ")} by \`node job-search/review-cvs.mjs\`.
Engines: TF-IDF (lexical) + embedding (sentence-transformers). Overall = mean of both.
These are simulated engine estimates, not real ATS numbers.

| Company | TF-IDF | Embedding | Overall | Tier / grade | Criteria met | Fit badge | Parse warnings |
|---|---:|---:|---:|---|---|---|---:|
${rows.join("\n")}

## Per-application detail

${detail}
`;
writeFileSync(join(root, "job-search", "cv-scores.md"), md);
console.log(`\n${results.length} package(s) scored → job-search/cv-scores.json + cv-scores.md`);
