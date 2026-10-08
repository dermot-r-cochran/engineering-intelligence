#!/usr/bin/env python3
"""Check that every relative link in the repository's Markdown resolves.

Standard library only; nothing to install. Walks every *.md file outside .git,
finds Markdown links and images of the form [text](target) and bare reference
definitions [id]: target, and fails if a relative target does not exist on
disk. External links (any scheme such as https:) and mailto are out of scope,
as AGENTS.md's rule is about repository pages. A fragment on a repository
page (page.md#heading) is checked against that page's headings.

    python3 tools/check_links.py            # exit 1 and list every broken link
    python3 tools/check_links.py --quiet    # only the failures

Run by .github/workflows/links.yml on every pull request.
"""
import os
import re
import sys
import urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LINK = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
REFDEF = re.compile(r"^\s*\[[^\]]+\]:\s*(\S+)", re.M)
HEADING = re.compile(r"^#{1,6}\s+(.*?)\s*#*\s*$", re.M)
SKIP_DIRS = {".git", "node_modules", "_site"}


def slug(heading):
    """GitHub's heading anchor: lower-case, punctuation dropped, spaces to hyphens."""
    text = re.sub(r"[`*_~\[\]()!]", "", heading).strip().lower()
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"\s+", "-", text)


def headings_of(path, cache):
    if path not in cache:
        try:
            with open(path, encoding="utf-8") as f:
                cache[path] = {slug(h) for h in HEADING.findall(f.read())}
        except OSError:
            cache[path] = set()
    return cache[path]


def markdown_files():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            if name.lower().endswith(".md"):
                yield os.path.join(dirpath, name)


def check(quiet=False):
    broken = []
    checked = 0
    cache = {}
    for md in sorted(markdown_files()):
        with open(md, encoding="utf-8") as f:
            text = f.read()
        targets = LINK.findall(text) + REFDEF.findall(text)
        for raw in targets:
            target = raw.strip("<>")
            parsed = urllib.parse.urlsplit(target)
            if parsed.scheme or target.startswith("//"):
                continue  # external: out of scope
            path_part = urllib.parse.unquote(parsed.path)
            fragment = parsed.fragment
            if path_part:
                base = ROOT if path_part.startswith("/") else os.path.dirname(md)
                full = os.path.normpath(os.path.join(base, path_part.lstrip("/")))
            else:
                full = md  # a bare #fragment on the same page
            checked += 1
            rel_md = os.path.relpath(md, ROOT)
            if not os.path.exists(full):
                broken.append(f"{rel_md}: {target} -> {os.path.relpath(full, ROOT)} does not exist")
                continue
            if fragment and full.lower().endswith(".md") and fragment.lower() not in headings_of(full, cache):
                broken.append(f"{rel_md}: {target} -> no heading '{fragment}' in {os.path.relpath(full, ROOT)}")
    if not quiet:
        print(f"check_links: {checked} relative link(s) checked across the repository's Markdown")
    for b in broken:
        print("BROKEN  " + b)
    if broken:
        print(f"check_links: {len(broken)} broken link(s)")
        return 1
    if not quiet:
        print("check_links: all relative links resolve")
    return 0


if __name__ == "__main__":
    sys.exit(check(quiet="--quiet" in sys.argv[1:]))
