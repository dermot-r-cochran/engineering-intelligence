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

## Questions to ask

- Which files and interfaces define the behavior being changed?
- What repository conventions and historical decisions are relevant?
- What tests or checks provide evidence that behavior is preserved?
- Are there affected users, integrations, or operational constraints?
- Does the change improve the repository's long-term legibility?

## Related topics

See [context engineering](context-engineering.md) for curating repository context and [natural language programming](natural-language-programming.md) for expressing change intent.

Where this is practised: see the [evidence page](evidence.md).
