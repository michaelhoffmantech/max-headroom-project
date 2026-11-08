"""Consequential preservation failures; all bytes and roots are temporary fixtures."""

import copy
import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock


PROJECT = Path(__file__).resolve().parents[1]
TOOL_PATH = PROJECT / "tools" / "dossier.py"
FIXTURE = PROJECT / "tests" / "fixtures" / "seed-records.json"


def load_tool():
    spec = importlib.util.spec_from_file_location("dossier_preservation_test", TOOL_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def stamp():
    return datetime.now(timezone.utc).isoformat()


class PreservationTests(unittest.TestCase):
    def setUp(self):
        self.mod = load_tool()
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.root = self.base / "project"
        self.backup_root = self.base / "illustrative-backup"
        self.root.mkdir()
        self.backup_root.mkdir()
        self.ds = self.mod.Dataset(self.root)
        (self.root / "config").mkdir()
        self.configure()
        (self.root / "docs").mkdir(exist_ok=True)
        (self.root / "docs" / "STATUS.md").write_text(
            "# Invented fixture status\nNo research has occurred.\n", encoding="utf-8"
        )
        self.result = self.ds.init(FIXTURE, "illustrative")
        self.open_session()

    def configure(self, backup=True):
        config = {
            "schema_version": 1,
            "roots": {
                "project": str(self.root),
                "primary_evidence": str(self.root / "evidence" / "originals"),
                "backup": str(self.backup_root) if backup else None,
            },
            "owner_authorized": True,
            "backup_failure_domain": "ILLUSTRATIVE same-volume temporary test roots only",
            "access_limits": {"project": "fixture", "primary_evidence": "fixture", "backup": "fixture"},
        }
        (self.root / "config" / "storage.local.json").write_text(json.dumps(config), encoding="utf-8")

    def change(self, operations, manifest=None):
        change = {
            "schema_version": 1,
            "actor": "preservation unittest",
            "reason": "Invented fixture exercise, never a research output",
            "expected_dataset_manifest": manifest or self.result["dataset_manifest"],
            "operations": operations,
        }
        self.result = self.ds.apply(change)
        return self.result

    def open_session(self):
        session = {
            "schema_version": 1, "id": "SES-0001", "revision": 1,
            "actor": "preservation unittest", "created_at": stamp(), "unknowns": {},
            "current_milestone": "foundation", "current_question": "Does the invented failure remain blocked?",
            "started_at": stamp(), "intended_completion_at": None,
            "findings": [], "completed_task_outputs": [], "disagreements": [], "gaps": [],
            "hypothesis_changes": [],
            "next_actions": [
                {"owner": "fixture runner", "output": f"invented action {n}", "dependencies": []}
                for n in range(1, 4)
            ],
            "waits": [], "deferred_branches": [], "closed_branches": [],
            "stopping_condition": None, "reopening_condition": None, "final_handoff": None,
            "closure_snapshot_id": None, "reserved_receipt_id": None, "intended_state": "active",
        }
        for key, value in session.items():
            if value is None:
                session["unknowns"][key] = "Active invented session has not been closed"
        self.change([{"op": "create", "entity_type": "sessions", "id": session["id"], "fields": session}])

    def ingest(self):
        supplied = self.base / "invented-input.txt"
        supplied.write_bytes(b"ILLUSTRATIVE invented acquisition bytes\n")
        metadata = {
            "restrictions": "Fixture only", "provenance_limits": "Invented local file, not evidence",
            "capture_date": None, "receiver_feed": None, "tape_generation": None,
            "original_media_history": "No historical medium; generated fixture",
            "digitization_history": "Generated text, no digitization",
            "completeness": "complete", "known_edits": [],
            "unknowns": {"capture_date": "Not a capture", "receiver_feed": "Not a recording", "tape_generation": "Not tape"},
        }
        self.result = self.ds.ingest("SRC-0001", supplied, metadata, "SES-0001")
        asset_id = self.result["asset_id"]
        return asset_id, self.asset(asset_id)

    def asset(self, asset_id):
        return json.loads((self.root / "evidence" / "metadata" / "assets" / f"{asset_id}.json").read_text(encoding="utf-8"))

    def original_path(self, asset):
        ref = asset.get("storage_ref", asset.get("storage"))
        self.assertIsInstance(ref, dict, "Asset must expose its canonical storage reference")
        roots = {"project": self.root, "primary_evidence": self.root / "evidence" / "originals", "backup": self.backup_root}
        return roots[ref["alias"]] / ref["relative_path"]

    def receipts(self):
        return [json.loads(p.read_text(encoding="utf-8")) for p in (self.root / "evidence" / "metadata" / "backups").glob("BAK-*.json")]

    def assert_not_confirmed(self, scope=None):
        self.assertFalse([r for r in self.receipts() if r.get("result") == "confirmed" and (scope is None or r.get("scope") == scope)])

    def test_changed_original_preserves_expected_hash_and_blocks_backup(self):
        asset_id, asset = self.ingest()
        expected = asset["sha256"]
        self.original_path(asset).write_bytes(b"corrupted invented bytes")
        with self.assertRaises(self.mod.DossierError) as caught:
            self.ds.backup(asset_id)
        self.assertEqual(5, caught.exception.exit_code)
        self.assertEqual(expected, self.asset(asset_id)["sha256"])
        self.assert_not_confirmed()

    def test_missing_backup_root_blocks_protection_without_success_receipt(self):
        asset_id, _ = self.ingest()
        self.configure(backup=False)
        with self.assertRaises(self.mod.DossierError) as caught:
            self.ds.backup(asset_id)
        self.assertEqual(4, caught.exception.exit_code)
        self.assert_not_confirmed()

    def test_interrupted_copy_never_confirms_backup(self):
        asset_id, _ = self.ingest()
        with mock.patch.object(self.mod, "copy_verified", side_effect=OSError("invented interrupted copy")):
            with self.assertRaises((self.mod.DossierError, OSError)):
                self.ds.backup(asset_id)
        self.assert_not_confirmed()

    def test_corrupted_backup_cannot_restore_or_replace_original(self):
        asset_id, asset = self.ingest()
        original = self.original_path(asset)
        original_bytes = original.read_bytes()
        result = self.ds.backup(asset_id)
        receipt_id = result["receipt_id"]
        objects = [p for p in self.backup_root.rglob("*") if p.is_file() and p.read_bytes() == original_bytes]
        self.assertTrue(objects, "Confirmed backup must contain the exact original bytes")
        objects[0].write_bytes(b"corrupted backup fixture")
        destination = self.root / "evidence" / "originals" / "new-restored-file.txt"
        with self.assertRaises(self.mod.DossierError) as caught:
            self.ds.restore_asset(asset_id, receipt_id, destination)
        self.assertEqual(5, caught.exception.exit_code)
        self.assertFalse(destination.exists())
        self.assertEqual(original_bytes, original.read_bytes())
        self.assertEqual(asset["sha256"], self.asset(asset_id)["sha256"])

    def test_stale_manifest_cannot_overwrite_newer_source_revision(self):
        stale = copy.deepcopy(self.result["dataset_manifest"])
        op = {"op": "update", "entity_type": "sources", "id": "SRC-0001", "expected_revision": 1,
              "fields": {"title": "First accepted invented update"}}
        self.change([op])
        before = (self.root / "registers" / "sources.csv").read_bytes()
        op["fields"]["title"] = "Stale invented overwrite"
        with self.assertRaises(self.mod.DossierError) as caught:
            self.change([op], manifest=stale)
        self.assertEqual(3, caught.exception.exit_code)
        self.assertEqual(before, (self.root / "registers" / "sources.csv").read_bytes())

    def test_interrupted_publication_retains_journal_and_can_finish(self):
        real_replace = self.mod.os.replace
        calls = 0

        def interrupt_once(source, destination):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError("invented publication interruption")
            return real_replace(source, destination)

        op = {"op": "update", "entity_type": "sources", "id": "SRC-0001", "expected_revision": 1,
              "fields": {"title": "Recoverable invented update"}}
        with mock.patch.object(self.mod.os, "replace", side_effect=interrupt_once):
            with self.assertRaises((self.mod.DossierError, OSError)):
                self.change([op])
        journals = list((self.root / "evidence" / "metadata" / "control").glob("CHG-*.json"))
        unfinished = [p for p in journals if json.loads(p.read_text(encoding="utf-8")).get("state") != "published"]
        self.assertTrue(unfinished, "Interrupted publication must retain a recovery journal")
        self.ds.recover(unfinished[-1].stem)
        self.assertIn(b"Recoverable invented update", (self.root / "registers" / "sources.csv").read_bytes())

    def test_missing_backup_does_not_close_research_session(self):
        self.configure(backup=False)
        status = self.root / "docs" / "STATUS.md"
        before = status.read_bytes()
        with self.assertRaises(self.mod.DossierError) as caught:
            self.ds.close_session("SES-0001", status)
        self.assertEqual(4, caught.exception.exit_code)
        self.assertEqual(before, status.read_bytes())
        self.assert_not_confirmed(scope="session")

    def test_changed_notes_during_snapshot_cannot_be_silently_overwritten(self):
        status = self.root / "docs" / "STATUS.md"
        real_copy = self.mod.copy_verified
        changed = False

        def edit_after_first_copy(source, destination, expected=None):
            nonlocal changed
            result = real_copy(source, destination, expected)
            if not changed:
                status.write_text("# Concurrent invented edit\n", encoding="utf-8")
                changed = True
            return result

        with mock.patch.object(self.mod, "copy_verified", side_effect=edit_after_first_copy):
            with self.assertRaises(self.mod.DossierError):
                self.ds.close_session("SES-0001", status)
        self.assertTrue(changed)
        self.assertEqual("# Concurrent invented edit\n", status.read_text(encoding="utf-8"))

    def test_unmirrored_control_commit_cannot_report_complete(self):
        status = self.root / "docs" / "STATUS.md"
        real_replace = self.mod.os.replace
        blocked = False

        def block_backup_control(source, destination):
            nonlocal blocked
            dest = Path(destination)
            if self.backup_root in dest.parents and "control" in dest.parts:
                blocked = True
                raise OSError("invented control mirror failure")
            return real_replace(source, destination)

        with mock.patch.object(self.mod.os, "replace", side_effect=block_backup_control):
            with self.assertRaises((self.mod.DossierError, OSError)):
                self.ds.close_session("SES-0001", status)
        self.assertTrue(blocked, "Closure must attempt a separately mirrored control commit")
        journals = [json.loads(p.read_text(encoding="utf-8")) for p in (self.root / "evidence" / "metadata" / "control").glob("CHG-*.json")]
        self.assertTrue(any(j.get("state") == "recovery_required" for j in journals))


if __name__ == "__main__":
    unittest.main()
