# Public tooling package verification

Checked 2026-11-08 against a new package directory:
`work/public-package-20261108T205128Z`. Only nine authorized tooling/fictional-fixture files
were copied. No private configuration, investigation plan, specs, registers, evidence, reports,
analysis products, or status/session files were included.

Decision: the tested public tooling package works independently of the private dossier.
Correct the storage template's same-volume instruction before publication (see remaining note).
This verification does not publish, authenticate evidence, or complete research milestones.

## Executed checks

| Check | Exit | Observed result |
| --- | --- | --- |
| `python -m unittest discover -s tests -v` | 0 | 92 tests passed in 56.980 seconds |
| CLI fictional init into `work/illustrative` | 0 | JSON ok, illustrative dataset |
| CLI records validation | 0 | JSON ok, structure_only |
| CLI foundation validation | 0 | JSON ok, structure_only |
| CLI delivery validation with file verification | 4 | blocked/not_ready; includes actual_dataset_required |
| CLI generated-file backup in a temporary illustrative dataset | 0 | confirmed receipt |
| CLI restore to clean new relative target | 0 | new linked recovery_copy, identical bytes |
| CLI repeat restore to occupied target | 3 | conflict/restore_exists; existing target preserved |
| CLI restored-dataset records validation with file verification | 0 | JSON ok |

The original generated fixture file remained unchanged. The recovery-copy record names its
original asset and receipt. The extra recovery exercise removed its temporary dataset on exit.
No fault injection or restoration was performed against actual evidence.

Exact commands, exit codes, JSON envelopes, and copied-file SHA-256/byte counts are in
`work/public-package-check.json`. Full test stdout/stderr and CLI envelopes are in the package
directory. Additional CLI recovery observations are in `work/public-cli-recovery-check.json`.
Repeat helpers are `work/check_public_package.py` and `work/public_cli_recovery_check.py`;
these operational verification files are private working artifacts and are not release files.

## Authorized public file list

- `.gitignore`
- `README.md`
- `tools/dossier.py`
- `config/storage.local.example.json`
- `tests/test_preservation.py`
- `tests/test_records.py`
- `tests/test_workflow.py`
- `tests/fixtures/README.md`
- `tests/fixtures/seed-records.json`

The tested tool hash is `6c62a5d743287ae7199260b79b1174822f6b70cbe9bd74a3f8664a4dcb813ad2`.
No mandatory third-party dependencies were installed. No Docker, npm, ESLint, Prettier,
Terraform, or Helm configuration was found; no additional ignore files are needed for those.
Git origin names the owner-authorized public repository. Nothing was staged, committed, or pushed.
README instructions are accurate and were left unchanged.

## Operator documentation notes for root

`config/storage.local.example.json` says a same-volume copy is illustrative-only, although the
implemented storage guard permits an explicitly owner-selected same-volume destination with a
recorded drive-loss limitation. Revise that instruction to match the actual contract and keep
the default false/unconfigured fields. This is a documentation correction, not a tested core change.

The private quickstart still describes the pre-implementation state and says there is no Git
repository. When completing T079, replace those historical operator phrases with current facts:
the implemented tool is runnable; Git tooling is configured; actual private preservation remains
separate and explicitly documents its same-drive limitation. Keep prerequisite warnings and
illustrative-versus-actual boundaries. No behavioral core defect was found in this package check.
