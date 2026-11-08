# Implementation Plan: Max Headroom Investigation Dossier

**Branch**: 001-investigation-dossier | **Date**: 2026-11-06 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from specs/001-investigation-dossier/spec.md.

The branch value is Spec Kit's feature identifier. This workspace has no Git repository or actual
Git branch; planning does not initialize one.

## Summary

Deliver an inspectable research dossier for the 1987-11-22 WGN-TV and WTTW intrusions, backed by
six canonical CSV registers, Markdown findings, JSON provenance records, and a small Python
integrity/workflow tool. Preserve the investigation plan's five workstreams, seven starter
sources, seven initial hypotheses, eleven backlog tasks, and four milestone reviews.

First delivery includes the usable dossier, a baseline built from real sources, and one actual
bounded analytical cycle with a documented distinguishing test and separate review. Examples may
prove the tools work but cannot satisfy that research outcome. Reports address the owner and
selected reviewers. Continue through ordinary milestone reviews without approval pauses while
retaining user control over outreach, spending, and scope changes.

Planning ends with design artifacts. No incident sources are acquired, no operational registers
are populated, and no research milestone is claimed complete by these documents.

## Technical Context

**Language/Version**: Python 3.13; Python 3.13.12 is available in this workspace.

**Primary Dependencies**: Python standard library: argparse, csv, json, pathlib, hashlib,
datetime, os, shutil, tempfile, and unittest. No mandatory third-party packages. FFmpeg/ffprobe
are optional, absent during planning, and introduced only for a justified media question.

**Storage**: UTF-8 Markdown; six UTF-8 CSV registers with fixed schemas and typed JSON collection
cells; JSON metadata sidecars and immutable revision/backup receipts. Storage aliases map portable
references to locally configured absolute roots. Large media may use an external primary store.
The owner supplies an authorized backup root and failure-domain description before production
backup confirmation; none has been assumed or configured.

**Testing**: Focused unittest tests with temporary illustrative datasets; schema/reference checks;
corruption, stale-write, and interrupted-backup exercises; manual source and reasoning review;
real-source baseline and analytical-cycle acceptance. See [quickstart.md](quickstart.md).

**Target Platform**: Windows and PowerShell for the first delivery. Keep metadata logic portable
within Python's filesystem capabilities; no server or browser application is required.

**Project Type**: File-based evidence dossier with a local command-line integrity/workflow helper.

**Performance Goals**: Stream file hashes and copies in bounded chunks. Metadata-only checks must
not scan media bytes unless integrity is requested. No response-time or throughput SLA is imposed
by the spec; avoid inventing a scale benchmark that displaces research.

**Constraints**: Originals are immutable; backups of acquired originals precede analysis; final
notes/register bytes are backed up before session completion. One writer at a time, expected
revision/hash checks, journaled multi-file publication, explicit unknowns and access gaps.
Historical architecture and clock claims remain evidence-bound. No automated outreach, spending,
live broadcast experiments, masked/distorted identity recognition, or generative recovered detail.

**Scale/Scope**: One owner-assisted investigation with selected reviewers, two stations, five
workstreams, six registers, initially 7 source aliases, 7 hypothesis aliases, and 11 task aliases.
No artificial record-count limit. Reassess storage and navigation if observed workload warrants it;
the initial scope does not require a dashboard, database, exhaustive archives, novelty, or identity.

## Constitution Check

Pre-research assessment: PASS. Post-design assessment: PASS. There are no requested exceptions.

| Principle / gate | Pre-research | Post-design evidence |
| --- | --- | --- |
| I. Evidence before narrative | PASS: scope is evidence-supported understanding, with identification optional. | PASS: claims separate observation/report/inference/speculation; lineage and exact locators are required; actual delivery excludes illustrative substitutes. |
| II. Preserved provenance and reproducibility | PASS: unchanged originals, SHA-256, and derivation links are mandatory. | PASS: asset and backup contracts bind bytes, inputs, settings, versions, and exact final session snapshots; unavailable protection is a blocker. |
| III. Alternatives and historical context | PASS: bounded questions, predictions before searches, and actual 1987 evidence govern work. | PASS: cycle metadata orders searches/tests; baseline contracts retain clock precision, historical components, alternatives, assumptions, and reversal evidence. |
| IV. Responsible human and AI research | PASS: privacy, outreach, spending, and attribution limits are accepted. | PASS: reports restrict private material; separate reasoning review is recorded without factual corroboration; no interface sends requests or spends money. |
| V. Dossier first and durable progress | PASS: one portable collection precedes application development. | PASS: six registers plus linked sidecars, preserved revisions, resumable status, and small integrity tools; no dashboard or parallel mutable account. |
| Governance and living plan | PASS: spec, plan foundation, and constitution agree. | PASS: all FR-001 through FR-034 and SC-001 through SC-010 have delivery/validation coverage below; operational checkpoints update the living research state. |

These passes assess the design. Actual implementation and research must pass the corresponding
checks independently; this table is not evidence of acquired media or completed investigations.

## Project Structure

### Documentation (this feature)

~~~text
specs/001-investigation-dossier/
  spec.md
  plan.md
  research.md
  data-model.md
  quickstart.md
  contracts/
    cli.md
    records.md
    reports.md
  checklists/requirements.md
  tasks.md                      # produced later by speckit-tasks
~~~

### Source Code (repository root)

The following is the proposed implementation layout; these operational artifacts are not created
by planning.

~~~text
README.md                       # entry point and current state
INVESTIGATION_PLAN.md            # existing living source of truth
docs/
  STATUS.md
  METHODS.md
  DECISIONS.md
registers/
  sources.csv
  claims.csv
  timeline.csv
  hypotheses.csv
  tasks.csv
  searches.csv
evidence/
  originals/                    # default primary root; large assets can be external
  metadata/
    assets/
    changes/
    control/                    # mutable journals, mirrored separately from frozen payloads
    backups/
    sessions/
derived/
  transcripts/
  frames/
  audio/
analysis/
  chronology/
  engineering/
  media-comparison/
  culture/
  geography/
  cycles/                       # bounded-question plans and results
reports/
  findings/                     # reviewed findings and reviewer records
    reviews/artifacts/          # immutable milestone document copies, grouped by RVW ID
  milestones/                   # four milestone decisions and deliverable inventory
config/
  dossier.json                  # schema version and dataset role
  seed-records.json             # curated from the source plan; contains no new findings
  storage.local.json             # private, machine-specific root mapping
tools/
  dossier.py                    # local integrity/workflow helper
tests/
  test_records.py
  test_preservation.py
  test_workflow.py
  fixtures/                     # explicitly illustrative; never evidence
private/                        # optional restricted working information, excluded from reports
work/                           # transactions, staging, temporary illustrative workspaces
~~~

**Structure Decision**: Follow the investigation plan's dossier layout, adding only metadata
locations and tools needed for repeated provenance and completion checks. JSON sidecars are part
of the same collection, not a second register system. Analysis scripts live with their bounded
question and are added only when needed. Local root mappings and restricted working information
stay outside shareable output and any optional version-control publication.

## Phase 0: Research Decisions

Complete: [research.md](research.md) records twelve decisions with rationale, alternatives, and
primary documentation. It resolves serialization, stable identity, unknown handling, write
conflicts, storage configuration, backups, media tooling, historical times, separate review, and
truthful validation.

A production backup destination, restricted archive access, specialist availability, and an
optional media executable are runtime dependencies. Their handling is fully defined; missing
inputs block dependent actions rather than remain unanswered architecture choices.

## Phase 1: Design and Validation

Complete:

- [data-model.md](data-model.md): canonical fields, relationships, identity rules, lifecycles,
  retained changes, preservation snapshots, and the seven starting hypotheses.
- [records contract](contracts/records.md): CSV/JSON encoding, evidence locators, change-sets,
  storage references, inspection status, and validation severity.
- [CLI contract](contracts/cli.md): local commands, machine-readable output, exit codes, and
  mutation/backup rules. This owner-facing interface is the reason contracts are provided.
- [report contract](contracts/reports.md): baseline, five workstreams, findings, review, milestone,
  session, and privacy requirements.
- [quickstart.md](quickstart.md): runnable scenarios to execute after implementation, including
  both illustrative failure tests and real delivery acceptance.

Post-design constitution review found no violations. No operational tool, test suite, application,
or incident analysis is implemented during this planning command.

## Delivery Sequence and Requirement Coverage

These are delivery stages for subsequent task generation, not a replacement for tasks.md.

| Stage / source tasks | Deliverable and review condition |
| --- | --- |
| Foundation: T01-T02 | Implement schemas and narrow integrity tools, configure authorized storage, seed S01-S07/H1-H7/T01-T11 faithfully, document methods and ID rules, prove the evidence model is inspectable, and confirm the session backup. |
| Baseline: T03-T06 | Search the defined 1987-11-23 through 1987-11-30 window first, inventory best available recordings, map dependence, build the chronology and dated historical signal paths, and review all four outputs with explicit gaps. |
| Conditional detail: T07-T09 | Transcribe/compare media, assess period references and public availability, and prepare focused archive/interview drafts as dependencies justify them. Missing listeners, records, or tools remain waiting states. |
| Actual test: T10 | Choose the attainable distinguishing question from the baseline, freeze alternatives/predictions before cycle searches, use real evidence, preserve the method/result, and revise hypotheses with reasons. An unresolved result can be valid; an unperformed test cannot. |
| Review and handoff: T11 | Obtain separate reasoning review, preserve any specialist limits and blind-listening dependencies, prepare owner/reviewer reports, inventory all workstream outputs, choose next actions, and close with confirmed final notes/register backups. |

Honor the source backlog's owners, dependencies, outputs, and reassessment timeboxes, including
T03/T06 reassessment after 2-3 research sessions. External waits are separate from effort estimates.
Foundation review must pass before expanded baseline collection. Source T08 keeps its T07
transcription/comparison prerequisite; preliminary public-availability research uses a separate
TASK and cannot complete T08. Milestone reviews use content-addressed document targets with
retained copies and fixed relied-on basis, as defined in the records/report contracts.
Routine reviews record decisions and continue authorized work under FR-032. If no useful work can
continue, save exact blockers and reopening conditions; do not substitute examples for delivery.

Owner-directed implementation update, 2026-11-07: use the public
michaelhoffmantech/max-headroom-project GitHub repository for tooling, with research data/reports
excluded from public commits. The owner selected a separate private backup directory on C:.
Explicit owner_selected_same_volume configuration permits verified copies there while recording
that they do not protect against loss of C:. GitHub is not the private research backup.

| Requirements | Design and acceptance coverage |
| --- | --- |
| FR-001-FR-003 | Six registers, seed aliases, dossier entry point and models; foundation gate; SC-001. |
| FR-004-FR-006 | Typed claims, locators, inspection state and source/asset lineage; records/reports contracts; SC-003 and SC-008. |
| FR-007-FR-009 | Immutable asset, acquisition metadata, receipts and search logs; corruption/access scenarios; SC-002 and SC-008. |
| FR-010-FR-012 | Chronology and engineering report contracts, clock and path fields, dated component/assumptions evidence; SC-004-SC-005. |
| FR-013-FR-015 | Media provenance, processing metadata, blind transcripts and period catalog; conditional analyses; SC-007. |
| FR-016-FR-018 | Frozen cycle plans, necessary conditions, status revisions, counterevidence and reopening records; SC-005. |
| FR-019-FR-021 | Finding and separate review records, audience/access notes, novelty search and specialist needs; SC-003 and SC-009. |
| FR-022-FR-024 | Session snapshots, task completion conditions, living status/plan updates and actual milestone gates; SC-001 and SC-004-SC-006. |
| FR-025-FR-027 | Records inventory, release context, neutral unsent drafts, user-only external actions and spending; SC-008. |
| FR-028-FR-029 | Restricted working information, report review and source-as-data controls; SC-003 and SC-008. |
| FR-030 | Canonical collection, configured roots, exact-content backup and staged closure; SC-002 and SC-006. |
| FR-031 | Evidence-based success and optional identification; actual review outcomes; SC-009. |
| FR-032 | Continue routine work; block only dependent actions; checkpoint journal/status; SC-009. |
| FR-033 | Bounded contemporaneous search coverage and image/text comparison; baseline validation; SC-004. |
| FR-034 | Five-workstream deliverable inventory distinguishing available/waiting/deferred products; SC-010. |

## Complexity Tracking

No constitutional exceptions or unjustified complexity are introduced. The helper's change,
backup, and closure safeguards address defined, repeatable evidence-integrity questions.
A database, dashboard, generic scraping framework, automatic contact system, and mandatory media
processing stack are excluded from the first delivery.
