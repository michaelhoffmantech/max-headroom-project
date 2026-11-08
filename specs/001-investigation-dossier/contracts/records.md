# Records and Storage Contract

Version 1. Applies to the six register schemas and sidecars in
[data-model.md](../data-model.md). This is a proposed interchange contract, not implemented code.

## Serialization

- CSV: UTF-8 without BOM on canonical writes; comma delimiter; double-quote quoting; escaped
  double quotes per the standard CSV writer; LF line endings; Python files opened with
  newline=''. Header order is the common fields followed by the entity's declared field list.
- Reject duplicate/missing/extra headers, short/long rows, malformed quoting, duplicate IDs,
  invalid enums, and mismatched types. Do not let DictReader silently hide width errors.
- JSON: UTF-8, schema_version 1, LF termination, finite numbers, unique object keys, and types
  matching the declared shape. Canonical writes sort object keys for stable diffs; array order
  is preserved. SHA-256 always covers actual saved bytes, not a reparsed equivalent.
- Collection cells carry JSON, not semicolon-separated strings. `_json` can denote an array or
  an explicitly documented object. No arbitrary evaluation or source-provided instructions.
- CSV booleans are true/false. Unknown required scalars are `unknown`, with a reason in
  unknowns_json. Use `not_applicable` only for a genuinely inapplicable field with an explanation.
  Do not serialize Python None as a blank cell. JSON unknowns use null plus the unknowns map.
- An empty array means no entries currently recorded. It neither proves absence nor removes
  the requirement to record an unestablished lineage, incomplete search, or unresolved caveat.
- Workflow timestamps include UTC offset or Z. Historical statements retain their own precision
  and unknown offset. Source date precision permits YYYY, YYYY-MM, YYYY-MM-DD, or a documented
  interval; do not pad an approximate date with invented components.

## Reusable shapes

Collection fields have fixed shapes: fields ending _ids_json contain arrays of ID strings;
legacy_aliases_json contains alias strings; supporting_evidence_json/contradicting_evidence_json
contain EvidenceRef objects; dependencies_json contains RecordRef objects. known_edits_json,
caveats_json, unsuccessful_results_json, and access_barriers_json contain descriptive strings.
unknowns_json maps field names to nonempty reasons. filters_json is an object of filter names to
string or string-array values. Other structured cells follow their entity-specific definitions
below and in the data model; JSON syntax alone does not establish a valid collection shape.

### RecordRef

An object with id, revision when referring to a fixed reviewed version, and optional note. Every
ID resolves to a current record or preserved retired/revision record. A current readiness check
flags a reviewed finding whose cited basis changed; it does not rewrite historical reports.

### EvidenceRef

Required: source_id, locator, role, and limits. Optional: asset_id, claim_id, and source_revision.
role describes what the source supports or contradicts; it does not change the claim category.

locator contains kind page/time/frame/paragraph/section/line/archive_unit/other, exact value or
range, precision, and contextual description. A time/frame locator identifies its recording asset
and time base, or explicitly records the uncertainty. An exact URL alone is insufficient when a
page, passage, time, or frame is needed to inspect the cited detail. A source not acquired locally
can still have a precise source locator and access caveat; do not fabricate an asset or checksum.
The locator's contextual text key is description. A time/frame citation supplies EvidenceRef.asset_id
and locator.time_base, or a nonempty locator.uncertainty explaining why that basis is unavailable.

Derivative processing manifests use method, executable, tool_version, arguments, settings,
time_base, stream_notes, and output_sha256. They retain every input relationship. Optional boolean
flags generative and claimed_as_recovered_evidence make the enhancement boundary explicit: generated
detail cannot be promoted as recovered evidence. These flags do not replace human source review.

### StorageRef

An object with alias, relative_path, and access_limit. Aliases resolve through local root
configuration. Relative paths must remain inside the resolved root; reject traversal and
unapproved symbolic links/junctions. Do not put private absolute paths into shareable reports.

### ReviewTarget

Every RVW has one tagged target object:

- For extraction, finding, blind_transcription, or specialist reviews: kind record, id, and
  revision. The ID/revision must resolve to an existing retained record. Preserve the reviewed
  evidence/narrative hashes alongside this target.
- For milestone reviews: kind milestone_document, milestone, document, sha256, byte_count,
  reviewed_copy, basis_records, and basis_files. milestone is foundation, baseline,
  analytical_cycle, or review. document and reviewed_copy are StorageRef objects with alias
  project. document is under reports/milestones/; reviewed_copy is an immutable copy under
  reports/findings/reviews/artifacts/RVW-ID/. Both must match the recorded SHA-256 and byte count
  when the review is created. This target uses content identity rather than an invented record ID
  or document revision. basis_records is an array of RecordRef objects with required revisions;
  basis_files is an array of objects with file (StorageRef), sha256, byte_count, and reviewed_copy
  (StorageRef under the same RVW artifact directory) for other outputs the decision relies on.
  Every retained copy must match its stated hash/size; paths must be unique within the review.
  Record the complete relied-on basis, without self-referencing
  the RVW, its copy, or a mutable control journal.

Retain reviewed document/basis copies and basis revisions in session preservation. apply stages
the copies with the new milestone RVW under the writer lock, checking expected input hashes and
never overwriting an existing copy; a mismatch aborts publication. Reverse lookup matches a
milestone review by milestone, document path, content hash, and basis. A changed target or relied-on
basis makes the review historical and requires a new review for current readiness. Unrelated
dataset edits do not invalidate it. Never edit a reviewed document merely to attach its RVW ID.
Sequencing gates use retained passing milestone snapshots and review times. Later legitimate
research does not retroactively undo a passed historical gate; presenting a revised milestone
as current requires a matching new review.

### Source inspection and account status

inspection_json has text, linked_media, underlying_records, and limits. Each scope describes
what was actually read/inspected/verified or remains uninspected/unknown; source retrieval alone
does not fill every scope as verified.

account_status_json has firsthand, retrospective, and limits. The two status fields use
yes/no/mixed/unknown/not_applicable independently. A firsthand retrospective interview can have
both fields yes. Do not flatten two axes into a single exclusive category.

date_precision_json describes publication_date and event_date precision, interval endpoints
where applicable, and supporting basis. An unknown day does not erase a documented year.

### Records research and unsent outputs

Source inspection_json may contain records_context. This is evidence-handling context for the
same Source row, not another register or an automatic authenticity decision:

- kind agency_release requires agency_identifiers (string array), release_letter_evidence
  (EvidenceRef array), pagination, and authentication_limits (nonblank descriptions). Empty
  identifier/evidence arrays and unknown pagination need reasons in records_context.unknowns.
  Missing context produces records_context_gap; partial/unknown completeness remains visible.
  The Source.completeness column remains the sole current completeness value.
- kind holding requires institution, holding_identifier, access_status (unconfirmed or
  confirmed), confirmation_evidence (EvidenceRef array), and limits. Unknown descriptions carry
  reasons in records_context.unknowns. Confirmed access requires actual cited confirmation
  evidence; a directory lead stays unconfirmed. Typed evidence resolves to existing sources and
  retained revisions. Structural validity never establishes that a holding exists.

Task output_refs_json may contain typed objects alongside ordinary output paths. A request_draft
or interview_guide object requires kind, file (StorageRef), sha256, and status unsent. This binds
local output bytes without authorizing any external action. File paths are containment-checked
on mutation; --verify-files also checks the current SHA-256, failing changed or missing bytes.

request_draft additionally requires records_requested (nonempty existing-record descriptions),
custodian, date_range, analytical_gap, and analytical_value. Unknown descriptions need output.unknowns
reasons and produce draft_dependency gaps. An unresolved required description cannot complete
the draft's Task. interview_guide requires prompts with nonblank personal_observation,
affected_feed, actions_taken, later_information, and verifying_records questions. These checks
validate declared scope and provenance, while separate review assesses neutrality, privacy, and
whether the prose actually supports the declarations. No field sends a request or conducts an interview.

### Cycle predictions and exclusions

necessary_conditions_json and predictions_json contain explicit descriptions, expected
observations, supporting references where known, and limits. exclusion_json for ruled_out
contains failed_condition, evidence_refs, assumptions, and exclusion_scope. A missing file or
unsuccessful query is a gap, never an automatic failed historical condition.

The cycle's frozen plan payload and hash are immutable after freeze. System-recorded freeze and
new-search/test timestamps establish ordering. Result updates do not alter the plan payload;
later predictions are exploratory amendments or a new cycle, never backdated replacements.

Cycle.required_tools is an optional list of executable strings or objects with executable,
optional expected_version, and arguments (literal analysis argument strings). start-analysis
resolves each declared executable, invokes only its fixed version flag (-version for ffmpeg/
ffprobe, otherwise --version) with shell disabled and a timeout, and blocks missing, failed, or
mismatched versions before recording an analysis start. It never executes the declared analysis
arguments during preflight. Metadata-only validation does not invoke executables.

Successful start-analysis records a command-owned analysis_tool_manifest containing executable,
resolved_path, reported version/version_output, declared arguments, probe_command, and checked_at.
This accompanies the command-owned analysis_input_manifest. Generic apply cannot create or alter
either manifest or the analysis-start timestamp. An empty tool manifest means this cycle declared
no executable dependency; it does not imply that absent media tools were used.

### Change-set

A change-set file has schema_version, actor, reason, expected_dataset_manifest, and operations.
Each operation states create/update/retire, entity_type, id, expected_revision/hash for existing
records, and proposed field values. Proposed new IDs must be the next unused values checked under
the lock. Return a conflict if another writer allocated them first; never silently renumber links.
References must resolve after the proposed change-set. A retirement retains its row and reason.
Reopening a ruled_out hypothesis supplies an operation-level reopening object with
new_evidence_refs (EvidenceRef array) or changed_assumption (nonempty explanation). Retain this
decision context with prior/proposed values; a generic edit reason alone cannot reopen an exclusion.

Record RVW decisions are accepted, accepted_with_limits, revise, or rejected. Milestone decisions
also allow continue, narrow, wait, assign_research, or close_branch. Blank or arbitrary decisions
cannot clear readiness. A passing foundation gate requires accepted, accepted_with_limits,
continue, or narrow; an unresolved waiting decision does not unlock expanded collection.

Reviews use ReviewTarget to bind record revisions or fixed milestone documents and their basis.
Resolve reviews and
readiness by reverse lookup from RVW records; do not change the reviewed claim/finding or append
to its narrative merely to attach a review decision. This prevents a bookkeeping change from
invalidating the very revision just reviewed. Actual content/evidence changes require re-review.

The helper preserves original/proposed revisions in CHG metadata, stages complete replacement
files, validates the proposed dataset, and publishes only after expected hashes still match.
The retained CHG file manifest excludes its own self-hash; the outer backup snapshot hashes the
already-frozen CHG bytes normally.
Unexpected manual edits are conflicts requiring reconciliation, not opportunities to invent the
lost previous values. Editing narratives directly is allowed, but revised reviewed findings
must be re-reviewed and every final note/register byte must enter the session snapshot.

## Local configuration

config/dossier.json declares schema_version, dataset_role actual/illustrative, and configured
entity locations. It contains no secrets. config/storage.local.json supplies absolute project,
primary_evidence, and backup roots plus owner-described backup failure domain and access limits.
An unset backup value is an explicit operational prerequisite, not a guessed path.

The default primary_evidence root may be contained within project. This intended containment is
allowed. Reject source/destination identity and any backup-root overlap with project or primary
evidence roots. A same-volume temporary copy
can be an illustrative test only; it cannot be described as protection against losing that
volume. Prefer a distinct volume/root for production local protection. The owner's 2026-11-07
selection of a separate C: backup directory permits owner_selected_same_volume: true with an
explicit limitation: verified separate copies protect against accidental changes, not loss of C:.
Never label that arrangement independent-volume protection. Reject overlapping roots regardless;
for remote storage, require the owner's failure-domain description rather than pretending the
path reveals the provider's infrastructure. Permission/access to a location is still required.

No command provisions storage, connects an account, initializes Git, publishes, sends a message,
files a records request, or spends money. Actual network discovery is conducted separately with
available research tools and registered afterward.

## Backup manifest and receipt

The snapshot manifest lists each covered source reference, intended final relative path,
byte_count, and sha256, plus snapshot ID, asset/session IDs, and creation time. For closure it
includes final staged handoff/session files and every final note/register needed by that session.
Coverage must also preserve derivative inputs/outputs needed to reproduce reported analyses.

Immutable CHG records can be in this payload; mutable publication/recovery control journals
cannot. Keep journals in evidence/metadata/control/ and separately mirror them to backup control
storage. Record actual publication/completion timestamps there without editing a confirmed
Session payload. Its intended_state/receipt reference becomes effective only when the journal,
receipt, and final hashes agree. Failure to preserve the mirrored commit remains recovery_required.

A BAK receipt contains scope original/session, covered IDs, storage aliases, failure-domain
description, exact manifest, attempt and verification times, method/tool version, result, and
failure/limitation details. Publish confirmed only after comparing every destination file with
the manifest. Keep matching receipt/manifest copies in primary metadata and backup storage.
Neither hashes itself; receipts are stored separately from the set whose hashes they attest.

Closed confirmations are immutable. Failed attempts retain their failure record; retries create
new IDs. A receipt cannot be repurposed to cover later file edits. Recovery copies retain their
relationship and verification evidence without changing an original's expected checksum.

A recovery copy uses Asset.kind recovery_copy, recovery_of_asset_id, and backup_receipt_id at a
new clean location. A derivative instead has all input asset IDs, no arbitrary singular source_id,
and source lineage derived from those inputs. Neither operation erases acquisition history.

## Validation severity

| Class | Examples | Consequence |
| --- | --- | --- |
| Invalid | Malformed schema, unresolved ID, lineage cycle, missing exclusion evidence, invalid enum. | Reject the mutation or acceptance check. |
| Conflict | Unexpected prior hash/revision, another writer, incomplete publication journal. | Stop that mutation; reconcile or finish the recorded journal. |
| Blocked | Missing authorized backup root, pending backup, required blind review/tool/input unavailable. | Block dependent analysis, closure, or readiness; continue unrelated authorized work. |
| Integrity failure | Original or backup bytes fail their expected hash/size. | Preserve prior records; reject affected eligibility and record the discrepancy. |
| Evidence gap | Unavailable archive, uncertain clock, unknown historical component, unsuccessful search. | Retain explicit limits; baseline can remain valid with the documented gap. |

The validator never changes confidence, authenticates material, repairs originals, converts an
unknown into a negative conclusion, or decides a person's involvement. Reviewers evaluate those
claims from inspectable evidence within the investigation standards.

Metadata-only validation reports structure_only/not_evaluated readiness. Actual cycle/delivery
readiness requires current source/backup byte checks and exact receipt coverage; omission of
verification is a blocker, not an implied pass.
