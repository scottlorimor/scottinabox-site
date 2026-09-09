"""Site checks for scottinabox-site. Stdlib only, no new dependencies.

Run from the repo root:

    python3 tests/test_site.py

Checks:
  1. Clean `hugo --minify` build exits 0.
   2. Expected pages exist in public/ (home, story, posts index,
      hello-world post, llms.txt, favicon.svg, CNAME).
   3. No broken internal links: every internal href/src in built HTML
      resolves to a file in public/, accounting for the baseURL
      path prefix from hugo.toml (root `/` on the custom domain,
      `/scottinabox-site/` on the github.io project URL).
   4. No leftover Cloudflare/pages.dev references in built output,
      and no stale scottlorimor.github.io references now that the
      site serves from the custom domain.
   5. Umami analytics partial is wired into baseof.html, renders
      nothing when `umamiWebsiteID` is empty, and renders the
      deferred script with the configured src plus ID when set.
"""

import os
import re
import shutil
import subprocess
import sys
from urllib.parse import urlsplit

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC = os.path.join(ROOT, "public")


def load_base_prefix():
    """Read the baseURL path prefix from hugo.toml (root `/` if none)."""
    try:
        with open(os.path.join(ROOT, "hugo.toml"), encoding="utf-8") as handle:
            text = handle.read()
    except OSError:
        return "/"
    match = re.search(r"""^baseURL\s*=\s*['"]([^'"]+)['"]""", text, re.MULTILINE)
    if not match:
        return "/"
    path = urlsplit(match.group(1)).path or "/"
    if not path.endswith("/"):
        path += "/"
    return path


BASE_PREFIX = load_base_prefix()
PREFIX_BARE = BASE_PREFIX.lstrip("/")

EXPECTED_FILES = [
    "index.html",
    "story/index.html",
    "posts/index.html",
    "posts/hello-world/index.html",
    "llms.txt",
    "favicon.svg",
    "CNAME",
]

STALE_PATTERNS = ["cloudflare", "pages.dev", "workers.dev", "scottlorimor.github.io"]

UMAMI_DEFAULT_SRC = "https://cloud.umami.is/script.js"
UMAMI_TEST_SRC = "https://umami.example.test/script.js"
UMAMI_TEST_ID = "test-website-id-1234"

LINK_RE = re.compile(
    r'''(?:href|src)\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+))''',
    re.IGNORECASE,
)

EXTERNAL_PREFIXES = ("http://", "https://", "//", "mailto:", "tel:", "data:", "#")


def fail(messages):
    for message in messages:
        print("FAIL: " + message)
    return False


def check_build():
    print("check: hugo build succeeds")
    if shutil.which("hugo") is None:
        return fail(["hugo binary not found on PATH"])
    shutil.rmtree(PUBLIC, ignore_errors=True)
    result = subprocess.run(
        ["hugo", "--minify"], cwd=ROOT, capture_output=True, text=True
    )
    if result.returncode != 0:
        return fail(["hugo --minify exited %d" % result.returncode, result.stderr.strip()])
    print("pass: hugo build succeeds")
    return True


def check_expected_pages():
    print("check: expected pages exist in public/")
    missing = [
        path for path in EXPECTED_FILES
        if not os.path.isfile(os.path.join(PUBLIC, path))
    ]
    if missing:
        return fail(["missing in public/: " + path for path in missing])
    print("pass: expected pages exist in public/")
    return True


def resolve_internal(url):
    """Map an internal URL to a file under public/. Return None if missing."""
    path = url.split("#", 1)[0].split("?", 1)[0]
    if not path or path == "/":
        path = "index.html"
    elif path.startswith(BASE_PREFIX):
        path = path[len(BASE_PREFIX):] or "index.html"
    elif path.startswith("/"):
        path = path[1:]
    if PREFIX_BARE and path.startswith(PREFIX_BARE):
        path = path[len(PREFIX_BARE):] or "index.html"
    candidates = [path]
    if not os.path.splitext(path)[1]:
        candidates = [path + ".html", path.rstrip("/") + "/index.html", path]
    for candidate in candidates:
        full = os.path.join(PUBLIC, candidate)
        if os.path.isfile(full):
            return full
    return None


def check_internal_links():
    print("check: no broken internal links")
    problems = []
    pages = []
    for dirpath, _dirs, files in os.walk(PUBLIC):
        for name in files:
            if name.endswith(".html"):
                pages.append(os.path.join(dirpath, name))
    if not pages:
        return fail(["no HTML pages found in public/"])
    for page in pages:
        with open(page, encoding="utf-8") as handle:
            html = handle.read()
        rel = os.path.relpath(page, PUBLIC)
        for match in LINK_RE.finditer(html):
            url = match.group(1) or match.group(2) or match.group(3) or ""
            if not url or url.startswith(EXTERNAL_PREFIXES):
                continue
            if not url.startswith("/"):
                if not PREFIX_BARE or not url.startswith(PREFIX_BARE):
                    continue
            if resolve_internal(url) is None:
                problems.append("%s links to %s (no file in public/)" % (rel, url))
    if problems:
        return fail(problems)
    print("pass: no broken internal links (%d pages scanned)" % len(pages))
    return True


def check_no_stale_refs():
    print("check: no stale hosting references")
    problems = []
    for dirpath, _dirs, files in os.walk(PUBLIC):
        for name in files:
            full = os.path.join(dirpath, name)
            try:
                with open(full, encoding="utf-8") as handle:
                    content = handle.read()
            except (UnicodeDecodeError, OSError):
                continue
            lowered = content.lower()
            for pattern in STALE_PATTERNS:
                if pattern in lowered:
                    problems.append(
                        "%s contains %r" % (os.path.relpath(full, PUBLIC), pattern)
                    )
    if problems:
        return fail(problems)
    print("pass: no stale hosting references")
    return True


def load_umami_config(text=None):
    """Return (url, website_id) from hugo.toml text (default: read the file)."""
    if text is None:
        with open(os.path.join(ROOT, "hugo.toml"), encoding="utf-8") as handle:
            text = handle.read()
    url = re.search(
        r"""^[ \t]*umamiURL\s*=\s*['"]([^'"]*)['"]""", text, re.MULTILINE
    )
    site_id = re.search(
        r"""^[ \t]*umamiWebsiteID\s*=\s*['"]([^'"]*)['"]""", text, re.MULTILINE
    )
    return (
        url.group(1).strip() if url else "",
        site_id.group(1).strip() if site_id else "",
    )


def built_html_files():
    pages = []
    for dirpath, _dirs, files in os.walk(PUBLIC):
        for name in files:
            if name.endswith(".html"):
                pages.append(os.path.join(dirpath, name))
    return pages


def rebuild():
    result = subprocess.run(
        ["hugo", "--minify"], cwd=ROOT, capture_output=True, text=True
    )
    return result


def check_analytics():
    print("check: umami analytics wiring plus both render branches")
    problems = []
    partial = os.path.join(ROOT, "layouts", "partials", "analytics.html")
    try:
        with open(partial, encoding="utf-8") as handle:
            partial_text = handle.read()
    except OSError:
        return fail(["missing layouts/partials/analytics.html"])
    for needle in ("data-website-id", "defer", "umamiWebsiteID", "umamiURL"):
        if needle not in partial_text:
            problems.append("analytics.html missing %r" % needle)
    baseof = os.path.join(ROOT, "layouts", "_default", "baseof.html")
    try:
        with open(baseof, encoding="utf-8") as handle:
            baseof_text = handle.read()
    except OSError:
        return fail(["missing layouts/_default/baseof.html"])
    if "analytics.html" not in baseof_text:
        problems.append("baseof.html does not include analytics.html partial")
    try:
        with open(os.path.join(ROOT, "hugo.toml"), encoding="utf-8") as handle:
            config_text = handle.read()
    except OSError:
        return fail(["missing hugo.toml"])
    if "umamiURL" not in config_text or "umamiWebsiteID" not in config_text:
        problems.append("hugo.toml missing umamiURL/umamiWebsiteID params")
    if problems:
        return fail(problems)

    url, site_id = load_umami_config(config_text)
    pages = built_html_files()
    if not pages:
        return fail(["no HTML pages found in public/"])
    if not site_id:
        for page in pages:
            with open(page, encoding="utf-8") as handle:
                html = handle.read()
            if "data-website-id" in html:
                problems.append(
                    "%s renders analytics script with empty umamiWebsiteID"
                    % os.path.relpath(page, PUBLIC)
                )
        if problems:
            return fail(problems)
        print("pass: analytics renders nothing when umamiWebsiteID is empty")
    else:
        expected_src = url or UMAMI_DEFAULT_SRC
        home = os.path.join(PUBLIC, "index.html")
        with open(home, encoding="utf-8") as handle:
            html = handle.read()
        if "data-website-id" not in html or site_id not in html:
            problems.append("home page missing configured data-website-id")
        if expected_src not in html:
            problems.append("home page missing configured umami src")
        if problems:
            return fail(problems)
        print("pass: analytics renders configured script on home page")

    config_path = os.path.join(ROOT, "hugo.toml")
    with open(config_path, encoding="utf-8") as handle:
        original = handle.read()
    patched = re.sub(
        r"""^[ \t]*umamiURL\s*=\s*['"][^'"]*['"]""",
        "umamiURL = '%s'" % UMAMI_TEST_SRC,
        original,
        flags=re.MULTILINE,
    )
    patched = re.sub(
        r"""^[ \t]*umamiWebsiteID\s*=\s*['"][^'"]*['"]""",
        "umamiWebsiteID = '%s'" % UMAMI_TEST_ID,
        patched,
        flags=re.MULTILINE,
    )
    try:
        with open(config_path, "w", encoding="utf-8") as handle:
            handle.write(patched)
        result = rebuild()
        if result.returncode != 0:
            return fail(
                ["hugo rebuild with test umami config exited %d" % result.returncode]
            )
        home = os.path.join(PUBLIC, "index.html")
        with open(home, encoding="utf-8") as handle:
            html = handle.read()
        if UMAMI_TEST_SRC not in html or UMAMI_TEST_ID not in html:
            problems.append("configured branch missing test src plus ID")
        if "defer" not in html.lower() or "data-website-id" not in html:
            problems.append("configured branch missing defer plus data-website-id")
        if problems:
            return fail(problems)
        print("pass: analytics renders script when umamiWebsiteID is set")
        return True
    finally:
        with open(config_path, "w", encoding="utf-8") as handle:
            handle.write(original)
        rebuild()


def main():
    os.chdir(ROOT)
    ok = True
    ok = check_build() and ok
    if os.path.isdir(PUBLIC):
        ok = check_expected_pages() and ok
        ok = check_internal_links() and ok
        ok = check_no_stale_refs() and ok
        ok = check_analytics() and ok
    if ok:
        print("all site checks passed")
        return 0
    print("site checks failed")
    return 1


if __name__ == "__main__":
    sys.exit(main())
