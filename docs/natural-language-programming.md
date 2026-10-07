# Natural language programming

Natural language programming uses ordinary language to express computational intent, often with an AI system translating that intent into code, queries, or actions. It can make technical work more accessible and speed up exploration, but natural language is often ambiguous and generated implementations require verification.

## Translate intent into checkable behavior

Describe the goal, relevant context, constraints, and expected behavior. Use examples and edge cases to make assumptions visible. For consequential changes, turn the request into explicit requirements or tests, inspect the generated implementation, and validate it in the target environment.

The person using the system remains responsible for judging whether the result is appropriate. A program that matches a prompt superficially may still violate repository conventions, miss an edge case, or solve the wrong problem.

## Questions to ask

- Is the requested outcome precise enough to verify?
- What assumptions and edge cases need to be made explicit?
- Does the implementation follow the intended constraints?
- What tests or independent evidence support the result?
- Who is accountable for the code and its effects?

## Related topics

See [repository-aware development](repository-aware-development.md) for grounding changes in a codebase and [AI evaluation](ai-evaluation.md) for verifying system behavior.

Where this is practised: see the [evidence page](evidence.md).
