---
description: Append post-merge changelog entry and sync llms.txt
---

Run this on `main` after a feature PR merges. It updates the daily changelog file plus `static/llms.txt` when site structure changes.

Preconditions (stop if any fail):
- Current branch is `main` with a clean tree. Current status:
!`git status --short`
!`git branch --show-current`
- Local `main` matches origin: run `git fetch origin && git status -sb`.

Steps:
1. If status output above is non-empty or branch is not `main`, stop and report. Never stash or discard without being asked.
2. Run `git checkout main && git pull`.
3. Find what to log: run `git log --oneline -20` and diff against the last entry in `changelog-YYYY-MM-DD.md` for today (UTC date, `date -u +%F`). Use today's file if it exists, else create `changelog-<today>.md` from the header in `changelog-2026-09-09.md:1`.
4. Draft one `### <section>` per merged PR or commit group since the last entry. Each section lists concrete file paths and behavior changes. Follow repo voice from `CLAUDE.md`: lead with the point, name files, no em dashes, none of these words: delve, crucial, robust, comprehensive, nuanced, intricate, foster, showcase, underscore, significant.
5. Update `static/llms.txt` only if any of these changed: `content/`, `hugo.toml` baseURL, contact links, `static/CNAME`. Keep the same three headers (`About`, `Key pages`, `Optional`). Keep lines under 120 chars.
6. If the change is user visible (content, layout, URL, domain), also prepend a `## <today> — <title>` entry to `CHANGELOG.md` with the same bullets.
7. Verify: run `python3 tests/test_site.py` from the repo root. If it fails, stop and report. Do not commit on failure.
8. Commit on a new branch `docs/changelog-<today>` (create it if missing, check it out if it exists), push, and report the next step: open a PR to `main`. Never push directly to `main`.
