#!/usr/bin/env node
// Convert every job-application/<Company>/Moamen_Basyoni_*.md CV draft into .docx and .pdf.
// Strips everything from the "## ⚠️ NOT PART OF CV" marker onward before converting.
//
// Usage:  node job-search/build-cvs.mjs [--only "Company Name"]
//
// Requires: pandoc + wkhtmltopdf on PATH.

import { readdirSync, readFileSync, writeFileSync, mkdtempSync, rmSync, statSync } from "node:fs";
import { join, dirname, basename } from "node:path";
import { tmpdir } from "node:os";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const repoRoot = join(dirname(fileURLToPath(import.meta.url)), "..");
const appsDir = join(repoRoot, "job-application");
const MARKER = /^#+\s*(⚠️\s*)?NOT PART OF /im;

const onlyIdx = process.argv.indexOf("--only");
const only = onlyIdx > -1 ? process.argv[onlyIdx + 1] : null;

const cssPath = join(tmpdir(), "cv-style.css");
writeFileSync(cssPath, `
  body{font-family:"Calibri","Segoe UI",Arial,sans-serif;font-size:10.5pt;line-height:1.35;color:#111;max-width:100%;margin:0}
  h1{font-size:20pt;margin:0 0 2pt;border:0}
  h1 + p strong, h1 + p{margin:0 0 6pt}
  h2{font-size:12pt;margin:12pt 0 3pt;border-bottom:1px solid #999;padding-bottom:1pt;text-transform:uppercase;letter-spacing:.4pt}
  h3{font-size:10.5pt;margin:8pt 0 1pt}
  ul{margin:2pt 0 6pt;padding-left:16pt}
  li{margin:1pt 0}
  p{margin:3pt 0}
  hr{border:0;border-top:1px solid #ccc;margin:8pt 0}
  a{color:#111;text-decoration:none}
`);

function cvDirs() {
  return readdirSync(appsDir)
    .filter((d) => { try { return statSync(join(appsDir, d)).isDirectory(); } catch { return false; } })
    .filter((d) => !only || d.toLowerCase().includes(only.toLowerCase()));
}

function convert(full, dir, srcFile) {
  const src = readFileSync(join(full, srcFile), "utf8");
  const m = src.match(MARKER);
  let body = m ? src.slice(0, m.index) : src;
  body = body.replace(/\n-{3,}\s*\n-{3,}\s*$/g, "\n").replace(/\s+$/, "") + "\n";

  const stem = basename(srcFile, ".md");
  const tmp = mkdtempSync(join(tmpdir(), "doc-"));
  const tmpMd = join(tmp, "doc.md");
  writeFileSync(tmpMd, body);
  try {
    execFileSync("pandoc", [tmpMd, "-o", join(full, `${stem}.docx`)], { stdio: "pipe" });
    execFileSync("pandoc", [tmpMd, "-o", join(full, `${stem}.pdf`), "--pdf-engine=wkhtmltopdf", "--css", cssPath,
      "-V", "margin-top=14mm", "-V", "margin-bottom=14mm", "-V", "margin-left=16mm", "-V", "margin-right=16mm"],
      { stdio: "pipe" });
    console.log(`✓  ${dir}/${stem}  ->  .docx + .pdf`);
    return true;
  } catch (e) {
    console.error(`✗  ${dir}/${stem}: ${e.message}\n${e.stderr?.toString() || ""}`);
    return false;
  } finally {
    rmSync(tmp, { recursive: true, force: true });
  }
}

let built = 0;
for (const dir of cvDirs()) {
  const full = join(appsDir, dir);
  const files = readdirSync(full);
  const targets = files.filter((f) => /^Moamen_Basyoni_.*\.md$/i.test(f));
  if (!targets.length) { console.log(`–  ${dir}: no CV / cover-letter markdown (needs Moamen_Basyoni_*.md), skipped`); continue; }
  for (const t of targets) if (convert(full, dir, t)) built++;
}

// Also build any Moamen_Basyoni_*.md sitting directly at the repo root — e.g. the
// full, untailored master CV that represents the whole profile rather than one job.
if (!only) {
  const rootTargets = readdirSync(repoRoot).filter((f) => /^Moamen_Basyoni_.*\.md$/i.test(f));
  for (const t of rootTargets) if (convert(repoRoot, ".", t)) built++;
}

console.log(`\n${built} document(s) built.`);
