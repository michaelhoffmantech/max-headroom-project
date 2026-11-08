# Local Dossier Command Contract

Version 1. Proposed executable: tools/dossier.py, implemented later. Commands run from the project
root with Python 3.13. Global options precede the command:

```text
python tools/dossier.py --root . --format json COMMAND ...
```

--root defaults to the current project; --format is text or json, default text. Paths supplied
by callers are validated against their declared root and access context. Storage configuration,
record schemas, and mutation rules are defined in [records.md](records.md) and
[data-model.md](../data-model.md).

--root selects the dataset/write root. Relative input arguments --seeds, --change-set, --metadata,
--handoff, and --file resolve from the invocation working directory, not from --root. Persisted
locations are converted to StorageRef values. The output argument --into for restore-asset is
relative to configured primary_evidence unless absolute, and must remain inside that root.

## Commands

| Command | Inputs | Behavior / result |
| --- | --- | --- |
| init | --seeds config/seed-records.json; --dataset-role actual or illustrative | Create the proposed dossier structure and six register headers, then faithfully seed the plan's aliases and metadata. Record seed provenance/hash. Idempotent for matching state; conflicting existing records fail without overwriting research. Never claims acquisition, authentication, or completed tasks. |
| apply | --change-set PATH | Check expected hashes/revisions, allocate/verify proposed new IDs under the writer lock, retain changes, validate references, and publish journaled current records. New milestone RVWs stage immutable document/basis copies according to ReviewTarget under the same lock; missing or mismatched bytes fail without overwriting copies. No original-byte changes or automatic status inference. |
| ingest | --source SRC-ID; --file PATH; --metadata PATH; --session SES-ID | Copy a supplied file into a new immutable asset location, hash and count actual bytes, and create AST metadata. Preserve unknown capture/provenance fields. Source must exist. Duplicate bytes do not merge capture lineages. On incomplete copy, do not publish a complete acquired asset. Initially backup_pending. |
| backup | --asset AST-ID | Read configured roots, copy to a new backup object, verify hash/size, and preserve a confirmed or failed BAK record. Reject unsafe/overlapping roots and missing production protection. Can protect an original or a derivative; does not authenticate either. |
| restore-asset | --asset AST-ID; --receipt BAK-ID; --into PATH | Verify a matching backup and restore into a clean, previously nonexistent location within the configured primary root. Verify copied bytes and create a new recovery_copy AST record linked to the original and receipt. Never replace the original location, metadata, or expected hash. |
| start-analysis | --cycle CYC-ID | Validate the frozen plan, expected input revisions/hashes, required tool/input availability, and confirmed acquired-original backups; record the analysis-start manifest/time. Does not execute media processing or make findings. |
| validate | --gate records, foundation, baseline, cycle, or delivery; --verify-files for actual readiness | Validate schema/relationships and the selected gate. Default gate records. Metadata-only mode reports structure_only/not_evaluated readiness. Cycle/delivery without verify-files returns blocked (4). Actual readiness reads source/backup bytes and receipt coverage; missing storage cannot be skipped as verified. |
| close-session | --session SES-ID; --handoff PATH | Stage final handoff/session records and note/register state, verify a complete backup snapshot, store receipt copies, then publish exact final bytes under a journal. Pending/failed protection cannot yield complete. |
| recover | --transaction CHG-ID; --finish | Finish only the verified staged outputs of an interrupted journal after checking expected state. Never overwrite originals, discard retained revisions, or perform an unrecorded repair. Report unresolved conflicts rather than guess. |

Global --format json suppresses progress prose on stdout; diagnostics may go to stderr. Commands
that change dataset files use the single-writer lock, checked prior hashes, retained changes,
and recovery journal. Read-only validation must not silently rewrite bad data or receipts.

No command has a send, publish, purchase, live-transmit, identity-recognition, or automatic
network-crawl action. No media decoder is required just to inspect CSV/JSON metadata. Execution
permissions for external storage and input files remain governed by the user's environment.

## JSON result

Each command emits one object with:

- schema_version: 1.
- command and status: ok, invalid, conflict, blocked, or error.
- dataset_role: actual or illustrative.
- changed_ids and created_paths: what the command actually published, empty for a read-only check.
- errors, blockers, and gaps: arrays with code, message, record/path reference, dependency, and
  next_action where applicable.
- checks: named pass/fail/not_applicable results for the requested gate.
- dataset_manifest: current canonical file hashes suitable for the next change-set's expected
  state; never a claim of independent backup or historical authenticity.
- receipt_id or transaction_id where applicable; readiness only for the gate actually evaluated.
- asset_id for ingest/restore-asset; readiness is structure_only, not_evaluated, ready, or not_ready.

Avoid placing private absolute roots, contacts, or uncorroborated allegations into shareable
validation output. Local detailed diagnostics can refer to restricted configuration when needed.

## Exit codes

| Code | Meaning |
| --- | --- |
| 0 | Requested operation/check succeeded. Named historical gaps may remain where that gate permits them. |
| 2 | Invalid arguments, schema, references, or unsafe path. |
| 3 | Writer/revision conflict or recovery-required publication. |
| 4 | An essential dependency or required backup/review is pending; operation is not complete. |
| 5 | I/O or byte-integrity failure; no success receipt or affected completion is published. |

When multiple failures coexist, return the most immediate operation-stopping condition and
include every detected issue in the result. Never convert nonzero completion into done status.

## Gate semantics

| Gate | Required checks |
| --- | --- |
| records | Serialization, IDs, relations, revision history, enums, locators, explicit unknowns, and journal consistency. No historical truth assertion. |
| foundation | records plus six usable registers; 7 source aliases, 7 hypothesis aliases, 11 task aliases with original limits/owners/dependencies/conditions; entry/status/method/decision documents; configured preservation dependency clearly recorded. |
| baseline | foundation plus retained evidence that foundation review passed before expanded collection; real-source dependency map, chronology/contradictions, recording inventory, dated signal paths with explicit unknowns; defined contemporary-search coverage and gaps; inspectable evidence references. |
| cycle | baseline plus frozen alternatives/predictions before attributed new searches/tests, verified original protection, actual method/result and hypothesis review, separate findings review, uncertainty and exclusion guards. |
| delivery | cycle on an actual dataset, all five workstream output statuses, owner/selected-reviewer report, four milestone decisions and their retained matching reviews, a current final milestone review, retained limits and permissions, next actions, and completed backed-up handoff. Illustrative datasets cannot pass this gate. |

Foundation and baseline gates do not mark tasks complete automatically. A structurally valid
baseline can name inaccessible records; it cannot consist of unexamined seed descriptions and
pretend they are newly inspected evidence. Human/separate AI review must still assess the real
source content and reasoning. Passing JSON checks alone never satisfies that review.

start-analysis always performs current byte/receipt checks, and close-session always copies and
verifies final bytes; neither has a metadata-only completion mode. Review records are separate
from the immutable reviewed revision/narrative. Session completion combines backed-up intended
payload, matching confirmed receipt, and coherently mirrored committed control journals.

## Failure and preservation rules

- No backup root: report dependency, allow unrelated schema work, and block affected analysis or
  session completion. Do not create a guessed destination or silently use work/.
- Changed original: preserve expected hash and previous receipts, fail affected analysis, and
  retain a discrepancy record through the normal change workflow.
- Changed notes after snapshot: invalidate current closure coverage; create a new snapshot.
- Interrupted multi-file publication: return recovery_required; complete only after coherent
  journal recovery. Do not describe several file replacements as an atomic transaction.
- recover finishes only a publication journal; restore-asset restores bytes to a new recovery
  location. These actions must not be conflated or silently rewrite original evidence.
- Unavailable media tools, archives, or listener: name the waiting task/dependency. Do not claim
  a clip was analyzed or a disputed phrase was independently transcribed.
- Real delivery remains incomplete if no actual distinguishing test can be performed. Save the
  blocker and reopening condition rather than substituting an illustrative successful run.
