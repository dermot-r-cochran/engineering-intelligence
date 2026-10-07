# Repository-aware development

Repository-aware development uses the existing codebase as essential context for making and reviewing changes. A repository contains more than source code: its tests, documentation, history, conventions, interfaces, and configuration encode constraints and prior decisions.

## Work from the repository's evidence

Before changing code, understand the relevant behavior, nearby patterns, and available checks. Verify assumptions against files and tests rather than relying on a task description or a generated summary alone. Keep changes focused, preserve unrelated behavior, and validate the affected paths.

AI tools can help navigate and modify a codebase, but they can miss implicit constraints or produce plausible changes that do not fit. Human review should check whether a change solves the actual problem, aligns with repository conventions, and has been adequately tested.

## Questions to ask

- Which files and interfaces define the behavior being changed?
- What repository conventions and historical decisions are relevant?
- What tests or checks provide evidence that behavior is preserved?
- Are there affected users, integrations, or operational constraints?
- Does the change improve the repository's long-term legibility?

## Related topics

See [context engineering](context-engineering.md) for curating repository context and [natural language programming](natural-language-programming.md) for expressing change intent.

Where this is practised: see the [evidence page](evidence.md).
