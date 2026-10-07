# AI evaluation

AI evaluation is the systematic assessment of a model or AI-enabled system against intended tasks, operating conditions, and potential harms. A useful evaluation makes the claim being tested explicit and gathers evidence relevant to real use; a single score rarely captures the full behavior of a system.

## Evaluate the system in context

Define the users, tasks, success criteria, and unacceptable outcomes before testing. Use representative cases, including difficult and failure-prone examples. Assess the complete workflow where possible: model behavior, supplied context, tools, user interaction, and review all affect outcomes.

Combine quantitative measures with qualitative inspection when appropriate. Document the evaluation setup and limitations so results can be interpreted and repeated. Re-evaluate after material changes to models, prompts, data, tools, or deployment conditions, and monitor for changes in actual use.

## Questions to ask

- What specific capability or risk does this evaluation address?
- Are cases representative of the intended users and conditions?
- What errors matter most, and how are their impacts weighted?
- What does the evaluation not establish?
- What evidence would lead us to change, limit, or stop deployment?

## Related topics

Evaluation is part of a broader [human-AI system](human-ai-systems.md) and depends on well-selected [context](context-engineering.md).
