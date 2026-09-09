# scottinabox-site

Personal site for Scott Lorimor, built with Hugo and deployed to GitHub Pages.

## Setup

Install Hugo (macOS):

```bash
brew install hugo
```

Enable the git hooks (blocks direct pushes to `main`):

```bash
git config core.hooksPath .githooks
```

Start each backlog item on a feature branch (an opencode guard blocks edits on `main`):

```
/start-todo <section> <n>
```

## Usage

Local dev server:

```bash
hugo server --buildDrafts
```

Build for production:

```bash
hugo
```

Output lands in `public/`.

## Tests

Site checks live in `tests/test_site.py` (python3 stdlib only, no install step):

```bash
python3 tests/test_site.py
```

The script builds with `hugo --minify`, then checks expected pages exist,
internal links resolve, and built output has no leftover Cloudflare/pages.dev
references. CI runs the same script on pushes and pull requests.

## Deploy

Push to `main` runs `.github/workflows/hugo.yaml`, which builds with Hugo and deploys to GitHub Pages.

Live URL: `https://scottlorimor.com/`

## Configuration

- **Hugo config**: `hugo.toml` — site title, base URL, and personal params

## Stack

- [Hugo](https://gohugo.io) — static site generator
- [Tailwind CSS](https://tailwindcss.com) (CDN) — utility-first CSS
- [GitHub Pages](https://pages.github.com) — hosting

## License

MIT