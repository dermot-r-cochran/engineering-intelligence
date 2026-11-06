# Human-AI systems

A human-AI system includes people, AI capabilities, tools, workflows, and the environment in which decisions are made. Its behavior is shaped not only by a model, but also by task design, context, interfaces, incentives, and the way people review and use its outputs.

## Design for collaboration

Begin with the human need and the consequences of error. Assign tasks to AI where it can provide useful assistance, and make human responsibilities explicit. People should have enough information and authority to question, correct, or decline an AI recommendation. Review should be meaningful rather than a ceremonial approval step.

AI outputs can be fluent without being accurate, complete, or appropriate. Systems should communicate uncertainty and limitations where possible, keep consequential decisions accountable, and provide routes for correction and escalation.

## Case note: the decision the model cannot make

The section above asks that human responsibilities be explicit, that people have the information to question an AI recommendation and the authority to decline it, and that review be meaningful rather than ceremonial. [hybrid-agent](https://github.com/dermot-r-cochran/hybrid-agent), one of the three repositories the [evidence page](evidence.md) lists for this topic, was created on 28 October 2026 from a prompt its author wrote and a coding agent carried out, and its design record (`docs/decisions.md`) quotes that prompt as fifteen founding rulings and holds everything since against them.

**What was tried.** The decision is kept out of the model by construction, not by instruction. Every report ends in the status `awaiting_human_review`, a default on the `Report` type that nothing in the package sets otherwise; every proposed action carries `requires_human_approval` and `executed`, which the parser never reads from the model's output, so a model that writes "executed: true" is not obeyed, and a report that reaches a human with either field wrong fails verification. What the human is given to question with is kept in five separate fields, observations, derived results, hypotheses, unknowns and proposed actions, so a reader can tell a figure the tools read from one the model proposed; every hypothesis must cite evidence that exists, every figure with a unit must match a computed result, and every file named must be in the deployed change. Where the system cannot answer, it says so as an unknown: a request the rules cannot parse, a model not assigned to an operation, malformed output, a provider error, an unreadable evidence file. Since 5 November the trace ends by counting the steps that took no model, "7 of 8" in the worked example, so a reader knows how much of a report came from arithmetic and how much from a proposal.

**What the record says happened.** Each of those has a test the README names, under the README-proof convention of the [engineering intelligence](engineering-intelligence.md#case-note-a-readme-that-names-its-proof) page: the end-to-end run (`tests/test_agent.py::test_regression_investigation_end_to_end`, one sound hypothesis passing and one deliberately flawed one failing on an invented citation, an invented number and a file not in the change), the authority fields (`::test_parse_hypotheses_accepts_fences_and_fixes_authority_fields`, `::test_verify_report_flags_actions_bypassing_approval`), the unknowns (`::test_missing_model_is_reported_not_substituted`, `::test_malformed_or_failing_llm_output_is_not_trusted`, `::test_unreadable_evidence_becomes_an_unknown`) and the count (`::test_report_counts_the_steps_that_took_no_model`). The approval test was strengthened on 5 November, after a deletion test found that two of the three report-level checks in `verify.py`, the approval check among them, could be cut back without any test failing (pull request #28): a check nothing fails when it is wrong is the ceremonial review the section above warns against. The human side of the system is in the record too. The author's rulings of 3 November on cost limits and team metrics were design without code, and on 5 November a set of design challenges written against sample code found three promises the rulings did not keep: a cap a single response could pass, a privacy rule that compared only the last published roster, and a folded squad that could be subtracted back out of its team's total. Each was closed the same day by a ruling the author accepted, in wording the record marks as the recommendation's and not his, with the challenge held as an expected failure until the sample met it. Then the author deferred team metrics altogether, with his reason quoted in the record, "Metrics are a secondary requirement if there is another way to show business value for concerned managers", and the rulings kept on file rather than struck. Two limits the record states. No real model is called; the evidence and the model's answers are mocks, so the repository shows how the system behaves, not how well a model performs. And the verifier's checks establish that a hypothesis is consistent with the evidence, which the README says plainly is not the same as true.

**What changed as a result.** The human decision is the one point in the repository with no code path round it, and the record now says where every other judgement sits: in a ruling, dated, in "do not re-propose" form, or in a challenge that fails until a ruling meets it. What the record does not yet show is a person reading a real report. Every run so far is against the mock evidence, so the section's question of whether the workflow encourages appropriate trust is answered only for the line that counts the steps without a model, not for a reader who had to act on one. Whether the first real investigation is written up as a case, or the count of steps is enough until a provider is wired in, is a decision for that repository, and its record would belong here.

## Questions to ask

- Who benefits from the system, and who bears its risks?
- Which tasks are assisted, which decisions remain human-owned, and why?
- Can users inspect the evidence and context behind consequential outputs?
- How are errors detected, corrected, and learned from?
- Do the workflow and interface encourage appropriate trust rather than blind reliance?

## Related topics

See [context engineering](context-engineering.md) for supplying useful context and [AI evaluation](ai-evaluation.md) for assessing system behavior.

Where this is practised: see the [evidence page](evidence.md).
