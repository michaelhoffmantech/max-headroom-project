# Max Headroom investigation dossier tools

Python 3.13 standard-library tools for an inspectable, file-based research dossier. The public
repository contains tooling and invented test fixtures. Research registers, evidence, findings,
local storage configuration, and current session notes stay private.

Run the checks from this directory:

```powershell
python -m unittest discover -s tests -v
python tools/dossier.py --help
```

For a temporary demonstration, use the explicitly fictional fixture:

```powershell
python tools/dossier.py --root work/illustrative --format json init --seeds tests/fixtures/seed-records.json --dataset-role illustrative
python tools/dossier.py --root work/illustrative --format json validate --gate records
```

The private investigation uses `INVESTIGATION_PLAN.md` as its foundation and `docs/STATUS.md`
plus the relevant registers for resumption. Every session reads those files first. Initializing
files or passing tests does not establish a historical finding or completed research milestone.

`config/storage.local.example.json` describes machine-local configuration. Acquired originals
remain unchanged, require verified backups before analysis, and retain SHA-256 as an integrity
check rather than authentication. Final notes/registers are backed up before session completion.
Public Git commits are not the private evidence backup. Outreach and spending remain owner-controlled.
