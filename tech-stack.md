# Tech Stack — scottinabox-site

## Core

| Layer | Technology | Notes |
|-------|-----------|-------|
| Static site generator | [Hugo](https://gohugo.io) v0.x | Fast Go-based SSG, custom layouts in `layouts/`, no external theme |
| Styling | [Tailwind CSS](https://tailwindcss.com) | Loaded via CDN, utility-first |
| Hosting | [GitHub Pages](https://pages.github.com) | Deployed at `scottlorimor.github.io/scottinabox-site/` via `.github/workflows/hugo.yaml` |
| Deploy | GitHub Actions | Push to `main` builds with Hugo 0.165.0 extended, uploads `public/` artifact |
| Content | Markdown | Standard Hugo content files |

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