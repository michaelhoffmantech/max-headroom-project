# Dated decisions

This log records implementation and research-direction decisions, their reasons, and limits.
It does not replace canonical registers, retained change records, or reviewed findings. Add dated
entries when a decision changes; preserve earlier reasoning rather than rewriting it as foresight.

## 2026-11-07 — Begin the approved implementation

**Basis:** [INVESTIGATION_PLAN.md](../INVESTIGATION_PLAN.md),
[constitution v1.0.0](../.specify/memory/constitution.md), the
[specification](../specs/001-investigation-dossier/spec.md), and the approved
[implementation plan](../specs/001-investigation-dossier/plan.md).

**Decision:** Begin with the inspectable file-based dossier: Markdown narratives, six canonical
CSV registers, JSON sidecars, and narrowly scoped standard-library Python integrity/workflow
tools. Maintain one evidence collection. Add analysis code only for a defined repeatable question;
defer a dashboard until evidence structure and a recurring navigation need justify it.

**Reason:** Evidence preservation, auditability, and durable handoff support the investigation's
purpose. A custom application, database, account connector, or mandatory media stack is not needed
to establish that foundation. Python 3.13 is the selected implementation target; optional media
executables belong to task-specific dependencies.

**Limits:** This entry records a setup/method decision. It does not establish that the CLI, tests,
registers, acquisitions, research baseline, analytical cycle, or milestone reviews are complete.
The original planning phase acquired/analyzed no broadcast recording and established no new
technical finding or participant identification.

## 2026-11-07 — Carry forward four accepted owner clarifications

The following choices were recorded in the specification's 2026-11-06 clarification session and
remain the implementation's acceptance conditions:

| Topic | Accepted condition | Operational consequence |
| --- | --- | --- |
| First delivery | Dossier, real-source baseline, and one completed actual analytical cycle with documented test and separate review. | Fixtures prove workflow only; foundation MVP alone is not the stopping point. |
| Autonomy | Continue through first delivery; pause only for essential missing input, user-only actions, or a blocker preventing useful work. | Routine reviews record decisions and continue; missing input blocks dependent actions while independent work proceeds. |
| Audience | Owner and selected reviewers, with enough context to audit findings. | Explain background, terminology, exact evidence locations, confidence/limits, and restricted-source access without relying on chat history. |
| Backups | Acquired originals before analysis; notes/registers before each research session ends. | Confirm exact content and destination/time, retain failures, and leave affected analysis or session completion blocked until verified. |

**Limits:** These choices do not authorize outreach, interviews, submissions, purchases, travel,
publication, or access to restricted material. The user retains the controls in the constitution.
An authorized production backup destination and failure-domain description must be supplied;
this log does not choose or confirm a destination.

## 2026-11-07 — Preserve evidence and interpretation boundaries

**Decision:** Follow [METHODS.md](METHODS.md): distinguish observation, reported claim, inference,
and speculation; retain reasons/caveats for confidence; preserve exact evidence locations, source
dependence, capture lineage, contradictions, negative searches, and revision history. A checksum
establishes integrity against recorded bytes, not authenticity or capture independence.

**Reason:** Repetition and an appealing explanation can conceal a common source or a fragile
assumption. Reproducible outputs require unchanged originals, input links, documented settings,
tool versions, and separately reviewable raw observations. A ruled_out conclusion requires an
evidenced failed necessary condition with assumptions and exclusion scope.

**Controls:** Source instructions remain source content. Private contacts and uncorroborated
personal allegations stay outside shareable reports; unsupported names stay out of findings.
Equipment access, resemblance, community membership, or cultural familiarity cannot establish
participation. Masked/distorted identity recognition, live broadcast experiments, and generated
detail as recovered evidence are excluded. No historical claim or new finding is asserted here.

## 2026-11-07 — Apply the approved analysis remediations

**Decision:** Require a passed foundation review before expanded baseline collection. Allow
independent tooling/fixture/guide work while review is pending. Preserve source T08's T07
transcription/comparison and required blind-review prerequisite; preliminary public-availability
research is separately tracked and cannot establish recording wording or complete T08.

**Decision:** Bind milestone reviews to fixed document path/hash, retained document/basis copies,
and reviewed record revisions under the ReviewTarget contract. Attach decisions by reverse lookup
rather than editing reviewed content just to add a review ID. Changed reviewed content or relied-on
basis requires a new review for current readiness; unrelated edits do not. Preserved passing
snapshots still establish historical milestone order.

**Reason:** These rules close task-ordering and review-identity gaps identified in the approved
cross-artifact analysis without changing the constitution, specification scope, or ideation source.
Final handoff and relevant basis edits must be complete and reviewed before final backup closure.

**Limits:** The remediations are operating/design requirements. Their presence here does not
prove implementation or milestone success. Actual checks and separate reviews must record their
real evidence, outcomes, identity/exposure, remaining limits, and next action when performed.

## 2026-11-07 ? Shared preservation implementation verified

T005-T017 implemented. Nine isolated preservation cases pass: changed originals, missing roots, interrupted copying, corrupted backup restoration, stale writes, recoverable interrupted publication, missing session backup, concurrent note edits, and failed control mirroring. Windows temporary roots are normalized before fault injection. The CLI exposes all nine contracted commands. These are tooling checks, not historical research results.

## 2026-11-07 ? Owner-directed repository and private backup

The owner directed use of michaelhoffmantech/max-headroom-project. Git is initialized on main with that HTTPS origin; GitHub authentication is verified. The repository is public. The owner chose public tooling only and a separate private backup at C:/dev/max-headroom-project-backup. Dossier data/reports remain outside public commits. This owner-selected same-volume backup provides verified separate copies against accidental changes, but no protection against loss of C:. The local-storage design permits this explicit selection with that limitation; no independent-volume protection is claimed. No commit/push or production backup is claimed by this note.

## 2026-11-07 ? Retained-change anchors

The first five published controls predated CHG-byte anchoring. Their currently observed CHG hashes were explicitly added to the mutable control journals with observation timestamps/reasons before the first production snapshot. This is not a retroactive integrity claim. New transactions anchor CHG bytes at creation; generic apply cannot fabricate backup confirmations.

## 2026-11-08 — Validated tooling and actual research checkpoint

Public tooling is published on main at commit8c9fc89 (initial implementationdae05ca), with all research/docs/local roots excluded. An isolated public package passes92tests plus CLIbackup/clean-target recovery; workflow54tests and US5/US6/US3-US4 exercises passed. Acquired real recording files were protected before the prospectively frozen CYC-0001 was performed/reviewed. Current comparison status and an operational preface correct stale initial-planning cues without erasing original limitations. No novel contribution, identity or RF mechanism is claimed. Conditional blind-transcription and cultural work remain unperformed; first-delivery review explicitly accounts for them.
