"""Site checks for scottinabox-site. Stdlib only, no new dependencies.

Run from the repo root:

    python3 tests/test_site.py

Checks:
  1. Clean `hugo --minify` build exits 0.
  2. Expected pages exist in public/ (home, story, posts index,
     hello-world post, llms.txt, favicon.svg).
  3. No broken internal links: every internal href/src in built HTML
     resolves to a file in public/, accounting for the
     /scottinabox-site/ subpath baseURL.
  4. No leftover Cloudflare/pages.dev references in built output.
"""

import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC = os.path.join(ROOT, "public")
BASE_PREFIX = "/scottinabox-site/"

EXPECTED_FILES = [
    "index.html",
    "story/index.html",
    "posts/index.html",
    "posts/hello-world/index.html",
    "llms.txt",
    "favicon.svg",
]

STALE_PATTERNS = ["cloudflare", "pages.dev", "workers.dev"]

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
    if path.startswith(BASE_PREFIX.lstrip("/")):
        path = path[len(BASE_PREFIX.lstrip("/")):] or "index.html"
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
            if not url.startswith(("/", BASE_PREFIX.lstrip("/"))):
                continue
            if resolve_internal(url) is None:
                problems.append("%s links to %s (no file in public/)" % (rel, url))
    if problems:
        return fail(problems)
    print("pass: no broken internal links (%d pages scanned)" % len(pages))
    return True


def check_no_stale_refs():
    print("check: no leftover Cloudflare/pages.dev references")
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
    print("pass: no leftover Cloudflare/pages.dev references")
    return True


def main():
    os.chdir(ROOT)
    ok = True
    ok = check_build() and ok
    if os.path.isdir(PUBLIC):
        ok = check_expected_pages() and ok
        ok = check_internal_links() and ok
        ok = check_no_stale_refs() and ok
    if ok:
        print("all site checks passed")
        return 0
    print("site checks failed")
    return 1


if __name__ == "__main__":
    sys.exit(main())
