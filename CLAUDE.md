# scottinabox-site

## Project context

This is a personal website project built with Hugo, a static site generator. The goal is to create a site called "scottinabox-site" that serves as a web presence. Hugo will handle the templating, content management, and static site generation. The project likely involves configuring Hugo themes, organizing content in markdown, and deploying the generated static files.

## Conventions

- Lead with the point. Be concrete: name files, functions, line numbers.
- Tie technical choices to user outcomes.
- Avoid corporate filler. No em dashes. No AI vocabulary (delve, crucial, robust, comprehensive, nuanced, intricate, foster, showcase, underscore, significant).
- DRY matters. Flag repetition.
- Tests are non-negotiable.
- Explicit > clever. Right-sized diff > minimal diff at the cost of clarity.
- Handle edge cases. Thoughtfulness > speed.

## Testing

Framework: `tests/test_site.py`, plain python3 with stdlib only. No new dependencies.

Run command: `python3 tests/test_site.py` (from the repo root).

The script does a clean `hugo --minify` build, then checks expected
pages exist in `public/`, internal links resolve to files in `public/`
(accounting for the `/scottinabox-site/` subpath baseURL), and built
output has no leftover Cloudflare/pages.dev references.

CI runs the same script as the `test` job in `.github/workflows/hugo.yaml`
on pushes to `main` and on pull requests. The `deploy` job runs on push only.

- Aim for 100% coverage on new logic. AI makes completeness cheap.
- Write a regression test for every fix.
- Cover both branches of every conditional. Apply with judgment on static
  content: the link resolver in `tests/test_site.py:resolve_internal`
  handles quoted and unquoted hrefs, directory and file targets.

## Skill routing

When the user's request matches an available skill, invoke it via the Skill tool. When in doubt, invoke the skill.

- Product ideas / brainstorming → `/office-hours`
- Strategy / scope → `/plan-ceo-review`
- Architecture → `/plan-eng-review`
- Design system / plan review → `/design-consultation` or `/plan-design-review`
- Full review pipeline → `/autoplan`
- Bugs / errors → `/investigate`
- QA / testing site behavior → `/qa` or `/qa-only`
- Code review / diff check → `/review`
- Visual polish → `/design-review`
- Ship / deploy / PR → `/ship` or `/land-and-deploy`
- Save progress → `/context-save`
- Resume context → `/context-restore`