# Tech Stack — scottinabox-site

## Core

| Layer | Technology | Notes |
|-------|-----------|-------|
| Static site generator | [Hugo](https://gohugo.io) v0.x | Fast Go-based SSG, custom layouts in `layouts/`, no external theme |
| Styling | [Tailwind CSS](https://tailwindcss.com) | Loaded via CDN, utility-first |
| Hosting | [Cloudflare Pages](https://pages.cloudflare.com) | Deployed at `scottinabox.pages.dev` |
| Deploy CLI | [Wrangler](https://developers.cloudflare.com/wrangler/) | `npx wrangler deploy` to push `public/` |
| Content | Markdown | Standard Hugo content files |

## Project structure

```
content/     — Markdown pages and posts
layouts/     — Hugo templates (custom, no external theme)
static/      — Static assets (images, etc.)
assets/      — Hugo asset pipeline (unused)
public/      — Build output (gitignored)
hugo.toml    — Hugo configuration
wrangler.jsonc — Cloudflare Pages configuration
```

## Local dev

```bash
hugo server --buildDrafts
```

## Build

```bash
hugo
```