# Feature Specification: Max Headroom Investigation Dossier

**Feature Branch**: None; no branch-creation hook is configured.

**Feature Directory**: specs/001-investigation-dossier

**Created**: 2026-11-06

**Status**: Draft

**Input**: User description: "please use INVESTIGATION_PLAN.md to create the specification."

**Foundation**: [Investigation plan](../../INVESTIGATION_PLAN.md) and
[constitution v1.0.0](../../.specify/memory/constitution.md).

The investigation covers the 1987-11-22 Chicago intrusions affecting WGN-TV's evening news
and WTTW's Doctor Who broadcast: their sequence, signal paths, video production, local media
references, and investigation history. The starting record is preliminary source discovery;
no broadcast recording was acquired or analyzed and no new technical finding or identification
was established in that planning phase.

## Clarifications

### Session 2026-11-06

- Q: What must be completed before you consider the first delivery of this investigation project ready? → A: The dossier, a real-source baseline, and one completed analytical cycle with a documented test and review.

- Q: When should the research assistant pause for your next direction during the agreed first delivery? → A: Continue through the first delivery; pause only for essential missing input, user-only actions, or a blocker that prevents further useful work.

- Q: Who should the first findings reports be written for? → A: You and selected reviewers, with enough context for them to audit the findings.

- Q: When must backups of acquired original files and research notes be confirmed? → A: Back up acquired original files before analysis; back up notes and registers before ending each research session.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Establish a trustworthy evidence dossier (Priority: P1)

As the researcher, I want one inspectable collection of sources, claims, events, hypotheses,
tasks, and searches so I can distinguish what is known from what is merely repeated or proposed.

**Why this priority**: Every subsequent finding depends on preserved evidence, honest source
status, and a shared record of uncertainty.

**Independent Test**: Register the seven starter references, a representative acquired file,
two dependent accounts, and an inaccessible source. A reviewer can inspect their provenance and
limits without needing a chronology, analysis tool, or dashboard.

**Acceptance Scenarios**:

1. **Given** only the investigation plan, **When** the dossier foundation is established,
   **Then** its entry point, research methods, decision history, status, and six registers are
   available with their required information; S01-S07, H1-H7, and T01-T11 retain mappings to
   their new stable identifiers and their stated verification, hypothesis, or task status.
2. **Given** an acquired recording, **When** it is registered, **Then** the unchanged original,
   acquisition date, integrity checksum, source relationship, restrictions, and separate
   original-media and digitization histories are inspectable, with unknowns explicitly marked;
   the acquired original has a confirmed backup before analysis starts.
3. **Given** several reports repeat one interview or several clips descend from one capture,
   **When** their claims are assessed, **Then** the common lineage is visible and the copies
   are not counted as independent confirmations.
4. **Given** a source cannot be retrieved or a search finds nothing, **When** the search is
   recorded, **Then** its query, coverage, barriers, and unsuccessful result remain visible
   without a claim that the underlying record never existed.
5. **Given** a reported statement and an untested interpretation, **When** their claims are
   recorded, **Then** each retains its evidence category, supporting and contradicting locations,
   confidence label and reasons, and unresolved caveats without upgrading interpretation to fact.
6. **Given** large media and a proposed additional analysis tool or interface, **When** storage
   and access are reviewed, **Then** the media has a documented backed-up location and access
   limits, all project views use one evidence collection, and tool adoption meets the stated
   repeatable-question or stabilized-model/navigation conditions.

---

### User Story 2 - Establish a baseline without false precision (Priority: P1)

As the researcher, I want a source-linked chronology, recording inventory, and historical
signal-path account so I can see where reports agree, conflict, or leave important gaps.

**Why this priority**: Mechanism testing requires a baseline that respects event boundaries,
reception paths, and the stations' documented 1987 configuration.

**Independent Test**: Use accounts with conflicting interruption durations, a recording of
uncertain capture lineage, and a partially documented historical signal path. The resulting
baseline exposes disagreements and unknowns without needing a completed analytical cycle.

**Acceptance Scenarios**:

1. **Given** accounts report different durations, **When** timeline entries are assembled,
   **Then** each retains its source, clock, Chicago local time and UTC offset, precision, and
   measurement boundaries; total disruption, black/static intervals, visible intrusion, and
   restoration are distinguishable wherever supported.
2. **Given** evidence from different stations or reception paths, **When** the baseline is
   reviewed, **Then** known over-the-air, studio-monitor, cable, and satellite paths remain
   distinguishable; unsupported equivalence and unsupported exact times remain unresolved.
3. **Given** incomplete historical records, **When** the baseline is reviewed, **Then** the
   source map, recording inventory, chronology, and dated 1987 signal-path diagram distinguish
   supported components from unknowns, and identify the evidence needed to resolve each gap.
4. **Given** the plan's S01 and S02 accounts describe roughly 30 and 25 seconds respectively
   for WGN, **When** the starting claims are registered, **Then** they retain their separate
   source locations and retrieval limits; different boundaries, rounding, and contradiction
   remain alternatives rather than an invented exact duration.

---

### User Story 3 - Test competing explanations (Priority: P1)

As the researcher, I want to choose a bounded question and test alternatives so a research
session changes what the evidence supports rather than merely accumulating material.

**Why this priority**: A distinguishing test can narrow uncertainty even when attribution
remains impossible or inaccessible records prevent a complete reconstruction.

**Independent Test**: Take one question and at least two alternatives through predictions,
evidence collection, a documented test, and a status review. This can use supplied evidence
without requiring new archive access or a full recording comparison.

**Acceptance Scenarios**:

1. **Given** an open question, **When** a cycle begins, **Then** alternatives, necessary
   conditions, distinguishing predictions, evidence needs, dependencies, and a timebox are
   recorded before searching for the cycle or conducting its test.
2. **Given** a completed test, **When** hypotheses are reviewed, **Then** supporting and
   contradicting evidence, assumptions, prior status, new status, and revision reasons remain
   inspectable; "ruled out" requires an evidenced failed necessary condition and stated scope.
3. **Given** a technical explanation, **When** feasibility is assessed, **Then** it uses
   documented historical architecture and justified parameter ranges, distinguishes entry
   points and production/playback/transmission roles, and uses records or offline modeling.
4. **Given** a blocked branch or an interesting AI connection, **When** next work is chosen,
   **Then** the branch records its stopping and reopening conditions, and the connection
   remains speculation until a testable prediction makes it a lead.
5. **Given** the seven initial hypotheses, **When** they are registered and compared,
   **Then** H1-H3 retain their entry-point questions while H4-H7 retain the partly prerecorded
   performance, shared transmitting site, insider-reference, and recording-artifact questions;
   different question scopes may coexist, and edits alone cannot establish that the entire
   performance was prerecorded.

---

### User Story 4 - Review findings and resume the investigation (Priority: P1)

As the project owner or a fresh reviewer, I want evidence-linked findings and a saved handoff
so I can audit conclusions and continue the project without reconstructing chat history.

**Why this priority**: Research progress must survive between sessions and remain reviewable
by someone who did not form the preferred explanation.

**Independent Test**: Give a reviewer a completed illustrative finding, a hypothesis revision,
and saved project state. Without conversation history, the reviewer can trace the finding,
identify unresolved limits, and recover the next actions.

**Acceptance Scenarios**:

1. **Given** a proposed finding, **When** it is reviewed, **Then** its question, claims,
   exact evidence locations, method, result, confidence with reasons, alternatives, limitations,
   and next action are available to the owner and selected reviewers, with necessary background
   and evidence-access limits explained; unsupported interpretation cannot enter shareable findings.
2. **Given** a session ends, **When** the handoff is saved, **Then** it identifies the current
   milestone and question, supported findings, disagreements, completed task results,
   hypothesis changes, external waits, deferred branches, and next three owned actions;
   backups of the session's notes and registers are confirmed before the session is marked complete.
3. **Given** a milestone review, **When** the owner evaluates progress, **Then** actual
   deliverables and named gaps determine whether to continue, narrow, wait, assign research,
   or close a branch; an unchecked backlog or planned output does not establish completion.
4. **Given** an asserted new connection and a second AI review, **When** novelty and confidence
   are assessed, **Then** prior-coverage searches support the novelty label and the additional
   AI review is recorded as reasoning review rather than independent factual corroboration.
5. **Given** an uncorroborated personal allegation, a resemblance-based identity claim, or
   instructions embedded in source material, **When** shareable findings are reviewed,
   **Then** unsupported names and allegations are withheld, private contact details stay
   outside the report, and source instructions do not authorize actions.
6. **Given** a completed cycle or milestone review and useful authorized work remaining,
   **When** the next action is chosen, **Then** the assistant records the review and continues
   without waiting for owner approval; essential missing input or user-only actions pause only
   dependent work, and overall research pauses only when no useful authorized work can continue.
7. **Given** a milestone review spans all five workstreams, **When** deliverables are checked,
   **Then** every expected output has a linked product or an explicit waiting/deferred reason;
   an inventory or planned analysis cannot stand in for a completed comparison, interpretation,
   real-source baseline, or distinguishing test.

---

### User Story 5 - Evaluate audiovisual and cultural clues (Priority: P2)

As the researcher, I want to compare surviving recordings and dated cultural references so I
can distinguish intrusion content from copying artifacts and later interpretation.

**Why this priority**: Detailed interpretations become useful after provenance and the
baseline are understood; they must not outrun the quality of surviving material.

**Independent Test**: Compare two supplied related clips with a disputed passage and one
claimed period reference. Record lineage, processing, alternative readings, blind review,
and the reference's dated availability without attempting to identify a participant.

**Acceptance Scenarios**:

1. **Given** related recordings, **When** they are compared, **Then** capture lineage,
   completeness, edits, cropping, damage, boundaries, continuity, and copying limits remain
   visible; derivatives link their inputs, methods, settings, and tool versions.
2. **Given** disputed audio or an apparent defect, **When** interpretation is recorded,
   **Then** uncertainty and alternative readings remain visible, a second transcription is
   obtained without the preferred wording, and possible recording-chain artifacts are
   considered; generative enhancement cannot be treated as recovered evidence.
3. **Given** an apparent cultural reference, **When** its significance is assessed,
   **Then** the underlying words or image, alternative readings, dated pre-incident material,
   public availability, and distinctiveness assessment support the interpretation or leave
   it unresolved; familiarity does not imply participation. The catalog also assesses period
   availability of masks, props, equipment, and technical knowledge, and leaves motive open
   where ordinary familiarity, parody, and grievance remain compatible with the evidence.
4. **Given** dates, names, or quotations extracted from scanned pages or transcripts,
   **When** they are proposed for a finding, **Then** they are checked against the underlying
   source and discrepancies are corrected or retained as explicit uncertainty before acceptance.

---

### User Story 6 - Prepare focused records and interview research (Priority: P2)

As the project owner, I want research gaps translated into narrow requests or neutral interview
guides so I can decide whether external research is worth pursuing and authorize it separately.

**Why this priority**: External work is valuable when it targets evidence that can distinguish
explanations, and may involve access restrictions, spending, or contact with other people.

**Independent Test**: Use one missing-record question and a third-party partial release to
prepare a request draft and interview guide. The draft identifies its purpose and custodian,
preserves release limitations, and remains unsent.

**Acceptance Scenarios**:

1. **Given** a missing institutional record, **When** research is prepared, **Then** existing
   releases and holdings are checked, third-party copies retain release context and completeness
   limits, and the proposed request identifies records, custodian, identifiers, date range,
   and how a response could change the analysis.
2. **Given** a proposed interview, **When** its guide is drafted, **Then** questions separate
   firsthand observations, information learned later, affected monitors or feeds, actions taken,
   and surviving records that could verify the account.
3. **Given** a draft request, interview, paid archive visit, or other outreach, **When** it is
   considered for action, **Then** submission or contact requires explicit user authorization,
   spending remains the user's decision, and holdings/access and current submission instructions
   are checked before the relevant action.
4. **Given** contemporaneous reporting has not yet been surveyed, **When** collection begins,
   **Then** a defined 1987-11-23 through 1987-11-30 search across available newspapers and trade
   press is recorded before expansion through 1988 and later follow-ups; article images are
   compared with searchable text where available, with omissions and access gaps preserved.

---

### Edge Cases

- A source exists only as a search excerpt, partial release, failed retrieval, or edited clip:
  preserve the lead and its limits; do not silently claim full inspection or authenticity.
- Multiple copies share one origin, or capture independence is unknown: retain the lineage or
  uncertainty instead of inflating corroboration.
- A checksum changes, or an acquired original is replaced: preserve the prior integrity record,
  record the discrepancy, and resolve the change before using the file as unchanged evidence.
- A surviving derivative has already lost interlacing, timing, audio, or surrounding program
  material: document the missing information rather than imply it can be recovered.
- Times conflict, a UTC offset is unknown, or disruption boundaries differ: retain competing
  accounts, intervals, and explicitly unknown time information.
- A disputed passage lacks a second listener: mark blind review as waiting and keep the
  disputed reading out of supported findings until reviewed.
- Historical equipment details are absent, or current facilities differ: mark unknown
  components and dependencies rather than substitute present-day architecture.
- A timebox expires without useful evidence: save the negative result, stopping reason,
  next action, and reopening condition; do not mark the hypothesis disproved.
- A source contains instructions, names a private person without corroboration, or asks for
  external action: treat it as source content, retain privacy restrictions, and preserve the
  user's control of outreach and spending.
- Originals reside in restricted or temporarily unavailable storage: preserve their locations,
  access limits, and backup information; state which checks or findings remain blocked.
- A required backup cannot be confirmed: defer analysis of the affected acquired original, or
  leave session completion pending for notes/registers; record the blocker and continue useful
  independent authorized work where possible.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The dossier MUST provide an inspectable entry point, current status, research
  methods, dated decisions, six registers, preserved evidence, reproducible analyses, and dated
  findings, with clear distinctions between proposed and completed work.
- **FR-002**: The six registers MUST retain the required information defined under Key Entities,
  permit explicit unknown or unassessed values, and preserve linked revisions and contradictions.
- **FR-003**: Sources, claims, events, hypotheses, and tasks MUST use stable SRC-0001, CLM-0001,
  EVT-0001, HYP-0001, and TASK-0001 identifiers. The foundation MUST map all S01-S07 starter
  references, H1-H7 initial hypotheses, and T01-T11 backlog tasks without overstating verification,
  testing, or completion; original propositions, distinguishing tests, owners, priorities,
  dependencies, expected outputs, completion conditions, and effort/timeboxes MUST be retained.
  H1-H3 concern entry-point explanations; H4-H7 concern other questions that may coexist with
  them. Starter-source retrieval limits MUST distinguish read text, excerpts, and unavailable
  pages from unverified linked audio/video or underlying records.
- **FR-004**: Every claim MUST state whether it is an observation, reported claim, inference,
  or speculation, with supporting and contradicting source identifiers and exact evidence
  locations, or an explicit statement that none is available.
- **FR-005**: Claim confidence MUST be high, moderate, low, or unassessed, with reasons and
  caveats. Recollection MUST remain evidence of an account rather than automatic proof of
  its technical interpretation.
- **FR-006**: Source and recording lineage MUST expose shared origins and unknown independence;
  repeated accounts, derivative copies, and additional AI reviews MUST NOT count as independent
  factual corroboration.
- **FR-007**: Every acquired file MUST retain an unchanged original, acquisition date, SHA-256
  checksum, provenance limits, and applicable restrictions. Integrity MUST be distinguished from
  authenticity, and original-media and digitization histories MUST be separate when known.
- **FR-008**: Every derivative MUST identify its inputs, method, processing settings, tool
  versions, and scripts where used, with originals available for comparison. Interlacing and
  timing present in acquired sources MUST be preserved before viewing copies are made, and
  absent information MUST be documented.
- **FR-009**: Search records MUST retain exact queries, scope, filters, dates, useful and
  unsuccessful results, and access barriers. Missing records and unsuccessful searches MUST
  remain gaps rather than proof that an event or record never existed.
- **FR-010**: The chronology MUST preserve competing reports, uncertainty intervals, clock
  sources, Chicago local time and UTC offset or explicit unknowns, precision, recording
  boundaries, and separate disruption/restoration phases; unsupported precision is prohibited.
  Clock provenance MUST distinguish displayed program clocks from later uploader captions;
  surrounding program material, contemporaneous reports, station statements, and surviving logs
  MUST be examined where available.
- **FR-011**: Baseline outputs MUST include a source-dependency map, recording inventory,
  chronology with contradictions, and 1987 station signal-path diagrams with dated supporting
  evidence and explicit unknown components, distinguishing reception/distribution paths.
  Historical diagrams MUST account for the studio-to-transmitter link, monitoring, remote
  control, and alternate feeds from studio output to viewers, marking unsupported parts unknown.
- **FR-012**: Mechanism assessment MUST compare external link interference, internal insertion,
  and downstream substitution, distinguish production, playback, transmission sites, and
  operators, and use documented 1987 conditions and justified parameter ranges. Predictions
  MUST address studio monitors, over-the-air reception, geographic reach, and recovery actions.
  Feasibility estimates MUST follow architecture documentation and retain unknown receiver
  behavior, antenna characteristics, obstructions, and equipment access; guessed locations or
  power values MUST NOT be presented as deductions. Reconstruction MUST use records and offline
  modeling; live broadcast experiments are excluded.
- **FR-013**: Recording research MUST seek the best available WGN and WTTW versions, preferably
  with surrounding program material, and record capture date, receiver/feed, tape generation,
  digitization, edits, prior processing, and unknowns. Comparison MUST retain capture lineage,
  provenance, completeness, and evidence for shared damage, cropping, subtitles, edit points,
  repeated movements, audio continuity, and picture-quality changes. Processing MUST be
  conservative, with originals available side by side; hum, pitch, distortion, and visual
  defects MUST be assessed as potentially introduced anywhere in the recording chain.
- **FR-014**: Transcripts MUST retain time locations, [unclear] passages, and alternative readings.
  Disputed audio MUST receive a second transcription without the preferred wording being shown.
  Extracted dates, names, quotations, and OCR or transcription used in findings MUST be checked
  against their underlying sources; generative enhancement MUST NOT serve as recovered evidence.
- **FR-015**: Each examined cultural reference MUST record its words or image, dated material
  available before 1987-11-22 or unresolved status, alternative readings, public availability,
  and an assessment of distinctiveness without inferring participation from familiarity.
  Period research MUST cover relevant broadcaster/station references, advertising, programs,
  music, masks, props, equipment, technical knowledge, and their period availability.
  Broadcasting, amateur radio, video
  production, college media, computer/BBS communities, and prank culture are research contexts,
  not involvement indicators. Motive MUST remain broad until evidence distinguishes ordinary
  familiarity, parody, grievance, or other alternatives.
- **FR-016**: Each research cycle MUST record one bounded question, alternatives, necessary
  conditions, distinguishing predictions, evidence needs, dependencies, expected output, and
  effort timebox before searching for the cycle or testing, then preserve its method, result,
  limitations, and next action. Raw observations MUST remain separately reviewable from
  interpretation. Each cycle MUST challenge the preferred explanation against its strongest
  alternative, source dependence, hidden assumptions, and evidence that could reverse it.
- **FR-017**: Hypothesis status MUST be untested, supported, weakened, ruled out, or unresolved.
  Every status change MUST preserve its prior state and reason; ruled out MUST require evidence
  of a failed necessary condition with the assumptions and scope of exclusion.
- **FR-018**: Superseded conclusions, uncertain readings, contradictory evidence, negative
  results, and closed or deferred branches MUST remain inspectable. A stopped branch MUST name
  what is missing, why work stopped, and what would justify reopening it.
- **FR-019**: Every finding MUST include its question, linked claims and exact evidence
  locations, method, result, confidence with reasons, alternatives, limitations, and next action.
  First-delivery reports MUST address the project owner and selected reviewers, explaining the
  background, terminology, and evidence-access limits needed to audit findings without relying
  on conversation history.
- **FR-020**: Findings MUST receive a separate review for traceability, source independence,
  reproducibility, historical fit, and attribution before inclusion in shareable reports.
  Review MUST challenge the favored explanation, without being shown that theory where
  practical, and identify any specialist-review need, including qualified historical broadcast
  engineering review for questions requiring that expertise. Unresolved limits MUST remain
  visible without treating AI review as new factual evidence.
- **FR-021**: Novelty assertions MUST distinguish new to this project, independent derivation
  of published work, and potentially new contribution, supported by a preserved prior-coverage
  search and remaining limits.
- **FR-022**: Session handoff MUST preserve the last-update date, milestone, bounded question,
  evidence-linked findings and confidence, disagreements and gaps, completed task outputs,
  hypothesis changes, next three actions with owners and dependencies, external waits, and
  deferred/closed branches with reopening conditions. Resumption MUST consult saved project
  state rather than rely on conversation history. Resumption MUST read the investigation plan,
  status note, and relevant registers. Milestone checkpoints MUST keep the living plan's task
  status, findings, open questions, and next priorities consistent with saved research state,
  preserving the context and limitations of earlier records.
- **FR-023**: Tasks MUST state an owner, question, priority, dependencies, method, expected
  output and completion condition, timebox, status, result, and next action. Status MUST be queued, active, waiting, done, or
  closed. Next work MUST favor attainable distinguishing evidence; blocked expensive work
  and repeated searches without new evidence MUST state a deferral or changed next action.
  Effort ranges MUST be treated as reassessment timeboxes, not delivery promises; external
  archive and records-request waits MUST be tracked separately.
- **FR-024**: Reviews MUST follow foundation, baseline, analytical-cycle, and review milestones.
  Foundation review MUST check the evidence model's usability; baseline review MUST account for
  the four FR-011 outputs and named access gaps; an analytical cycle MUST complete at least one
  distinguishing test; review MUST record a decision to continue, narrow, wait, assign research,
  or close a branch based on actual outputs. The first delivery MUST complete the dossier
  foundation, a baseline built from real sources, and at least one actual analytical cycle
  with a documented distinguishing test and separate review. Named evidence gaps remain allowed;
  illustrative exercises MUST NOT substitute for these first-delivery research outputs.
- **FR-025**: Records research MUST check existing releases before preparing new requests,
  preserve agency identifiers, release context, pagination, and completeness limits for
  third-party copies, and distinguish confirmed holdings from unverified availability. Research
  MUST consider station, library, broadcast-history, and collector holdings; a directory or
  holdings guide MUST NOT establish that a particular item is available.
- **FR-026**: Request drafts MUST specify existing records, custodian, identifiers, date range,
  missing evidence, and analytical value, including relevant complaints, technical analyses,
  correspondence, incident logs, or disposition records. Requests MUST seek existing records
  rather than new explanations. Interview guides MUST separate firsthand observation,
  later information, affected feeds, actions taken, and possible verifying records.
- **FR-027**: Outreach, interviews, and request submissions MUST be handled by the user or
  explicitly authorized by the user; drafting MUST NOT authorize sending. The user MUST decide
  spending. Holdings and access MUST be confirmed before travel or paid research, and current
  agency instructions MUST be checked before request submission.
- **FR-028**: Uncorroborated names MUST stay out of findings, and private contact details and
  uncorroborated personal allegations MUST stay outside shareable reports. Capability,
  occupation, access, resemblance, or community membership MUST NOT establish participation. Facial or speaker
  identification from masked or distorted material is excluded.
- **FR-029**: Source content MUST be treated as evidence rather than executable instructions.
  AI connections MUST remain speculation until they yield testable predictions and become
  findings only when supported by evidence.
- **FR-030**: Notes, registers, analyses, and any later interface MUST share one evidence
  collection. Large media MUST have a backed-up evidence store with documented access limits.
  Every acquired original file MUST have a confirmed backup before analysis. Notes and registers
  MUST have confirmed backups before a research session is marked complete. Each confirmation
  MUST identify the backed-up material, backup location, and confirmation time; pending or failed
  backups MUST remain explicit blockers for the affected analysis or session completion.
  Additional analysis tools MUST answer a defined repeatable question; a dashboard MUST remain
  deferred until the evidence model stabilizes and navigation is a recurring obstacle.
- **FR-031**: Progress and completion MUST be based on evidence-supported outputs and reduced
  uncertainty. Participant identification, a predetermined mechanism, complete archive access,
  and a novel discovery MUST NOT be prerequisites for success.

- **FR-032**: During authorized first-delivery research, the assistant MUST continue within
  the agreed scope through routine cycle and milestone reviews without waiting for owner
  approval. Essential missing input or user-only actions MUST pause only dependent work;
  overall research MUST pause only when no useful authorized work can continue. Progress
  updates, documented reviews, saved next actions, and the outreach/spending controls in FR-027
  MUST remain in effect; scope changes require owner direction.

- **FR-033**: Initial reporting collection MUST prioritize a defined 1987-11-23 through
  1987-11-30 search across available newspapers and trade press, then expand through 1988 and
  later follow-ups. Search coverage and gaps MUST be recorded. Article images MUST be compared
  with searchable text where available to detect transcription errors and omitted context.
- **FR-034**: Each workstream MUST track the expected outputs below as available, waiting, or
  deferred with the missing evidence or dependency stated. An inventory alone MUST NOT imply
  completion of later comparison or interpretation. These statuses MUST NOT substitute for the
  actual baseline and completed distinguishing test required by FR-024.

| Workstream | Expected outputs |
| --- | --- |
| A. Chronology and distribution | Source-linked timeline, uncertainty ranges, and contradiction list. |
| B. Recording provenance and comparison | Recording inventory, lineage notes, annotated transcript, and reproducible comparison report. |
| C. Historical engineering | Dated signal-path diagrams, explicit assumptions table, and comparison of explanations. |
| D. Period media and culture | Reference catalog with dates, exact evidence locations, alternative readings, and distinctiveness assessments. |
| E. Records and human research | Records inventory, gaps, targeted request drafts or interview guides, and source-linked notes. |

### Key Entities *(include if feature involves data)*

The following are required record contents, not a storage or software design.

- **Source**: Stable identifier, creator, title, publication and event dates, URL or archive
  identifier, access date, source type, firsthand/retrospective status, parent source, retrieval
  status, local file when acquired, completeness, known edits, restrictions, and provenance limits.
- **Claim**: Stable identifier, one precise proposition, observation/reported claim/inference/
  speculation category, supporting and contradicting source identifiers and exact locations,
  confidence with reasons, and unresolved caveats.
- **Event**: Stable identifier, station, event description, time or interval, timezone and UTC
  offset, clock source, precision, reception path where known, recording boundaries, related
  claims, and competing reports.
- **Hypothesis**: Stable identifier, proposition, necessary conditions, distinguishing predictions,
  evidence for and against, dependencies, next test, status, and revision history.
- **Task**: Stable identifier, question, owner, priority, dependencies, method, expected output
  and completion condition, effort/timebox, status, result, and next action.
- **Search**: Question, repository, exact query, filters, date, coverage, useful and unsuccessful
  results, and access barriers.
- **Evidence Asset and Derivative**: Source relationship, acquisition date, unchanged original
  location, checksum, restrictions, original-media and digitization histories, capture lineage,
  completeness, capture date, receiver/feed, tape generation, input relationships, and processing
  history where applicable, with explicit unknowns. Acquired originals
  also record backup location and pre-analysis confirmation time.
- **Finding and Review**: Bounded question, claims and evidence locations, method, result,
  confidence and rationale, alternatives, limitations, next action, reviewer observations,
  unresolved specialist questions, novelty classification, and review decision.
- **Session and Milestone Record**: Dated current state, milestone, bounded question, completed
  outputs, hypothesis changes, gaps, external waits, next actions and owners, stopping/reopening
  conditions, milestone decision, and confirmation of notes/register backups before session
  completion.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Foundation review accounts for all six registers, all seven starter sources,
  all seven initial hypotheses, and all eleven initial backlog tasks, with mappings, statuses,
  retrieval limits, and dependencies preserved; proposed research is not reported as completed.
- **SC-002**: A reviewer can inspect acquisition date, integrity record, provenance limits, and
  original location for 100% of acquired files. Every acquired original used in analysis has a
  backup location and confirmation time preceding that analysis. The reviewer can trace 100%
  of derivatives to their inputs and documented processing without mistaking integrity for
  authenticity.
- **SC-003**: Every finding proposed for sharing has exact supporting evidence locations,
  confidence reasons, alternatives, limitations, and a review decision. Every first-delivery
  report gives the owner and selected reviewers the background, terminology, and evidence-access
  limits needed to audit its findings without conversation history; no unsupported attribution
  or unreviewed disputed reading enters shareable findings.
- **SC-004**: Before first-delivery acceptance, a baseline built from real sources accounts
  for all four baseline outputs for the two stations, exposes competing times and affected-path
  claims, and names unavailable evidence and unknown historical components without requiring
  inaccessible archives to be resolved.
- **SC-005**: Before first-delivery acceptance, at least one actual bounded analytical cycle
  using real evidence completes one distinguishing test with alternatives and predictions
  written before the cycle's searches and testing, a preserved result, a justified hypothesis-status
  review, and a
  separate findings review, even when the outcome remains unresolved.
- **SC-006**: In a handoff exercise, a fresh reviewer recovers the current milestone, bounded
  question, supported findings, hypothesis changes, unresolved gaps, external waits, and next
  three owned actions from saved project material without conversation history or an oral briefing.
  Every completed research session records confirmation that its notes and registers were backed
  up before session completion.
- **SC-007**: A representative recording/reference review retains all disputed readings,
  derivative lineage, blind-transcription outcome or explicitly waiting review, and dated
  reference evidence or unresolved status; the reviewer can explain which conclusions the
  material supports and which limits prevent stronger conclusions.
- **SC-008**: In representative blocked-source, dependent-account, speculative-identity, and
  unauthorized-outreach cases, every case retains its limitation or control; zero drafts are
  sent and zero unsupported identities are promoted to findings.
- **SC-009**: Each milestone review identifies its completed outputs, remaining gaps, and one
  explicit next decision. The project owner can accept a useful correction, authenticated
  source, narrower explanation, or justified unresolved outcome without requiring identification.
  Every routine review with useful authorized work remaining records a next action and proceeds
  without an owner-approval pause; any pause identifies the essential input, user-only action,
  or blocker and the condition for resuming.

- **SC-010**: Each of the five workstreams has a deliverable/status record accounting for every
  expected output in FR-034, with actual products linked to their evidence and unfinished
  products explicitly waiting or deferred with reasons. The baseline and completed real-evidence
  test remain mandatory under SC-004 and SC-005.

## Assumptions

- This is one dossier-and-workflow feature covering all five workstreams and the four milestones
  in the plan. Specification creation records future requirements; it does not acquire media,
  conduct research, create the operational dossier, send requests, or establish findings.
- The primary actors are the project owner, an AI research assistant, and a separate reviewer;
  the owner may also serve as a blind second listener. First-delivery findings reports are
  written for the owner and selected reviewers. No public service or multi-user account
  system is required for this feature.
- The plan remains the source of truth for scope and starting leads, and the constitution
  governs evidence handling and review. The specification adds acceptance conditions without
  treating the plan's unverified starting record as an independently confirmed finding.
- The active workspace is the project location. The different proposed project-home path in
  the plan does not request a directory move.
- The initial feature provides inspectable project material rather than a custom application.
  Storage formats, analysis tooling, and detailed file layout belong to implementation planning.
- Workflow checks may use supplied evidence or clearly labeled illustrative records when
  external material is unavailable. Illustrative records MUST remain separate from actual
  evidence and MUST NOT be cited as findings or used to claim operational milestones complete.
  First-delivery acceptance additionally requires the actual dossier foundation, a real-source
  baseline, and one completed real-evidence analytical cycle with its test and separate review.
- External archives, custodians, personal recordings, qualified specialist review, and a blind
  listener may be unavailable. Their absence is a named dependency or waiting state, not an
  automatic project failure or a negative historical conclusion.
- Detailed audiovisual analysis depends on an inventoried recording; engineering feasibility
  depends on dated architecture evidence; cultural interpretation depends on verified readings
  and period material. A suitable distinguishing question is selected after the baseline review.
- Outreach, spending, travel, access to restricted archives, live broadcast experiments,
  masked/distorted face or voice identification, and participant attribution are not automatic
  actions or completion requirements. The exclusions and user controls in FR-012 and FR-027
  through FR-031 apply.
- Analysis tools may be added for specific reproducible questions. A dashboard and exhaustive
  collection of all surviving evidence are outside the initial delivery. Novelty and participant
  identification remain possible evidence-supported outcomes, but neither is required or promised;
  the evidence, privacy, and attribution rules remain in effect.

The following mapping records plan coverage; the investigation plan remains the detailed source
of truth. The four recorded user clarifications refine first-delivery acceptance, autonomy,
report audience, and backup checkpoints.

| Investigation plan section | Specification coverage |
| --- | --- |
| 1. Purpose and success | Incident scope above; FR-019, FR-024, FR-031; SC-003-SC-005 and SC-009. |
| 2. Dossier and staged tooling | FR-001, FR-030; US1; dossier-first assumptions. Detailed formats and layout remain planning decisions. |
| 3. Starting record and uncertainties | Preliminary-state scope above; FR-003-FR-006, FR-010; US2 scenario 4. |
| 4. Registers and evidence standards | FR-002-FR-009, FR-014, FR-017-FR-018, FR-028-FR-029; Key Entities; SC-001-SC-003. |
| 5A. Chronology and distribution | FR-010-FR-012, FR-034; US2; SC-004. |
| 5B. Provenance and media comparison | FR-007-FR-008, FR-013-FR-014, FR-034; US5; SC-002 and SC-007. |
| 5C. Historical engineering | FR-011-FR-012, FR-020, FR-034; US3 scenario 3; SC-004-SC-005. |
| 5D. Chicago media and culture | FR-015, FR-028, FR-034; US5 scenario 3; SC-007 and SC-010. |
| 5E. Records and human research | FR-025-FR-028, FR-033-FR-034; US6; SC-008 and SC-010. |
| 6. Initial hypotheses | FR-003, FR-016-FR-018; US3 scenario 5; SC-001 and SC-005. |
| 7. Repeatable research cycle | FR-016-FR-023, FR-029, FR-032; US3-US4; SC-005-SC-006 and SC-009. |
| 8. T01-T11 and four milestones | FR-003, FR-023-FR-024, FR-033-FR-034; US1-US4; SC-001 and SC-004-SC-010. |
| 9. AI, user, and independent review roles | FR-014, FR-020-FR-021, FR-027-FR-029, FR-032; actor assumptions; SC-003 and SC-009. |
| 10. Status and handoff | FR-022-FR-023, FR-030, FR-032; US4; SC-006 and SC-009. |
| 11. Starter sources S01-S07 | FR-003, FR-006, FR-009, FR-025; US1; SC-001. Preserve the plan's item-specific retrieval and verification limits. |
| 12. Immediate next session | FR-003, FR-023-FR-024, FR-033; task dependencies preserve T01-T02 before expanded collection; inventory and baseline inform test selection. |
