"""Chronology, cycle, review, and external-action boundaries on invented data."""

import copy
from contextlib import redirect_stderr
from datetime import timedelta
import io
from pathlib import Path
import subprocess
import unittest
from unittest import mock

import test_records as records


class WorkflowCase(records.DossierCase):
    def cycle(self, **overrides):
        values = {
            "question": "Which invented boundary explains the difference?",
            "alternatives": ["Different invented boundaries", "Rounded invented reporting"],
            "necessary_conditions": [{"description": "The invented accounts describe the same fixture"}],
            "predictions": [{"description": "Boundary definitions distinguish the alternatives"}],
            "evidence_needs": ["Two invented accounts"], "dependencies": [],
            "expected_output": "An explicitly illustrative comparison", "timebox": "one test run",
            "planned_by": "fixture author", "search_ids": [], "input_assets": [],
            "input_claims": [{"id": "CLM-0001", "revision": 1}], "state": "planned",
            "strongest_alternative": "The invented source accounts may be dependent",
            "source_dependence": "SRC-0002 repeats SRC-0001", "hidden_assumptions": [],
            "reversal_evidence": "An independent invented account with exact boundaries",
            "hypothesis_changes": [], "finding_ids": [], "limitations": ["Invented fixture only"],
        }
        values.update(overrides)
        cycle = self.mod.sidecar("cycles", "CYC-0001", **values)
        self.create("cycles", cycle)
        return self.row("CYC-0001")

    def review(self, target, review_type="extraction", identifier="RVW-0001", **overrides):
        values = {
            "review_type": review_type, "target": target,
            "author_identity": "fixture author", "author_type": "AI",
            "reviewer_identity": "separate fixture reviewer", "reviewer_type": "AI",
            "reviewer_instance": "isolated invented reviewer instance",
            "preferred_theory_exposure": "withheld", "exposure_rationale": "Invented blind exercise",
            "evidence_inspected": [{"id": "SRC-0001", "revision": 1}],
            "findings": ["Only an invented account is supported; not historical evidence"],
            "unresolved_specialist_questions": [], "reviewed_at": self.mod.utcnow(),
            "decision": "accepted", "superseded_review_id": None,
        }
        values.update(overrides)
        review = self.mod.sidecar("reviews", identifier, **values)
        self.create("reviews", review)
        return self.row(identifier)

    def milestone_target(self, identifier="RVW-0001", with_basis_file=False):
        path = self.root / "reports" / "milestones" / "foundation.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("# Invented foundation review\nDecision: continue an illustrative exercise.\n", encoding="utf-8")
        ref = lambda relative: {"alias": "project", "relative_path": relative, "access_limit": "fixture only"}
        target = {
            "kind": "milestone_document", "milestone": "foundation",
            "document": ref("reports/milestones/foundation.md"),
            **self.mod.hash_file(path),
            "reviewed_copy": ref(f"reports/findings/reviews/artifacts/{identifier}/foundation.md"),
            "basis_records": [{"id": "CLM-0001", "revision": 1}, {"id": "SRC-0001", "revision": 1}],
            "basis_files": [],
        }
        if with_basis_file:
            basis = self.root / "analysis" / "chronology" / "fixture-basis.md"
            basis.parent.mkdir(parents=True, exist_ok=True)
            basis.write_text("An invented supporting note.\n", encoding="utf-8")
            target["basis_files"].append({
                "file": ref("analysis/chronology/fixture-basis.md"), **self.mod.hash_file(basis),
                "reviewed_copy": ref(f"reports/findings/reviews/artifacts/{identifier}/basis.md"),
            })
        return target

    def finding(self, cycle_id, **overrides):
        path = self.root / "reports" / "findings" / "FND-0001.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("# Invented finding\nThis is an illustrative account only, not a historical conclusion.\n", encoding="utf-8")
        evidence = copy.deepcopy(self.row("CLM-0001")["supporting_evidence_json"])
        evidence[0]["source_revision"] = self.row("SRC-0001")["revision"]
        values = {
            "cycle_id": cycle_id, "question": "What does the invented account support?",
            "claims": [{"id": "CLM-0001", "revision": 1}], "evidence": evidence,
            "method": "Read the invented passage", "result": "Only an invented report is supported",
            "confidence": "unassessed", "confidence_reasons": "Illustrative source, not evidence",
            "alternatives": ["The invented account may be dependent"], "limitations": ["Fixture only"],
            "next_action": "Obtain an independent invented account",
            "narrative": {"alias": "project", "relative_path": "reports/findings/FND-0001.md", "access_limit": "fixture", "sha256": self.mod.hash_file(path)["sha256"]},
            "audience": "owner_and_selected_reviewers", "access_limits": "Fixture only",
            "novelty_category": None, "novelty_search_ids": [],
        }
        values.update(overrides)
        result = self.mod.sidecar("findings", "FND-0001", **values)
        self.create("findings", result)
        return self.row("FND-0001")


class BaselineAcceptanceTests(WorkflowCase):
    def test_conflicting_duration_reports_and_unknown_clock_offset_survive(self):
        row = self.common("EVT-0001")
        row.update(station="WGN-TV", event="Invented disagreement exercise", phase="total_disruption",
                   time_local_start="unknown", time_local_end="unknown", timezone_label="Chicago local time",
                   utc_offset="unknown", clock_source="Two invented accounts; no observed clock",
                   precision="approximate source reports, not measured duration", reception_paths_json=[],
                   recording_boundaries_json=[], related_claim_ids_json=["CLM-0001", "CLM-0002"],
                   competing_reports_json=[
                       {"claim_id": "CLM-0001", "reported_interval": "roughly 25 seconds", "clock_source": "invented report A", "precision": "approximate", "caveat": "Invented test value"},
                       {"claim_id": "CLM-0002", "reported_interval": "roughly 30 seconds", "clock_source": "invented report B", "precision": "approximate", "caveat": "Invented test value"},
                   ])
        row["unknowns_json"] = {k: "No measured clock in this illustrative exercise" for k in ["time_local_start", "time_local_end", "utc_offset"]}
        self.create("timeline", row)
        saved = self.row("EVT-0001")
        self.assertEqual("unknown", saved["utc_offset"])
        self.assertEqual("unknown", saved["time_local_start"])
        self.assertEqual(2, len(saved["competing_reports_json"]))
        self.assertNotEqual(saved["competing_reports_json"][0]["reported_interval"], saved["competing_reports_json"][1]["reported_interval"])

    def test_baseline_requires_foundation_review_instead_of_seed_counts_alone(self):
        result = self.ds.validate("baseline")
        self.assertEqual("blocked", result["status"])
        self.assertIn("foundation_review", {item["code"] for item in result["blockers"]})
        self.assertNotEqual("ready", result["readiness"])

    def test_unexamined_sources_do_not_satisfy_actual_baseline(self):
        self.ds.role = "actual"  # Exercise actual gate logic without publishing/relabeling fixture files.
        result = self.ds.validate("baseline")
        self.assertIn("actual_inspected_sources", {item["code"] for item in result["blockers"]})
        self.assertIn("contemporary_survey", {item["code"] for item in result["blockers"]})


class CycleAcceptanceTests(WorkflowCase):
    def test_system_freezes_original_predictions_and_ignores_backdated_request(self):
        before = self.mod.timestamp(self.mod.utcnow())
        cycle = self.cycle(frozen_at="1900-01-01T00:00:00Z", frozen_plan_sha256="invented")
        self.assertGreaterEqual(self.mod.timestamp(cycle["frozen_at"]), before)
        self.assertEqual(self.mod.record_hash(cycle["plan"]), cycle["frozen_plan_sha256"])
        original = copy.deepcopy(cycle["plan"])
        with self.assertRaises(self.mod.DossierError):
            self.update("cycles", cycle["id"], {"predictions": [{"description": "Preferred idea invented after searching"}]})
        self.assertEqual(original, self.row(cycle["id"])["plan"])

    def test_cycle_search_cannot_predate_frozen_plan(self):
        cycle = self.cycle()
        search = self.row("SRCH-0001")
        search.update(id="SRCH-0002", revision=1, cycle_id=cycle["id"], executed_at=(self.mod.timestamp(cycle["frozen_at"]) - timedelta(seconds=1)).isoformat())
        search["unknowns_json"].pop("cycle_id", None)
        with self.assertRaises(self.mod.DossierError) as caught:
            self.create("searches", search)
        self.assertEqual("search_order", caught.exception.code)

    def test_unperformed_cycle_cannot_be_marked_tested(self):
        cycle = self.cycle()
        self.result = self.ds.start_analysis(cycle["id"])
        with self.assertRaises(self.mod.DossierError) as caught:
            self.update("cycles", cycle["id"], {"state": "tested", "test_performed": False,
                                               "method": "Unperformed method", "result": "Invented unsupported result"})
        self.assertEqual("actual_test", caught.exception.code)
        self.assertEqual("active", self.row(cycle["id"])["state"])

    def test_unprotected_original_blocks_analysis_start(self):
        asset_id, asset = self.ingest()
        cycle = self.cycle(input_assets=[{"id": asset_id, "revision": asset["revision"], "sha256": asset["sha256"]}])
        with self.assertRaises(self.mod.DossierError) as caught:
            self.ds.start_analysis(cycle["id"])
        self.assertEqual(4, caught.exception.exit_code)
        self.assertIsNone(self.row(cycle["id"])["analysis_started_at"])
        self.assertEqual("planned", self.row(cycle["id"])["state"])

    def test_required_missing_tool_blocks_only_the_affected_cycle(self):
        cycle = self.cycle(required_tools=["invented_fixture_executable_that_cannot_exist_7c71"])
        with self.assertRaises(self.mod.DossierError) as caught:
            self.ds.start_analysis(cycle["id"])
        self.assertEqual(4, caught.exception.exit_code)
        self.assertEqual("ok", self.ds.validate("records")["status"])

    def test_required_blind_listening_task_blocks_cycle_while_queued(self):
        cycle = self.cycle(dependencies=[{"id": "TASK-0007", "note": "Required blind second transcription before disputed audio interpretation"}])
        with self.assertRaises(self.mod.DossierError) as caught:
            self.ds.start_analysis(cycle["id"])
        self.assertEqual(4, caught.exception.exit_code)
        self.assertEqual("planned", self.row(cycle["id"])["state"])

    def test_missing_record_is_not_an_evidenced_necessary_condition_failure(self):
        with self.assertRaises(self.mod.DossierError) as caught:
            self.update("hypotheses", "HYP-0001", {"status": "ruled_out", "exclusion_json": {
                "failed_condition": "An invented archive query returned no result", "evidence_refs": [],
                "assumptions": ["Absence was incorrectly assumed to prove failure"], "exclusion_scope": "Invented exercise",
            }})
        self.assertEqual("exclusion", caught.exception.code)
        self.assertEqual("untested", self.row("HYP-0001")["status"])

    def test_reopening_exclusion_requires_new_evidence_or_changed_assumption(self):
        evidence = self.row("CLM-0001")["supporting_evidence_json"]
        self.update("hypotheses", "HYP-0001", {"status": "ruled_out", "exclusion_json": {
            "failed_condition": "The invented necessary condition was measured to fail", "evidence_refs": evidence,
            "assumptions": ["Invented account is accurate within this isolated exercise"], "exclusion_scope": "Only the invented condition",
        }})
        with self.assertRaises(self.mod.DossierError):
            self.update("hypotheses", "HYP-0001", {"status": "unresolved", "exclusion_json": {}})
        self.assertEqual("ruled_out", self.row("HYP-0001")["status"])

    def test_metadata_only_cycle_or_delivery_can_never_be_ready(self):
        for gate in ["cycle", "delivery"]:
            with self.subTest(gate=gate):
                result = self.ds.validate(gate)
                self.assertEqual("blocked", result["status"])
                self.assertIn("file_verification_required", {x["code"] for x in result["blockers"]})
                self.assertNotEqual("ready", result["readiness"])
        actual_check = self.ds.validate("delivery", True)
        self.assertIn("actual_dataset_required", {x["code"] for x in actual_check["blockers"]})


class ReviewAcceptanceTests(WorkflowCase):
    def test_record_review_attaches_without_changing_reviewed_claim(self):
        path = self.root / "registers" / "claims.csv"
        before = path.read_bytes()
        review = self.review({"kind": "record", "id": "CLM-0001", "revision": 1})
        self.assertEqual(before, path.read_bytes())
        self.assertEqual(1, self.row("CLM-0001")["revision"])
        self.assertTrue(self.ds._valid_review(review))
        self.update("claims", "CLM-0001", {"proposition": "A changed invented proposition needs re-review"})
        self.assertFalse(self.ds._valid_review(review))

    def test_same_author_identity_cannot_be_relabelled_separate_review(self):
        with self.assertRaises(self.mod.DossierError) as caught:
            self.review({"kind": "record", "id": "CLM-0001", "revision": 1}, reviewer_identity="fixture author")
        self.assertEqual("separate_reviewer", caught.exception.code)

    def test_blind_transcription_rejects_exposure_to_preferred_wording(self):
        with self.assertRaises(self.mod.DossierError) as caught:
            self.review({"kind": "record", "id": "CLM-0001", "revision": 1}, review_type="blind_transcription", preferred_theory_exposure="shown preferred wording")
        self.assertEqual("blind_review", caught.exception.code)

    def test_milestone_copies_are_fixed_and_unrelated_edits_do_not_invalidate(self):
        target = self.milestone_target(with_basis_file=True)
        original = self.ds.resolve(target["document"]).read_bytes()
        review = self.review(target, review_type="milestone")
        self.assertEqual(original, self.ds.resolve(target["document"]).read_bytes())
        self.assertEqual(original, self.ds.resolve(target["reviewed_copy"]).read_bytes())
        self.assertEqual(self.ds.resolve(target["basis_files"][0]["file"]).read_bytes(), self.ds.resolve(target["basis_files"][0]["reviewed_copy"]).read_bytes())
        self.update("sources", "SRC-0007", {"title": "Unrelated invented edit"})
        self.assertTrue(self.ds._valid_review(review))
        self.update("claims", "CLM-0001", {"proposition": "Changed relied-on invented claim"})
        self.assertFalse(self.ds._valid_review(review))
        self.assertTrue(self.ds._valid_review(review, current=False))

    def test_missing_milestone_basis_or_mismatched_hash_is_rejected(self):
        target = self.milestone_target()
        target.pop("basis_records")
        with self.assertRaises(self.mod.DossierError):
            self.review(target, review_type="milestone")
        target = self.milestone_target()
        target["sha256"] = "0" * 64
        with self.assertRaises(self.mod.DossierError) as caught:
            self.review(target, review_type="milestone")
        self.assertEqual(5, caught.exception.exit_code)
        self.assertFalse(list((self.root / "reports/findings/reviews/artifacts").rglob("foundation.md")))

    def test_edited_milestone_stays_historical_without_mutating_review_copy(self):
        target = self.milestone_target()
        review = self.review(target, review_type="milestone")
        preserved = self.ds.resolve(target["reviewed_copy"]).read_bytes()
        self.ds.resolve(target["document"]).write_text("Changed invented review document\n", encoding="utf-8")
        self.assertFalse(self.ds._valid_review(review))
        self.assertTrue(self.ds._valid_review(review, current=False))
        self.assertEqual(preserved, self.ds.resolve(target["reviewed_copy"]).read_bytes())

    def test_privacy_rejection_does_not_become_shareable_review(self):
        review = self.review({"kind": "record", "id": "CLM-0001", "revision": 1},
                             decision="rejected", findings=["Uncorroborated invented personal allegation must remain outside findings"],
                             unresolved_specialist_questions=["Independent evidence is absent"])
        self.assertFalse(self.ds._valid_review(review))
        self.assertFalse([r for entity, r in self.ds.records().values() if entity == "findings"])


class ExternalResearchAcceptanceTests(WorkflowCase):
    def test_partial_release_keeps_release_context_and_completeness_limits(self):
        self.update("sources", "SRC-0003", {
            "source_type": "agency release", "completeness": "partial",
            "inspection_json": {"text": "invented pages inspected", "linked_media": "not applicable", "underlying_records": "unverified", "limits": "Invented pages 2-3 only; no release letter or agency identifier"},
            "provenance_limits": "Partial third-party fixture copy; missing pagination context prevents complete-file authentication",
        })
        row = self.row("SRC-0003")
        self.assertEqual("partial", row["completeness"])
        self.assertEqual("unverified", row["inspection_json"]["underlying_records"])
        self.assertIn("missing pagination", row["provenance_limits"])

    def test_unconfirmed_holding_and_unknown_custodian_stay_explicit(self):
        source = self.row("SRC-0003")
        unknowns = source["unknowns_json"]
        unknowns["source_locator"] = "Invented holdings directory does not confirm a custodian or available item"
        self.update("sources", "SRC-0003", {"source_locator": "unknown", "unknowns_json": unknowns,
                                            "provenance_limits": "No holding, access, custodian, or release context confirmed"})
        row = self.row("SRC-0003")
        self.assertEqual("unknown", row["source_locator"])
        self.assertEqual("blocked", row["retrieval_status"])

    def test_sender_purchase_and_interview_execution_commands_are_absent(self):
        before = self.ds.manifest()
        for action in ["send", "publish", "purchase", "submit-request", "interview"]:
            with self.subTest(action=action):
                with redirect_stderr(io.StringIO()):
                    with self.assertRaises(SystemExit) as caught:
                        self.mod.main(["--root", str(self.root), action])
                self.assertEqual(2, caught.exception.code)
        self.assertEqual(before, self.ds.manifest())


class WorkflowIntegrityRegressionTests(WorkflowCase):
    def test_unknown_review_decision_cannot_clear_readiness(self):
        with self.assertRaises(self.mod.DossierError):
            self.review({"kind": "record", "id": "CLM-0001", "revision": 1}, decision="unrecognized invented decision")

    def test_a_receipt_for_another_session_cannot_complete_new_session(self):
        self.result = self.ds.close_session("SES-0001", self.root / "docs" / "STATUS.md")
        first = self.row("SES-0001")
        self.assertTrue(self.ds._closure_complete(first))
        forged = copy.deepcopy(first)
        forged.update(id="SES-0002", revision=1, created_at=self.mod.utcnow(), started_at=self.mod.utcnow())
        try:
            self.create("sessions", forged)
        except self.mod.DossierError:
            return  # Rejection at publication is also valid; it must never become complete.
        self.assertFalse(self.ds._closure_complete(self.row("SES-0002")))

    def test_new_research_note_after_snapshot_invalidates_current_closure(self):
        self.result = self.ds.close_session("SES-0001", self.root / "docs" / "STATUS.md")
        session = self.row("SES-0001")
        self.assertTrue(self.ds._closure_complete(session, current=True))
        (self.root / "docs" / "new-invented-note.md").write_text("New research note requires another snapshot.\n", encoding="utf-8")
        self.assertFalse(self.ds._closure_complete(session, current=True))
        self.assertTrue(self.ds._closure_complete(session, current=False))

    def test_inherited_inspection_does_not_count_as_new_actual_source_review(self):
        source = self.row("SRC-0001")
        inspection = source["inspection_json"]
        inspection.update(text="read text inherited from planning", inherited_only=True)
        self.update("sources", source["id"], {"access_date": "2001-01-01", "inspection_json": inspection})
        self.ds.role = "actual"  # Gate exercise only; fixture files remain explicitly illustrative.
        result = self.ds.validate("baseline")
        self.assertIn("actual_inspected_sources", {item["code"] for item in result["blockers"]})

    def test_cycle_cannot_forge_a_verified_analysis_start_through_apply(self):
        cycle = self.cycle()
        with self.assertRaises(self.mod.DossierError):
            self.update("cycles", cycle["id"], {
                "state": "tested", "test_performed": True, "analysis_started_at": self.mod.utcnow(),
                "analysis_input_manifest": [], "method": "Invented method", "result": "Invented result",
            })
        self.assertEqual("planned", self.row(cycle["id"])["state"])

    def test_recorded_analysis_start_and_input_manifest_are_immutable(self):
        cycle = self.cycle()
        self.result = self.ds.start_analysis(cycle["id"])
        started = self.row(cycle["id"])
        self.assertTrue(started["analysis_input_manifest"])
        for field, value in [
            ("analysis_started_at", (self.mod.timestamp(started["analysis_started_at"]) + timedelta(seconds=1)).isoformat()),
            ("analysis_input_manifest", []),
        ]:
            with self.subTest(field=field):
                with self.assertRaises(self.mod.DossierError):
                    self.update("cycles", cycle["id"], {field: value})
                self.assertEqual(started[field], self.row(cycle["id"])[field])

    def test_finding_review_becomes_stale_when_its_source_basis_changes(self):
        cycle = self.cycle()
        finding = self.finding(cycle["id"])
        review = self.review({"kind": "record", "id": finding["id"], "revision": 1}, review_type="finding")
        self.assertTrue(self.ds._valid_review(review))
        self.update("sources", "SRC-0001", {"provenance_limits": "Changed source basis now needs re-review"})
        self.assertFalse(self.ds._valid_review(review))
        self.assertEqual(1, self.row(finding["id"])["revision"])

    def test_novelty_assertion_requires_preserved_prior_coverage_search(self):
        cycle = self.cycle()
        with self.assertRaises(self.mod.DossierError) as caught:
            self.finding(cycle["id"], novelty_category="potentially_new_contribution", novelty_search_ids=[])
        self.assertEqual("novelty_search", caught.exception.code)


class ToolDependencyAcceptanceTests(WorkflowCase):
    def tool_context(self, expected="7.1"):
        executable = self.base / "invented-ffprobe.exe"
        executable.write_bytes(b"Mocked executable bytes; never executed")
        cycle = self.cycle(required_tools=[{
            "executable": "ffprobe", "expected_version": expected,
            "arguments": ["-show_streams", "-of", "json"],
        }])
        return cycle, executable

    def test_required_tool_version_is_probed_and_manifest_is_command_owned(self):
        cycle, executable = self.tool_context()
        completed = subprocess.CompletedProcess([str(executable), "-version"], 0, stdout="ffprobe version 7.1 Copyright fixture\n", stderr="")
        with mock.patch.object(self.mod.shutil, "which", return_value=str(executable)):
            with mock.patch("subprocess.run", return_value=completed) as probe:
                self.result = self.ds.start_analysis(cycle["id"])
        probe.assert_called_once()
        command = probe.call_args.args[0]
        self.assertEqual([str(executable), "-version"], command)
        self.assertFalse(probe.call_args.kwargs.get("shell", False))
        self.assertGreater(probe.call_args.kwargs.get("timeout", 0), 0)
        started = self.row(cycle["id"])
        manifest = started["analysis_tool_manifest"]
        self.assertEqual(1, len(manifest))
        self.assertEqual("ffprobe", manifest[0]["executable"])
        self.assertEqual(str(executable), manifest[0]["resolved_path"])
        self.assertEqual("7.1", manifest[0]["version"])
        self.assertEqual(["-show_streams", "-of", "json"], manifest[0]["arguments"])
        changed = copy.deepcopy(manifest)
        changed[0]["version"] = "invented later replacement"
        with self.assertRaises(self.mod.DossierError):
            self.update("cycles", cycle["id"], {"analysis_tool_manifest": changed})
        self.assertEqual(manifest, self.row(cycle["id"])["analysis_tool_manifest"])

    def test_unexpected_tool_version_blocks_start_without_analysis_result(self):
        cycle, executable = self.tool_context(expected="7.1")
        completed = subprocess.CompletedProcess([str(executable), "-version"], 0, stdout="ffprobe version 8.0 Copyright fixture\n", stderr="")
        with mock.patch.object(self.mod.shutil, "which", return_value=str(executable)):
            with mock.patch("subprocess.run", return_value=completed):
                with self.assertRaises(self.mod.DossierError) as caught:
                    self.ds.start_analysis(cycle["id"])
        self.assertEqual(4, caught.exception.exit_code)
        self.assertEqual("planned", self.row(cycle["id"])["state"])
        self.assertIsNone(self.row(cycle["id"])["analysis_started_at"])

    def test_metadata_validation_does_not_probe_analysis_executables(self):
        self.tool_context()
        with mock.patch("subprocess.run", side_effect=AssertionError("Metadata-only validation must not execute media tools")) as probe:
            result = self.ds.validate("records")
        probe.assert_not_called()
        self.assertEqual("ok", result["status"])
        self.assertEqual("structure_only", result["readiness"])


class StructuredRecordsResearchAcceptanceTests(WorkflowCase):
    def context(self, kind):
        if kind == "agency_release":
            return {
                "kind": kind, "agency_identifiers": ["INVENTED-CASE-1"],
                "release_letter_evidence": copy.deepcopy(self.row("CLM-0001")["supporting_evidence_json"]),
                "pagination": "Invented pages 2-3 of an incomplete release",
                "authentication_limits": "Illustrative partial third-party copy; not authenticated as a complete file",
            }
        return {
            "kind": "holding", "institution": "Invented fixture archive", "holding_identifier": "unknown",
            "access_status": "unconfirmed", "confirmation_evidence": [],
            "limits": "A directory lead does not confirm this item or access",
            "unknowns": {"holding_identifier": "No item or custodian has been confirmed"},
        }

    def set_context(self, context):
        inspection = self.row("SRC-0003")["inspection_json"]
        inspection["records_context"] = context
        return self.update("sources", "SRC-0003", {"inspection_json": inspection, "completeness": "partial"})

    def draft(self, kind="request_draft", **overrides):
        name = "invented-request.md" if kind == "request_draft" else "invented-interview.md"
        path = self.root / "reports" / "requests" / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("# Unsent illustrative draft\nNo external action is authorized.\n", encoding="utf-8")
        result = {
            "kind": kind,
            "file": {"alias": "project", "relative_path": path.relative_to(self.root).as_posix(), "access_limit": "fixture"},
            "sha256": self.mod.hash_file(path)["sha256"], "status": "unsent",
        }
        if kind == "request_draft":
            result.update(records_requested=["Existing invented incident log"], custodian="Invented archive custodian",
                          date_range="1987-11-22 through 1988-01-01", analytical_gap="No incident log was found",
                          analytical_value="A log could distinguish invented monitoring accounts")
        else:
            result["prompts"] = {
                "personal_observation": "What did you personally observe?", "affected_feed": "Which monitor or feed?",
                "actions_taken": "What did you do?", "later_information": "What did you learn later or from reporting?",
                "verifying_records": "What surviving record could verify this?",
            }
        result.update(overrides)
        return result

    def test_release_context_missing_required_pagination_is_rejected(self):
        context = self.context("agency_release")
        context.pop("pagination")
        with self.assertRaises(self.mod.DossierError):
            self.set_context(context)

    def test_unknown_release_context_remains_named_gap_without_authentication_upgrade(self):
        context = self.context("agency_release")
        context.update(agency_identifiers=[], release_letter_evidence=[], pagination="unknown",
                       unknowns={"agency_identifiers": "No agency number confirmed", "release_letter_evidence": "Release letter unavailable", "pagination": "Only an unnumbered extract survives"})
        self.set_context(context)
        result = self.ds.validate("records")
        self.assertIn("records_context_gap", {gap["code"] for gap in result["gaps"]})
        self.assertEqual("partial", self.row("SRC-0003")["completeness"])
        self.assertEqual("unverified", self.row("SRC-0003")["inspection_json"]["underlying_records"])

    def test_confirmed_holding_requires_actual_confirmation_evidence(self):
        context = self.context("holding")
        context.update(access_status="confirmed", holding_identifier="INVENTED-BOX-1")
        with self.assertRaises(self.mod.DossierError):
            self.set_context(context)

    def test_request_draft_cannot_be_recorded_as_sent_by_local_workflow(self):
        draft = self.draft(status="sent")
        with self.assertRaises(self.mod.DossierError):
            self.update("tasks", "TASK-0009", {"output_refs_json": [draft]})

    def test_unknown_draft_custodian_is_gap_and_cannot_complete_task(self):
        draft = self.draft(custodian="unknown", unknowns={"custodian": "The responsible custodian has not been verified"})
        self.update("tasks", "TASK-0009", {"status": "active", "output_refs_json": [draft]})
        result = self.ds.validate("records")
        self.assertIn("draft_dependency", {gap["code"] for gap in result["gaps"]})
        with self.assertRaises(self.mod.DossierError):
            self.update("tasks", "TASK-0009", {"status": "done", "result": "Must not mark incomplete draft ready"})

    def test_interview_guide_requires_observation_vs_later_knowledge_prompts(self):
        guide = self.draft("interview_guide")
        guide["prompts"].pop("later_information")
        with self.assertRaises(self.mod.DossierError):
            self.update("tasks", "TASK-0009", {"output_refs_json": [guide]})

    def test_draft_bytes_are_verified_when_file_checks_are_requested(self):
        draft = self.draft()
        self.update("tasks", "TASK-0009", {"output_refs_json": [draft]})
        self.ds.resolve(draft["file"]).write_text("Changed illustrative draft needs a new hash\n", encoding="utf-8")
        self.assertEqual("ok", self.ds.validate("records")["status"])
        with self.assertRaises(self.mod.DossierError) as caught:
            self.ds.validate("records", True)
        self.assertEqual(5, caught.exception.exit_code)

    def test_complete_request_and_neutral_guide_remain_unsent_and_verify_exact_bytes(self):
        drafts = [self.draft(), self.draft("interview_guide")]
        before = {draft["file"]["relative_path"]: self.ds.resolve(draft["file"]).read_bytes() for draft in drafts}
        self.update("tasks", "TASK-0009", {"status": "active", "output_refs_json": drafts})
        result = self.ds.validate("records", True)
        self.assertEqual("ok", result["status"])
        saved = self.row("TASK-0009")["output_refs_json"]
        self.assertEqual(["unsent", "unsent"], [draft["status"] for draft in saved])
        self.assertEqual("active", self.row("TASK-0009")["status"])
        for draft in saved:
            self.assertEqual(before[draft["file"]["relative_path"]], self.ds.resolve(draft["file"]).read_bytes())


class FinalReadinessAcceptanceTests(WorkflowCase):
    """Readiness must account for real outputs rather than matching five names."""

    OUTPUTS = [
        ("A. Chronology", "Source-linked timeline"),
        ("A. Chronology", "Uncertainty ranges"),
        ("A. Chronology", "Contradiction list"),
        ("B. Recording", "Recording inventory"),
        ("B. Recording", "Lineage notes"),
        ("B. Recording", "Annotated transcript"),
        ("B. Recording", "Reproducible comparison report"),
        ("C. Engineering", "Dated signal-path diagrams"),
        ("C. Engineering", "Assumptions table"),
        ("C. Engineering", "Comparison of explanations"),
        ("D. Culture", "Reference catalog"),
        ("E. Records", "Records inventory"),
        ("E. Records", "Gaps"),
        ("E. Records", "Targeted request drafts or interview guides"),
        ("E. Records", "Source-linked notes"),
    ]

    def inventory_rows(self):
        return [[group, output, "waiting", "", "Invented record or review is unavailable; reopen when supplied"]
                for group, output in self.OUTPUTS]

    def inventory(self, rows):
        path = self.root / "reports/milestones/workstreams.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("# Illustrative output inventory\n\n"
                        "| Workstream | Output | Status | Product | Reason/dependency |\n"
                        "| --- | --- | --- | --- | --- |\n" +
                        "".join("| " + " | ".join(row) + " |\n" for row in rows), encoding="utf-8")
        return path

    def inventory_issues(self):
        return [issue for issue in self.ds.validate("delivery")["blockers"]
                if issue["code"].startswith("workstream_")]

    def test_five_names_without_output_accounting_do_not_satisfy_inventory(self):
        path = self.root / "reports/milestones/workstreams.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("Chronology Recording Engineering Culture Records\n", encoding="utf-8")
        self.assertTrue(self.inventory_issues())

    def test_missing_or_duplicate_output_is_rejected(self):
        rows = self.inventory_rows()
        self.inventory(rows[:-1])
        self.assertTrue(self.inventory_issues())
        self.inventory(rows + [rows[0]])
        self.assertTrue(self.inventory_issues())

    def test_unperformed_output_requires_explicit_reason(self):
        rows = self.inventory_rows()
        rows[0][-1] = ""
        self.inventory(rows)
        self.assertTrue(self.inventory_issues())

    def test_available_output_requires_existing_non_scaffold_product(self):
        rows = self.inventory_rows()
        rows[0][2:] = ["available", "analysis/chronology/fixture-product.md", ""]
        self.inventory(rows)
        self.assertTrue(self.inventory_issues())
        product = self.root / rows[0][3]
        product.parent.mkdir(parents=True, exist_ok=True)
        product.write_text("# Invented output\n\n**Status:** unfilled scaffold; no completed research\n", encoding="utf-8")
        self.assertTrue(self.inventory_issues())

    def test_unknown_status_and_escaping_product_are_rejected(self):
        rows = self.inventory_rows()
        rows[0][2] = "done"
        self.inventory(rows)
        self.assertTrue(self.inventory_issues())
        rows[0][2:] = ["available", "../outside-project.md", ""]
        self.inventory(rows)
        self.assertTrue(self.inventory_issues())

    def test_all_fifteen_outputs_can_honestly_mix_available_waiting_and_deferred(self):
        rows = self.inventory_rows()
        product = self.root / "analysis/chronology/fixture-product.md"
        product.parent.mkdir(parents=True, exist_ok=True)
        product.write_text("# Invented completed comparison\n\nRecorded fixture observations and limits are inspectable.\n", encoding="utf-8")
        rows[0][2:] = ["available", "analysis/chronology/fixture-product.md", "Fixture only, not real evidence"]
        rows[-1][2] = "deferred"
        self.inventory(rows)
        self.assertEqual([], self.inventory_issues())
        # Other real-delivery blockers still apply to this illustrative dataset.
        self.assertEqual("blocked", self.ds.validate("delivery")["status"])

    def test_blank_question_cannot_be_closed_as_substantive_handoff(self):
        self.update("sessions", "SES-0001", {"current_question": " "})
        with self.assertRaises(self.mod.DossierError) as caught:
            self.ds.close_session("SES-0001", self.root / "docs/STATUS.md")
        self.assertEqual(4, caught.exception.exit_code)
        self.assertEqual([], list((self.root / "evidence/metadata/backups").glob("BAK-*.json")))

    def test_blank_action_or_untyped_dependencies_cannot_close_session(self):
        session = self.row("SES-0001")
        actions = copy.deepcopy(session["next_actions"])
        actions[0]["owner"] = ""
        self.update("sessions", "SES-0001", {"next_actions": actions})
        with self.assertRaises(self.mod.DossierError):
            self.ds.close_session("SES-0001", self.root / "docs/STATUS.md")
        actions[0]["owner"] = "fixture runner"
        actions[0]["dependencies"] = "not an array"
        self.update("sessions", "SES-0001", {"next_actions": actions})
        with self.assertRaises(self.mod.DossierError):
            self.ds.close_session("SES-0001", self.root / "docs/STATUS.md")

    def test_blank_completed_output_cannot_close_session(self):
        self.update("sessions", "SES-0001", {"completed_task_outputs": [""]})
        with self.assertRaises(self.mod.DossierError):
            self.ds.close_session("SES-0001", self.root / "docs/STATUS.md")

    def test_incomplete_finding_is_exposed_as_draft(self):
        cycle = self.cycle()
        finding = self.finding(cycle["id"], question=None)
        self.assertEqual("draft", self.ds.validate()["finding_states"][finding["id"]])

    def test_substantive_finding_awaits_separate_review(self):
        finding = self.finding(self.cycle()["id"])
        self.assertEqual("review_pending", self.ds.validate()["finding_states"][finding["id"]])

    def test_reviewed_finding_still_needs_access_context_for_sharing(self):
        finding = self.finding(self.cycle()["id"], access_limits=None)
        self.review({"kind": "record", "id": finding["id"], "revision": 1}, review_type="finding")
        self.assertEqual("reviewed", self.ds.validate()["finding_states"][finding["id"]])

    def test_shareable_finding_returns_to_review_pending_when_basis_changes(self):
        finding = self.finding(self.cycle()["id"])
        self.review({"kind": "record", "id": finding["id"], "revision": 1}, review_type="finding")
        self.assertEqual("shareable_for_selected_reviewers", self.ds.validate()["finding_states"][finding["id"]])
        self.update("sources", "SRC-0001", {"provenance_limits": "Changed fixture source basis"})
        self.assertEqual("review_pending", self.ds.validate()["finding_states"][finding["id"]])


if __name__ == "__main__":
    unittest.main()
