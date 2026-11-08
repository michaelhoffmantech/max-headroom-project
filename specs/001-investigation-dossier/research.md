# Design Research: Investigation Dossier

Date: 2026-11-06. Inputs: [specification](spec.md), [investigation plan](../../INVESTIGATION_PLAN.md),
and [constitution](../../.specify/memory/constitution.md). This is implementation-design research;
it does not acquire incident evidence or establish historical findings.

## R1. Portable dossier and a small integrity tool

- **Decision:** Use Markdown narratives, the six CSV registers named in the investigation plan,
  JSON metadata sidecars, and Python 3.13 standard-library tools. The available interpreter is
  Python 3.13.12. Implement one local command entry point, `tools/dossier.py`, for repeated schema,
  provenance, revision, backup, and completion checks. Do not build a dashboard or service.
- **Rationale:** The repetitive question is whether evidence and saved state satisfy the recorded
  research rules. Small tools answer that question while the dossier remains readable directly.
- **Alternatives considered:** A database, web application, general research platform, or mandatory
  notebook stack adds inspection and maintenance work before a navigational problem exists.
  Manual inspection alone cannot reliably detect changed bytes and dangling relationships.

## R2. Six canonical registers with explicit collections

- **Decision:** Keep one canonical current row per record in the six CSV files. Use scalar cells
  for single values and designated `_json` cells for arrays or objects. JSON sidecars own asset,
  cycle, finding, review, session, and backup details; CSV and Markdown refer to those records.
  The exact boundaries are defined in [data-model.md](data-model.md).
- **Rationale:** This supports multiple parents, evidence locations, contradictions, and task
  dependencies without inventing an ambiguous delimiter or another relationship register.
  Python CSV normally reads strings, permits short/extra rows through DictReader behavior, and
  writes None as an irreversible empty string. The implementation must therefore check header
  uniqueness, row width, types, and unknown markers explicitly. See the
  [Python 3.13 CSV documentation](https://docs.python.org/3.13/library/csv.html).
- **Alternatives considered:** JSON-only registers obscure the plan's tabular workflow. Separate
  link tables are valid but add maintained artifacts. Supporting both link representations
  would create two possible accounts of the same relationship.

## R3. Explicit unknowns and strict parsing

- **Decision:** Use `unknown` for an unknown CSV scalar and `not_applicable` only where the schema
  permits it. Explain unknowns in `unknowns_json`. JSON uses null plus an unknown-reason entry for
  unknown scalar values. Empty collections mean no items currently recorded, never proof of
  historical absence. Preserve the specified confidence, hypothesis, and task vocabularies.
  Reject duplicate JSON keys, non-finite numbers, malformed collection shapes, and CSV columns
  not defined by schema version 1.
- **Rationale:** Defaults must not manufacture precision or evidence. Python JSON decoding needs
  explicit configuration to reject duplicate names and non-finite values; consult its
  [documented behavior](https://docs.python.org/3.13/library/json.html).
- **Alternatives considered:** Blank required cells, implicit booleans, delimiter-separated lists,
  or automatic category guesses lose the distinctions the investigation requires.

## R4. Stable identity and retained changes

- **Decision:** Allocate monotonically increasing IDs per documented prefix; never reuse or
  renumber an allocated ID. Preserve S01-S07, H1-H7, and T01-T11 aliases. Use one writer lock for
  dataset mutations. Apply changes from a change-set that states expected previous revisions and
  hashes, actor, reason, and proposed values. Retain prior/new values in immutable change records.
  Acquire bytes separately from this mutable-record mechanism.
- **Rationale:** This prevents silent overwrites, lost exclusions, and accidental reassignment of
  historical citations. A different ID or checksum does not establish source independence.
- **Alternatives considered:** Last-writer-wins editing loses history. Git may be useful later but
  is not sufficient record-level provenance and is not installed as a repository by this plan.
  Concurrent multi-user editing would require a larger coordination mechanism.

## R5. File publication and interrupted work

- **Decision:** Write each mutable file through a temporary file in its own directory, then
  replace it after validating the expected prior hash. Multi-file changes use a journal with
  staged outputs and expected hashes. An interrupted publication is `recovery_required`, not a
  successful update. Recovery may finish only the journaled outputs; it never rewrites originals.
- **Rationale:** A file replacement is not a transaction covering a set of CSV and JSON files.
  Cross-filesystem replacement can fail; keep staging on the destination filesystem. See
  [os.replace](https://docs.python.org/3.13/library/os.html#os.replace).
  Immutable CHG records retain proposed/prior values; mutable publication/recovery state is a
  separate control journal, mirrored outside the frozen backup payload.
- **Alternatives considered:** Treating several writes as atomic or silently rolling back evidence
  files can create a mixed account. A database transaction is unnecessary for the single-writer
  first delivery when interrupted states are explicit and recoverable.

## R6. Storage roots are explicit operational configuration

- **Decision:** Configure local absolute paths for `project`, `primary_evidence`, and `backup`
  roots. Persistent evidence references use a storage alias plus relative path. The default
  primary evidence root can be `evidence/originals/` in the active workspace; large media can use
  an explicitly configured external root. The owner supplies an authorized backup destination
  and its failure-domain description. An unset backup root remains a runtime prerequisite.
- **Rationale:** No production backup location is known. Do not invent a drive, provision cloud
  storage, move the project, or label a same-volume temporary copy independent protection.
  Allow the default primary root inside project; reject backup overlap with either protected
  root and reject identical source/destination objects. Check local volumes where
  observable, but do not pretend automatic checks prove a remote service's failure domain.
- **Alternatives considered:** Hard-coded absolute paths leak private details and impede moving
  the dossier. A `work/` copy is suitable only for explicitly illustrative backup tests.

## R7. Backup confirmation binds exact content

- **Decision:** Preserve originals unchanged, compute SHA-256 and byte count at ingest, and
  confirm a separate backup object by reading and matching its content. An immutable receipt
  records covered paths, hashes, sizes, storage aliases, verification time, and limitations.
  Analysis requires a confirmed receipt matching the current original. Hash mismatches preserve
  expected values and prior receipts, block affected analysis, and create a discrepancy record.
- **Rationale:** Existence and modification time do not prove that the required bytes were copied.
  Hashes prove integrity, not authenticity. Python supports streaming file hashing through
  [hashlib](https://docs.python.org/3.13/library/hashlib.html#file-hashing).
  File-copy functions do not preserve every filesystem attribute, so acquisition metadata must
  be recorded explicitly; see [shutil limitations](https://docs.python.org/3.13/library/shutil.html).
- **Alternatives considered:** File-size-only checks, overwriting a previous backup, automatic
  repair of originals, and claims of a forensic filesystem clone are rejected.

## R8. Close sessions without invalidating the backup

- **Decision:** Session close holds the writer lock, stages the final handoff and session record,
  freezes the complete notes/register snapshot, copies and verifies that exact final snapshot,
  stores the receipt in both locations, and only then publishes the already-backed-up final
  handoff/session payload. Effective completion and actual completion time belong to the separate
  mirrored control journal, not a later edit of backed-up Session bytes. The journal makes an
  interrupted publication recoverable. Manifests and receipts exclude their own self-hashes;
  their copies and the mutable control journal are preserved separately.
- **Rationale:** Editing STATUS.md after backing it up would leave the completed handoff outside
  the confirmed snapshot. The confirmation must cover final bytes, not an earlier draft.
- **Alternatives considered:** A timestamp-only confirmation or a completed flag written before
  verification would misstate the user's backup checkpoint.
- **Failure behavior:** Missing destination, modified snapshot inputs, copy failure, or failed
  verification leaves closure pending. Continue independent useful work under the agreed
  autonomy rule; do not mark the affected session complete.

## R9. Media tools remain conditional

- **Decision:** FFmpeg/ffprobe are optional dependencies for a specifically justified media task.
  Neither executable was found during planning. Record exact versions, full arguments, stream
  selection, time-base interpretation, input/output hashes, and rationale when used. Preserve
  interlacing and timing present in acquired material; transformations produce new assets.
- **Rationale:** Source discovery, chronology, and document-based tests can proceed without an
  installed media suite. [FFprobe](https://ffmpeg.org/ffprobe.html) can produce JSON stream/format
  reports when needed. [FFmpeg streamcopy](https://ffmpeg.org/ffmpeg.html#Streamcopy) avoids
  decoding/encoding but still produces a derivative container rather than an unchanged file.
- **Alternatives considered:** Installing a mandatory suite before a question needs it, default
  deinterlacing, frame-rate conversion, cropping, audio normalization, or generative enhancement
  would add work or alter clues prematurely. Missing tools block only their dependent task.

## R10. Historical times stay separate from workflow timestamps

- **Decision:** Use offset-aware ISO timestamps for workflow actions. Keep reported local event
  times, intervals, clock sources, precision, timezone labels, and UTC offsets as separate fields;
  an unknown historical offset stays unknown. Mandatory validation does not require IANA timezone
  data or infer a 1987 offset from current facilities or the host timezone.
- **Rationale:** Python distinguishes aware from naive datetimes, and Windows may not provide
  IANA timezone data. See [datetime](https://docs.python.org/3.13/library/datetime.html) and
  [zoneinfo data availability](https://docs.python.org/3.13/library/zoneinfo.html).
- **Alternatives considered:** Converting every statement immediately into one exact UTC instant
  would hide contradictory clocks and unsupported precision.

## R11. Separate review and truthful validation

- **Decision:** Record actual author/reviewer identities and types, review time, findings,
  specialist needs, and decision. A separate AI reasoning review can clear ordinary structural
  and reasoning questions; it is not factual corroboration. Routine reviews do not impose an
  owner-approval pause. Disputed audio still needs blind second transcription, and unresolved
  expert questions retain their limits.
- **Rationale:** Automated checks can establish structure, links, timestamps, and integrity;
  they cannot authenticate a source or judge historical truth. Review remains evidence-based.
- **Alternatives considered:** Counting self-checks as a separate reviewer, counting AI agreement
  as evidence, or requiring owner approval of every routine cycle conflicts with the spec.
  Resolve review attachments by reverse lookup from ReviewTarget: record ID/revision for record
  reviews, or milestone document path/hash with retained document/basis copies for milestone
  reviews. Do not mutate the reviewed claim/finding or narrative merely to attach the reviewer
  decision. Changed reviewed content/basis requires a new review for current readiness; preserved
  passing snapshots still establish historical milestone order.

## R12. Meaningful checks and actual delivery

- **Decision:** Use focused standard-library unittest cases and isolated illustrative fixtures
  for corruption, missing links, invalid exclusions, stale writes, and backup interruption.
  Fixture workspaces carry `dataset_role=illustrative` and cannot pass actual delivery acceptance.
  The real delivery requires real sources, the four baseline products, and one actual bounded
  test plus separate review. [unittest](https://docs.python.org/3.13/library/unittest.html) is
  sufficient for these checks.
- **Rationale:** A working validator and an attractive dossier scaffold do not satisfy the
  research outcome the owner selected.
- **Alternatives considered:** Treating synthetic examples as research completion or generating
  tests that only mirror field assignments would provide misleading assurance.

All design decisions needed for Phase 1 are resolved. The authorized production backup root,
external archive access, media tools when needed, blind listening, and specialist availability
are explicit operational dependencies, not unanswered architecture decisions.

Design review refinements: actual cycle/delivery readiness requires current byte/receipt checks;
metadata-only checks cannot assert protection. Derivatives retain all input source lineages.
Restore creates an explicit recovery_copy at a clean location, distinct from journal recovery.
Frozen cycle plan content is hashed and retained so later predictions cannot be backdated.

Implementation update, 2026-11-07: the owner selected public GitHub version control for tooling
and a separate private C: directory for backups. This overrides the earlier no-Git setup choice
and permits explicitly owner-selected same-volume copies with a recorded drive-loss limitation.
Research data and reports stay outside public commits; a local copy is never described as
independent-volume protection.
