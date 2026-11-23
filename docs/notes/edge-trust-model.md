# Edge AI trust model: a first design note

*Draft, 22 November 2026; open questions generalised into principles and parameters, 23 November 2026. Nothing here is built as one system. This note reads what the repositories already enforce, layer by layer, against the [research direction](../index.md#research-direction) of edge AI, and lists what is missing.*

## What this note is

An edge device reasons and acts on its own hardware, often offline, within tight budgets, and sometimes alongside other devices. A trust model for such a device has to answer five questions: what evidence may come in, how a belief changes, what may be written to memory, how the views of several agents are combined, and what may leave the device.

Several repositories by the same author already answer one of those questions each, with a test behind the answer. None was written for the edge, and none knows about the others. This note puts them in one order so that the gaps between them are visible.

Every statement below carries one of three labels, following the distinction [AGENTS.md](../../AGENTS.md) asks for:

- **Enforced:** in code today, with a named test that fails if it is broken. The test is the citation.
- **Proposed:** written down in a decision record that has not been accepted. Nothing is built.
- **Design:** this note's own proposal: a principle that holds whatever a deployment chooses, and the parameter or interface where the choice is made. It is interpretation, not a finding, and no repository enforces it yet.

Where a choice depends on the deployment (one device or a fleet, attended or unattended, model training or discrete decisions), the note does not pick an answer. It states the principle the answer must keep, names the choice as a parameter, and gives a default that is safe when nothing else is known. The [parameters](#parameters) are collected at the end.

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

**Design: the rate limiter sits where writes converge.** The principle is that every path into a store passes one limit, so a limit no writer can split. Where that limit runs is a parameter, `rate_limit_scope`, behind one limiter interface: `device` (an in-process window, as ADR-0008 runs today) when one device owns its store, `shared` (a distributed limiter, such as ADR-0013's Redis) when several devices write to one store. Default: `device`, because a device that may be offline cannot depend on a server for its own safety checks. ADR-0013 becomes one implementation of `shared` rather than a requirement on every device.

## Layer 4: aggregation across agents

Two repositories combine several contributors' views. They answer different questions, and they do not agree on where weight comes from.

**Voting: exact and deterministic. Enforced.** Voting allocates a fixed number of discrete slots among candidates from voters' graded preferences, with exact rational arithmetic, conservation asserted at every phase, and ties broken by candidate id. Every voter's normalised weight is one; no voter reports their own weight.

- Same input, same output: `tests/properties.rs`, properties `allocation_is_deterministic`, `voter_order_never_influences_the_result` and `candidate_order_never_influences_the_result`.
- Conservation: `allocation_conserves_slots_and_covers_every_candidate` and `normalized_weights_sum_to_exactly_one` in the same file.
- Behaviour pinned against 300 golden scenarios: `tests/parity.rs`, `matches_the_python_engine_case_for_case`.

**foundation-model: weighted by self-reported loss. Enforced as written.** `ExpertiseWeightedAggregator` merges model updates with weight `reputation / validation_loss`. Fact, from `foundation_model/voting.py` and `foundation_model/p2p.py`: the validation loss arrives with each contributor's update and the aggregator does not check it, the peer-to-peer path uses a node's own training loss as the proxy, and reputation rises when an update agrees with the round's consensus (cosine similarity). Optional tail-trimming drops the highest and lowest weights. Tests: `tests/test_voting.py::test_lower_loss_gives_higher_weight`, `::test_expert_outvotes_majority`, `::test_trim_excludes_inflated_reputation_and_worst_loss`, `::test_aggregate_penalises_the_misaligned_contributor_through_cosine`.

**Design: weight comes from the trust layer, never from the contributor.** The principle: a contributor's weight in any aggregation is supplied by the trust layer (below), and is never stated by the contributor about itself, nor raised by agreeing with the others. The aggregation method is a separate, pluggable choice behind one interface that takes contributions and trust-supplied weights:

- `exact_allocation` for discrete decisions among options (which task, which reading, which candidate), where exactness and a loud stop matter more than speed. Voting is the reference.
- `weighted_average` for continuous values such as model parameters. foundation-model's averaging is the reference.

Either method can run with any trust source, so the method is chosen by the shape of the decision and the weight by the trust layer. Fact: foundation-model as written does not meet the principle, because its weight inputs are self-reported loss and agreement-based reputation. Feeding it trust-supplied weights keeps its averaging and changes only where the weights come from.

## Layer 5: egress, what may leave the device

**Enforced, on one machine.**

- **A private engineering agent** by the same author (described, not named, as [the evidence page](../evidence.md) asks) sends every network request it makes itself through a single function that permits HTTPS to an allowlist of hosts and nothing else. Every remote write (a push, an issue, a pull request) asks a person each time and is appended to a local actions ledger. Its tests check the host rule over an enumerated space of look-alike hosts, check that no remote-write command shape can ever be trusted for a whole session, and check the ledger's format. Commands the agent runs open their own connections and rely on the person's confirmation, not on the allowlist; its own record says so.
- **hybrid-agent** executes nothing. The fields that say whether an action ran and whether it needs human approval are set by code, never by the model, and every report ends awaiting human review. Tests: `tests/test_agent.py::test_parse_hypotheses_accepts_fences_and_fixes_authority_fields`, `::test_verify_report_flags_actions_bypassing_approval`, `::test_missing_model_is_reported_not_substituted`.

**Design: one door, refuse by default, record everything.** These hold in every deployment: all traffic the agent originates passes one door; the door allows only listed destinations; everything that leaves is appended to a local ledger; and anything not explicitly allowed is refused. What varies is who approves a remote write, a parameter `egress_approval`:

- `each_time`: a person confirms each one, as the private agent does today. Suits an attended device.
- `pre_approved`: a person approves a list of action shapes in advance; anything outside the list is refused and recorded, never queued for an absent person. Suits an unattended robot or sensor node.

Default: `each_time` where a person is present, and otherwise `pre_approved` with an empty list, which sends nothing until someone approves something.

## Across the layers: peers, identity and trust

**Proposed, not built.** swarm ADR-0006 (11 November 2026) places any peer network in swarm, with hybrid-agents as its nodes, and rules that agreement between peers is not evidence. ADR-0007 (22 November 2026) proposes how trust in an edge node is set and revised:

- each node signs its reports with a key created on the device and enrolled by a person; an unsigned or unenrolled report is refused, and identity is not trust;
- trust is held per node and per kind of observation, starts below the admission threshold, and rises only on checked outcomes from outside the swarm, never on agreement, volume, time online or the node's own claims;
- nodes a person declares correlated count once per belief per window;
- late reports are ordered by receipt and keep the node's own timestamp as a stated value;
- revocation refuses later reports and lists affected beliefs for review without recomputing them.

Both records are Proposed, and ADR-0007 lapses if ADR-0006 is not accepted. Neither has a guard test yet; each gets one on acceptance.

**Design: trust rests on behaviour over time and consistency with other data sources.** Two weak links are designed out, and one basis is put in their place (the author, 23 November 2026):

- **Key management is a weak link.** A key can be copied from a device that is taken apart, lost with it, or never rotated, and a scheme whose trust depends on keys staying secret fails quietly when one does not.
- **Peer trust is not reliable either.** A peer's vouching for another peer, a shared reputation score and a peer's record of its own accuracy are all things the receiving node has not seen. Trust passed from node to node spreads one mistake or one compromised node across the network.
- **What trust rests on instead:** a source's behaviour over time, and the consistency of what it reports with other data sources.

So each node holds its own trust in each source (a peer, or one of its own sensors), built from two kinds of evidence it can assess itself:

1. **Consistency with other data sources.** A report is compared with independent sources bearing on the same thing: the node's own sensors, a reference instrument, a later ground truth, or another source in a different correlation group. Consistency adds to α and inconsistency to β, by the ADR-0005 arithmetic. Sources in the same correlation group are not independent of each other, so they cannot confirm each other. This is how the rule "agreement between peers is not evidence" is kept: agreement counts only across sources that do not share a cause, and peers merely repeating one another never do.
2. **Behaviour over time.** A source's record is kept as a time series, not only as a total. A long consistent record earns more than a short one, but it is never a licence. A change in behaviour, such as a source that was consistent and stops being, or one whose reports suddenly shift in rate, range or pattern, is itself evidence. A shift triggers a review of that source and lowers the weight of its newer reports until they are consistent again. This guards against a node that behaves well to build a record and then switches.

Nothing else raises trust. Not a signature, which at most helps say which source a report claims to come from. Not another peer's trust or endorsement, so trust never passes from one node to another. Not volume, time online without checks, or the source's own claims. Consequences:

- **A new source starts with no trust.** Its reports are recorded as claims, which are proposals and never beliefs, until enough of them have been compared with other sources. A report that no other source can ever bear on earns no weight.
- **A copied key or a compromised peer gains little.** Whoever holds it can send reports only at the trust this node has already built for that source. Each report is still capped by `max_confidence_delta` and deduplicated within its correlation group, and a change in behaviour lowers the weight of new reports.
- **Attribution is pluggable.** How a report is tied to a source is a parameter, `attribution`: a signature, the physical channel it arrived on, or a combination. No choice changes the weight.
- **No global score.** Two nodes may hold different trust in the same source, because each compared it against different data. That is intended: there is no shared trust table to poison.

This differs from ADR-0007 as proposed in three places: section 1 makes a signature from an enrolled key a condition of admission, section 3 has a person set each pair's starting trust, and section 4 counts checks made outside the swarm (a person's inspection, a reference instrument) as checks of a node, where this note treats them as data sources a report is compared against. All three fit only if signatures are read as attribution, a person's setting can lower trust but never raise it above what consistency and behaviour support, and an outside check counts as one more data source the node compares reports against. Whether to amend ADR-0007 is a matter for swarm, not this note.

## Gaps

| Gap | What exists | What is missing |
| --- | --- | --- |
| Peer trust | swarm ADR-0006 and ADR-0007, Proposed | Acceptance, a source field on `Evidence` (a breaking change, per ADR-0007), a per-node trust table built from behaviour over time and consistency with other data sources (see *Across the layers*), and guard tests. foundation-model's agreement-based reputation contradicts it today. |
| Device identity | ADR-0007 section 1, Proposed | Any code, and an `attribution` method whose failure costs no more than the trust a node has already built for that source (see *Across the layers*). |
| Offline sync | ADR-0007 section 6 (late reports), Proposed; careful-memory ADR-0015 (optimistic locking), accepted, not built | How two stores that diverged while offline are merged. Append-only records help, since nothing is overwritten, but no repository says what happens when two devices revised the same belief apart. |
| Rate limiting across devices | careful-memory ADR-0013 (Redis), accepted, not built | The distributed limiter, needed only where `rate_limit_scope` is `shared` (see layer 3). |
| Shared causes | Stated as a limit in swarm ADR-0005; declared groups in ADR-0007 | Undeclared correlation still counts twice. No repository claims to detect it. |
| Budget | Nothing | No figure for memory, latency or power for any of the checks above. ADR-0007 calls its own budget claim THEORY until measured. |
| One composed system | Nothing | No repository runs all five layers together. Each test above proves its layer in isolation. |

## Principles

These are the design's fixed points, ten of them. A deployment may tune every parameter below, but no setting may break one of these.

1. **Evidence is admitted on its grounds, never on agreement, repetition, volume or fluency.** (Enforced in swarm for one store; proposed for peers in ADR-0006 and ADR-0007.)
2. **Confidence and trust are derived from counts, never written.** (Enforced in swarm and careful-memory for beliefs; proposed for node trust in ADR-0007.)
3. **Every record is appended, nothing is overwritten.** (Enforced in both stores.)
4. **Weight comes from the trust layer, never from the contributor.** (Design.)
5. **Every write path into a store passes one limit.** (Enforced for one process in careful-memory; design across devices.)
6. **Nothing leaves except through one door, by default it is refused, and what leaves is recorded.** (Enforced on one machine; design for the edge.)
7. **A check that guards the device runs on the device.** It needs no network to say no. (Design, following ADR-0007 section 8.)
8. **Trust never rests on a cryptographic signature or a secret key.** A signature may help attribute a report; it never adds weight, and the design holds when a key is copied. (Design; the author, 23 November 2026.)
9. **Trust never passes from peer to peer.** No endorsement, shared score or self-report raises it. (Design; the author, 23 November 2026.)
10. **Trust rests on behaviour over time and consistency with other data sources.** It is built per node and per source. Agreement counts only across sources that share no cause, and a change in behaviour is itself evidence. (Design; the author, 23 November 2026.)

## Parameters

Each choice the first draft left as an open question is now a parameter. The default is the safe setting when nothing else is known.

| Parameter | Layer | Values | Default | Principle kept |
| --- | --- | --- | --- | --- |
| `rate_limit_scope` | 3 | `device`, `shared` | `device` | 5, 7 |
| `aggregation_method` | 4 | `exact_allocation`, `weighted_average` | by the shape of the decision | 4 |
| `weight_source` | 4 | the trust layer only | the trust layer | 1, 4 |
| `egress_approval` | 5 | `each_time`, `pre_approved` | `each_time` if attended, else `pre_approved` with an empty list | 6 |
| `starting_trust` | across | zero, or a figure below the admission threshold | zero: nothing a source sends moves a belief until enough of it has been compared with other sources | 1, 10 |
| `behaviour_window` | across | a duration or a count of reports | left open; a deployment sets it to the pace its sources change at | 10 |
| `behaviour_shift_test` | across | a pluggable test of rate, range or pattern against the source's own history | flag and review; never silently lower stored beliefs | 3, 10 |
| `trust_decay_without_checks` | across | none, or towards the starting figure | none | 2 |
| `correlation_window` | across | a duration | left to ADR-0007's acceptance | 1 |
| `attribution` | across | signature, physical channel, or a combination | whatever the deployment has; it never changes the weight | 8, 9 |

`starting_trust`, `trust_decay_without_checks` and `correlation_window` are the items ADR-0007 itself leaves open; they are listed so that one table holds every choice. Where this note's design should eventually be recorded as a decision, and in which repository, is a separate question: the note binds nothing, and an ADR binds only in its own repository.
