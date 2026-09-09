# Backlog — scottinabox-site

## Content

1. [x] Add a blog post section (`content/posts/`).
   - **Priority:** P1
2. [ ] Write "What got you here, won't get you there" blog post.
   - **Priority:** P1

## Design

1. [x] Add a favicon.
   - **Priority:** P2
2. [x] Center blog post content for reading comfort (override homepage right-aligned layout).
   - **Priority:** P1
3. [ ] Use actual email address (replace scott@scottinabox.com).
   - **Priority:** P2

## Infrastructure

1. [x] Use GitHub Pages (migrated from Cloudflare).
   - **Priority:** P1
2. [x] Swap to custom domain name (scottlorimor.com via `static/CNAME` plus `baseURL`).
   - **Priority:** P1
3. [ ] Research mapping this to Substack.
   - **Priority:** P2
4. [x] Add test suite.
   - **Priority:** P1
5. [x] Add GitHub Actions for production deploys (`.github/workflows/hugo.yaml`).
   - **Priority:** P1
6. [x] Add website tracking analytics.
   - **Priority:** P2
7. [ ] Buy GitHub Pro and make this repo private again.
   - **Priority:** P2

## Agent-facing

1. [x] Add `llms.txt` for LLM/agent consumption (site info, key pages, optional `llms-full.txt` with full content).
   - **Priority:** P2

## Completed

- [x] Scaffold Hugo site with layouts and CSS.
- [x] Deploy to Cloudflare Pages via Wrangler.
- [x] Replace placeholder content with real structure (homepage revamp).
- [x] Migrate hosting from Cloudflare to GitHub Pages.
- [x] Add GitHub Actions deploy workflow.
- [x] Protect main (pre-push hook plus GitHub branch protection).
- [x] Add test suite (`tests/test_site.py`) with CI test job on push and PR.
- [x] Add branch guard (opencode require-branch plugin plus /start-todo command).