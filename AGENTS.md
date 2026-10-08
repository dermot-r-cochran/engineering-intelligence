# Repository guidance

This repository is a knowledge system first and a software project second. When contributing:

- Follow the principles in the README: evidence over assertion, evaluation over hype, context over isolated prompts, and human judgment over automation.
- Preserve the distinction between sourced evidence, interpretation, and speculation. Cite sources for claims that depend on external facts.
- Keep writing practical, clear, and accessible. Avoid jargon, unsupported certainty, and content that duplicates an existing page.
- Treat human impact, privacy, safety, accessibility, and accountability as part of system design and evaluation.
- Prefer focused changes that improve the accuracy, usefulness, or navigation of the knowledge base.
- Do not invent sources, findings, repository conventions, or test results. State uncertainty plainly.

Before finishing a change, review the rendered Markdown structure and verify that links to repository pages resolve: `python3 tools/check_links.py` does this (standard library only, run on every pull request by the Links workflow), and a broken relative link fails the check. Run existing checks when relevant; do not introduce build or test tooling for documentation-only edits without a clear need.
