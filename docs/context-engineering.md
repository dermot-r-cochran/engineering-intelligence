# Context engineering

Context engineering is the deliberate selection, organization, and maintenance of the information and resources available to an AI system for a task. Context can include instructions, repository files, examples, conversation history, tools, and constraints. Its quality affects what the system can notice and how well its output fits the task.

## Make context useful

Start from the task and identify the information needed to complete it safely and correctly. Prefer relevant, authoritative, current sources over large volumes of loosely related material. Make priorities, constraints, and expected outputs explicit, and preserve links back to source material where possible.

Context is not a substitute for evaluation. Information may be incomplete, stale, or contradictory; generated outputs may still be wrong. Review important sources, expose uncertainty, and update context as the task or environment changes. Avoid including sensitive information unless it is necessary and authorized.

## Case note: what the model is told

The section above asks for context that is relevant, current and explicit about its limits, and says that context is not a substitute for evaluation. [careful-memory](https://github.com/dermot-r-cochran/careful-memory), the repository the [evidence page](evidence.md) lists for this topic, recorded on 10 April 2026, the day of the repository's first commit (the decision records themselves carry an earlier placeholder date), exactly what a language model is told from its store and how, in three of its decision records (ADR-0006, ADR-0011 and ADR-0012).

**What was tried.** Memory reaches the model's prompt as text and nothing else: no fine-tuning, no per-user adapter, no raw retrieved text. Only active beliefs at or above a confidence threshold (0.6 by default) go into the prompt, strongest first, each as one hedged sentence, "It is probably that Alice prefers dark mode", so the model is told how far to trust each line and the prompt never carries the counts behind it. When nothing qualifies, the block says so, "No reliable memories are available for this user context", rather than leaving an empty section. The preamble tells the model to ground every long-term assumption in the block and to express uncertainty where the block is uncertain. An agent reaches the store through three tools, and no tool result carries the two Bayesian counters. The store has no evidence type for model inference, on purpose, so model output cannot be recorded as what it is; an agent that files its own output under one of the three permitted types is not stopped by the enum.

**What the record says happened.** Most of that has a test in the repository: the preamble and its uncertainty line (`tests/test_prompt.py::TestSystemPreamble::test_preamble_in_system_prompt`, `::test_uncertainty_instruction_present`), the no-memory line (`::TestNoMemoryCase::test_placeholder_when_empty`), the hedge wording (`::TestMemoryInjection::test_confidence_language_present`), the three tools and the absent counters (`tests/test_tools.py::TestThreeToolSurface`, three tests added on 31 October 2026 after the first row of the README's guarantee table had admitted that no test pinned the count of three), the missing evidence type (`tests/test_poisoning_and_isolation.py::TestSelfReinforcement::test_no_llm_inference_evidence_type`), and that building the prompt writes nothing (`tests/test_service.py::TestSummaryAndPrompt::test_assemble_prompt_is_read_only`). The threshold, the active-only filter and the strongest-first order have none. The README's Quick Start, which ends by printing the assembled block, has been run as printed by a test since 19 October 2026; that day's pull request records that it had not run as printed before, because its proposal gave no evidence type and the gate blocked it, and no test had run the block. Two things the record does not support. ADR-0011 says instruction-following is probabilistic and the memory layer "cannot guarantee the model respects it"; nothing in the repository calls a model, so whether one does is untested there. The second is currency: both ADR-0005 and ADR-0011 oblige decay to be applied before a record goes into a prompt, so that a belief no one has reinforced is not told with last month's confidence; in the code, decay is a separate platform call, `run_decay`, and `assemble_prompt` reads records as last stored, while the risk register's R-11 row says decay is applied in `build_summary()`, which it is not. A prompt built between decay runs carries whatever confidence was last persisted.

**What changed as a result.** The read side of the store has a test behind most of its promises, and the README names some of them, which is the README-proof convention of the [engineering intelligence](engineering-intelligence.md#case-note-a-readme-that-names-its-proof) page applied to what a model is told. The README also claims the one promise none of those tests reach, that the agent is "grounded in verifiable, decay-adjusted beliefs", and names no test beside it. The decay-before-prompt rule is written in two decision records, a risk-register row and that README line, and run by nothing, so the warning above, that context may be stale, holds even in a repository with decay built in for that reason. Whether the repair is to apply decay on the read path without persisting it, or to record the rule as the caller's duty, is a decision for that repository, and its record would belong here.

## Questions to ask

- What does the system need to know to perform this task?
- Which sources are authoritative, current, and relevant?
- What constraints or uncertainties could change the answer?
- Is any included information sensitive or unnecessary?
- How will the output be checked against its sources and intended use?

## Related topics

Context is a core part of [repository-aware development](repository-aware-development.md) and [human-AI systems](human-ai-systems.md).

Where this is practised: see the [evidence page](evidence.md).
