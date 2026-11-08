# Validation Guide: Investigation Dossier

The dossier CLI and isolated test suite are implemented. This guide describes repeatable
operator workflows; commands with example IDs or input files require the current dataset's
actual values. Read docs/STATUS.md before resuming an existing investigation. A command shown
here is not proof that its corresponding research or final delivery has been completed.

Run from the active project root. References: [CLI contract](contracts/cli.md),
[record contract](contracts/records.md), [data model](data-model.md), and
[output contract](contracts/reports.md). Use the actual source plan and spec when assessing content.

## 1. Prerequisites

- Python 3.13; Python 3.13.12 is available in this workspace. No package installation is required
  for the core dossier checks. The owner-authorized public Git repository contains tooling and
  fictional fixtures only; actual research and its private backups remain separate.
- Implemented tools and meaningful isolated tests, plus a curated config/seed-records.json
  preserving the investigation plan's real metadata and its source-plan hash.
- For actual research, owner-authorized primary/backup roots in config/storage.local.json.
  The backup destination and failure domain must be supplied before protection is confirmed.
  This investigation uses the owner's separate private C: directory with explicit same-volume
  selection and a recorded limitation: verified separate copies do not protect against loss of C:.
  For another installation, configure its actual authorized roots; do not copy machine-specific
  values or claim a temporary work/ copy provides production protection.
- Research sources and any acquired files must be inspectable or have explicit access limits.
  FFmpeg/ffprobe, restricted archives, blind listeners, and specialists are task-specific
  dependencies; their absence must remain visible rather than block unrelated work.

The commands use SES-0001 as the example first research session. Close every actual session at
its end and open a new ID when continuing; do not leave one session open across milestones merely
to postpone its notes/register backup. Final delivery uses the actual final session ID.

```powershell
python --version
python tools/dossier.py --help
```

Expected: Python 3.13 and the command interface in the contract, without requiring a server,
account connection, media suite, or database.

## 2. Prove the tools with isolated illustrative data

```powershell
python -m unittest discover -s tests -v
python tools/dossier.py --root work/illustrative --format json init --seeds tests/fixtures/seed-records.json --dataset-role illustrative
python tools/dossier.py --root work/illustrative --format json validate --gate foundation
python tools/dossier.py --root work/illustrative --format json validate --gate delivery --verify-files
```

The illustrative foundation can be structurally usable. The final command must return nonzero
with actual_dataset_required; illustrative records cannot pass real delivery. Metadata-only
results explicitly report structure_only/not_evaluated rather than preservation readiness.
Fixtures remain outside actual evidence and are never cited in findings.

The unittest suite must exercise consequential behavior:

| Scenario | Expected outcome |
| --- | --- |
| Bad CSV width/header, invalid collection JSON, duplicate keys/IDs, or dangling links | Invalid result; no silent coercion or dataset mutation. |
| Shared interview/capture lineage and multi-input derivative | All sources/inputs retained; no extra factual corroboration from copies or arbitrary single parent. |
| Firsthand retrospective account and year-only source date | Both status axes retained; known year preserved without invented month/day. |
| Superseded conclusion and stale concurrent change | Prior values/reason remain inspectable; stale write conflicts rather than overwrites. |
| Ruled-out hypothesis without an evidenced failed necessary condition | Rejected; no negative conclusion from a missing record. |
| Search/test predates its frozen cycle plan | Cycle gate fails; initial discovery remains separately labeled. |
| Predictions are edited after a new cycle search | Frozen plan/hash stays unchanged; later ideas require a dated exploratory amendment or new cycle. |
| Original or backup copy has changed bytes | Integrity failure, expected hash preserved, no false confirmation. |
| Missing destination or interrupted copy | Backup stays pending/failed; no analysis or closure eligibility for the affected content. |
| Notes change after snapshot freeze | Closure is invalidated; a new snapshot is required. |
| Publication interrupted after receipt confirmation | recovery_required; finish only journaled expected bytes; immutable CHG/Session payloads do not change after backup. |
| Review is attached to a claim/finding | RVW reverse lookup preserves the target revision; no perpetual re-review caused by a backlink edit. |
| Milestone review targets a document | ReviewTarget identifies the milestone/path/hash, retained identical copy, and fixed basis; changed reviewed bytes or basis require re-review, while unrelated edits do not. |
| Expanded collection starts before foundation review | Task readiness blocks expanded collection until T027's recorded foundation review passes; independent tooling remains available. |
| Preliminary availability notes exist before transcription/comparison | Separate TASK/preliminary entries remain distinct from T08; recording-derived interpretation and T08 completion require T07's outputs and required blind review. |
| Restore to clean target, mismatched restore, or existing destination | Valid restore creates linked recovery_copy; mismatch/existing destination fails without replacing the original. |
| Illustrative data made otherwise structurally complete | Actual delivery still fails; passing fixture tests is not research completion. |

Do not run destructive fault injection against the real dossier. Tests use temporary workspaces,
explicit illustrative backup roots, and clearly labeled invented material.

## 3. Establish the actual foundation

```powershell
python tools/dossier.py --format json init --seeds config/seed-records.json --dataset-role actual
python tools/dossier.py --format json validate --gate foundation
```

Inspect the result and files, not only the exit code:

- All six registers have the documented headers. S01-S07, H1-H7, T01-T11 mappings preserve item
  locators, read/excerpt/unavailable limits, untested hypotheses, queued tasks, owners,
  dependencies, completion conditions, and reassessment timeboxes.
- H1-H3 retain entry-point questions; H4-H7 retain production, site, insider-reference, and
  artifact questions that can coexist. No false technical finding, identity, or acquired media
  is seeded. Later initialization does not overwrite actual research.
- README, status, methods, and dated decisions explain how to resume and where actual/restricted
  material belongs. Configure authorized storage and record its protection limits.
- Foundation metadata checks can report structure_only while backup configuration is pending;
  the research session cannot be closed complete until its final notes/register backup succeeds.

For a new investigation, prepare work/open-session.json as a create change-set for SES-0001,
using the model's actual start time, owner, current question, and milestone. When resuming this
dossier, inspect existing sessions and allocate the next valid ID rather than recreating SES-0001.
Prepare future changes through the same contract rather than overwriting register history.

```powershell
python tools/dossier.py --format json apply --change-set work/open-session.json
```

Expected: a retained CHG record and active session, with no claim of completed source research.

## 4. Acquire and protect a real supplied file

Register the actual source item first. Prepare work/acquisition.json with its true acquisition
context, restrictions, capture/digitization history, and explicit unknowns. These are inputs from
the actual acquisition, not values copied from illustrative fixture metadata.

```powershell
$sourceId = Read-Host 'Registered source ID for this exact item'
$evidenceFile = Read-Host 'Full path to the acquired file'
$ingested = python tools/dossier.py --format json ingest --source $sourceId --file $evidenceFile --metadata work/acquisition.json --session SES-0001 | ConvertFrom-Json
python tools/dossier.py --format json backup --asset $ingested.asset_id
python tools/dossier.py --format json validate --gate records --verify-files
```

Expected: unchanged acquired bytes, an AST record with acquisition date/SHA-256/byte count,
separate provenance histories, and a BAK receipt matching a verified copy. A checksum is not
authentication. Missing destination or failed verification must block the affected analysis.
Reading a web page without acquiring a file does not create an invented asset or checksum.

When restoration is needed, use restore-asset with the original AST ID, matching receipt, and a
clean new location; inspect the recovery_of_asset_id relationship and unchanged expected hash.
Use recover only for an interrupted publication journal. They are different operations.

```powershell
$assetId = Read-Host 'Original AST ID to restore'
$receiptId = Read-Host 'Matching confirmed BAK ID'
$newTarget = Read-Host 'New relative path inside primary_evidence'
python tools/dossier.py --format json restore-asset --asset $assetId --receipt $receiptId --into $newTarget
```

An existing destination must fail with conflict/restore_exists (exit 3). Restoration creates a
new recovery_copy record; inspect its original-asset and receipt links and verify the copied
bytes. A restore exercise belongs in an isolated illustrative dataset unless actual recovery
is needed.

## 5. Produce the real baseline

Follow T03-T06 dependencies from the source plan. Log exact queries and coverage for the defined
1987-11-23 through 1987-11-30 window before expanding through 1988 and later follow-ups. Compare
article images and searchable text where available. Record every access barrier and negative search.

Prepare the four baseline outputs in the output contract:

1. Source-dependency map distinguishing repeated testimony and capture lineages.
2. Chronology/contradiction list retaining the reported WGN duration disagreement, clock sources,
   Chicago local times/offsets, precision, separate event boundaries, and reception paths.
3. Best-available WGN/WTTW recording inventory with capture/receiver/tape/processing details and
   explicit unavailable or derivative-only limits.
4. Dated 1987 signal-path diagrams with supported components, monitoring, remote control,
   alternate feeds, unknowns, and initial engineering assumptions.

```powershell
python tools/dossier.py --format json validate --gate baseline --verify-files
```

Expected: real inspected sources support the products; named inaccessible evidence may remain.
The validator checks structure, links, and preservation. A reviewer still checks that the cited
sources support the text and that current facilities have not replaced historical documentation.
All five workstreams receive an output/status inventory; missing later transcripts/catalogs or
requests remain explicitly waiting/deferred rather than falsely completed.

## 6. Complete one actual analytical cycle

Select the attainable distinguishing question after inventory/baseline review. Store CYC-0001
with alternatives, necessary conditions, predictions, evidence needs, dependencies, method,
expected output, and timebox before its new searches or test. Log the strongest alternative,
source dependence, hidden assumptions, and what would reverse the conclusion.

```powershell
python tools/dossier.py --format json apply --change-set work/plan-cycle.json
python tools/dossier.py --format json start-analysis --cycle CYC-0001
```

Then perform the question's actual recorded method with real evidence, preserving inputs,
observations separately from interpretation, transformations/settings/versions where used,
result, limitations, and next action. Add/compare hypotheses without forcing certainty.
No universal FFmpeg command is prescribed: choose a transformation only when the question needs
it, preserve original timing/interlacing, and register every output as a derivative.

Update results through work/cycle-result.json. Obtain a genuinely separate reasoning review;
record it as RVW metadata targeting unchanged finding/claim revisions. Do not append a reviewer
link to the reviewed narrative and invalidate its hash. Blind-transcribe disputed audio and
record unresolved specialist needs. Neither AI agreement nor generated enhancement is evidence.

```powershell
python tools/dossier.py --format json apply --change-set work/cycle-result.json
python tools/dossier.py --format json apply --change-set work/separate-review.json
python tools/dossier.py --format json validate --gate cycle --verify-files
```

Expected: an actual test/result, justified hypothesis changes, and a separately reviewed finding
or documented unresolved result. A ruled-out status requires a failed necessary condition with
evidence, assumptions, and scope. An unavailable input or unperformed test cannot pass.

## 7. Close the session and assess first delivery

Update the living plan/status, source-linked finding, milestone decision, and five-workstream
inventory. Explain terminology/access limits for the owner and selected reviewers. Include next
three owned actions, waits, branch stopping/reopening conditions, novelty search where asserted,
and privacy review. Requests remain drafts; this sequence sends nothing and spends nothing.

Prepare work/final-handoff.md for publication as final STATUS.md. The closure operation stages
all final bytes, confirms their backup, mirrors control records separately, and only then
publishes the backed-up handoff/session payload. Actual completion time belongs to the control
journal; intended Session bytes are not edited after confirmation.

```powershell
python tools/dossier.py --format json close-session --session SES-0001 --handoff work/final-handoff.md
python tools/dossier.py --format json validate --gate delivery --verify-files
```

Expected: coherent committed control records and matching receipt in both stores; final local
notes/registers match the covered snapshot; all SC-001 through SC-010 outcomes have inspectable
evidence. If another research session was needed, use its actual SES ID instead of SES-0001.

A fresh reviewer must recover milestone/question, findings/confidence, hypothesis changes,
gaps/waits, and next three actions without chat history. Participant identification and novelty
remain optional, evidence-supported outcomes. Review records a continue/narrow/wait/assign/close
decision without imposing a routine owner-approval pause.

If no actual feasible test can be completed, first delivery remains incomplete with named
dependencies. Save the handoff and reopening condition; do not replace the agreed outcome with
a scaffold or successful illustrative test. Tools passing cannot authenticate the sources or
replace review of the historical reasoning.

## Executed implementation checks, 2026-11-08

The [isolated public-package check](../../reports/milestones/exercises/public-package-check.md)
copied only the nine public tooling/fictional-fixture files to a fresh directory. All 92 tests
passed. Fictional init, records and foundation commands returned exit 0; the latter metadata
checks reported structure_only. Delivery with --verify-files returned exit 4 with
actual_dataset_required. An additional CLI backup/clean-target recovery exercise passed,
preserved the original bytes and linked the recovery copy; repeating the restore correctly
returned exit 3. No actual evidence was damaged or replaced.

The supplied-data exercises separately checked an illustrative cycle/report/handoff, the
[US5 comparison/reference capability](../../reports/milestones/exercises/us5-exercise.md)
(11 checks), and the [US6 release/request/interview capability](../../reports/milestones/exercises/us6-exercise.md)
(12 checks). The records exercise also ran all 54 workflow tests successfully. The US3/US4
exercise measured a marker in generated input, retained frozen predictions, attached fictional
review metadata without changing the reviewed finding, closed a verified temporary snapshot,
and confirmed a changed source-basis record invalidates current readiness. These are capability checks;
the fictional reviewer is not an actual independent source or factual reviewer.

The actual baseline and CYC-0001/FND-0001 have separate real-source records and review metadata.
Their research outcome is assessed through the cycle gate and milestone reports, not these
fixtures. Final delivery still requires its current report review, fresh-reviewer handoff and
confirmed final session snapshot. Read the current saved status rather than treating this
dated execution note as the latest delivery decision.
