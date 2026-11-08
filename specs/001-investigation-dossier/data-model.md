# Data Model: Investigation Dossier

Schema version: 1. Governing inputs: [spec.md](spec.md) and
[constitution](../../.specify/memory/constitution.md). Serialization is defined in
[contracts/records.md](contracts/records.md); narrative outputs in
[contracts/reports.md](contracts/reports.md).

## 1. Canonical ownership and identity

The six CSV registers own current source, claim, event, hypothesis, task, and search facts.
JSON sidecars own assets, cycles, findings/reviews, sessions, backup confirmations, and change
events. Markdown explains these facts and links to exact record revisions; it is not another
editable register. Generated tables and diagrams identify the input revision set.

| Entity | ID | Canonical home |
| --- | --- | --- |
| Source | SRC-0001 | registers/sources.csv |
| Claim | CLM-0001 | registers/claims.csv |
| Event | EVT-0001 | registers/timeline.csv |
| Hypothesis | HYP-0001 | registers/hypotheses.csv |
| Task | TASK-0001 | registers/tasks.csv |
| Search | SRCH-0001 | registers/searches.csv |
| Evidence asset, including a derivative | AST-0001 | evidence/metadata/assets/AST-0001.json |
| Bounded research cycle | CYC-0001 | analysis/cycles/CYC-0001.json |
| Finding | FND-0001 | reports/findings/FND-0001.json, with linked Markdown |
| Review | RVW-0001 | reports/findings/reviews/RVW-0001.json |
| Session | SES-0001 | evidence/metadata/sessions/SES-0001.json |
| Backup attempt/confirmation | BAK-0001 | evidence/metadata/backups/BAK-0001.json |
| Retained change record | CHG-0001 | evidence/metadata/changes/CHG-0001.json |

Mutable publication/recovery control is stored separately in
evidence/metadata/control/CHG-0001.json and mirrored to backup control storage. It is not part of
the frozen payload it coordinates. The immutable CHG record preserves the intended revisions;
the control journal records actual publication/completion events.
The immutable CHG manifest excludes its own file/hash; an outer backup snapshot can then hash
that frozen CHG file normally without recursion.

Numbers have at least four digits, increase monotonically per prefix, and never reset or reuse
retired IDs. Allocation considers existing rows, sidecars, journals, and retained tombstones
under the writer lock. Never renumber during sorting or export. Preserve legacy aliases, including
S01-S07, H1-H7, and T01-T11; aliases must be unique within their original namespace.

A source identifies an intellectual item/edition, not its download. Repeat acquisition of the
same item produces another asset with its own acquisition history. A changed edition is a separate
source linked to its predecessor. Identical file hashes do not collapse independent acquisitions,
prove independent capture, authenticate origin, or authorize merging allegations.

## 2. Common register fields

Every CSV header begins, in this order, with:

`id,revision,retired,legacy_aliases_json,unknowns_json`

- `id`: entity-specific prefix and number; unique and immutable.
- `revision`: positive integer; starts at 1 and increments on each accepted change.
- `retired`: literal true or false; retirement preserves the row, aliases, reason, and references.
- `legacy_aliases_json`: array of original plan identifiers, otherwise an empty array.
- `unknowns_json`: object mapping unknown field names to reasons or acquisition/review gaps.

All fields listed below are required columns; unknown values follow the records contract.
Descriptions are strings unless a typed enum, numeric value, date/time, or JSON collection is
specified. Each canonical change retains prior/new values, actor, timestamp, reason, and previous
hash/revision. The current row does not duplicate its whole revision history.

### Sources

Following the common fields, use:

`creator,title,publication_date,event_date,date_precision_json,source_locator,access_date,source_type,account_status_json,parent_source_ids_json,retrieval_status,inspection_json,asset_ids_json,completeness,known_edits_json,restrictions,provenance_limits`

- Publication/event dates retain YYYY, YYYY-MM, or YYYY-MM-DD precision, explained in
  date_precision_json; access dates are full ISO dates or explicit unknown markers. An interval
  and its evidence basis can be retained in the precision object. A publication date is not the
  event date, and a known year does not authorize inventing a month/day.
- `source_locator` is a URL, archive identifier, or precisely described holding, retaining its type
  in the locator text. Never replace an original locator with a later convenient copy silently.
- `source_type` describes the actual item: contemporary reporting, retrospective interview,
  station record, engineering manual, recording, period advertisement, agency release, or other
  documented type. `account_status_json` records firsthand and retrospective status on separate
  axes, each yes/no/mixed/unknown/not_applicable, with limits. Firsthand testimony can also be
  retrospective; these statuses must not be treated as mutually exclusive.
- `parent_source_ids_json` links underlying accounts/editions. The provenance explanation states
  what dependence is established and what remains unknown. The known dependence graph is acyclic.
- `retrieval_status`: not_attempted, excerpt_only, partial, retrieved, blocked, or unavailable.
- `inspection_json` separately records text inspection, linked media inspection, and underlying
  record verification, with limits. A read transcript cannot imply inspected audio.
  Optional records_context retains released-record identifiers/letter evidence/pagination or
  holding/access confirmation with explicit gaps, using the records contract's tagged shapes.
  This context does not duplicate or upgrade Source.completeness or authenticate a case file.
- `asset_ids_json` links acquired copies. Their local files are resolved through asset storage
  references; the source row does not keep a second independently editable copy of those paths.
- `completeness`: complete, partial, or unknown, relative to the described item, not the whole
  historical case. Edits, restrictions, and provenance limits remain explicit even when retrieved.

### Claims

`proposition,category,supporting_evidence_json,contradicting_evidence_json,confidence,confidence_reasons,caveats_json`

- One proposition per row. `category`: observation, reported_claim, inference, or speculation.
- Both evidence collections use the EvidenceRef shape in the records contract. Evidence can
  support that somebody made a statement without supporting the technical content of the statement.
- `confidence`: high, moderate, low, or unassessed; reasons are required for every state.
- Extraction checks are separate RVW records targeting the claim ID/revision and source basis;
  resolve them by reverse lookup rather than editing the reviewed claim to attach a review ID.
  They are required where names, dates, quotations, OCR, or transcripts used in findings needed
  checking. An unchecked disputed reading cannot become supported wording.

### Timeline events

`station,event,phase,time_local_start,time_local_end,timezone_label,utc_offset,clock_source,precision,reception_paths_json,recording_boundaries_json,related_claim_ids_json,competing_reports_json`

- `station` identifies WGN-TV, WTTW, both, or not_applicable for a related investigation event.
- `phase` distinguishes normal programming, total_disruption, black_or_static, visible_intrusion,
  restoration, investigation_event, or unknown. An event can be a boundary or an interval.
- Reported local times, timezone label, offset, clock source, and precision are separate.
  Unknown offsets are not inferred from the execution host. Endpoints cannot imply greater
  precision than their source. Preserve competing timing accounts instead of averaging them.
- `reception_paths_json` contains documented path labels and claim references. Unknown reach is
  not treated as uniform impact on over-the-air, studio-monitor, cable, and satellite feeds.
- `recording_boundaries_json` links phase boundaries to asset/time/frame locators.
- `competing_reports_json` stores objects containing claim_id, reported interval/time, clock
  source, precision, and caveat. These are attributed reports, not extra asserted event truths.

### Hypotheses

`proposition,question_scope,necessary_conditions_json,predictions_json,supporting_claim_ids_json,contradicting_claim_ids_json,dependencies_json,next_test,status,exclusion_json`

- `status`: untested, supported, weakened, ruled_out, or unresolved. Seed H1-H7 as untested.
- `question_scope` distinguishes entry point, production timing, transmitting site, insider
  knowledge, artifact origin, or a documented added question. Different scopes can coexist.
- Conditions/predictions are explicit descriptions with supporting claim references where known.
- `exclusion_json` is empty unless ruled_out; then it must include failed_condition, evidence
  references, assumptions, and exclusion_scope. Missing records cannot fill failed_condition.
- Every transition retains the previous status and reason. Reopening ruled_out requires the new
  evidence or changed assumption and does not delete the old exclusion.

### Tasks

`question,owner,priority,dependencies_json,method,expected_output,completion_condition,output_refs_json,effort_timebox,external_wait,status,result,next_action,reopening_condition`

- `owner` names AI, owner, selected reviewer/listener, or a named collaborative role; it does not
  grant permission for contact or spending. Retain the plan's original task owners.
- `status`: queued, active, waiting, done, or closed. `done` requires output references and a result
  satisfying its completion condition. `closed` requires a stopping reason. `waiting` names the
  dependency and next action. Reopening done/closed retains the earlier result and gives a reason.
- Dependencies resolve to existing entity IDs. Task dependency cycles are invalid; a blocked task
  does not block unrelated authorized tasks. Effort/timeboxes are review points, not deadlines;
  external waits are recorded separately.
  Optional typed request_draft/interview_guide outputs bind unsent files and hashes to narrow
  records requests or neutral prompts. Required unknowns remain dependencies; verification reads
  the declared output bytes only when requested. The records contract defines these shapes.

### Searches

`question,repository,exact_query,filters_json,executed_at,coverage,useful_source_ids_json,unsuccessful_results_json,access_barriers_json,cycle_id`

- `executed_at` is the actual offset-aware workflow timestamp; its date satisfies the search-date
  requirement. Record the exact query and repository even when nothing useful is found.
- `coverage` states date ranges, collections, issues, or pages actually examined. A failed query
  does not establish complete repository coverage.
- `cycle_id` links a bounded cycle or is not_applicable for initial discovery, with the stage
  recorded in coverage. New cycle searches must follow that cycle's frozen plan timestamp.

## 3. Structured sidecars

Sidecars include schema_version, id, revision, actor, created_at, and unknowns, with entity-specific
fields below. JSON timestamps are offset-aware. Closed reviews, confirmations, and change records
are immutable; corrections create a new record referencing the predecessor.

| Entity | Required information and relationships |
| --- | --- |
| Asset | kind acquired_original, derivative, or recovery_copy; source_id required for acquired originals; acquisition/creation date/time; storage reference; SHA-256; byte_count; media/capture date, receiver/feed, tape generation; original-media history; digitization history; completeness; known edits; restrictions; provenance limits; input asset IDs and locators; processing method, settings, executable/version/arguments, stream/time-base notes, and output hashes for derivatives. A derivative's source_id is null/not_applicable and its source lineage is derived from all input assets. A recovery copy records recovery_of_asset_id and backup_receipt_id. |
| Cycle | bounded question, alternatives, necessary conditions, predictions, evidence needs, dependencies, expected output, timebox, planned_by, frozen_at, frozen_plan_sha256 and retained immutable plan payload, actual search IDs, test input assets/claims, analysis-start timestamp, method, result, limitations, strongest alternative, source-dependence review, hidden assumptions, reversal evidence, hypothesis changes, finding IDs, stopping/reopening conditions, and state. |
| Finding | cycle_id, question, claim IDs plus reviewed revisions, exact evidence references, method, result, confidence and reasons, alternatives, limitations, next action, narrative path/hash, audience owner_and_selected_reviewers, access limits, and novelty category/search IDs where asserted. Matching reviews and readiness are derived from separate RVW records, without editing the reviewed finding or narrative to attach review links. |
| Review | review_type extraction/finding/milestone/blind_transcription/specialist; target using the records contract's ReviewTarget (fixed record ID/revision, or a milestone document with content hash, retained copy, and reviewed basis); author and reviewer identities/types; reviewer instance; preferred-theory exposure and rationale; evidence inspected; review findings; unresolved specialist questions; reviewed_at; decision; and superseded review ID where applicable. |
| Session | current milestone/question, started_at and intended_completion_at, findings and completed task outputs, disagreements/gaps, hypothesis changes, next three actions with owners/dependencies, waits, deferred/closed branches, stopping/reopening conditions, final handoff reference, closure snapshot ID, reserved receipt ID, and intended_state. Effective completion and actual publication/completion timestamps are determined by the separate control journal, receipt, and coherent final hashes. |
| Backup | original/session scope; covered asset/session IDs; source and destination aliases; failure-domain description; snapshot manifest with exact paths, SHA-256, and byte counts; attempt/confirmation timestamps; copy/verification method and version; result confirmed/failed; restrictions/limits; failure reason; and predecessor attempt when relevant. |
| Change | actor, preparation timestamp, reason, record IDs, previous and proposed revisions/values/hashes, and intended final file manifest. Immutable retained values support reconstruction of superseded conclusions. Mutable publication state and recovery events belong to the separate control journal, not this covered payload. |

Asset backup eligibility is derived from a matching confirmed receipt plus current content checks;
it is not an editable claim that a file is safe. Capture lineage remains separate from a software
transformation's input list. A backup receipt does not authenticate origin or establish capture
independence. Recovered bytes are a new recovery copy with a recorded relationship, never a silent
overwrite of the original or of its expected hash.

For a multi-source derivative, retain every input AST reference and obtain all source lineages
transitively; never invent a single source parent. Recovery copies preserve the original content
hash and provenance relationship but identify their new location and recovery time separately.

## 4. State transitions and guards

| Record / operation | Progression and guards |
| --- | --- |
| Acquired original | Registered -> backup_pending -> backup_confirmed -> analysis_eligible. The latter two are derived conditions. A mismatch or unavailable confirmation blocks affected analysis while retaining prior expected values and receipts. |
| Cycle | planned -> active -> tested -> reviewed. A blocked cycle records the missing dependency; closure records its result or stopping/reopening condition. frozen_at precedes the first new search and test for that cycle. An unperformed test cannot become tested. |
| Hypothesis | Transitions among the five specified statuses require reason and evidence/caveat references. ruled_out has the additional failed-necessary-condition guard; reopening preserves the previous exclusion. |
| Task | queued -> active/waiting/closed; active -> waiting/done/closed; waiting -> queued/active/closed. done/closed may reopen with a retained prior outcome and explicit reason. Imported historical transitions need an explained import record rather than invented action timestamps. |
| Finding | draft -> review_pending -> reviewed -> shareable_for_selected_reviewers. Separate reasoning review and unresolved-limit checks guard readiness. Shareable is a local readiness designation, not publication or outreach authorization. |
| Session | active -> closing -> complete after exact-content backup and coherent publication. Missing backup gives pending_backup; interrupted multi-file publication gives recovery_required. Neither state means complete. |
| Control journal | prepared -> staged -> published; interruption -> recovery_required. Only recorded expected outputs may be finished during recovery. A single-file replace is not a multi-file transaction. The immutable CHG payload does not change state after backup. |

Review identities must identify the actual separate reviewer, not merely repeat the author's
self-check under another label. A separate AI review does not increase factual corroboration.
Blind transcription records that preferred wording was withheld. Expert needs can remain limits
on a finding's scope; they must not silently disappear when a tool validates its structure.

Cycle.required_tools declares optional executable/version/argument requirements. start-analysis
captures actual version probes in analysis_tool_manifest alongside its verified input manifest;
these manifests and the start timestamp are command-owned and cannot be fabricated through apply.
Only fixed version flags are probed; actual analysis remains a separately performed, recorded method.
No decoder or executable probe is required for ordinary metadata-only validation.

Milestones remain Markdown outputs rather than a new entity/register. A milestone RVW identifies
the document through ReviewTarget.kind milestone_document, retains the reviewed bytes under
reports/findings/reviews/artifacts/RVW-ID/, and fixes its relied-on record revisions/file hashes.
Current milestone readiness uses reverse lookup against that target and basis; a later change
requires re-review without changing the preserved historical review or its document copy.

Freeze the cycle's plan subobject with a tool-recorded timestamp and content hash before its
first new query/test. Results may evolve without changing that payload. Later ideas are dated
exploratory amendments or a new cycle with fresh predictions; they cannot overwrite the frozen
plan or be described as pre-search predictions. Retain the original payload and amendment history.

An approved historical report references fixed record revisions. Later source/claim changes keep
that report intact but mark its current readiness for re-review where the cited basis changed.
Retaining history is not permission to present superseded findings as current conclusions.

## 5. Storage and session snapshots

Local storage configuration maps project, primary_evidence, and backup aliases to absolute roots.
Record paths are relative to the declared alias and must resolve within that root, without
traversal or unapproved links. Private absolute paths and contact details are excluded from reports.

An original backup confirms the exact acquired file bytes before analysis. A session backup covers
all final research notes, registers, findings, diagrams/analysis notes, the living investigation
plan, and metadata needed to interpret the session, including relevant change and asset records.
New acquired originals are independently covered by their asset receipts. Derivatives used in
findings must also have preserved locations and be included in the session manifest or a linked
verified asset manifest; omission cannot silently break reproducibility.

Closure protocol:

1. Lock the dataset, check expected hashes, and stage the final handoff/session bytes plus final
   note/register state and immutable CHG payload. Reserve the receipt ID and record a complete
   coverage manifest and intended completion time. The Session payload expresses intended_state;
   it does not assert completion without a committed control journal and matching receipt.
2. Copy this final snapshot to the configured backup root and compare hashes/byte counts.
3. Preserve matching manifest/receipt copies locally and in the backup destination. Exclude their
   own self-hashes and mutable control journals from the frozen payload to avoid recursion;
   separately mirror those control records. This exclusion does not omit actual notes/registers
   or immutable retained changes.
4. Publish the already-backed-up final bytes under the control journal. Record actual publication
   and completion timestamps in that journal, without editing the backed-up Session payload.
   Complete only when final hashes match, the receipt is confirmed, and matching committed control
   records are preserved in both stores. A failure to mirror leaves closure recovery_required.

Any intervening edit invalidates that snapshot's coverage and requires a new snapshot/receipt.
Failure before confirmation leaves the session pending; failure during publication requires
finishing the journaled publication before completion can pass. No newly edited final STATUS.md
may be written after confirmation without another backup covering its new bytes.

Restore uses a clean, previously nonexistent destination and a new AST recovery_copy record with
recovery_of_asset_id and backup_receipt_id. Verify receipt/hash/size before and after copying;
preserve the original record, location, expected hash, and discrepancy. A valid recovery copy can
be an explicitly selected analysis input using the original's matching byte confirmation and its
documented recovery chain. Never silently redirect an original's path. Journal recovery only
finishes staged metadata publication; it is a different operation from restoring asset bytes.

## 6. Seed preservation

Curate config/seed-records.json during implementation from the actual investigation plan, recording
the plan version/hash used. Do not rely on a general Markdown-table parser or refresh seeds by
overwriting existing research. Initialization is idempotent and fails on conflicting existing IDs.

- S01-S07 map to SRC-0001 through SRC-0007; retain exact source locators, text/excerpt/retrieval
  limits, access dates where stated, and the distinction from uninspected linked media/records.
- H1-H7 map to HYP-0001 through HYP-0007; preserve propositions, necessary-condition unknowns,
  distinguishing evidence, and next-test descriptions. They begin as test candidates.
- T01-T11 map to TASK-0001 through TASK-0011; preserve priorities, owners, dependencies, outputs,
  completion conditions, and effort/timeboxes. They start queued; no output is implied to exist.

| Hypothesis | Scope retained |
| --- | --- |
| H1 | External replacement on a studio-to-transmitter path. |
| H2 | Studio/internal feed insertion. |
| H3 | Downstream distribution substitution. |
| H4 | At least part of the performance prerecorded; edits alone do not establish the whole event was prerecorded. |
| H5 | One transmitting site for both intrusions; distinguish video set from transmitter location and test dated geometry/equipment constraints. |
| H6 | References required insider knowledge; test public pre-incident availability. |
| H7 | Apparent clues introduced by copying, encoding, or interpretation; test capture lineage and unprocessed comparisons. |

H1-H3 concern entry points. H4-H7 can coexist with them because they address different questions.
Initial chronology claims preserve the reported WGN duration disagreement and source retrieval
limits, not an invented precise timeline. New hypotheses may be added as evidence warrants.

## 7. Validation boundaries

- Reject invalid schemas/enums, missing required explanations, duplicate/reused IDs, dangling
  links, lineage/dependency cycles, changed originals, stale writes, and false completion guards.
- Report historical unknowns, inaccessible records, unavailable tools/listeners, and unresolved
  readings as named gaps or waiting dependencies. Baseline review permits explicit access gaps.
- Preserve observations separately from interpretation. Record the actual 1987 source for each
  supported signal-path component, or mark it unknown; current facilities are not a substitute.
- A fixture dataset has dataset_role illustrative and remains outside evidence roots. It cannot
  pass actual delivery acceptance, even when structurally complete.
- Structural validation does not authenticate a recording, verify a human interpretation, or
  replace separate source and reasoning review. Actual delivery additionally needs the real
  four-product baseline, actual distinguishing test, reviewed finding/result, five-workstream
  output inventory, and completed backed-up handoff.
- Metadata-only checks cannot assert preservation or delivery readiness. Production cycle and
  delivery validation require current byte/receipt verification; otherwise report not_evaluated
  or blocked rather than ready.
