# Engineering intelligence

Engineering intelligence is the practice of improving engineering decisions and outcomes by bringing together people, technical systems, evidence, and accumulated knowledge. It is not simply automation or a measure of individual intelligence. It concerns how a group or system notices what matters, learns from results, and adapts its work.

## A working perspective

Engineering work takes place within a context: goals, constraints, tools, prior decisions, and the people affected by the result. Useful intelligence depends on making that context legible, testing assumptions against evidence, and incorporating feedback. AI can contribute analysis or generation, but people remain responsible for goals, trade-offs, and decisions.

## Case note: a README that names its proof

The first principle here is evidence over assertion, and the cheapest place to practise it is a repository's own README, which is where most of its assertions live. The convention, decided on 10 October 2026 after a review found README claims with no check behind them, and since called the README-proof convention in the repositories that carry it: a row or line that claims a capability names the test that proves it, as the test runner addresses it (file, class and test), or says plainly that there is none yet; and a documentation check in CI fails the pull request if a named test does not exist or a count in the README no longer matches the code.

**What was tried.** Eight repositories by the same author adopted it on that one day: [careful-memory](https://github.com/dermot-r-cochran/careful-memory), [shadow-architect](https://github.com/dermot-r-cochran/shadow-architect), [world-model](https://github.com/dermot-r-cochran/world-model), [foundation-model](https://github.com/dermot-r-cochran/foundation-model), [swarm](https://github.com/dermot-r-cochran/swarm), [visual-llm](https://github.com/dermot-r-cochran/visual-llm), [applied-statistics-for-AI-engineers](https://github.com/dermot-r-cochran/applied-statistics-for-AI-engineers) and this one, each with a standard-library `check_docs` script in CI. The [architecture-definition-model](https://github.com/dermot-r-cochran/architecture-definition-model) carries the same table (its *What Is Checked* section) for a repository that is a specification rather than code, where the claims are about documents. In this repository the convention is the last paragraph of the README and `tools/check_docs.py`.

**What the record says happened.** The convention sorts a README's claims into three kinds that read differently: proved (a named test that exists), open (a row that says "designed, not implemented" or "no test yet"), and not a claim code can prove at all, which is what the principles on these pages are and why the [evidence page](evidence.md) exists. careful-memory's README records the first repair: from 27 October 2026 its check resolves every named test against `tests/`, because a renamed or removed guard had otherwise left its row reading as proven. The architecture-definition-model records the limit: a check can prove that a status line is present and well formed, but whether the status chosen is the right one is still a judgement.

**What changed as a result.** A README under the convention reads as a list of promises with a pointer beside each, and a reader who doubts a row has one file to open. The cost is a line per claim and a short script; what it buys is that the document and the code can no longer drift apart silently. What it does not buy is the correctness of the test itself, or any judgement call; those stay with the reader, as the [human-AI systems](human-ai-systems.md) page says they should.

## Questions to ask

- What outcome are we trying to improve, and for whom?
- What evidence supports the current understanding of the problem?
- Which knowledge and constraints should inform the work?
- How will we tell whether the result is useful, reliable, and acceptable?
- What did the result teach us that should change future work?

## Related topics

Explore [human-AI systems](human-ai-systems.md), [AI evaluation](ai-evaluation.md), and [repository-aware development](repository-aware-development.md).

Where this is practised: see the [evidence page](evidence.md).
