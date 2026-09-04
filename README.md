# scottinabox-site

Personal site for Scott Lorimor, built with Hugo and deployed to Cloudflare Pages.

## Setup

Install Hugo (macOS):

```bash
brew install hugo
```

## Usage

Local dev server:

```bash
`hugo server --buildDrafts
````

Build for production:

```bash
hugo
```

Output lands in `public/`.

## Deploy

Deploy to Cloudflare Pages via Wrangler:

```bash
npx wrangler deploy
```

## Configuration

- **Hugo config**: `hugo.toml` — site title, base URL, and personal params
- **Wrangler config**: `wrangler.jsonc` — Cloudflare Pages project settings

## Stack

- [Hugo](https://gohugo.io) — static site generator
- [Tailwind CSS](https://tailwindcss.com) (CDN) — utility-first CSS
- [Cloudflare Pages](https://pages.cloudflare.com) — hosting

## License

MIT