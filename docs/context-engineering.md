# Context engineering

Context engineering is the deliberate selection, organization, and maintenance of the information and resources available to an AI system for a task. Context can include instructions, repository files, examples, conversation history, tools, and constraints. Its quality affects what the system can notice and how well its output fits the task.

## Make context useful

Start from the task and identify the information needed to complete it safely and correctly. Prefer relevant, authoritative, current sources over large volumes of loosely related material. Make priorities, constraints, and expected outputs explicit, and preserve links back to source material where possible.

Context is not a substitute for evaluation. Information may be incomplete, stale, or contradictory; generated outputs may still be wrong. Review important sources, expose uncertainty, and update context as the task or environment changes. Avoid including sensitive information unless it is necessary and authorized.

## Questions to ask

- What does the system need to know to perform this task?
- Which sources are authoritative, current, and relevant?
- What constraints or uncertainties could change the answer?
- Is any included information sensitive or unnecessary?
- How will the output be checked against its sources and intended use?

## Related topics

Context is a core part of [repository-aware development](repository-aware-development.md) and [human-AI systems](human-ai-systems.md).

Where this is practised: see the [evidence page](evidence.md).
