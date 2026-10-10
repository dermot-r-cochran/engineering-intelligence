#!/usr/bin/env python3
"""Check that the README's lists match what is on disk, and that no Markdown
file carries more than one front-matter block.

Standard library only; nothing to install. The companion check_links.py
proves that links resolve; this check proves the two claims a link check
cannot: that the README and docs/index.md list every topic page under
docs/ and nothing that is not there, and that no page has picked up a
second front-matter block (what a stray fragment left by a merge looks
like). A topic page is any docs/*.md other than index.md and evidence.md.

    python3 tools/check_docs.py            # exit 1 and list every problem

Run by .github/workflows/links.yml on every pull request.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
NOT_TOPICS = {"index.md", "evidence.md"}
LINK = re.compile(r"\[[^\]]*\]\(([^)\s#]+)")
SKIP_DIRS = {".git", "node_modules", "_site"}


def markdown_files():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            if name.lower().endswith(".md"):
                yield os.path.join(dirpath, name)


def front_matter_blocks(text):
    """Count front-matter blocks: a '---' line opening a block closed by another,
    at the top of the file or immediately after a previous block."""
    lines = text.replace("\r\n", "\n").split("\n")
    count = 0
    i = 0
    while i < len(lines) and lines[i].strip() == "---":
        close = next((j for j in range(i + 1, len(lines)) if lines[j].strip() == "---"), None)
        if close is None:
            break
        count += 1
        i = close + 1
        while i < len(lines) and not lines[i].strip():
            i += 1
    return count


def section(text, heading):
    """The lines of one '## heading' section, up to the next heading."""
    match = re.search(rf"^## {re.escape(heading)}\s*$(.*?)(?=^#|\Z)", text, re.M | re.S)
    return match.group(1) if match else ""


def listed_pages(text, prefix):
    """Topic pages linked from a section, as bare file names under docs/."""
    found = set()
    for target in LINK.findall(text):
        if target.startswith(prefix) and target.endswith(".md"):
            name = target[len(prefix):]
            if "/" not in name and name not in NOT_TOPICS:
                found.add(name)
    return found


def on_disk():
    return {n for n in os.listdir(DOCS) if n.endswith(".md") and n not in NOT_TOPICS}


def compare(label, listed, disk, problems):
    for missing in sorted(disk - listed):
        problems.append(f"{label} does not list docs/{missing}")
    for extra in sorted(listed - disk):
        problems.append(f"{label} lists docs/{extra}, which is not a topic page on disk")


def check():
    problems = []
    for md in sorted(markdown_files()):
        with open(md, encoding="utf-8") as f:
            text = f.read()
        blocks = front_matter_blocks(text)
        if blocks > 1:
            problems.append(f"{os.path.relpath(md, ROOT).replace(os.sep, '/')}: {blocks} front-matter blocks")

    disk = on_disk()
    with open(os.path.join(ROOT, "README.md"), encoding="utf-8") as f:
        readme = f.read()
    with open(os.path.join(DOCS, "index.md"), encoding="utf-8") as f:
        index = f.read()
    compare("README.md Explore", listed_pages(section(readme, "Explore"), "docs/"), disk, problems)
    compare("docs/index.md Topics", listed_pages(section(index, "Topics"), ""), disk, problems)

    print(f"check_docs: {len(disk)} topic page(s) under docs/")
    for p in problems:
        print("PROBLEM  " + p)
    if problems:
        print(f"check_docs: {len(problems)} problem(s)")
        return 1
    print("check_docs: README and docs/index.md list every topic page; no file has more than one front-matter block")
    return 0


if __name__ == "__main__":
    sys.exit(check())
