# Edge AI trust model: a first design note

*Draft, 22 November 2026. Nothing here is built as one system. This note reads what the repositories already enforce, layer by layer, against the [research direction](../index.md#research-direction) of edge AI, and lists what is missing.*

## What this note is

An edge device reasons and acts on its own hardware, often offline, within tight budgets, and sometimes alongside other devices. A trust model for such a device has to answer five questions: what evidence may come in, how a belief changes, what may be written to memory, how the views of several agents are combined, and what may leave the device.

Several repositories by the same author already answer one of those questions each, with a test behind the answer. None was written for the edge, and none knows about the others. This note puts them in one order so that the gaps between them are visible.

Every statement below carries one of three labels, following the distinction [AGENTS.md](../../AGENTS.md) asks for:

- **Enforced:** in code today, with a named test that fails if it is broken. The test is the citation.
- **Proposed:** written down in a decision record that has not been accepted. Nothing is built.
- **Guess:** this note's own reading. It is interpretation, not a finding, and the author has not ruled on it.

## The layers at a glance

| Layer | Question | Where it is answered today | Status |
| --- | --- | --- | --- |
| 1. Evidence admission | What may count as evidence? | [swarm](https://github.com/dermot-r-cochran/swarm) (EPISTEME), `EpistemicCore` | Enforced, single store |
| 2. Belief update | How far may one record move a belief? | swarm ADR-0005; [careful-memory](https://github.com/dermot-r-cochran/careful-memory) ADR-0001 | Enforced, single store |
| 3. Memory write gate | Who may write, and what is refused? | careful-memory, three-stage pipeline | Enforced, except the distributed parts |
| 4. Aggregation across agents | How are several agents' views combined? | [Voting](https://github.com/dermot-r-cochran/Voting); [foundation-model](https://github.com/dermot-r-cochran/foundation-model) | Enforced, but the two answer different questions |
| 5. Egress | What may leave the device? | a private engineering agent; [hybrid-agent](https://github.com/dermot-r-cochran/hybrid-agent) | Enforced for one machine |
| Across all five | Who is the peer, and why trust it? | swarm ADR-0006 and ADR-0007 | Proposed |

## Layer 1: evidence admission

**Enforced.** In swarm, evidence is validated before it can touch a belief. `EpistemicCore.evaluate_update` refuses an update when the evidence has been seen before, when its reliability is below a threshold (0.5 by default), or when the grounds are language, repetition, consensus or appeal to authority alone. The core is pure: it returns a decision and writes nothing.

- Threshold and duplicates: `tests/test_core.py::TestUpdateEligibility::test_ineligible_low_reliability`, `::test_ineligible_duplicate_evidence`, `::test_threshold_boundary_exactly_equal`.
- Language and social proof are not evidence: `tests/test_core.py::TestUpdateEligibility::test_language_only_update_rejected`, `::test_authority_appeal_rejected`.
- Repetition cannot drift a belief: `tests/test_experience.py::TestLongHorizonStability::test_adversarial_repetition_does_not_drift_belief` and the property `tests/test_properties.py::test_repetition_never_compounds_through_the_loop`.
- The core writes nothing (ADR-0001): `tests/test_core.py::TestSideEffectFree::test_core_does_not_import_storage`.

careful-memory has a second admission check in front of its store: the MetaGate refuses a proposal that names no evidence type, and there is no evidence type for a model's own inference, so model output can never reinforce a belief (its ADR-0006). Tests: `tests/test_meta_gate.py::TestMetaGateLevels::test_no_evidence_type_is_low`, `tests/test_poisoning_and_isolation.py::TestSelfReinforcement::test_no_llm_inference_evidence_type`.

**The edge gap (fact, from swarm ADR-0007's own context).** swarm's `Evidence` records no source: nothing says which device, sensor or person an observation came from, and the reliability is whatever the caller supplies. On one machine that is the caller's responsibility. Across devices it means a device can state its own reliability.

## Layer 2: belief update

**Enforced.** In both stores, confidence is derived from counts and never written directly.

- swarm (ADR-0005): confidence is the mean of a Beta posterior; supporting evidence adds its reliability to α, counter-evidence to β, and one record's weight is reduced so the mean never moves by more than `max_confidence_delta`. Tests: `tests/test_core.py::TestBetaPosterior::test_one_record_never_moves_confidence_beyond_the_cap`, `::test_cap_reduces_the_weight_rather_than_the_mean_alone`, the property `tests/test_properties.py::test_one_record_never_moves_confidence_beyond_the_cap`, and the two guards that confidence has no write path of its own, `tests/test_models.py::TestBetaConfidence::test_confidence_cannot_be_asserted_apart_from_counts` and `tests/test_memory.py::TestBetaCounts::test_confidence_has_no_write_path_of_its_own`.
- careful-memory (ADR-0001, ADR-0005): confidence is α/(α+β), and decay shrinks both counts toward the Beta(1,1) prior, never below it. Its property tests are in `tests/test_bayesian_properties.py`.
- Both keep an append-only record: swarm ADR-0002, guarded by `tests/test_memory.py::TestOnDisk::test_second_connection_cannot_alter_or_remove_the_trail`; careful-memory ADR-0007.

**Known limit (fact, stated in swarm ADR-0005).** Two records with a shared unseen cause count as two. On one machine that is rare. In a group of devices with the same sensor model or the same on-device model, it is the normal case.

## Layer 3: the memory write gate

**Enforced.** careful-memory lets an agent reach storage only through three tools, and routes every write through three gates, where a refusal at any gate stops the request:

1. **MetaGate:** refuses a proposal with no documented evidence type (`tests/test_meta_gate.py::TestMetaGateLevels::test_no_evidence_type_is_low`), and never changes a belief while it assesses (`tests/test_meta_gate.py::TestMetaGateNoBeliefMutation::test_alpha_unchanged_after_assess`).
2. **WriteGate:** context isolation, authority ordering (`user < system < verified_system`), rate limits and outlier rejection. Tests: `tests/test_poisoning_and_isolation.py::TestCrossContextIsolation::test_write_gate_blocks_wrong_context`, `::TestAuthorityEnforcement::test_lower_authority_cannot_update_higher`, `::TestRateLimit::test_flood_rejected`, and `tests/test_gate.py::TestEvidenceUpdate::test_outlier_swing_rejected`.
3. **MemoryReviewer:** refuses mass contradiction, defers near-duplicates, and downgrades or refuses a direct high-confidence assertion. Tests: `tests/test_poisoning_and_isolation.py::TestMassContradiction::test_mass_contradiction_rejected_by_reviewer`, `::TestNearDuplicate::test_duplicate_deferred`, `::TestDirectSemanticAssertion::test_very_high_confidence_semantic_rejected`.

The three-tool surface itself is pinned by `tests/test_tools.py::TestThreeToolSurface::test_exactly_three_tools`.

**Accepted but not built (fact, from careful-memory's ADR index).** Distributed rate limiting backed by Redis (ADR-0013, risk R-01), ownership validation at the API boundary (ADR-0014, R-02) and optimistic locking (ADR-0015, R-03). The rate limiter that runs is the in-process one of ADR-0008.

**Guess.** On a single offline device, the in-process limiter may be the right one, not a stopgap: Redis is a server, and an edge device may have no server to reach. Redis matters again only once several devices write to one shared store. Whether ADR-0013 should be read that way is the author's call.

## Layer 4: aggregation across agents

Two repositories combine several contributors' views. They answer different questions, and they do not agree on where weight comes from.

**Voting: exact and deterministic. Enforced.** Voting allocates a fixed number of discrete slots among candidates from voters' graded preferences, with exact rational arithmetic, conservation asserted at every phase, and ties broken by candidate id. Every voter's normalised weight is one; no voter reports their own weight.

- Same input, same output: `tests/properties.rs`, properties `allocation_is_deterministic`, `voter_order_never_influences_the_result` and `candidate_order_never_influences_the_result`.
- Conservation: `allocation_conserves_slots_and_covers_every_candidate` and `normalized_weights_sum_to_exactly_one` in the same file.
- Behaviour pinned against 300 golden scenarios: `tests/parity.rs`, `matches_the_python_engine_case_for_case`.

**foundation-model: weighted by self-reported loss. Enforced as written.** `ExpertiseWeightedAggregator` merges model updates with weight `reputation / validation_loss`. Fact, from `foundation_model/voting.py` and `foundation_model/p2p.py`: the validation loss arrives with each contributor's update and the aggregator does not check it, the peer-to-peer path uses a node's own training loss as the proxy, and reputation rises when an update agrees with the round's consensus (cosine similarity). Optional tail-trimming drops the highest and lowest weights. Tests: `tests/test_voting.py::test_lower_loss_gives_higher_weight`, `::test_expert_outvotes_majority`, `::test_trim_excludes_inflated_reputation_and_worst_loss`, `::test_aggregate_penalises_the_misaligned_contributor_through_cosine`.

**Guess: the two cannot simply be swapped.** Voting suits a discrete decision among options (which task, which reading, which candidate), where exactness and a loud stop matter more than speed. foundation-model's aggregator suits averaging model parameters. At the edge, the weakness is in where foundation-model's weight comes from, not in the averaging: a device that under-reports its loss gains weight, and reputation earned by agreeing with the consensus is the trust-from-agreement that swarm ADR-0006 and ADR-0007 refuse. One way to reconcile them, offered for the author to accept or reject: keep the averaging, and replace both weight inputs with the per-device trust that ADR-0007 proposes, which rises only on independently checked outcomes.

## Layer 5: egress, what may leave the device

**Enforced, on one machine.**

- **A private engineering agent** by the same author (described, not named, as [the evidence page](../evidence.md) asks) sends every network request it makes itself through a single function that permits HTTPS to an allowlist of hosts and nothing else. Every remote write (a push, an issue, a pull request) asks a person each time and is appended to a local actions ledger. Its tests check the host rule over an enumerated space of look-alike hosts, check that no remote-write command shape can ever be trusted for a whole session, and check the ledger's format. Commands the agent runs open their own connections and rely on the person's confirmation, not on the allowlist; its own record says so.
- **hybrid-agent** executes nothing. The fields that say whether an action ran and whether it needs human approval are set by code, never by the model, and every report ends awaiting human review. Tests: `tests/test_agent.py::test_parse_hypotheses_accepts_fences_and_fixes_authority_fields`, `::test_verify_report_flags_actions_bypassing_approval`, `::test_missing_model_is_reported_not_substituted`.

**Guess.** For an edge device the same two rules carry over directly: one door for traffic the agent originates, with an allowlist, and a local ledger of everything that left. What does not carry over is the person at the confirmation prompt. A robot or a sensor node often runs unattended, so "ask every time" would become "refuse unless pre-approved, and record". That is a design choice for the author, not a finding.

## Across the layers: peers, identity and trust

**Proposed, not built.** swarm ADR-0006 (11 November 2026) places any peer network in swarm, with hybrid-agents as its nodes, and rules that agreement between peers is not evidence. ADR-0007 (22 November 2026) proposes how trust in an edge node is set and revised:

- each node signs its reports with a key created on the device and enrolled by a person; an unsigned or unenrolled report is refused, and identity is not trust;
- trust is held per node and per kind of observation, starts below the admission threshold, and rises only on checked outcomes from outside the swarm, never on agreement, volume, time online or the node's own claims;
- nodes a person declares correlated count once per belief per window;
- late reports are ordered by receipt and keep the node's own timestamp as a stated value;
- revocation refuses later reports and lists affected beliefs for review without recomputing them.

Both records are Proposed, and ADR-0007 lapses if ADR-0006 is not accepted. Neither has a guard test yet; each gets one on acceptance.

## Gaps

| Gap | What exists | What is missing |
| --- | --- | --- |
| Peer trust | swarm ADR-0006 and ADR-0007, Proposed | Acceptance, a source field on `Evidence` (a breaking change, per ADR-0007), the trust and enrolment tables, and the guard tests ADR-0007 lists. foundation-model's agreement-based reputation contradicts it today. |
| Device identity | ADR-0007 section 1, Proposed | Any code. ADR-0007 deliberately names no signature scheme or key store. Where the key lives on a device that can be taken apart is open. |
| Offline sync | ADR-0007 section 6 (late reports), Proposed; careful-memory ADR-0015 (optimistic locking), accepted, not built | How two stores that diverged while offline are merged. Append-only records help, since nothing is overwritten, but no repository says what happens when two devices revised the same belief apart. |
| Rate limiting across devices | careful-memory ADR-0013 (Redis), accepted, not built | The distributed limiter, and a ruling on whether a single offline device needs it at all (see the guess under layer 3). |
| Shared causes | Stated as a limit in swarm ADR-0005; declared groups in ADR-0007 | Undeclared correlation still counts twice. No repository claims to detect it. |
| Budget | Nothing | No figure for memory, latency or power for any of the checks above. ADR-0007 calls its own budget claim THEORY until measured. |
| One composed system | Nothing | No repository runs all five layers together. Each test above proves its layer in isolation. |

## Open questions for the author

1. Should foundation-model's aggregation weight move off self-reported loss and agreement-based reputation, towards ADR-0007's checked-outcome trust, or should it stay a model-training tool outside the trust model?
2. On an unattended device, is egress "refuse unless pre-approved, and record"?
3. Does a single offline device need ADR-0013's distributed limiter, or only a fleet sharing one store?
4. Where should this note live once it settles: here as a note, as a proposed ADR in swarm beside ADR-0006 and ADR-0007, or both?
