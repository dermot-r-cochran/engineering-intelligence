# Repository-aware development

Repository-aware development uses the existing codebase as essential context for making and reviewing changes. A repository contains more than source code: its tests, documentation, history, conventions, interfaces, and configuration encode constraints and prior decisions.

## Work from the repository's evidence

Before changing code, understand the relevant behavior, nearby patterns, and available checks. Verify assumptions against files and tests rather than relying on a task description or a generated summary alone. Keep changes focused, preserve unrelated behavior, and validate the affected paths.

AI tools can help navigate and modify a codebase, but they can miss implicit constraints or produce plausible changes that do not fit. Human review should check whether a change solves the actual problem, aligns with repository conventions, and has been adequately tested.

## Shared code ages at the rate of what it abstracted

Reusable components, SDKs and templates tend to lose relevance over time, until new repositories set them aside or work around them and write fresh code instead. This is not usually a failure of the component's quality. A reusable thing is a bet on what will stay the same, and it loses relevance at the rate at which that thing changes. A component that abstracted a fact that held, such as a protocol, a data shape or a regulatory rule, keeps earning its place. One that abstracted a convenience of its moment, such as a framework's idiom, a team's preferences or the deployment target of the day, ages as those conveniences change, which is every few years.

Three conditions make the decline faster. A shared library has an owner and a consumer, and the owner's reasons to change it rarely match the consumer's reasons at the moment the consumer needs it, so the consumer forks or works around rather than waits. A template is copied, not linked, so a new repository receives whatever the template believed on the day it was copied and has no path to what it learns later. And generated code has changed the arithmetic: when fresh code costs an afternoon, understanding and bending a stale component can cost more, and a rational team writes fresh.

What holds up is thinner than a framework. A specification with a conformance test outlives several generations of implementation, because it says what must be true rather than how. A reference implementation that a new repository can read and copy the relevant part of outlives one it must depend on whole. And a retirement rule beats silent decay: a component not adopted by the next two repositories that could have used it is marked as superseded, with the reason, so later work goes around it on purpose rather than by discovery.

The repository-aware question that follows is which shared things still describe the current context and which are records of an earlier one. Both are evidence; only the first is a constraint.

The expectation that reuse pays is not wrong; it is aimed at a unit that has moved. When writing code was the expensive part, reusing code was the lever. Now the expensive parts are around the code: knowing what it must satisfy, how to tell whether it does, and why an earlier decision was made. Those reuse well, as tests, contracts, decision records and worked examples a new repository can read and copy from, because they come from experience a generator does not have. A component that wraps them in last year's idiom is cheap to regenerate, and the regeneration usually fits better. The exception is where the shared thing is itself the fact, a protocol, a schema everyone speaks, a security boundary; there divergence costs more than any awkwardness, and the discipline runs the other way.

## Case note: one check, written ten times

The section above was written from practice, and recorded on 8 October 2026, before any repository on the [evidence page](evidence.md) had tested it. The author's repositories have since produced one shared thing of exactly the kind it describes, so the claim can be held against a record. The README-proof convention (the [engineering intelligence](engineering-intelligence.md#case-note-a-readme-that-names-its-proof) page has the convention itself) needs a check in CI, and that check was never made a package. The first script was written for the [architecture-definition-model](https://github.com/dermot-r-cochran/architecture-definition-model) on 6 October 2026 as a source check for a documentation site; on 10 October it gained the README-count check and eight more repositories gained scripts of their own, and [hybrid-agent](https://github.com/dermot-r-cochran/hybrid-agent) a tenth on 31 October.

**What was tried.** Each repository received the specification, which is one sentence (a claim names its proof or says there is none), and a reference implementation to read, not a library to depend on. Four of the scripts say so in their opening lines: "The shape follows architecture-definition-model's .github/scripts/check_docs.py." in [foundation-model](https://github.com/dermot-r-cochran/foundation-model), [swarm](https://github.com/dermot-r-cochran/swarm) and [visual-llm](https://github.com/dermot-r-cochran/visual-llm), and "the shape follows foundation-model's" in hybrid-agent. Each was then written against the claims its own README makes: the sampler classes and scale presets in foundation-model, the ADR index and the module tests in swarm, the module tree in [shadow-architect](https://github.com/dermot-r-cochran/shadow-architect), the ADR range in [careful-memory](https://github.com/dermot-r-cochran/careful-memory), the normative-status line on every page of the architecture-definition-model, the lesson and question counts in [applied-statistics-for-AI-engineers](https://github.com/dermot-r-cochran/applied-statistics-for-AI-engineers), the topic list here. The ten scripts run from 101 to 233 lines and no two match. A shared library would have had to know all of those claims, or none of them.

**What the record says happened.** The cost the section predicts for copying arrived within three weeks. careful-memory's README cites nineteen tests by name as the proof of its claims, and on 27 October its check learned to resolve every citation against `tests/`, because, in the words of that day's commit, "a renamed or removed test left its row reading as proven while pointing at nothing". [world-model](https://github.com/dermot-r-cochran/world-model) and swarm cite their tests the same way, by file and name, and their checks still check what they checked on 10 October and resolve no citation, because a copy has no path to what the original learns later. The exception the section names is in the record too: [star-rangers](https://github.com/dermot-r-cochran/star-rangers) and the photography site share four byte-identical deploy scripts, and CI in each diffs them against the other's `main` ([RELATED-REPOSITORIES.md](https://github.com/dermot-r-cochran/star-rangers/blob/main/RELATED-REPOSITORIES.md)), because there the shared thing is the deploy path itself and divergence would cost more than the discipline does.

**What changed as a result.** Less than the section would predict, so far. The two checks that fell behind have not been brought level, and nothing in the related-repositories map yet marks a shared component as superseded under the retirement rule above, so that rule stands as a hypothesis by this repository's own standard. What the record does support is the thinner shape: one sentence of specification and a reference implementation to read have outlived ten writings, and each one fits its repository in a way a shared package could not have. Whether the two lagging checks are brought level by hand, or left until their repositories next change, is a decision for those repositories, and its record would belong here.

## Questions to ask

- Which files and interfaces define the behavior being changed?
- What repository conventions and historical decisions are relevant?
- What tests or checks provide evidence that behavior is preserved?
- Are there affected users, integrations, or operational constraints?
- Does the change improve the repository's long-term legibility?

## Related topics

See [context engineering](context-engineering.md) for curating repository context and [natural language programming](natural-language-programming.md) for expressing change intent.

Where this is practised: see the [evidence page](evidence.md).
