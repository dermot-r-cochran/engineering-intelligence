# Contributing

Contributions that make the repository more useful, accurate, and navigable are welcome. This is a knowledge project: a focused correction, useful example, or well-supported question can be as valuable as a new document.

## Before proposing a change

- Read the relevant page and its links in the [documentation index](docs/index.md).
- Prefer improving an existing page over creating a near-duplicate.
- For factual or empirical claims, provide a source or clearly identify the claim as a hypothesis, interpretation, or open question.
- Explain why a proposal matters and who could use it.

## Writing and review

- Use clear, direct language; define specialized terms where they first appear.
- Distinguish evidence from opinion, and describe limitations and uncertainty.
- Prefer concrete examples and evaluation criteria to unsupported predictions.
- Consider effects on people, privacy, safety, accessibility, and human accountability.
- Link related pages so readers can follow concepts across the repository.

## Submitting changes

Keep changes focused and use descriptive commit or pull request summaries. For substantive changes, describe the problem, the evidence or reasoning behind the proposed approach, and any unresolved questions. Documentation-only changes do not need a software test suite; check links, spelling, and Markdown structure before submitting.

Before pushing, run the checks CI runs:

```bash
python3 tools/check_links.py
python3 tools/check_docs.py
```

## How a pull request is reviewed

The repository has one maintainer, Dermot Cochran, so a pull request may wait a while before anyone looks at it.

- CI must be green. A failing check is the first thing to fix.
- The review may be assisted by an AI tool, which reads the change and reports to the maintainer. It does not approve or merge anything.
- **Every outside pull request is merged by the maintainer, never by an automated process or an AI tool,** however small.
- A pull request may be declined, or asked to change shape, when it moves the project somewhere it is not meant to go. That is not a judgement on the work.

## Licence

Contributions are accepted under this repository's licence, the MIT License (`LICENSE`), the same terms everyone else receives it under. No sign-off line and no contributor licence agreement are required. Only contribute work you have the right to license on these terms.
