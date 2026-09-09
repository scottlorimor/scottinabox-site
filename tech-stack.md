# Tech Stack — scottinabox-site

## Core

| Layer | Technology | Notes |
|-------|-----------|-------|
| Static site generator | [Hugo](https://gohugo.io) v0.x | Fast Go-based SSG, custom layouts in `layouts/`, no external theme |
| Styling | [Tailwind CSS](https://tailwindcss.com) | Loaded via CDN, utility-first |
| Hosting | [GitHub Pages](https://pages.github.com) | Deployed at `scottlorimor.com` (custom domain via `static/CNAME`) via `.github/workflows/hugo.yaml` |
| Deploy | GitHub Actions | Push to `main` builds with Hugo 0.165.0 extended, uploads `public/` artifact |
| Content | Markdown | Standard Hugo content files |
| Testing | python3 stdlib (`tests/test_site.py`) | `python3 tests/test_site.py`; CI `test` job on push and PR |
| Analytics | [Umami](https://umami.is) Cloud | Deferred script in `layouts/partials/analytics.html`, IDs in `hugo.toml` |

## Project structure

```
content/     — Markdown pages and posts
layouts/     — Hugo templates (custom, no external theme)
static/      — Static assets (images, etc.)
assets/      — Hugo asset pipeline (unused)
public/      — Build output (gitignored)
hugo.toml    — Hugo configuration
.github/workflows/hugo.yaml — GitHub Pages deploy workflow
```

## Local dev

```bash
hugo server --buildDrafts
```

## Build

```bash
hugo
```