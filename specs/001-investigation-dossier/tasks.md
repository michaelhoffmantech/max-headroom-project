---
description: "Dependency-ordered implementation and research tasks for the Max Headroom investigation dossier"
---

# Tasks: Max Headroom Investigation Dossier

**Input**: [spec.md](spec.md), [plan.md](plan.md), [research.md](research.md),
[data-model.md](data-model.md), [quickstart.md](quickstart.md), and the
[CLI](contracts/cli.md), [records](contracts/records.md), and [reports](contracts/reports.md)
contracts. The [investigation plan](../../INVESTIGATION_PLAN.md) remains the foundation;
the [constitution](../../.specify/memory/constitution.md) governs evidence and review.

**Prerequisites**: Design artifacts are complete. These checkboxes schedule future work; no
operational tool, source acquisition, actual test, or research milestone is completed by this file.

**Tests**: Include the specification's explicit handoff exercise (SC-006), representative
recording/reference review (SC-007), and negative-case exercise (SC-008), plus the integrity and
ordering guards required by SC-002/SC-005. The approved plan selects focused unittest contract
and integration checks. Author these included cases before their missing implementation and
confirm expected failures, then rerun at the story checkpoint. Do not add blanket coverage tests,
a new framework, or tests that merely repeat assignments.

**Organization**: Setup, shared foundations, six stories in priority order (US1-US4 P1,
US5-US6 P2), then cross-cutting delivery validation. Task IDs describe this implementation
backlog; source T01-T11 aliases and TASK-0001-style register IDs remain distinct.

## Format: Task ID, optional parallel marker, story label, and exact paths

Every actionable item is one unchecked T001-style checklist line. Story phases include US1-US6
labels; setup/foundation/polish omit them. A P marker means the listed dependency/phase entry is
already complete and the task can be authored beside the other marked task without shared-file
writes. It never authorizes simultaneous register mutations.

## Path Conventions

All paths in task descriptions are relative to the active project root. Feature documents are
under specs/001-investigation-dossier/. Operational paths follow plan.md, including tools/dossier.py,
the six registers, JSON sidecars, analysis/, reports/, docs/, private/, and work/.
Actual storage locations use authorized aliases in config/storage.local.json.

The CLI remains one small entry point. Tasks that edit tools/dossier.py or the same test file
must be serialized, even if other story work is ready. Do not introduce a dashboard, database,
automatic crawler, sender, or paid dependency.

## Execution and Blocker Rules

- Explicit dependencies below control readiness; phase numbering groups story priorities rather
  than requiring an unrelated blocked research branch to halt all implementation.
- All shared foundation tasks must complete before story implementation. Story tests and guide
  drafts can use isolated supplied data; actual baseline/test/review work uses real sources.
  Expanded collection requires T027's passed foundation review, without a new owner-approval pause.
- Production backup configuration is essential input, never guessed. T025 records its state;
  T028, affected original analyses, and T083 cannot complete without the required confirmation.
  Continue independent useful code/fixture/documentation work under the agreed autonomy policy.
- T046 is mandatory for first delivery. If the chosen test needs media, blind listening, cultural
  evidence, or institutional records, complete the applicable T065-T068/T073 prerequisites first,
  then return to T046. Those branches depend on the baseline, not the completed test.
- Conditional detailed-work tasks T065-T068 and T073-T074 stay unchecked when unperformed.
  Document a specific waiting/deferred source TASK state, missing evidence, next action, and
  reopening condition. T069/T078 assess capability and account for those states; they do not
  mark the underlying work done or waive T046. Source T08 retains T07 as a completion prerequisite;
  separate preliminary availability work under T064 does not complete T068 or source T08.
- Close each actual research session at its end with backed-up final notes/registers; do not
  postpone every backup until the last phase. If closure is pending, never claim it complete.
- Review actual source content and reasoning separately from machine validation. No task sends
  outreach, submits a records request, conducts an interview, purchases access, or publishes.
  Owner-only decisions and unresolved expert/listener needs remain explicit dependencies.
- Check a task only after its described work and completion condition are met. A passed fixture
  proves tooling, not a historical finding, a real baseline, or a completed actual test.

## Phase 1: Setup (Shared Infrastructure)

**Goal**: Prepare the file-based project without creating findings, acquiring evidence, installing optional media packages, or initializing Git.

### Implementation

- [X] T001 Create the planned directory skeleton and entry stub in README.md, tools/, tests/fixtures/, config/, docs/, registers/, evidence/metadata/, analysis/, derived/, reports/, private/, and work/; add .gitignore exclusions for machine-specific roots, private information, large media, bytecode, and temporary fixtures without initializing Git.

### Preparation

- [X] T002 [P] Define schema_version 1 and actual/illustrative dataset roles in config/dossier.json and an unset-backup template in config/storage.local.example.json; keep production roots out of shared metadata. (Depends on T001.)
- [X] T003 [P] Document evidence/interpretation separation, source-as-data handling, required user controls, repeatable questions, and checkpoint conventions in docs/METHODS.md and docs/DECISIONS.md, deriving them from the constitution and four accepted clarifications. (Depends on T001.)
- [X] T004 [P] Create clearly invented temporary-workspace seeds in tests/fixtures/seed-records.json and fixture guidance in tests/fixtures/README.md; set dataset_role illustrative and forbid importing fixture claims/assets into actual evidence. (Depends on T001.)

**Checkpoint**: The planned paths, configuration declarations, and isolated fixtures exist; no source-plan or constitution rewrite.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Goal**: Provide the shared record and preservation primitives required by every story, including session closure before any actual research session can be marked complete.

**Critical gate**: Complete this shared foundation before story implementation. Missing production storage still blocks only the dependent actual operation; it does not prevent building/testing these primitives.

### Acceptance checks

- [X] T005 Author the contract/failure cases required by SC-002, SC-006, SC-008 and quickstart.md in tests/test_preservation.py: changed bytes, interrupted copying/publication, missing roots, stale writes, snapshot edits, and control-journal mirroring; confirm expected failures before implementing the missing behavior. (Depends on T002, T003, T004.)

### Implementation

- [X] T006 Implement strict UTF-8 CSV/JSON codecs and common fields in tools/dossier.py using header "id,revision,retired,legacy_aliases_json,unknowns_json"; enforce "All fields listed below are required columns; unknown values follow the records contract.", "entity-specific prefix and number; unique and immutable.", "positive integer; starts at 1 and increments on each accepted change.", "literal true or false; retirement preserves the row, aliases, reason, and references.", "array of original plan identifiers, otherwise an empty array.", and "object mapping unknown field names to reasons or acquisition/review gaps."; reject duplicate keys, non-finite JSON, malformed quoting, and wrong headers/row widths. Preserve explicit unknown/not_applicable scalars and enforce "Do not serialize Python None as a blank cell." and "JSON unknowns use null plus the unknowns map.". (Depends on T005.)
- [X] T007 Implement Sources and Searches schemas in tools/dossier.py with exact additional headers "creator,title,publication_date,event_date,date_precision_json,source_locator,access_date,source_type,account_status_json,parent_source_ids_json,retrieval_status,inspection_json,asset_ids_json,completeness,known_edits_json,restrictions,provenance_limits" and "question,repository,exact_query,filters_json,executed_at,coverage,useful_source_ids_json,unsuccessful_results_json,access_barriers_json,cycle_id"; enforce "not_attempted, excerpt_only, partial, retrieved, blocked, or unavailable.", "complete, partial, or unknown, relative to the described item, not the whole historical case.", "axes, each yes/no/mixed/unknown/not_applicable, with limits.", "A read transcript cannot imply inspected audio.", "Publication/event dates retain YYYY, YYYY-MM, or YYYY-MM-DD precision, explained in date_precision_json; access dates are full ISO dates or explicit unknown markers.", "is the actual offset-aware workflow timestamp; its date satisfies the search-date requirement.", and "New cycle searches must follow that cycle's frozen plan timestamp."; retain locator type, coverage, negative results, and barriers. (Depends on T006.)
- [X] T008 Implement Claims and Timeline schemas in tools/dossier.py with headers "proposition,category,supporting_evidence_json,contradicting_evidence_json,confidence,confidence_reasons,caveats_json" and "station,event,phase,time_local_start,time_local_end,timezone_label,utc_offset,clock_source,precision,reception_paths_json,recording_boundaries_json,related_claim_ids_json,competing_reports_json"; enforce "One proposition per row.", "observation, reported_claim, inference, or speculation.", "high, moderate, low, or unassessed; reasons are required for every state.", "WGN-TV, WTTW, both, or not_applicable for a related investigation event.", "normal programming, total_disruption, black_or_static, visible_intrusion, restoration, investigation_event, or unknown.", and "Unknown offsets are not inferred from the execution host."; preserve independent clock/precision/boundary/path fields and attributed competing reports. (Depends on T007.)
- [X] T009 Implement Hypotheses and Tasks schemas in tools/dossier.py with headers "proposition,question_scope,necessary_conditions_json,predictions_json,supporting_claim_ids_json,contradicting_claim_ids_json,dependencies_json,next_test,status,exclusion_json" and "question,owner,priority,dependencies_json,method,expected_output,completion_condition,output_refs_json,effort_timebox,external_wait,status,result,next_action,reopening_condition"; enforce "untested, supported, weakened, ruled_out, or unresolved. Seed H1-H7 as untested.", "is empty unless ruled_out; then it must include failed_condition, evidence references, assumptions, and exclusion_scope.", "queued, active, waiting, done, or closed.", "requires output references and a result satisfying its completion condition.", "requires a stopping reason.", and "names the dependency and next action."; retain owners, output conditions, question scopes, evidence, effort/timeboxes, and reopening reasons. Enforce "queued -> active/waiting/closed; active -> waiting/done/closed; waiting -> queued/active/closed." and "Imported historical transitions need an explained import record rather than invented action timestamps.". (Depends on T008.)
- [X] T010 Define Asset, Cycle, Finding, Review, Session, Backup, and immutable Change sidecar shapes in tools/dossier.py from data-model.md section 3; enforce "Sidecars include schema_version, id, revision, actor, created_at, and unknowns, with entity-specific fields below. JSON timestamps are offset-aware.", "Closed reviews, confirmations, and change records are immutable; corrections create a new record referencing the predecessor.", "kind acquired_original, derivative, or recovery_copy", "source_id required for acquired originals", "A derivative's source_id is null/not_applicable and its source lineage is derived from all input assets.", "A recovery copy records recovery_of_asset_id and backup_receipt_id.", "review_type extraction/finding/milestone/blind_transcription/specialist", "audience owner_and_selected_reviewers", and "result confirmed/failed"; require every remaining field in the entity table rather than inventing defaults. (Depends on T009.)
- [X] T011 Implement ID allocation, RecordRef/EvidenceRef/StorageRef and tagged ReviewTarget validation, revision/content-based reverse review lookup, immutable milestone document/basis copies, and graph checks in tools/dossier.py; enforce "Numbers have at least four digits, increase monotonically per prefix, and never reset or reuse retired IDs.", "The known dependence graph is acyclic.", "Task dependency cycles are invalid; a blocked task does not block unrelated authorized tasks.", and "Required: source_id, locator, role, and limits. Optional: asset_id, claim_id, and source_revision."; validate all required collection item shapes and preserve retired references and alias uniqueness. (Depends on T010.)
- [X] T012 Implement checked change-set publication and recover --finish in tools/dossier.py, retaining immutable evidence/metadata/changes/CHG records separately from evidence/metadata/control/ journals; enforce "prepared -> staged -> published; interruption -> recovery_required." and "The immutable CHG manifest excludes its own file/hash; an outer backup snapshot can then hash that frozen CHG file normally without recursion."; use a single-writer lock, expected prior revisions/hashes, same-directory staging, and explicit interrupted multi-file recovery without touching original bytes. (Depends on T011.)
- [X] T013 Implement alias resolution and production/illustrative storage checks in tools/dossier.py for config/storage.local.json: allow primary_evidence inside project, reject backup overlap and traversal/unapproved links, require owner-described production failure domains, and leave an unset/unreachable backup as a dependent-action blocker rather than choosing a destination. Enforce "Record paths are relative to the declared alias and must resolve within that root, without traversal or unapproved links.". (Depends on T012.)
- [X] T014 Implement bounded file hashing/copying and immutable original/session BAK receipts in tools/dossier.py and evidence/metadata/backups/; enforce "Asset backup eligibility is derived from a matching confirmed receipt plus current content checks; it is not an editable claim that a file is safe."; compare SHA-256 and byte_count, preserve failed attempts and prior expected hashes, and never authenticate origin or overwrite an existing original/backup. Derive "Registered -> backup_pending -> backup_confirmed -> analysis_eligible." without a user-editable safety flag. (Depends on T013.)
- [X] T015 Implement the shared close-session backend in tools/dossier.py using final staged notes/registers, immutable CHG payloads, reserved receipt IDs, and mirrored control journals; enforce "Effective completion and actual publication/completion timestamps are determined by the separate control journal, receipt, and coherent final hashes.", "A failure to mirror leaves closure recovery_required.", and "No newly edited final STATUS.md may be written after confirmation without another backup covering its new bytes."; include the living plan and reproducibility metadata while excluding only self-hashes/mutable controls from the frozen payload. Enforce "active -> closing -> complete after exact-content backup and coherent publication." and "Missing backup gives pending_backup; interrupted multi-file publication gives recovery_required. Neither state means complete.". (Depends on T014.)
- [X] T016 Expose the common command router, apply, backup, close-session, recover, --help, dataset_manifest, and text/JSON result envelope in tools/dossier.py per contracts/cli.md; use exit codes 0/2/3/4/5, resolve relative input paths from invocation CWD, select writes through --root, and keep diagnostics/private roots out of shareable stdout. (Depends on T015.)
- [X] T017 Run the isolated preservation/journal cases in tests/test_preservation.py against tools/dossier.py; prove no success receipt or complete state is emitted after hash mismatch, interrupted copy, changed snapshot, or missing mirrored commit, and document only actual outcomes in docs/DECISIONS.md. (Depends on T016.)

**Checkpoint**: Shared schema, change, storage, backup, closure, and CLI primitives pass isolated checks. An unknown production backup location does not block unrelated code or fixture work.

---

## Phase 3: User Story 1 - Establish a trustworthy evidence dossier (Priority: P1)

**Goal**: Deliver the inspectable six-register foundation, faithful seed mappings, immutable acquisitions and verified backup/restore operations.

**Independent Test**: Register all seven starter references plus supplied dependent-account, inaccessible-source, and acquired-file examples in an isolated illustrative dataset; inspect provenance/limits and run the actual foundation gate without claiming a real baseline.

### Acceptance checks for US1

- [X] T018 [P] [US1] Author source/claim/reference and init/ingest/backup/restore command acceptance cases in tests/test_records.py for US1 scenarios 1-6 and SC-008; cover dual firsthand/retrospective status, partial dates, shared lineages, explicit unknowns, idempotent seeds, conflicting IDs, milestone ReviewTarget/retained-copy validation before the foundation review, and fixture-vs-actual separation. (Depends on T017.)

### Preparation for US1

- [X] T019 [P] [US1] Curate config/seed-records.json from INVESTIGATION_PLAN.md, recording its hash and all S01-S07/H1-H7/T01-T11 aliases, exact locators/inspection limits, hypothesis scopes/distinguishing tests, owners, priorities, dependencies, outputs, completion conditions, and timeboxes; keep hypotheses untested and tasks queued without inventing inspected media or completed research. (Depends on T017.)

### Implementation for US1

- [X] T020 [US1] Implement non-destructive init and faithful seed materialization in tools/dossier.py across registers/sources.csv, registers/claims.csv, registers/timeline.csv, registers/hypotheses.csv, registers/tasks.csv, and registers/searches.csv; preserve matching existing research and reject conflicting records. (Depends on T018, T019.)
- [X] T021 [US1] Implement ingest and the asset-facing backup command integration in tools/dossier.py; create new immutable acquisition bytes and AST metadata, retain capture/provenance unknowns and restrictions, and require a matching confirmed receipt before analysis rather than treating checksums as authentication. (Depends on T020.)
- [X] T022 [US1] Implement restore-asset in tools/dossier.py to verify a BAK receipt and create a linked recovery_copy at a clean new primary location; preserve original metadata/path/hash and discrepancies, and keep this operation separate from recover --finish. (Depends on T021.)
- [X] T023 [US1] Implement validate --gate records/foundation and --verify-files in tools/dossier.py, including exact row/sidecar/revision checks, source/capture dependence, review reverse lookup, current bytes/receipt coverage, structure_only metadata results, and original/recovery-copy eligibility without silently repairing records. (Depends on T022.)
- [X] T024 [US1] Populate README.md, docs/STATUS.md, and docs/METHODS.md with current foundation state, record/command conventions, private-material boundaries, storage aliases, checkpoint rules, and the distinction between inherited planning inspection and newly performed research. (Depends on T023.)
- [X] T025 [US1] Create config/storage.local.json with actual authorized project/primary roots and record backup readiness in docs/STATUS.md; use an owner-authorized backup location and failure-domain description only when supplied, otherwise keep backup unset and name the essential dependency without claiming production protection. (Depends on T024.)
- [X] T026 [US1] Inspect the starter sources within T02's bounded effort and register their actual source dependence, extraction limits, access barriers, and closest underlying accounts in registers/sources.csv, registers/claims.csv, and registers/searches.csv; preserve S01-S07 aliases and record unestablished parents honestly. (Depends on T025.)
- [X] T027 [US1] Run tests/test_records.py and the US1 independent exercise, then validate the actual foundation via tools/dossier.py and record the usability assessment and next decision in reports/milestones/foundation.md, then preserve a matching milestone RVW using ReviewTarget with its fixed document/basis copies; resolve and re-review failures before unlocking expanded collection. A supplied fixture proves tooling but cannot be cited as acquired incident evidence or a real baseline. (Depends on T026.)
- [X] T028 [US1] Close the actual foundation research session through tools/dossier.py using docs/STATUS.md and evidence/metadata/sessions/ plus evidence/metadata/backups/; require confirmed final notes/register bytes before marking that session complete, and retain a pending closure if the owner backup input is absent. (Depends on T027.)

**Checkpoint**: A usable foundation increment is demonstrated; production closure remains pending until an authorized backup is confirmed. This MVP is not the agreed first-delivery stopping point.

---

## Phase 4: User Story 2 - Establish a baseline without false precision (Priority: P1)

**Goal**: Produce a real-source dependency map, chronology/contradictions, recording inventory, and dated historical signal paths.

**Independent Test**: Use supplied conflicting duration accounts, uncertain capture lineage, and partially documented 1987 paths to prove the baseline preserves disagreements and explicit gaps, independently of a completed analytical cycle.

### Acceptance checks for US2

- [X] T029 [P] [US2] Author chronology and baseline-output contract exercises in tests/test_workflow.py for US2 scenarios 1-4: reported 25/30-second differences, event phases, unknown offsets, distinct reception paths, source retrieval limits, and real-vs-unexamined seed baselines. (Depends on T017.)

### Preparation for US2

- [X] T030 [P] [US2] Prepare clearly unfilled output structures in analysis/chronology/source-map.md, analysis/chronology/timeline.md, analysis/chronology/contradictions.md, analysis/media-comparison/recording-inventory.md, analysis/engineering/signal-paths.md, and analysis/engineering/assumptions.md from contracts/reports.md; do not label scaffolds completed research. (Depends on T017.)

### Implementation for US2

- [X] T031 [US2] Implement chronology/path/precision validation in tools/dossier.py without deriving historical offsets from the host or averaging conflicting reports; distinguish displayed program clock from later uploader caption and preserve separate total-disruption, static/black, visible-intrusion, and restoration boundaries. (Depends on T029, T030, T023.)
- [X] T032 [US2] Perform the defined 1987-11-23 through 1987-11-30 contemporary newspaper/trade-press survey in registers/searches.csv and registers/sources.csv before expanding through 1988/later follow-ups; compare article images with searchable text where available, register exact evidence, and reassess T03 after 2-3 research sessions with gaps preserved. (Depends on T027, T031.)
- [X] T033 [US2] Build analysis/chronology/source-map.md from inspected accounts and canonical parent/capture relationships, exposing repetition, unknown independence, and retrieval limits; apply supporting register updates through tools/dossier.py instead of maintaining a second mutable account. (Depends on T032.)
- [X] T034 [US2] Locate and inventory the best available WGN/WTTW versions in analysis/media-comparison/recording-inventory.md and evidence/metadata/assets/, recording capture date, receiver/feed, tape generation, digitization, completeness, surrounding material, edits/processing, restrictions, and derivative-only/unavailable limits; protect acquired originals before analysis. Recording discovery may proceed independently of T032 after the foundation review passes. (Depends on T027, T030.)
- [X] T035 [US2] Populate registers/timeline.csv, analysis/chronology/timeline.md, and analysis/chronology/contradictions.md from real source locations, preserving clock origin, Chicago local time/offset or unknowns, precision, intervals, event boundaries, and distinct feed reports without forcing exact duration. (Depends on T033, T034.)
- [X] T036 [US2] Reconstruct supported 1987 station paths in analysis/engineering/signal-paths.md and analysis/engineering/assumptions.md using dated station/licensing/manual/trade/engineering evidence; include studio-to-transmitter links, monitoring, remote control, alternate feeds, viewers, and unknown receiver/antenna/obstruction/access parameters; reassess T06 after 2-3 sessions and use no live experiments. (Depends on T032.)
- [X] T037 [US2] Implement validate --gate baseline in tools/dossier.py against the four output contracts and exact sources, search coverage, historical components, named gaps, and the retained passed foundation review before expanded collection; do not accept a restatement of uninspected seed descriptions or interpret schema success as authenticated facts. (Depends on T031, T036.)
- [X] T038 [US2] Run the US2 independent exercise and actual baseline --verify-files check with tools/dossier.py; inspect source content and record the four-product review and next decision in reports/milestones/baseline.md, docs/STATUS.md, and the living INVESTIGATION_PLAN.md without erasing initial limitations; preserve the milestone RVW with its fixed document/basis copies. (Depends on T033, T034, T035, T036, T037.)

**Checkpoint**: Baseline products cite real inspected sources or concrete searched-for gaps; structural checks do not substitute for historical review.

---

## Phase 5: User Story 3 - Test competing explanations (Priority: P1)

**Goal**: Freeze alternatives before new searches, perform one attainable real test, and preserve justified hypothesis changes and separate review.

**Independent Test**: Take one supplied question with at least two alternatives through a frozen plan, ordered search/test events, result, exclusion/reopening guards, and review without requiring external archive access.

### Acceptance checks for US3

- [X] T039 [P] [US3] Author cycle/start-analysis/exclusion contract cases in tests/test_workflow.py for late searches, altered frozen predictions, missing original protection, unfounded ruled_out states, changed assumptions/reopening, and coherent actual-versus-illustrative cycle readiness. (Depends on T017.)

### Preparation for US3

- [X] T040 [P] [US3] Document question scoping, H1-H3 entry-point alternatives versus coexisting H4-H7 questions, necessary conditions, predictions, timeboxes, and raw-observation/reversal-evidence conventions in analysis/cycles/README.md; include no invented actual result. (Depends on T017.)

### Implementation for US3

- [X] T041 [US3] Implement Cycle validation and immutable plan publication in tools/dossier.py and analysis/cycles/: enforce "Freeze the cycle's plan subobject with a tool-recorded timestamp and content hash before its first new query/test." and "Results may evolve without changing that payload."; retain frozen_plan_sha256 and the original payload, classifying later predictions as dated exploratory amendments or a new cycle rather than backdating them. Preserve "planned -> active -> tested -> reviewed." and reject a tested state for an unperformed test. (Depends on T039, T040, T037.)
- [X] T042 [US3] Implement hypothesis transitions in tools/dossier.py with "Every transition retains the previous status and reason." and "Reopening ruled_out requires the new evidence or changed assumption and does not delete the old exclusion."; require the evidenced failed necessary condition, assumptions, and scope, preserve negative results/contradictions, and never infer exclusion from missing records. (Depends on T041.)
- [X] T043 [US3] Implement start-analysis in tools/dossier.py with current original/recovery-chain byte/receipt checks, frozen cycle/input revisions, required tool/input dependencies, and an actual analysis-start manifest/time; unavailable dependencies block only affected work and do not produce a test result. (Depends on T042.)
- [X] T044 [US3] Implement actual method/result, input/derivative links, strongest alternative, source dependence, hidden assumptions, reversal evidence, finding references, and validate --gate cycle in tools/dossier.py; require --verify-files and a real separate review rather than metadata-only or AI-agreement readiness. (Depends on T043.)
- [X] T045 [US3] Choose the highest-information attainable bounded question from the real baseline and save analysis/cycles/CYC-0001.json with alternatives, conditions, distinguishing predictions/evidence, dependencies, expected output, and timebox before its new searches; if media or archival inputs are needed, link the relevant US5/US6 waiting work instead of guessing. (Depends on T038, T044.)
- [X] T046 [US3] Perform the actual bounded method with real inspected evidence and preserved/protected inputs, recording queries in registers/searches.csv and observations, method, timestamps, result, limitations, and reversal evidence in analysis/cycles/CYC-0001.json and analysis/cycles/CYC-0001.md; leave this task unchecked if the required test cannot be performed. (Depends on T045.)
- [X] T047 [US3] Apply the real outcome and justified hypothesis/claim revisions through tools/dossier.py to registers/hypotheses.csv, registers/claims.csv, and reports/findings/FND-0001.json with its narrative; preserve prior states and source locations, and distinguish a supported finding from a speculative connection or merely reported account. (Depends on T046.)
- [X] T048 [US3] Obtain an actual separate reasoning/source review for the completed test in reports/findings/reviews/RVW-0001.json, targeting fixed IDs/revisions and narrative hashes; record actual reviewer identity/exposure, unresolved specialist needs, confidence reasons, and next action without counting AI agreement as independent factual corroboration. (Depends on T047.)
- [X] T049 [US3] Run tests/test_workflow.py and the independent supplied-evidence exercise, then assess the real cycle with tools/dossier.py --format json validate --gate cycle --verify-files; record only the actually performed test/review in reports/milestones/analytical-cycle.md and source-task T10 status in registers/tasks.csv; preserve a matching milestone RVW with its fixed document/basis copies. (Depends on T048.)

**Checkpoint**: The actual distinguishing test is performed and reviewed; unresolved is a valid result, but an unperformed or illustrative test cannot satisfy first delivery.

---

## Phase 6: User Story 4 - Review findings and resume the investigation (Priority: P1)

**Goal**: Provide auditable owner/reviewer reports, derived review readiness, novelty limits, living checkpoints, and backed-up resumable sessions.

**Independent Test**: Give a fresh reviewer a supplied completed finding, hypothesis revision, and saved state; they must recover the current question, supporting evidence, limits, and next actions without chat history.

### Acceptance checks for US4

- [X] T050 [P] [US4] Author review/report/handoff/delivery contract exercises in tests/test_workflow.py for reverse review lookup without target edits, milestone document targets and retained copies, rejected mismatched hashes or missing basis, changed cited bases versus unrelated edits, owner/reviewer context, missing specialist/blind review limits, fixture rejection, metadata-only blocking, and final-byte closure coherence. (Depends on T017.)

### Preparation for US4

- [X] T051 [P] [US4] Prepare reports/findings/README.md and reports/milestones/README.md from contracts/reports.md, specifying finding fields, exact reviewed revisions, milestone ReviewTarget/basis copies, privacy checks, all-five-workstream output inventory, four milestone decisions, next actions, and the difference between local shareable readiness and publication. (Depends on T017.)

### Implementation for US4

- [X] T052 [US4] Implement extraction/finding/milestone/blind_transcription/specialist RVW validation and derived finding readiness in tools/dossier.py; enforce "Review identities must identify the actual separate reviewer, not merely repeat the author's self-check under another label." and "Shareable is a local readiness designation, not publication or outreach authorization."; validate both ReviewTarget variants and their fixed basis/copies, and use reverse lookup to invalidate current readiness for changed reviewed content/basis without editing a reviewed target just to attach a decision; unrelated edits must not invalidate a review. Derive "draft -> review_pending -> reviewed -> shareable_for_selected_reviewers." from the actual matching reviews. (Depends on T050, T051, T044.)
- [X] T053 [US4] Implement novelty-category, prior-coverage-search, audience/access-limit, confidence/caveat, specialist-need, and privacy-review checks in tools/dossier.py; preserve unsupported identities/private contacts outside findings and label AI connections speculation until testable predictions and evidence justify promotion. (Depends on T052.)
- [X] T054 [US4] Integrate Session/task/milestone state and five-workstream output accounting in tools/dossier.py with docs/STATUS.md and reports/milestones/; require current question, findings/confidence, disagreements/gaps, outputs, hypothesis changes, next three owned/dependent actions, waits, and stopping/reopening conditions while preserving the shared closure backend. (Depends on T053.)
- [X] T055 [US4] Implement validate --gate delivery in tools/dossier.py: actual dataset, real four-product baseline, actual test plus separate review, five-workstream statuses, reviewed owner/reviewer report, four milestone decisions with retained matching reviews, a current final milestone review, and coherently completed backed-up handoff; reject omitted --verify-files, illustrative substitution, and false done states. (Depends on T054.)
- [X] T056 [US4] Prepare the actual reports/findings/FND-0001.md and linked metadata for the owner and selected reviewers from the reviewed real cycle, explaining terminology, exact evidence, confidence, alternatives, limitations, and restricted-source access without conversation history or unsupported attribution. (Depends on T049, T055.)
- [X] T057 [US4] Search prior coverage before any novelty assertion and record it in registers/searches.csv, reports/findings/FND-0001.json, and docs/STATUS.md; distinguish new_to_project, independent_derivation, and potentially_new_contribution, preserve specialist/blind-listening waits, and re-review any changed finding content. (Depends on T056.)
- [X] T058 [US4] Obtain and preserve a separate final report review in reports/findings/reviews/RVW-0002.json with evidence inspected, privacy/attribution assessment, actual reviewer identity, preferred-theory exposure, unresolved specialist needs, and decision; keep narrative/revision bytes fixed when attaching the review. (Depends on T057.)
- [X] T059 [US4] Run the independent fresh-reviewer handoff exercise and tests/test_workflow.py, update current checkpoints in INVESTIGATION_PLAN.md and docs/STATUS.md, and close each actual session through tools/dossier.py only after final note/register backup confirmation; record valid routine next decisions without approval pauses. (Depends on T058.)

**Checkpoint**: All actual findings/handoffs remain reviewable, routine reviews continue authorized work, and completed sessions have final-byte backup confirmation.

---

## Phase 7: User Story 5 - Evaluate audiovisual and cultural clues (Priority: P2)

**Goal**: Support conservative, reproducible recording comparisons and period-reference evaluation without overrunning provenance or implying identification.

**Independent Test**: Use two supplied related clips, one disputed passage, and a claimed period reference to inspect lineage, processing, blind review, dated availability, and remaining limits.

### Acceptance checks for US5

- [X] T060 [P] [US5] Author media/reference record and output contract exercises in tests/test_records.py for multi-input lineage, shared damage, lost timing/interlacing, uncertain wording, blind-review absence, extraction checks, period dates, widespread availability, and generative-detail exclusion. (Depends on T017.)

### Preparation for US5

- [X] T061 [P] [US5] Document conservative processing, complete capture histories, side-by-side originals, required versions/arguments/stream/time-base manifests, blind transcription, and dated cultural-context rules in analysis/media-comparison/README.md and analysis/culture/README.md; make media executables conditional rather than mandatory dependencies. (Depends on T017.)

### Implementation for US5

- [X] T062 [US5] Implement derivative/recovery lineage and processing-manifest checks in tools/dossier.py, enforcing "For a multi-source derivative, retain every input AST reference and obtain all source lineages transitively; never invent a single source parent."; preserve capture lineage separately from transformation inputs, all settings/versions/hashes, and missing information rather than recovering invented detail. (Depends on T060, T061, T023.)
- [X] T063 [US5] Integrate task-specific executable/version/argument and source/backup preflight checks into tools/dossier.py and docs/METHODS.md; absent FFmpeg/ffprobe or a required recording/listener yields an explicit waiting task, without installation or decoding being required for ordinary metadata checks. (Depends on T062.)
- [X] T064 [US5] Prepare the source-linked catalog and uncertainty/extraction-check conventions in analysis/culture/reference-catalog.md and derived/transcripts/README.md, accounting for dates before 1987-11-22, exact locations, alternative readings, distinctiveness, props/equipment/knowledge availability, and broad motive alternatives; record any independent preliminary availability research under a separate source TASK and label its entries preliminary, without interpreting unverified recording content or completing source T08. (Depends on T063, T027.)
- [X] T065 [US5] When the baseline justifies detailed media work, obtain the best available relevant versions, extend analysis/media-comparison/recording-inventory.md and AST metadata through tools/dossier.py, and confirm original backups before probing/processing; otherwise record the specific waiting/deferred dependency and leave unperformed acquisition unchecked. (Depends on T034, T064.)
- [X] T066 [US5] For the bounded media question, create only the needed reproducible analysis in analysis/media-comparison/compare_recordings.py, preserved derived/frames/ or derived/audio/ outputs, and analysis/media-comparison/comparison-report.md; compare boundaries/repeated movement/audio/picture quality and copying artifacts with originals, retaining settings/versions and no default destructive enhancement. (Depends on T065.)
- [ ] T067 [US5] Create the actual time-coded derived/transcripts/annotated-transcript.md with unclear/alternative readings and obtain derived/transcripts/blind-transcription.md without revealing preferred words; retain actual reviewer/exposure records, keep disputed readings out of supported findings while review is waiting, and leave unperformed listening unchecked. (Depends on T065.)
- [ ] T068 [US5] After T066/T067 supply source T07's completed comparison/transcription and required blind review, populate analysis/culture/reference-catalog.md for verified recording words/images from actual pre-incident material and registered searches: broadcaster/station references, advertising/programs/music, masks/props/equipment/knowledge, and relevant communities; assess public availability/distinctiveness without inferring involvement or a narrow motive. If required T07 review is waiting, leave T068/source T08 unperformed; preliminary availability work remains separately recorded under T064. (Depends on T066, T067, T038.)

### Integration for US5

- [X] T069 [US5] Run tests/test_records.py and the isolated US5 comparison/reference exercise; integrate completed products or precise waiting/deferred dependencies into reports/milestones/workstreams.md, docs/STATUS.md, and source T07/T08 records in registers/tasks.csv, preserving actual performed-vs-unperformed status and review needs; source T08 cannot become done until source T07's output/completion condition, including required blind review, is satisfied. (Depends on T064.)

**Checkpoint**: Capability is tested independently; actual detailed analysis occurs only when justified and its dependencies exist. Unperformed media/listening work stays unchecked and waiting/deferred.

---

## Phase 8: User Story 6 - Prepare focused records and interview research (Priority: P2)

**Goal**: Turn documented gaps into authenticated record inventories and neutral unsent requests/interview guides under the owner's external-action controls.

**Independent Test**: Use one supplied missing-record question and partial release to prepare a narrow request and neutral interview guide that retain completeness limits and remain unsent.

### Acceptance checks for US6

- [X] T070 [P] [US6] Author released-record, draft-request, neutral-interview, privacy, and authorization-boundary contract exercises in tests/test_workflow.py for US6 scenarios 1-4 and SC-008, including incomplete releases, unconfirmed holdings, unknown custodians, and zero external actions. (Depends on T017.)

### Preparation for US6

- [X] T071 [P] [US6] Prepare reports/records/README.md, reports/requests/README.md, and reports/interviews/README.md from contracts/reports.md, distinguishing existing records from new explanations, confirmed holdings from directory leads, firsthand observation from later knowledge, and drafts from submission. (Depends on T017.)

### Implementation for US6

- [X] T072 [US6] Implement records-source completeness/release-context and unsent-draft readiness checks in tools/dossier.py using canonical Source inspection/provenance fields, exact record locators, and owner-only action dependencies; do not add a sender, account connection, or duplicate mutable case register. (Depends on T070, T071, T023.)
- [X] T073 [US6] Search existing agency releases and station/library/broadcast-history/collector holdings for the documented baseline gaps; populate reports/records/inventory.md plus registers/sources.csv and registers/searches.csv with release letters, agency identifiers, pagination, completeness, holding/access confirmation, and barriers, preserving unverified/partial status. (Depends on T072, T038.)
- [X] T074 [US6] For an actionable evidence gap, prepare reports/requests/record-request.md specifying existing complaints/technical analyses/correspondence/logs/disposition records, custodian, identifiers, date range, missing evidence, and how a response could change analysis; verify current agency instructions before any future authorized submission and keep this task's output an unsent draft. (Depends on T073.)
- [X] T075 [US6] Prepare reports/interviews/neutral-guide.md around personal observation, affected monitor/feed, actions, later information/reporting exposure, and verifying records; keep private contact information or uncorroborated allegations in private/ rather than findings, and conduct no interview or outreach. (Depends on T072, T038.)
- [X] T076 [US6] Record any essential owner-only archive access, outreach, travel, or spending decision with dependencies and analytical value in docs/STATUS.md and registers/tasks.csv; confirm holdings/access before proposed travel or paid research and keep independent useful work moving without treating a draft as permission. (Depends on T072.)
- [X] T077 [US6] Run tests/test_workflow.py and the isolated US6 partial-release/request/interview exercise, verifying exact scope and missing-record limitations in reports/records/README.md; no request, message, interview, purchase, or unsupported identity may result from the exercise. (Depends on T075, T076.)

### Integration for US6

- [X] T078 [US6] Integrate completed records/guide/draft products and precise waiting/deferred states in reports/milestones/workstreams.md, docs/STATUS.md, and source T09 records in registers/tasks.csv; keep acquisition/submission and drafting completion separate, and do not check unperformed requests/searches as completed. (Depends on T077.)

**Checkpoint**: Useful drafts and gaps are inspectable; no task sends requests, contacts people, schedules travel, or spends money.

---

## Phase 9: Polish & Cross-Cutting Concerns

**Goal**: Verify the implemented tool and real first delivery, not just checked boxes or an attractive scaffold.

### Implementation

- [X] T079 Run the implemented guide in specs/001-investigation-dossier/quickstart.md and python -m unittest discover -s tests -v against isolated fixtures, checking exact command/path semantics, JSON/exit codes, clean-target restoration, and actual-vs-illustrative gates; update only genuinely changed operator instructions in README.md and docs/DECISIONS.md. (Depends on T027, T049, T059, T069, T078.)
- [X] T080 Review all FR-001 through FR-034 and SC-001 through SC-010 against actual products in reports/milestones/delivery-review.md and reports/milestones/workstreams.md; require the four real baseline products, performed real test/review, all workstream statuses, source aliases/conditions, and honest blocked/deferred states without waiving first-delivery scope. (Depends on T079.)
- [X] T081 Perform a separate cross-output source/reasoning/privacy review in reports/findings/reviews/ and reports/milestones/delivery-review.md, checking exact extracts, source dependence, historical architecture, uncertain clocks/audio, optional novelty/identification, and owner-only external actions; revise and re-review changed findings before freezing final notes, then preserve the review milestone RVW against the fixed delivery-review.md document and relied-on basis. (Depends on T080.)
- [X] T082 Have a fresh reviewer recover the milestone/question, supported findings/confidence, hypothesis changes, gaps/waits, and next three owned actions from saved project files without chat history; record the actual result and remaining limitations in reports/milestones/delivery-review.md and obtain a replacement matching milestone RVW after those edits, before final session closure. (Depends on T081.)
- [X] T083 Update final INVESTIGATION_PLAN.md checkpoints, registers/tasks.csv, docs/STATUS.md, and relevant session metadata with actual outcomes and branch reopening conditions; refresh any milestone review affected by these final document/basis edits before staging, then use tools/dossier.py close-session for the actual final SES ID; confirm final snapshot/receipt and mirrored commit before marking research-session completion. (Depends on T082.)
- [X] T084 Run tools/dossier.py --format json validate --gate delivery --verify-files against the actual dossier and inspect reports/milestones/delivery-review.md plus evidence/metadata/control/ for coherent completion; report the verified result without modifying already-backed-up notes, and require another confirmed snapshot after any subsequent note/register edit. (Depends on T083.)

**Checkpoint**: Real delivery passes current-content gates with separate review and a protected handoff; unavailable conditional deep research remains honestly documented.

---

## Dependencies & Execution Order

### Phase Dependencies

1. Setup T001-T004 precedes shared foundations T005-T017.
2. Foundation T017 unlocks each story's isolated tests and independent guide/seed preparation.
3. US1 record/ingest readiness unlocks real starter mapping; T027's passed foundation review
   unlocks expanded baseline collection. T034 recording discovery need not wait for T032's survey.
4. US2 supplies the real baseline for US3's actual test and US5/US6's justified deeper work.
5. US3's actual reviewed result feeds US4's final reporting; US4 tooling can be implemented while
   that research is waiting. Conditional US5/US6 inputs may feed the selected US3 test.
6. Final validation T079-T084 requires implemented capabilities and honest output states, including
   a performed/reviewed real T046 test. Optional deep research cannot stand in for it.

### User Story Dependencies

| Story | Tooling / independent-test prerequisite | Actual research prerequisite |
| --- | --- | --- |
| US1 | T017; T018 and T019 can be authored together. | Faithful starter registration; real closure requires owner-authorized backup protection. |
| US2 | T017 for tests/templates; T023 before baseline helper integration. | T027 passed foundation review precedes expanded collection; T034 recording discovery can proceed independently of T032. Source/asset dependencies remain explicit. |
| US3 | T017 for tests/guidance; T037 before cycle helper integration. | T038 real baseline, frozen T045 plan, protected inputs, and any selected US5/US6 evidence; then T046-T049. |
| US4 | T017 for tests/guidance; T044 cycle helper before review/readiness integration. | T049 actual reviewed cycle for final report; staged final-byte closure uses shared T015 backend. |
| US5 | T017 for tests/guidance; T023 before media helper integration. | Baseline inventory and a justified question; T068/source T08 requires completed T07 comparison/transcription and required blind review. Preliminary availability work is separate; missing dependencies remain waiting. |
| US6 | T017 for tests/guidance; T023 before records-source checks. | Baseline gaps and confirmed accessible sources/holdings; external contact/spending always remains owner-controlled. |

~~~mermaid
flowchart TD
  S["Setup T001-T004"] --> F["Shared foundations T005-T017"]
  F --> U1["US1 dossier capability and starter mapping"]
  F --> D2["US2-US6 isolated tooling/tests/guides"]
  U1 --> FR["Passed foundation review T027"]
  FR --> B["US2 real baseline T038"]
  B --> CP["US3 frozen cycle plan T045"]
  CP --> A["US3 actual test and review T046-T049"]
  B --> M["US5 justified media/culture work"]
  B --> R["US6 justified records work"]
  M -. "only if needed by selected test" .-> A
  R -. "only if needed by selected test" .-> A
  A --> H["US4 reviewed report and handoff"]
  H --> Q["Final real-delivery checks T079-T084"]
  M --> Q
  R --> Q
  D2 --> Q
~~~

The M/R-to-Q edges require implemented capability and truthful available/waiting/deferred
inventory, not fabricated completion of every conditional research task. If a missing M/R input
is necessary for T046, the selected test remains blocked until supplied or legitimately rescoped
within the bounded question. Missing evidence is never a failed necessary condition by itself.

### Within Each Story

Included acceptance checks precede their implementation. Validate models before integrating
services/CLI commands and validate the increment before declaring its research outcome complete.
All canonical writes use one writer, retained changes, expected hashes, and the shared journal.
Supplied-data exercises make stories independently testable; actual investigation data has the
explicit operational dependencies shown above.

### Parallel Opportunities

- After T001: T002, T003, and T004 write different files and can be authored concurrently.
- After T017: each story's paired marked check/guide/seed tasks can be authored independently.
- Actual queries/read-only review can be coordinated across workstreams, but canonical writes,
  tools/dossier.py changes, and same-file test changes are always serialized.
- Parallel work is an available scheduling option, not a requirement to delegate or create agents.

## Parallel Example: US1

After T017, these two independent authoring tasks can run together:

- T018: Author source/claim/reference and init/ingest/backup/restore command acceptance cases in tests/test_records.py for US1 scenarios 1-6 and SC-008; cover dual firsthand/retrospective status, partial dates, shared lineages, explicit unknowns, idempotent seeds, conflicting IDs, milestone ReviewTarget/retained-copy validation before the foundation review, and fixture-vs-actual separation.
- T019: Curate config/seed-records.json from INVESTIGATION_PLAN.md, recording its hash and all S01-S07/H1-H7/T01-T11 aliases, exact locators/inspection limits, hypothesis scopes/distinguishing tests, owners, priorities, dependencies, outputs, completion conditions, and timeboxes; keep hypotheses untested and tasks queued without inventing inspected media or completed research.

Finish the listed check/preparation prerequisites before the story's implementation. Do not run
same-file helper/test edits or actual register updates concurrently.

## Parallel Example: US2

After T017, these two independent authoring tasks can run together:

- T029: Author chronology and baseline-output contract exercises in tests/test_workflow.py for US2 scenarios 1-4: reported 25/30-second differences, event phases, unknown offsets, distinct reception paths, source retrieval limits, and real-vs-unexamined seed baselines.
- T030: Prepare clearly unfilled output structures in analysis/chronology/source-map.md, analysis/chronology/timeline.md, analysis/chronology/contradictions.md, analysis/media-comparison/recording-inventory.md, analysis/engineering/signal-paths.md, and analysis/engineering/assumptions.md from contracts/reports.md; do not label scaffolds completed research.

Finish the listed check/preparation prerequisites before the story's implementation. Do not run
same-file helper/test edits or actual register updates concurrently.

## Parallel Example: US3

After T017, these two independent authoring tasks can run together:

- T039: Author cycle/start-analysis/exclusion contract cases in tests/test_workflow.py for late searches, altered frozen predictions, missing original protection, unfounded ruled_out states, changed assumptions/reopening, and coherent actual-versus-illustrative cycle readiness.
- T040: Document question scoping, H1-H3 entry-point alternatives versus coexisting H4-H7 questions, necessary conditions, predictions, timeboxes, and raw-observation/reversal-evidence conventions in analysis/cycles/README.md; include no invented actual result.

Finish the listed check/preparation prerequisites before the story's implementation. Do not run
same-file helper/test edits or actual register updates concurrently.

## Parallel Example: US4

After T017, these two independent authoring tasks can run together:

- T050: Author review/report/handoff/delivery contract exercises in tests/test_workflow.py for reverse review lookup without target edits, milestone document targets and retained copies, rejected mismatched hashes or missing basis, changed cited bases versus unrelated edits, owner/reviewer context, missing specialist/blind review limits, fixture rejection, metadata-only blocking, and final-byte closure coherence.
- T051: Prepare reports/findings/README.md and reports/milestones/README.md from contracts/reports.md, specifying finding fields, exact reviewed revisions, milestone ReviewTarget/basis copies, privacy checks, all-five-workstream output inventory, four milestone decisions, next actions, and the difference between local shareable readiness and publication.

Finish the listed check/preparation prerequisites before the story's implementation. Do not run
same-file helper/test edits or actual register updates concurrently.

## Parallel Example: US5

After T017, these two independent authoring tasks can run together:

- T060: Author media/reference record and output contract exercises in tests/test_records.py for multi-input lineage, shared damage, lost timing/interlacing, uncertain wording, blind-review absence, extraction checks, period dates, widespread availability, and generative-detail exclusion.
- T061: Document conservative processing, complete capture histories, side-by-side originals, required versions/arguments/stream/time-base manifests, blind transcription, and dated cultural-context rules in analysis/media-comparison/README.md and analysis/culture/README.md; make media executables conditional rather than mandatory dependencies.

Finish the listed check/preparation prerequisites before the story's implementation. Do not run
same-file helper/test edits or actual register updates concurrently.

## Parallel Example: US6

After T017, these two independent authoring tasks can run together:

- T070: Author released-record, draft-request, neutral-interview, privacy, and authorization-boundary contract exercises in tests/test_workflow.py for US6 scenarios 1-4 and SC-008, including incomplete releases, unconfirmed holdings, unknown custodians, and zero external actions.
- T071: Prepare reports/records/README.md, reports/requests/README.md, and reports/interviews/README.md from contracts/reports.md, distinguishing existing records from new explanations, confirmed holdings from directory leads, firsthand observation from later knowledge, and drafts from submission.

Finish the listed check/preparation prerequisites before the story's implementation. Do not run
same-file helper/test edits or actual register updates concurrently.

## Requirement and Acceptance Coverage

The source clauses remain normative; task quotes preserve their constraints with line wrapping
collapsed only for checklist readability.

| Requirement | Tasks |
| --- | --- |
| FR-001 | T001, T020, T024 |
| FR-002 | T006, T007, T008, T009, T010, T023 |
| FR-003 | T011, T019, T020, T026 |
| FR-004 | T008, T023, T047 |
| FR-005 | T008, T047, T053 |
| FR-006 | T007, T011, T026, T033, T062 |
| FR-007 | T010, T014, T021, T022 |
| FR-008 | T010, T062, T063, T066 |
| FR-009 | T007, T032, T073 |
| FR-010 | T008, T031, T035 |
| FR-011 | T030, T033, T034, T036, T038 |
| FR-012 | T036, T045, T046 |
| FR-013 | T034, T062, T065, T066 |
| FR-014 | T011, T052, T048, T067, T081 |
| FR-015 | T064, T068 |
| FR-016 | T041, T043, T045, T046 |
| FR-017 | T009, T042, T047 |
| FR-018 | T012, T042, T047, T054 |
| FR-019 | T010, T052, T056 |
| FR-020 | T048, T052, T058, T081 |
| FR-021 | T053, T057 |
| FR-022 | T015, T024, T054, T059, T082, T083 |
| FR-023 | T009, T012, T019, T054 |
| FR-024 | T027, T032, T037, T038, T049, T080, T084 |
| FR-025 | T072, T073 |
| FR-026 | T074, T075 |
| FR-027 | T003, T076, T077 |
| FR-028 | T003, T053, T058, T081 |
| FR-029 | T003, T053, T047 |
| FR-030 | T002, T013, T014, T015, T025, T028, T083 |
| FR-031 | T056, T080, T084 |
| FR-032 | T054, T059, T076, T083 |
| FR-033 | T032 |
| FR-034 | T054, T069, T078, T080 |

| Measurable outcome | Tasks |
| --- | --- |
| SC-001 | T019, T027 |
| SC-002 | T017, T021, T022, T023, T028, T083 |
| SC-003 | T048, T052, T056, T058, T081 |
| SC-004 | T032, T033, T034, T035, T036, T038 |
| SC-005 | T041, T045, T046, T047, T048, T049 |
| SC-006 | T054, T059, T082, T083 |
| SC-007 | T060, T065, T066, T067, T068, T069 |
| SC-008 | T018, T029, T050, T070, T077 |
| SC-009 | T038, T049, T059, T080, T083 |
| SC-010 | T054, T069, T078, T080 |

### Source Backlog Preservation

The investigation plan's T01-T11 aliases are not renumbered to match implementation checkboxes.
They remain TASK-0001 through TASK-0011 in the actual register with their original owners,
dependencies, conditions, and timeboxes. This table traces their work without declaring it done.

| Source task | Implementation / actual-research coverage |
| --- | --- |
| T01 | T001, T020, T024, T027, T028 |
| T02 | T019, T026, T033 |
| T03 | T032 |
| T04 | T034, T065 |
| T05 | T035 |
| T06 | T036 |
| T07 | T066, T067 |
| T08 | T068 |
| T09 | T073, T074, T075, T076 |
| T10 | T045, T046, T047 |
| T11 | T048, T056, T057, T058, T059, T080, T081, T082, T083, T084 |

### Constraint Ownership

| Data-model / contract constraint group | Implementing tasks |
| --- | --- |
| Required headers, common fields, unknowns, strict CSV/JSON types | T006-T010 |
| Source/date/inspection axes and search chronology | T007, T026-T027, T031-T032 |
| Claims, timeline phases, precision, confidence, evidence locators | T008, T011, T023, T035 |
| Hypothesis/task enums, transitions, exclusions, reopening conditions | T009, T042, T047, T054 |
| Sidecar required/conditional fields, derivative and recovery relationships | T010, T014-T015, T021-T022, T041, T052, T062 |
| Monotonic unique identity, aliases, graph/reference constraints | T011-T012, T019-T020 |
| Storage boundaries, current-byte protection, receipt and closure guards | T013-T017, T023, T025, T028, T043, T055, T059, T083-T084 |
| Immutable pre-search plan, actual method/result and separate review | T041-T049, T052, T058 |
| Audience, novelty, privacy, reviewer identity, and handoff readiness | T011, T027, T038, T049-T059, T075-T076, T080-T084 |

## Implementation Strategy

### MVP First: US1 Foundation Increment

Complete T001-T028 as the first independently demonstrable increment: a portable six-register
dossier with faithful source/hypothesis/task seeds, explicit uncertainty, preserved acquired
bytes, verified protection/recovery behavior, and resumable state. This is a foundation MVP,
not the owner's agreed first delivery. Do not stop the authorized run there merely because the
fixture tests pass.

### Incremental Delivery

1. Implement shared preservation and record mechanics before actual research needs them.
2. Demonstrate US1 and establish the real source baseline through US2.
3. Implement US3/US4 research and review readiness, then choose and perform the real bounded test.
4. Use US5/US6 capabilities when they provide distinguishing evidence; run those conditional
   branches before T046 when needed, without manufacturing archive/listener availability.
5. Keep separate reviews, living-plan updates, per-session protection, and owned next actions
   current throughout. Ordinary reviews are progress checkpoints, not new permission gates.
6. Finish T079-T084 against the actual dossier. If the real test, essential review, or backup
   cannot be completed, preserve the blocker and report incomplete first delivery truthfully.

### Parallel Team Strategy

Parallelize only the marked independent authoring work after its dependencies. Assign one writer
for canonical records and one active editor for tools/dossier.py and each test file. Review can
use another actual reviewer, with its identity and inspected evidence recorded; agreement is not
independent factual corroboration. No task requires concurrent agents or a multi-user service.

## Notes

- This file creates future tasks only. All 84 checkboxes start unchecked.
- The six source registers and their stable IDs remain the underlying evidence collection.
- Leave conditional unperformed work unchecked and named waiting/deferred; preserve negative
  searches, superseded conclusions, extraction limits, and branch reopening conditions.
- Never bypass production protection with an illustrative same-volume copy or metadata-only pass.
- No new historical conclusion, participant identity, source authenticity, or milestone completion
  follows merely from generating tasks or implementing the validator.
- Paths naming CYC-0001/FND-0001/RVW-0001 describe the first legitimately allocated records. If already occupied, use the next valid ID, update all references coherently, and preserve the existing research.
- The implementation phase follows this backlog; task generation does not execute its actions.
