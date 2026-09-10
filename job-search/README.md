# Job search tooling

Local-only. Nothing here submits applications or contacts anyone — it collects listings and builds CVs. You review and submit each job yourself.

## Files

| File | What it is |
|---|---|
| `pipeline.md` | The master tracker — every job, fit %, status, links |
| `collect.mjs` | Playwright collector — drives your logged-in Chrome to gather job listings → `jobs_raw.json` |
| `build-cvs.mjs` | Converts each `job-application/*/Moamen_Basyoni_*.md` (CV and cover letter) to `.docx` + `.pdf` (strips the "NOT PART OF …" notes section first) |
| `applications.json` | Single source of truth for the root `README.md` dashboard (company, role, fit %, status, links) |
| `gen-readme.mjs` | Regenerates the repo root `README.md` from `applications.json` + the files in each folder |
| `jobs_raw.json` | Raw collected listings (git-ignored) |
| `to-submit.md` | End-of-day submit list: CV file + application link per job |

## 1. Collect jobs

**a. Launch Chrome with a debug port** (one time per session):

```powershell
# fully quit Chrome first (check the tray)
& "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --profile-directory="Default"
```

Keep all your logins. Make sure you're signed into LinkedIn in that window.

**b. Run the collector** with one or more LinkedIn job-search URLs (set your own filters on LinkedIn first — keyword, location, date-posted, then copy the URL):

```powershell
cd F:\PoCs\Profile\job-search
node collect.mjs --search "https://www.linkedin.com/jobs/search/?keywords=senior%20.net%20developer&location=Egypt&f_TPR=r604800" --details
```

- `--details` also grabs each full job description (slower, ~4s/job)
- `--max 120` cap total new jobs
- multiple `--search` allowed
- if LinkedIn shows a security check, solve it in the Chrome window and press Enter

**c.** Tell Claude: *"read jobs_raw.json"* — it triages, scores fit, updates `pipeline.md`, and for each job ≥70% fit creates `job-application/<Company>/` with:
- `<Company>_Job_Description.md` — the job description
- `Moamen_Basyoni_CV_<Company>.md` — tailored CV (+ a "gaps to close" section)
- `Moamen_Basyoni_Cover_Letter_<Company>.md` — headline (for the LinkedIn note / email opener) + full cover letter

(`<Company>` = folder name with non-alphanumerics replaced by `_`)

Rules for all three live in `../profile.md` §14 and §14b.

## 2. Build CVs

```powershell
cd F:\PoCs\Profile\job-search
node build-cvs.mjs                 # all drafts
node build-cvs.mjs --only "Raya"   # one company
```

Needs `pandoc` and `wkhtmltopdf` on PATH (already installed via winget).

## 3. Refresh the root README dashboard

After adding an application, editing `applications.json`, or rebuilding CVs:

```powershell
node F:\PoCs\Profile\job-search\gen-readme.mjs
```

## Notes

- Wuzzuf blocks automated access in its robots.txt — collect from there by manual copy-paste instead.
- Go easy on LinkedIn: one or two searches per run, not dozens. Automated behavior on your account carries some risk.
