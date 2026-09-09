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

## Deploy

Push to `main` runs `.github/workflows/hugo.yaml`, which builds with Hugo and deploys to GitHub Pages.

Live URL: `https://scottlorimor.github.io/scottinabox-site/`

## Configuration

- **Hugo config**: `hugo.toml` — site title, base URL, and personal params

## Stack

- [Hugo](https://gohugo.io) — static site generator
- [Tailwind CSS](https://tailwindcss.com) (CDN) — utility-first CSS
- [GitHub Pages](https://pages.github.com) — hosting

## License

MIT