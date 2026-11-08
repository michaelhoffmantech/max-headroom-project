"""Record/CLI acceptance checks using invented data in isolated temporary roots."""

import copy
import csv
import io
import json
from pathlib import Path
import subprocess
import sys
import unittest

import test_preservation as preservation


class DossierCase(unittest.TestCase):
    """Shared fixture helpers, without inheriting preservation test methods."""

    setUp = preservation.PreservationTests.setUp
    configure = preservation.PreservationTests.configure
    change = preservation.PreservationTests.change
    open_session = preservation.PreservationTests.open_session
    ingest = preservation.PreservationTests.ingest
    asset = preservation.PreservationTests.asset
    original_path = preservation.PreservationTests.original_path

    def row(self, identifier):
        return copy.deepcopy(self.ds.records()[identifier][1])

    def update(self, entity, identifier, fields):
        previous = self.row(identifier)
        return self.change([{
            "op": "update", "entity_type": entity, "id": identifier,
            "expected_revision": previous["revision"],
            "expected_hash": self.mod.record_hash(previous), "fields": fields,
        }])

    def create(self, entity, record):
        return self.change([{"op": "create", "entity_type": entity, "id": record["id"], "fields": record}])

    def common(self, identifier):
        return {"id": identifier, "revision": 1, "retired": False,
                "legacy_aliases_json": [], "unknowns_json": {}}


class RecordAcceptanceTests(DossierCase):
    def test_init_creates_unfilled_foundation_documents_and_planned_directories(self):
        other = self.mod.Dataset(self.base / "fresh-illustrative-dossier")
        other.init(preservation.FIXTURE, "illustrative")
        for relative in ["README.md", "docs/STATUS.md", "docs/METHODS.md", "docs/DECISIONS.md"]:
            with self.subTest(document=relative):
                path = other.root / relative
                self.assertTrue(path.is_file(), f"init must create missing foundation document {relative}")
                self.assertTrue(path.read_text(encoding="utf-8").strip())
        for relative in ["evidence/originals", "derived/transcripts", "derived/frames", "derived/audio",
                         "analysis/chronology", "analysis/engineering", "analysis/media-comparison", "analysis/culture",
                         "analysis/geography", "analysis/cycles", "reports/milestones", "private", "work"]:
            with self.subTest(directory=relative):
                self.assertTrue((other.root / relative).is_dir(), relative)

    def test_init_preserves_existing_notes_and_does_not_claim_research_completion(self):
        destination = self.base / "owner-notes-target"
        (destination / "docs").mkdir(parents=True)
        notes = {
            "README.md": b"# Owner entry point\nKeep this existing text unchanged.\n",
            "docs/STATUS.md": b"# Owner state\nResearch and backup remain pending.\n",
            "docs/METHODS.md": b"# Owner methods\nExisting evidence handling rules.\n",
        }
        for relative, content in notes.items():
            (destination / relative).write_bytes(content)
        other = self.mod.Dataset(destination)
        first = other.init(preservation.FIXTURE, "illustrative")
        second = other.init(preservation.FIXTURE, "illustrative")
        self.assertEqual(first["dataset_manifest"], second["dataset_manifest"])
        for relative, content in notes.items():
            with self.subTest(note=relative):
                self.assertEqual(content, (destination / relative).read_bytes())
        self.assertTrue(all(row["status"] == "queued" for entity, row in other.records().values() if entity == "tasks"))
        self.assertFalse([row for entity, row in other.records().values() if entity in {"assets", "findings", "backups"}])

    def test_dual_account_axes_and_year_precision_survive_csv_roundtrip(self):
        source = self.row("SRC-0001")
        self.assertEqual("yes", source["account_status_json"]["firsthand"])
        self.assertEqual("yes", source["account_status_json"]["retrospective"])
        self.assertEqual("2001", source["publication_date"])
        self.assertEqual("unknown", source["event_date"])
        self.assertIn("event_date", source["unknowns_json"])

    def test_idempotent_matching_seeds_do_not_rewrite_research(self):
        before = self.ds.manifest()
        result = self.ds.init(preservation.FIXTURE, "illustrative")
        self.assertEqual(before, result["dataset_manifest"])
        self.assertEqual([], result["changed_ids"])

    def test_conflicting_seed_init_retains_current_source(self):
        self.update("sources", "SRC-0001", {"title": "Accepted invented research revision"})
        before = self.ds.manifest()
        with self.assertRaises(self.mod.DossierError) as caught:
            self.ds.init(preservation.FIXTURE, "illustrative")
        self.assertEqual(3, caught.exception.exit_code)
        self.assertEqual(before, self.ds.manifest())

    def test_duplicate_seed_identifiers_are_rejected_without_collapse(self):
        seeds = json.loads(preservation.FIXTURE.read_text(encoding="utf-8"))
        duplicate = copy.deepcopy(seeds["registers"]["sources"][0])
        duplicate["title"] = "Conflicting duplicate invented source"
        seeds["registers"]["sources"].append(duplicate)
        other = self.mod.Dataset(self.base / "duplicate-seed-target")
        with self.assertRaises(self.mod.DossierError):
            other.init(seeds, "illustrative")
        self.assertFalse((other.root / "registers" / "sources.csv").exists())

    def test_fixture_seeds_cannot_initialize_actual_dataset(self):
        other = self.mod.Dataset(self.base / "actual-target")
        with self.assertRaises(self.mod.DossierError) as caught:
            other.init(preservation.FIXTURE, "actual")
        self.assertEqual("fixture_isolation", caught.exception.code)

    def test_unknown_scalar_requires_a_reason(self):
        source = self.row("SRC-0001")
        source["unknowns_json"].pop("event_date")
        with self.assertRaises(self.mod.DossierError):
            self.mod.validate_record("sources", source)

    def test_source_lineage_exposes_common_parent_and_rejects_cycle(self):
        self.assertEqual(["SRC-0001"], self.row("SRC-0002")["parent_source_ids_json"])
        before = self.ds.manifest()
        with self.assertRaises(self.mod.DossierError) as caught:
            self.update("sources", "SRC-0001", {"parent_source_ids_json": ["SRC-0002"]})
        self.assertEqual("dependency_cycle", caught.exception.code)
        self.assertEqual(before, self.ds.manifest())

    def test_dangling_parent_and_duplicate_alias_are_rejected(self):
        with self.assertRaises(self.mod.DossierError):
            self.update("sources", "SRC-0001", {"parent_source_ids_json": ["SRC-9999"]})
        with self.assertRaises(self.mod.DossierError):
            self.update("sources", "SRC-0002", {"legacy_aliases_json": ["S01"]})

    def test_retired_id_and_alias_cannot_be_reallocated(self):
        old = self.row("SRC-0007")
        self.change([{"op": "retire", "entity_type": "sources", "id": old["id"],
                      "expected_revision": old["revision"], "fields": {}}])
        self.assertTrue(self.row(old["id"])["retired"])
        with self.assertRaises(self.mod.DossierError):
            self.create("sources", old)
        next_source = self.row("SRC-0001")
        next_source.update(id="SRC-0008", revision=1, legacy_aliases_json=["S07"])
        with self.assertRaises(self.mod.DossierError):
            self.create("sources", next_source)

    def test_short_long_wrong_headers_and_unclosed_csv_quotes_fail(self):
        rows = [self.row("SRC-0001")]
        good = self.mod.register_bytes("sources", rows).decode("utf-8")
        parsed = list(csv.reader(io.StringIO(good)))
        variants = []
        for width_delta in [-1, 1]:
            values = parsed[1][:-1] if width_delta == -1 else parsed[1] + ["extra"]
            stream = io.StringIO(newline="")
            writer = csv.writer(stream, lineterminator="\n")
            writer.writerow(parsed[0]); writer.writerow(values)
            variants.append(stream.getvalue())
        variants += [good.replace("id,revision", "wrong,revision", 1), good.splitlines()[0] + '\n"unclosed\n']
        for n, content in enumerate(variants):
            with self.subTest(variant=n):
                path = self.base / f"bad-{n}.csv"
                path.write_text(content, encoding="utf-8")
                with self.assertRaises(self.mod.DossierError):
                    self.mod.read_register(path, "sources")

    def test_duplicate_json_keys_nonfinite_values_and_wrong_collection_types_fail(self):
        for payload in ['{"x":1,"x":2}', '{"x":NaN}', '{"x":Infinity}']:
            with self.subTest(payload=payload):
                with self.assertRaises(self.mod.DossierError):
                    self.mod.parse_json(payload)
        source = self.row("SRC-0001")
        source["parent_source_ids_json"] = "SRC-0002"
        with self.assertRaises(self.mod.DossierError):
            self.mod.validate_record("sources", source)

    def test_inaccessible_source_and_failed_search_do_not_become_negative_evidence(self):
        self.assertEqual("blocked", self.row("SRC-0003")["retrieval_status"])
        search = self.row("SRCH-0001")
        self.assertTrue(search["unsuccessful_results_json"])
        self.assertTrue(search["access_barriers_json"])
        self.assertFalse(search["useful_source_ids_json"])
        self.assertTrue(all(self.row(f"HYP-{n:04d}")["status"] == "untested" for n in range(1, 8)))

    def test_restore_creates_new_recovery_asset_without_replacing_original(self):
        asset_id, original = self.ingest()
        original_file = self.original_path(original)
        before = original_file.read_bytes()
        receipt = self.ds.backup(asset_id)["receipt_id"]
        target = self.root / "evidence" / "originals" / "clean-recovery.txt"
        result = self.ds.restore_asset(asset_id, receipt, target)
        recovered = self.asset(result["asset_id"])
        self.assertEqual("recovery_copy", recovered["kind"])
        self.assertEqual(asset_id, recovered["recovery_of_asset_id"])
        self.assertEqual(receipt, recovered["backup_receipt_id"])
        self.assertEqual(before, target.read_bytes())
        self.assertEqual(before, original_file.read_bytes())
        with self.assertRaises(self.mod.DossierError):
            self.ds.restore_asset(asset_id, receipt, target)

    def test_cli_relative_inputs_follow_invocation_cwd_and_json_envelope(self):
        invocation = self.base / "invocation"
        invocation.mkdir()
        (invocation / "local-seeds.json").write_bytes(preservation.FIXTURE.read_bytes())
        target = self.base / "cli-dataset"
        command = [sys.executable, str(preservation.TOOL_PATH), "--root", str(target), "--format", "json",
                   "init", "--seeds", "local-seeds.json", "--dataset-role", "illustrative"]
        completed = subprocess.run(command, cwd=invocation, capture_output=True, text=True)
        self.assertEqual(0, completed.returncode, completed.stderr or completed.stdout)
        result = json.loads(completed.stdout)
        self.assertEqual("illustrative", result["dataset_role"])
        self.assertEqual("init", result["command"])
        for key in ["schema_version", "changed_ids", "created_paths", "errors", "blockers", "gaps", "checks", "dataset_manifest"]:
            self.assertIn(key, result)
        self.assertTrue((target / "registers" / "sources.csv").is_file())


class MediaAcceptanceTests(DossierCase):
    def media_inputs(self):
        first, original = self.ingest()
        metadata = {key: copy.deepcopy(original[key]) for key in [
            "capture_date", "receiver_feed", "tape_generation", "original_media_history",
            "digitization_history", "completeness", "known_edits", "restrictions", "provenance_limits", "unknowns",
        ]}
        self.result = self.ds.ingest("SRC-0002", self.base / "invented-input.txt", metadata, "SES-0001")
        return [first, self.result["asset_id"]]

    def derivative(self, inputs, **overrides):
        path = self.root / "derived" / "frames" / "invented-comparison.txt"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"ILLUSTRATIVE comparison output; not a recovered frame\n")
        values = {
            "kind": "derivative", "source_id": None, "acquired_at": self.mod.utcnow(),
            "storage": {"alias": "project", "relative_path": "derived/frames/invented-comparison.txt", "access_limit": "fixture"},
            **self.mod.hash_file(path), "capture_date": None, "receiver_feed": None, "tape_generation": None,
            "original_media_history": "Invented text, not historical media", "digitization_history": "No digitization",
            "completeness": "complete", "known_edits": [], "restrictions": "Fixture only",
            "provenance_limits": "Invented sources; no authenticated capture or recovered detail",
            "input_asset_ids": inputs, "input_locators": [],
            "processing": {
                "method": "Compare invented text bytes", "settings": {"copy_bytes": True},
                "executable": "python", "tool_version": "illustrative fixture 1", "arguments": ["--invented"],
                "time_base": "not_applicable: generated text has no media clock",
                "stream_notes": "No analog timing/interlacing exists in generated fixture text",
                "output_sha256": self.mod.hash_file(path)["sha256"],
                "generative": False, "claimed_as_recovered_evidence": False,
            },
        }
        values.update(overrides)
        return self.mod.sidecar("assets", "AST-0003", **values)

    def test_identical_bytes_do_not_merge_sources_or_all_derivative_inputs(self):
        inputs = self.media_inputs()
        self.assertNotEqual(inputs[0], inputs[1])
        self.assertEqual(self.asset(inputs[0])["sha256"], self.asset(inputs[1])["sha256"])
        self.assertEqual("SRC-0001", self.asset(inputs[0])["source_id"])
        self.assertEqual("SRC-0002", self.asset(inputs[1])["source_id"])
        derivative = self.derivative(inputs)
        self.create("assets", derivative)
        saved = self.asset(derivative["id"])
        self.assertEqual(inputs, saved["input_asset_ids"])
        self.assertIsNone(saved["source_id"])
        self.assertEqual(["SRC-0001"], self.row("SRC-0002")["parent_source_ids_json"])

    def test_multisource_derivative_rejects_arbitrary_single_source_parent(self):
        inputs = self.media_inputs()
        bad = self.derivative(inputs, source_id="SRC-0001")
        with self.assertRaises(self.mod.DossierError):
            self.create("assets", bad)

    def test_derivative_requires_complete_reproducible_processing_manifest(self):
        inputs = self.media_inputs()
        good = self.derivative(inputs)
        for key in ["method", "settings", "executable", "tool_version", "arguments", "time_base", "output_sha256", "stream_notes"]:
            with self.subTest(missing=key):
                bad = copy.deepcopy(good)
                bad["processing"].pop(key)
                with self.assertRaises(self.mod.DossierError):
                    self.ds._validate_sidecar("assets", bad)

    def test_lost_timing_and_interlacing_remain_explicit_limits(self):
        inputs = self.media_inputs()
        derivative = self.derivative(inputs)
        derivative["processing"]["time_base"] = "unknown: supplied derivative already lost timing"
        derivative["processing"]["stream_notes"] = "Interlacing absent in input; cannot be recovered"
        derivative["provenance_limits"] = "Shared cropping/damage may come from copying; capture independence unestablished"
        self.create("assets", derivative)
        saved = self.asset(derivative["id"])
        self.assertIn("already lost", saved["processing"]["time_base"])
        self.assertIn("cannot be recovered", saved["processing"]["stream_notes"])
        self.assertIn("independence unestablished", saved["provenance_limits"])

    def test_time_location_requires_recording_basis_or_explicit_uncertainty(self):
        claim = self.row("CLM-0001")
        claim.update(id="CLM-0003", revision=1)
        claim["supporting_evidence_json"][0]["locator"] = {
            "kind": "time", "value": "00:00:01", "precision": "approximate",
            "description": "Invented disputed passage without a recording basis",
        }
        with self.assertRaises(self.mod.DossierError):
            self.create("claims", claim)
        claim["supporting_evidence_json"][0]["locator"]["uncertainty"] = "Recording asset and time base are unknown; inherited transcript lead only"
        self.create("claims", claim)
        self.assertIn("unknown", self.row("CLM-0003")["supporting_evidence_json"][0]["locator"]["uncertainty"])

    def test_generative_output_cannot_be_claimed_as_recovered_evidence(self):
        inputs = self.media_inputs()
        derivative = self.derivative(inputs)
        derivative["processing"].update(generative=True, claimed_as_recovered_evidence=True)
        with self.assertRaises(self.mod.DossierError):
            self.create("assets", derivative)

    def test_unclear_reading_keeps_alternatives_without_claiming_supported_words(self):
        self.update("claims", "CLM-0001", {
            "proposition": "Invented disputed audio: [unclear]; two readings remain possible",
            "category": "inference", "confidence": "unassessed",
            "confidence_reasons": "No blind second transcription is available",
            "caveats_json": ["Alternative reading A", "Alternative reading B", "Blind review waiting; no supported wording"],
        })
        claim = self.row("CLM-0001")
        self.assertIn("[unclear]", claim["proposition"])
        self.assertEqual("unassessed", claim["confidence"])
        self.assertEqual(3, len(claim["caveats_json"]))
        self.assertFalse([r for entity, r in self.ds.records().values() if entity == "findings"])

    def test_period_source_date_must_be_real_and_partial_precision_is_retained(self):
        source = self.row("SRC-0007")
        with self.assertRaises(self.mod.DossierError):
            self.update("sources", source["id"], {"publication_date": "1987-11-32"})
        precision = source["date_precision_json"]
        precision["publication_date"] = {"precision": "year", "basis": "Invented period catalog fixture; month/day not established"}
        self.update("sources", source["id"], {"publication_date": "1987", "date_precision_json": precision,
                                              "provenance_limits": "Invented widespread-availability lead, not evidence of participation"})
        self.assertEqual("1987", self.row(source["id"])["publication_date"])
        self.assertFalse([r for entity, r in self.ds.records().values() if entity == "findings"])


class RecordIntegrityRegressionTests(DossierCase):
    def test_changed_published_change_payload_conflicts_even_when_current_rows_match(self):
        current = self.ds.manifest()
        change_file = sorted((self.root / "evidence" / "metadata" / "changes").glob("CHG-*.json"))[0]
        change = json.loads(change_file.read_text(encoding="utf-8"))
        change["reason"] = "Tampered invented retained reasoning while current rows remain untouched"
        change_file.write_bytes(self.mod.json_bytes(change))
        self.assertEqual(current, self.ds.manifest())
        for operation in [
            lambda: self.ds.validate("records"),
            lambda: self.update("sources", "SRC-0001", {"title": "Must not publish over damaged history"}),
        ]:
            with self.subTest(operation=operation):
                with self.assertRaises(self.mod.DossierError) as caught:
                    operation()
                self.assertEqual(3, caught.exception.exit_code)
                self.assertEqual(current, self.ds.manifest())

    def test_generic_apply_cannot_forge_a_confirmed_backup_receipt(self):
        asset_id, _ = self.ingest()
        self.result = self.ds.backup(asset_id)
        genuine = self.row(self.result["receipt_id"])
        self.assertEqual("confirmed", genuine["result"])
        forged = copy.deepcopy(genuine)
        forged.update(id="BAK-0002", revision=1, created_at=self.mod.utcnow())
        before = self.ds.manifest()
        with self.assertRaises(self.mod.DossierError):
            self.create("backups", forged)
        self.assertEqual(before, self.ds.manifest())
        self.assertNotIn("BAK-0002", self.ds.records())

    def test_original_identity_cannot_be_rewritten_to_hide_changed_content(self):
        identifier, asset = self.ingest()
        variants = [
            {"sha256": "0" * 64}, {"byte_count": asset["byte_count"] + 1},
            {"storage": {"alias": "primary_evidence", "relative_path": "different.txt", "access_limit": "fixture"}},
            {"kind": "derivative"},
        ]
        for fields in variants:
            with self.subTest(fields=fields):
                with self.assertRaises(self.mod.DossierError):
                    self.update("assets", identifier, fields)
                self.assertEqual(asset, self.asset(identifier))

    def test_reference_fields_reject_valid_ids_of_wrong_entity_type(self):
        with self.assertRaises(self.mod.DossierError):
            self.update("sources", "SRC-0001", {"parent_source_ids_json": ["CLM-0001"]})
        with self.assertRaises(self.mod.DossierError):
            self.update("hypotheses", "HYP-0001", {"supporting_claim_ids_json": ["SRC-0001"]})

    def test_nested_exclusion_evidence_requires_existing_source_and_revision(self):
        for source_id, revision in [("SRC-9999", 1), ("SRC-0001", 999)]:
            with self.subTest(source=source_id, revision=revision):
                ev = copy.deepcopy(self.row("CLM-0001")["supporting_evidence_json"][0])
                ev.update(source_id=source_id, source_revision=revision)
                with self.assertRaises(self.mod.DossierError):
                    self.update("hypotheses", "HYP-0001", {"status": "ruled_out", "exclusion_json": {
                        "failed_condition": "Invented measured necessary-condition failure", "evidence_refs": [ev],
                        "assumptions": ["Invented bounded measurement"], "exclusion_scope": "Only invented fixture",
                    }})


if __name__ == "__main__":
    unittest.main()
