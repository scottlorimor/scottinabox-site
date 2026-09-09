# CHANGELOG

## 2026-09-08 — Homepage redesign

- Changed background to dark concrete (#2c2c2a) with SVG fractal noise texture
- Restructured homepage: "Scott's Story" → /story/, "Let's do some work together" → LinkedIn, "Get in touch" → obfuscated mailto
- Added "Thinking" section linking to /posts/
- Removed "I do stuff" bio paragraph
- Positioned content with margin-right: 350px, margin-bottom: 200px for Z-pattern eye tracking
- Created 4 SVG icon partials: thinking (brain), story (book), work (overlapping circles), touch (envelope)
- Icons placed outside links, stroke 2, color #a8a8a8; links styled sage green (#b5c9a9) with #e2eccd hover
- Icons scaled to 1.66em with 0.41em right margin
- Reordered sections: Scott's Story first, Thinking second
- Swapped fonts: DM Sans 300 (body), DM Serif Display 400 (headings); removed all-caps from sub-headings
- Changed story icon to open book shape
- Added mobile responsive breakpoint at 768px (resets margins, full-width main)
- Updated backlog: marked placeholder content done, replaced "about page" with "My Story" post, removed light/dark toggle, added real email task, added llms.txt task
- Scaffolded blog section: content/posts/_index.md, layouts/_default/list.html, layouts/_default/single.html
- Hugo builds clean (5 pages)
- Created hello-world.md test post in content/posts/hello-world/
- Numbered all backlog tasks under respective headers for easier reference
- Added SVG favicon (static/favicon.svg) with dark concrete background and sage "S"
- Added llms.txt at static/llms.txt with site info, key pages, and contact
- Centered blog content: .content-page class with max-width 40rem, margin auto
- Removed timestamps from /posts/ listing; kept timestamps on single post pages
- Made single.html conditional: timestamp + "Back to Thinking" only for /posts/, "Home" link for other pages
- Created blank Scott's Story page at content/story.md

---

**Token totals:** 725.2k in | 21.7k out | 20.0k reasoning | 7943.7k cache read | 0.0k cache write | $1.38