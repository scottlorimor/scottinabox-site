# Architecture — scottinabox-site

Static Hugo site. Sources build to `public/`, which deploys to GitHub Pages on every push to `main`.

```mermaid
flowchart LR
    content["content/ — markdown pages + posts"]
    layouts["layouts/ — templates + partials"]
    static["static/ — CNAME, favicon, llms.txt"]
    config["hugo.toml — baseURL + params"]
    content --> hugo
    layouts --> hugo
    static --> hugo
    config --> hugo
    hugo["hugo --minify"] --> public["public/ — build output, gitignored"]
    public --> tests["tests/test_site.py — 6 checks"]
    tests -->|pass| workflow[".github/workflows/hugo.yaml — test + deploy jobs"]
    workflow --> pages["GitHub Pages"]
    pages --> site["scottlorimor.com"]
    site --> umami["Umami Cloud — deferred pageview script"]
    site --> agents["agents — via /llms.txt"]
```

## Notes

- Local dev runs `hugo server --buildDrafts`, production builds with `hugo --minify` (Hugo 0.165.0 extended in CI).
- CI runs the `test` job on pushes and pull requests. The `deploy` job runs on push to `main` only.
- `public/` is gitignored and rebuilt from scratch by every build and test run.
- Analytics renders only when `umamiWebsiteID` is set in `hugo.toml`. See `layouts/partials/analytics.html`.
