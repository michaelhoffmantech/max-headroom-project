#!/usr/bin/env python3
"""Local evidence dossier: checked records, retained changes, verified preservation."""
from __future__ import annotations
import argparse
import copy
import csv
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

VERSION = 1
COMMON = "id,revision,retired,legacy_aliases_json,unknowns_json".split(",")
FIELDS = {
"sources": "creator,title,publication_date,event_date,date_precision_json,source_locator,access_date,source_type,account_status_json,parent_source_ids_json,retrieval_status,inspection_json,asset_ids_json,completeness,known_edits_json,restrictions,provenance_limits",
"claims": "proposition,category,supporting_evidence_json,contradicting_evidence_json,confidence,confidence_reasons,caveats_json",
"timeline": "station,event,phase,time_local_start,time_local_end,timezone_label,utc_offset,clock_source,precision,reception_paths_json,recording_boundaries_json,related_claim_ids_json,competing_reports_json",
"hypotheses": "proposition,question_scope,necessary_conditions_json,predictions_json,supporting_claim_ids_json,contradicting_claim_ids_json,dependencies_json,next_test,status,exclusion_json",
"tasks": "question,owner,priority,dependencies_json,method,expected_output,completion_condition,output_refs_json,effort_timebox,external_wait,status,result,next_action,reopening_condition",
"searches": "question,repository,exact_query,filters_json,executed_at,coverage,useful_source_ids_json,unsuccessful_results_json,access_barriers_json,cycle_id"
}
HEADERS = {k: COMMON + v.split(",") for k,v in FIELDS.items()}
PREFIX = dict(zip(list(FIELDS)+["assets","cycles","findings","reviews","sessions","backups","changes"],["SRC","CLM","EVT","HYP","TASK","SRCH","AST","CYC","FND","RVW","SES","BAK","CHG"]))
LOCATIONS = {k:f"registers/{k}.csv" for k in FIELDS}
LOCATIONS.update(assets="evidence/metadata/assets", cycles="analysis/cycles", findings="reports/findings", reviews="reports/findings/reviews", sessions="evidence/metadata/sessions",backups="evidence/metadata/backups",changes="evidence/metadata/changes",control="evidence/metadata/control")
OBJECT_CELLS={"unknowns_json","date_precision_json","account_status_json","inspection_json","filters_json","exclusion_json"}
ID_RE = re.compile(r"^(SRC|CLM|EVT|HYP|TASK|SRCH|AST|CYC|FND|RVW|SES|BAK|CHG)-([0-9]{4,})$")
UNKNOWN = {"unknown","not_applicable"}
WORKSTREAM_OUTPUTS = {
"A": ["Source-linked timeline", "Uncertainty ranges", "Contradiction list"],
"B": ["Recording inventory", "Lineage notes", "Annotated transcript", "Reproducible comparison report"],
"C": ["Dated signal-path diagrams", "Assumptions table", "Comparison of explanations"],
"D": ["Reference catalog"],
"E": ["Records inventory", "Gaps", "Targeted request drafts or interview guides", "Source-linked notes"]
}
SIDECAR_FIELDS = {
"assets": "kind,source_id,acquired_at,storage,sha256,byte_count,capture_date,receiver_feed,tape_generation,original_media_history,digitization_history,completeness,known_edits,restrictions,provenance_limits,input_asset_ids,input_locators,processing",
"cycles": "question,alternatives,necessary_conditions,predictions,evidence_needs,dependencies,expected_output,timebox,planned_by,frozen_at,frozen_plan_sha256,plan,search_ids,input_assets,input_claims,analysis_started_at,method,result,limitations,strongest_alternative,source_dependence,hidden_assumptions,reversal_evidence,hypothesis_changes,finding_ids,stopping_condition,reopening_condition,state",
"findings": "cycle_id,question,claims,evidence,method,result,confidence,confidence_reasons,alternatives,limitations,next_action,narrative,audience,access_limits,novelty_category,novelty_search_ids",
"reviews": "review_type,target,author_identity,author_type,reviewer_identity,reviewer_type,reviewer_instance,preferred_theory_exposure,exposure_rationale,evidence_inspected,findings,unresolved_specialist_questions,reviewed_at,decision,superseded_review_id",
"sessions": "current_milestone,current_question,started_at,intended_completion_at,findings,completed_task_outputs,disagreements,gaps,hypothesis_changes,next_actions,waits,deferred_branches,closed_branches,stopping_condition,reopening_condition,final_handoff,closure_snapshot_id,reserved_receipt_id,intended_state",
"backups": "scope,covered_ids,source_alias,destination_alias,failure_domain,manifest,attempted_at,confirmed_at,method,tool_version,result,restrictions,limits,failure_reason,predecessor_attempt"
}
SIDECAR_FIELDS={k:v.split(",") for k,v in SIDECAR_FIELDS.items()}

class DossierError(Exception):
    def __init__(self, code, message=None, exit_code=2, reference=None):
        super().__init__(message or code)
        self.code, self.exit_code, self.reference = code, exit_code, reference

def require(condition, code, message, exit_code=2):
    if not condition: raise DossierError(code,message,exit_code)

def utcnow():
    return datetime.now(timezone.utc).isoformat()

def timestamp(value):
    try:
        result=datetime.fromisoformat(value.replace("Z","+00:00"))
        require(result.utcoffset() is not None,"timestamp_offset","Workflow timestamp requires offset")
        return result
    except (ValueError,TypeError,AttributeError):
        raise DossierError("timestamp","Invalid offset-aware timestamp")

def _pairs(items):
    result={}
    for k,v in items:
        require(k not in result,"duplicate_json_key",f"Duplicate JSON key: {k}")
        result[k]=v
    return result

def parse_json(value):
    try:
        return json.loads(value,object_pairs_hook=_pairs,parse_constant=lambda v: (_ for _ in ()).throw(DossierError("nonfinite_json","Non-finite JSON number")))
    except (ValueError,TypeError) as exc:
        raise DossierError("json",f"Invalid JSON: {exc}") from exc

def load_json(path):
    try: return parse_json(Path(path).read_text(encoding="utf-8"))
    except (OSError,UnicodeError) as exc: raise DossierError("read_json","Cannot read UTF-8 JSON",5) from exc

def json_bytes(value):
    try: return (json.dumps(value,ensure_ascii=False,sort_keys=True,indent=2,allow_nan=False)+"\n").encode("utf-8")
    except (ValueError,TypeError) as exc: raise DossierError("json","Cannot serialize typed JSON") from exc

def record_hash(record):
    return hashlib.sha256(json_bytes(record)).hexdigest()

def hash_file(path):
    h=hashlib.sha256(); count=0
    with Path(path).open("rb") as stream:
        for data in iter(lambda:stream.read(1024*1024),b""):
            count+=len(data); h.update(data)
    return {"sha256":h.hexdigest(),"byte_count":count}

def atomic_write(path,data):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    fd,temp=tempfile.mkstemp(prefix="."+path.name+".",suffix=".tmp",dir=path.parent)
    try:
        with os.fdopen(fd,"wb") as stream: stream.write(data);stream.flush();os.fsync(stream.fileno())
        os.replace(temp,path)
    finally:
        if os.path.exists(temp): os.unlink(temp)

def copy_verified(source,destination,expected=None):
    source,destination=Path(source),Path(destination)
    expected=expected or hash_file(source)
    destination.parent.mkdir(parents=True,exist_ok=True)
    with source.open("rb") as src,destination.open("xb") as dst:
        shutil.copyfileobj(src,dst,1024*1024)
        dst.flush();os.fsync(dst.fileno())
    require(hash_file(destination)==expected,"copy_integrity","Copied bytes differ from expected content",5)
    return expected

def _date(value):
    try:
        if re.fullmatch(r"\d{4}",value): return 1<=int(value)<=9999
        if re.fullmatch(r"\d{4}-\d{2}",value): datetime.strptime(value,"%Y-%m");return True
        datetime.strptime(value,"%Y-%m-%d");return True
    except (ValueError,TypeError): return False

def _strings(value):
    return isinstance(value,list) and all(isinstance(v,str) and v for v in value)

def validate_record(entity,row):
    require(isinstance(row,dict) and set(row)==set(HEADERS[entity]),"headers",f"Wrong fields for {entity}")
    require(bool(re.fullmatch(PREFIX[entity]+r"-[0-9]{4,}",str(row["id"]))),"id","Wrong ID prefix or format")
    require(type(row["revision"]) is int and row["revision"]>0,"revision","Positive integer revision required")
    require(type(row["retired"]) is bool,"retired","retired must be boolean")
    require(_strings(row["legacy_aliases_json"]),"aliases","Aliases must be strings")
    unknowns=row["unknowns_json"]
    require(isinstance(unknowns,dict) and all(isinstance(k,str) and isinstance(v,str) and v.strip() for k,v in unknowns.items()),"unknowns","Unknown reasons must be nonempty")
    for key,value in row.items():
        if key.endswith("_json"):
            require(isinstance(value,dict if key in OBJECT_CELLS else list),"collection_shape",f"Wrong collection type: {key}")
            if key.endswith("_ids_json") or key in {"known_edits_json","caveats_json","unsuccessful_results_json","access_barriers_json"}:
                require(_strings(value),"collection_shape",f"Strings required: {key}")
        elif key not in {"revision","retired"}:
            require(isinstance(value,str) and bool(value.strip()),"blank_scalar",f"Nonblank scalar required: {key}")
            if value in UNKNOWN: require(key in unknowns,"unknown_reason",f"Missing reason: {key}")
    if entity=="sources":
        for key in ["publication_date","event_date","access_date"]:
            v=row[key]
            require(v in UNKNOWN or _date(v) or (key!="access_date" and "/" in v and key in row["date_precision_json"]),"date",f"Invalid date: {key}")
            if key=="access_date" and v not in UNKNOWN: require(len(v)==10,"access_date","Access dates are full dates")
        require(row["retrieval_status"] in {"not_attempted","excerpt_only","partial","retrieved","blocked","unavailable"},"retrieval_status","Invalid retrieval status")
        require(row["completeness"] in {"complete","partial","unknown"},"completeness","Invalid completeness")
        a=row["account_status_json"]
        require(set(a)=={"firsthand","retrospective","limits"} and a["firsthand"] in {"yes","no","mixed","unknown","not_applicable"} and a["retrospective"] in {"yes","no","mixed","unknown","not_applicable"} and bool(a["limits"]),"account_status","Separate account axes and limits required")
        require({"text","linked_media","underlying_records","limits"}<=set(row["inspection_json"]),"inspection","Inspection scopes required")
        require({"publication_date","event_date"}<=set(row["date_precision_json"]),"date_precision","Date precision descriptions required")
    if entity=="claims":
        require(row["category"] in {"observation","reported_claim","inference","speculation"},"category","Invalid claim category")
        require(row["confidence"] in {"high","moderate","low","unassessed"},"confidence","Invalid confidence")
        require(bool(row["confidence_reasons"].strip()),"confidence_reason","Confidence requires reasons")
        for ev in row["supporting_evidence_json"]+row["contradicting_evidence_json"]: validate_evidence(ev)
    if entity=="timeline":
        require(row["station"] in {"WGN-TV","WTTW","both","not_applicable"},"station","Invalid station")
        require(row["phase"] in {"normal programming","total_disruption","black_or_static","visible_intrusion","restoration","investigation_event","unknown"},"phase","Invalid event phase")
        require(row["utc_offset"] in UNKNOWN or bool(re.fullmatch(r"[+-](?:0\d|1[0-4]):[0-5]\d",row["utc_offset"])),"utc_offset","Explicit historical offset or unknown required")
        for item in row["competing_reports_json"]: require(isinstance(item,dict) and {"claim_id","clock_source","precision"}<=set(item),"competing_report","Attributed competing reports required")
    if entity=="hypotheses":
        require(row["status"] in {"untested","supported","weakened","ruled_out","unresolved"},"hypothesis_status","Invalid hypothesis status")
        e=row["exclusion_json"]
        if row["status"]=="ruled_out":
            require(all(e.get(k) for k in ["failed_condition","evidence_refs","assumptions","exclusion_scope"]),"exclusion","Ruled out needs evidenced necessary-condition failure")
            for ev in e["evidence_refs"]: validate_evidence(ev)
        else: require(not e,"exclusion","Exclusion belongs only to ruled_out current state; history retained in CHG")
    if entity=="tasks":
        require(row["status"] in {"queued","active","waiting","done","closed"},"task_status","Invalid task status")
        if row["status"]=="done": require(bool(row["output_refs_json"]) and row["result"] not in UNKNOWN,"task_done","Done requires output and actual result")
        if row["status"] in {"waiting","closed"}:
            require(row["next_action"] not in UNKNOWN and row["reopening_condition"] not in UNKNOWN,"stopped_branch","Stopped work requires next/reopening conditions")
            if row["status"]=="waiting": require(bool(row["dependencies_json"]) or row["external_wait"] not in UNKNOWN,"waiting_dependency","Waiting dependency required")
    if entity=="searches":
        timestamp(row["executed_at"])
        require(all(isinstance(v,(str,list)) and (not isinstance(v,list) or _strings(v)) for v in row["filters_json"].values()),"filters","Filter values must be strings/string arrays")
    if entity in {"tasks","hypotheses"}:
        for d in row["dependencies_json"]: require(isinstance(d,dict) and bool(ID_RE.fullmatch(str(d.get("id","")))),"dependency","RecordRef dependency required")
    if entity=="hypotheses":
        for k in ["necessary_conditions_json","predictions_json"]:
            for d in row[k]: require(isinstance(d,dict) and bool(d.get("description")),"prediction_shape","Conditions/predictions need descriptions")
    validate_research_record(entity,row)

def validate_research_record(entity,row):
    """Optional structured records research; no source authentication or external action."""
    def described(value,unknowns,key):
        require(isinstance(value,str) and bool(value.strip()),"research_context",f"Nonblank research description required: {key}")
        if value in UNKNOWN:require(bool(unknowns.get(key)),"unknown_reason",f"Missing research uncertainty reason: {key}")
    if entity=="sources":
        context=row["inspection_json"].get("records_context")
        if context is None:return
        require(isinstance(context,dict) and context.get("kind") in {"agency_release","holding"},"records_context","Tagged release or holding context required")
        unknowns=context.get("unknowns",{})
        require(isinstance(unknowns,dict) and all(isinstance(v,str) and v.strip() for v in unknowns.values()),"unknowns","Context uncertainty reasons required")
        if context["kind"]=="agency_release":
            require({"agency_identifiers","release_letter_evidence","pagination","authentication_limits"}<=set(context),"records_context","Release context needs identifiers, release evidence, pagination, and limits")
            require(_strings(context["agency_identifiers"]) and isinstance(context["release_letter_evidence"],list),"records_context","Release identifiers/evidence must be arrays")
            for key in ["agency_identifiers","release_letter_evidence"]:
                if not context[key]:require(bool(unknowns.get(key)),"unknown_reason",f"Explain unavailable release context: {key}")
            for key in ["pagination","authentication_limits"]:described(context[key],unknowns,key)
            for ev in context["release_letter_evidence"]:validate_evidence(ev)
        else:
            require({"institution","holding_identifier","access_status","confirmation_evidence","limits"}<=set(context),"holding_context","Holding identity, access status, evidence, and limits required")
            for key in ["institution","holding_identifier","limits"]:described(context[key],unknowns,key)
            require(context["access_status"] in {"unconfirmed","confirmed"} and isinstance(context["confirmation_evidence"],list),"holding_context","Holding access status/evidence required")
            if context["access_status"]=="confirmed":require(bool(context["confirmation_evidence"]),"holding_confirmation","Confirmed holding requires actual confirmation evidence")
            for ev in context["confirmation_evidence"]:validate_evidence(ev)
    if entity=="tasks":
        for output in row["output_refs_json"]:
            if not isinstance(output,dict) or output.get("kind") not in {"request_draft","interview_guide"}:continue
            require({"file","sha256","status"}<=set(output) and isinstance(output["file"],dict) and {"alias","relative_path","access_limit"}<=set(output["file"]),"research_output","Draft needs file reference, hash, and status")
            require(output["status"]=="unsent","unsent_draft","Local draft readiness never records or authorizes sending")
            require(isinstance(output["sha256"],str) and bool(re.fullmatch(r"[0-9a-f]{64}",output["sha256"])),"research_output","Draft hash must identify exact bytes")
            unknowns=output.get("unknowns",{})
            require(isinstance(unknowns,dict),"unknowns","Draft uncertainty reasons must be an object")
            if output["kind"]=="request_draft":
                required=["custodian","date_range","analytical_gap","analytical_value"]
                require({"records_requested",*required}<=set(output),"request_draft","Narrow existing-record request fields required")
                require(_strings(output["records_requested"]) and bool(output["records_requested"]),"request_draft","Name the existing records requested")
                for key in required:described(output[key],unknowns,key)
                if row["status"]=="done":require(all(output[k] not in UNKNOWN for k in required),"draft_dependency","Unresolved custodian/scope/value cannot complete the draft task",4)
            else:
                prompts=output.get("prompts",{})
                required=["personal_observation","affected_feed","actions_taken","later_information","verifying_records"]
                require(isinstance(prompts,dict) and all(isinstance(prompts.get(k),str) and prompts[k].strip() and prompts[k] not in UNKNOWN for k in required),"interview_guide","Separate personal observation, feed, actions, later knowledge, and verifying-record prompts required")

def validate_evidence(ev):
    require(isinstance(ev,dict) and {"source_id","locator","role","limits"}<=set(ev),"evidence_ref","EvidenceRef fields required")
    require(str(ev["source_id"]).startswith("SRC-"),"evidence_source","Evidence source ID required")
    l=ev["locator"]
    require(isinstance(l,dict) and {"kind","value","precision","description"}<=set(l),"locator","Exact typed locator required")
    require(l["kind"] in {"page","time","frame","paragraph","section","line","archive_unit","other"} and bool(l["value"]),"locator","Invalid locator kind/value")
    require(all(isinstance(ev[k],str) and ev[k].strip() for k in ["source_id","role","limits"]),"evidence_ref","Evidence identity, role, and limits must be nonblank")
    if l["kind"] in {"time","frame"}:
        require(bool(ev.get("asset_id") and l.get("time_base")) or bool(l.get("uncertainty")),"media_locator","Time/frame evidence requires its asset/time base or explicit uncertainty")

def register_bytes(entity,rows):
    stream=io.StringIO(newline="")
    writer=csv.writer(stream,lineterminator="\n");writer.writerow(HEADERS[entity])
    for row in rows:
        validate_record(entity,row)
        writer.writerow([json.dumps(row[k],ensure_ascii=False,sort_keys=True,allow_nan=False) if k.endswith("_json") else str(row[k]).lower() if type(row[k]) is bool else row[k] for k in HEADERS[entity]])
    return stream.getvalue().encode("utf-8")

def read_register(path,entity):
    try:
        with Path(path).open(encoding="utf-8",newline="") as stream:
            reader=csv.reader(stream,strict=True)
            require(next(reader,None)==HEADERS[entity],"headers",f"Exact {entity} headers required")
            rows=[]
            for cells in reader:
                require(len(cells)==len(HEADERS[entity]),"row_width",f"Wrong {entity} row width")
                row=dict(zip(HEADERS[entity],cells))
                for k in row:
                    if k.endswith("_json"): row[k]=parse_json(row[k])
                require(bool(re.fullmatch(r"[1-9]\d*",row["revision"])),"revision","Positive decimal revision required")
                row["revision"]=int(row["revision"])
                require(row["retired"] in {"true","false"},"retired","Literal boolean required")
                row["retired"]=row["retired"]=="true"
                validate_record(entity,row);rows.append(row)
            return rows
    except (csv.Error,UnicodeError) as exc: raise DossierError("csv","Invalid CSV encoding/quoting") from exc

def write_register(path,entity,rows):
    atomic_write(path,register_bytes(entity,rows))

def sidecar(entity,identifier,**values):
    unknowns={}
    record={"schema_version":1,"id":identifier,"revision":1,"actor":"research_assistant","created_at":utcnow(),"unknowns":unknowns}
    for k in SIDECAR_FIELDS[entity]:
        record[k]=values.get(k)
        if record[k] is None: unknowns[k]="Not yet established; do not infer."
    supplied_unknowns=values.pop("unknowns",{})
    unknowns.update(supplied_unknowns)
    record.update(values)
    for k,v in values.items():
        if v is not None: unknowns.pop(k,None)
    return record


class Dataset:
    def __init__(self,root):
        self.root=Path(root).resolve()
        self.locations=dict(LOCATIONS)
        cfg=self.root/"config/dossier.json"
        self.config=load_json(cfg) if cfg.exists() else {"schema_version":1,"dataset_role":"actual","entity_locations":dict(LOCATIONS)}
        self.locations.update(self.config.get("entity_locations",{}))
        self.role=self.config.get("dataset_role","actual")

    def path(self,entity,identifier=None):
        p=self.root/self.locations[entity]
        require(p.resolve().is_relative_to(self.root),"dataset_path","Dataset path leaves project")
        return p/(identifier+".json") if identifier else p

    def records(self):
        result={}
        for entity in FIELDS:
            path=self.path(entity)
            for row in read_register(path,entity) if path.exists() else []:
                require(row["id"] not in result,"duplicate_id","Duplicate record ID")
                result[row["id"]]=(entity,row)
        for entity in SIDECAR_FIELDS:
            for p in sorted(self.path(entity).glob(PREFIX[entity]+"-*.json")):
                row=load_json(p);require(row["id"] not in result,"duplicate_id","Duplicate ID")
                result[row["id"]]=(entity,row)
        return result

    def manifest(self):
        result={}
        for e in FIELDS:
            p=self.path(e)
            if p.exists(): result[p.relative_to(self.root).as_posix()]=hash_file(p)
        for e in SIDECAR_FIELDS:
            for p in sorted(self.path(e).glob(PREFIX[e]+"-*.json")):
                result[p.relative_to(self.root).as_posix()]=hash_file(p)
        return result

    def response(self,command,**values):
        result={"schema_version":1,"command":command,"status":"ok","dataset_role":self.role,"changed_ids":[],"created_paths":[],"errors":[],"blockers":[],"gaps":[],"checks":[],"dataset_manifest":self.manifest()}
        result.update(values);return result

    def _id(self,entity,extra=()):
        prefix=PREFIX[entity];nums=[]
        for key in list(self.records())+list(extra):
            if key.startswith(prefix+"-"): nums.append(int(key.split("-")[1]))
        for p in self.path("changes").glob("CHG-*.json"):
            for operation in load_json(p).get("operations",[]):
                for label in ("previous","proposed"):
                    retained=operation.get(label)
                    if retained and retained["id"].startswith(prefix+"-"):
                        nums.append(int(retained["id"].split("-")[1]))
        if entity=="assets":
            for p in self.storage()["primary_evidence"].glob("AST-*"):
                if re.fullmatch(r"AST-\d{4,}",p.name): nums.append(int(p.name.split("-")[1]))
        if entity=="changes":
            for p in self.path("changes").glob("CHG-*.json"): nums.append(int(p.stem.split("-")[1]))
            for p in self.path("control").glob("CHG-*.json"): nums.append(int(p.stem.split("-")[1]))
        return f"{prefix}-{max(nums,default=0)+1:04d}"

    @contextmanager
    def lock(self,recovery=False):
        p=self.path("control")/"writer.lock";p.parent.mkdir(parents=True,exist_ok=True)
        try: stream=p.open("x",encoding="utf-8")
        except FileExistsError: raise DossierError("writer_conflict","A writer lock exists; inspect before recovery",3)
        try:
            stream.write(json.dumps({"pid":os.getpid(),"created_at":utcnow()}));stream.close()
            if not recovery:
                for journal in self.path("control").glob("CHG-*.json"):
                    require(load_json(journal).get("state")=="published","recovery_required","Finish pending journal before another mutation",3)
            yield
        finally:
            p.unlink(missing_ok=True)

    def _history(self):
        history={}
        for p in sorted(self.path("changes").glob("CHG-*.json"),key=lambda p:int(p.stem.split("-")[1])):
            journal=self.path("control",p.stem)
            if not journal.exists() or load_json(journal).get("state")!="published":continue
            ch=load_json(p)
            for op in ch.get("operations",[]):
                for name in ("previous","proposed"):
                    r=op.get(name)
                    if r: history[(r["id"],r["revision"])]=r
        for _,r in self.records().values(): history[(r["id"],r["revision"])]=r
        return history

    def _expected(self):
        expected={}
        for p in sorted(self.path("control").glob("CHG-*.json"),key=lambda p:int(p.stem.split("-")[1])):
            j=load_json(p)
            if j.get("state")=="published":
                for item in j.get("outputs",[]): expected[item["path"]]=item["new"]
        return expected

    def _assert_tracked(self):
        for p in self.path("control").glob("CHG-*.json"):
            journal=load_json(p)
            if journal.get("state")=="published":
                change=self.path("changes",p.stem)
                require(journal.get("change_integrity") is not None and change.exists() and hash_file(change)==journal["change_integrity"],"change_integrity","Retained change differs from its anchored control record",3)
        for rel,expected in self._expected().items():
            if rel.startswith("registers/") or (rel.endswith(".json") and any(rel.startswith(self.locations[e]+"/") for e in SIDECAR_FIELDS)):
                p=self.root/rel
                require(p.exists() and hash_file(p)==expected,"manual_edit_conflict","Canonical bytes differ from retained publication; reconcile without inventing history",3)

    def _publish(self,outputs,actor,reason,operations=None,closure=None):
        identifier=self._id("changes")
        journal_path=self.path("control",identifier)
        staged=[]; manifest={}
        for rel,data in outputs.items():
            p=self.root/rel;require(p.resolve().is_relative_to(self.root),"publication_path","Publication leaves dataset")
            require(not p.resolve().is_relative_to((self.root/"evidence/originals").resolve()),"original_immutable","Metadata publication cannot replace originals")
            p.parent.mkdir(parents=True,exist_ok=True)
            stage=p.parent/("."+p.name+"."+identifier+".stage")
            require(not stage.exists(),"staging_conflict","Staged path already exists",3)
            with stage.open("xb") as stream: stream.write(data);stream.flush();os.fsync(stream.fileno())
            old=hash_file(p) if p.exists() else None
            new=hash_file(stage);manifest[rel]=new
            staged.append({"path":rel,"staged":stage.relative_to(self.root).as_posix(),"previous":old,"new":new})
        change={"schema_version":1,"id":identifier,"revision":1,"actor":actor,"created_at":utcnow(),"unknowns":{},"reason":reason,"operations":operations or [],"intended_final_file_manifest":manifest}
        chpath=self.path("changes",identifier);chpath.parent.mkdir(parents=True,exist_ok=True)
        with chpath.open("xb") as stream: stream.write(json_bytes(change))
        journal={"id":identifier,"state":"staged","prepared_at":utcnow(),"outputs":staged,"closure":closure,"change_integrity":hash_file(chpath)}
        if closure:
            self._protect_closure(journal)
        atomic_write(journal_path,json_bytes(journal))
        try:
            self._finish_journal(journal)
        except Exception as exc:
            journal["state"]="recovery_required";journal["failure"]=type(exc).__name__
            atomic_write(journal_path,json_bytes(journal))
            if isinstance(exc,DossierError): raise
            raise DossierError("recovery_required","Interrupted publication retained; recover the journal",3) from exc
        return identifier

    def _finish_journal(self,journal):
        if journal.get("closure"):
            require(journal["closure"].get("confirmed"),"snapshot_pending","Session snapshot is not confirmed",4)
        for item in journal["outputs"]:
            dest=self.root/item["path"];stage=self.root/item["staged"]
            current=hash_file(dest) if dest.exists() else None
            if current==item["new"]: continue
            require(current==item["previous"],"recovery_conflict","Destination differs from recorded old/new bytes",3)
            require(stage.exists() and hash_file(stage)==item["new"],"staging_integrity","Staged bytes are unavailable or changed",5)
            os.replace(stage,dest)
        journal["state"]="published";journal["published_at"]=utcnow()
        if journal.get("closure"):
            journal["completed_at"]=utcnow()
            backup=self.storage(require_backup=True)["backup"]
            atomic_write(backup/"control"/(journal["id"]+".json"),json_bytes(journal))
        atomic_write(self.path("control",journal["id"]),json_bytes(journal))

    def recover(self,transaction):
        with self.lock(recovery=True):
            j=load_json(self.path("control",transaction));self._finish_journal(j)
        return self.response("recover",transaction_id=transaction)

    def init(self,seeds,role):
        seed=load_json(seeds) if not isinstance(seeds,dict) else copy.deepcopy(seeds)
        require(seed.get("schema_version")==1 and role in {"actual","illustrative"},"seed_schema","Schema1/role required")
        require(seed.get("dataset_role")==role,"fixture_isolation","Cannot import seeds across actual/illustrative roles")
        if self.manifest():
            require(self.role==role,"dataset_role","Dataset role cannot change")
            current=self.records()
            for e,rows in seed["registers"].items():
                for row in rows:
                    require(row["id"] in current and current[row["id"]][1]==row,"seed_conflict","Existing research differs from seeds; initialization leaves it intact",3)
            with self.lock():
                outputs,created=self._scaffolds(role)
                identifier=self._publish(outputs,"initializer","Fill missing unfilled foundation scaffolds without resetting research") if outputs else None
            return self.response("init",created_paths=created,transaction_id=identifier)
        self.role=role;self.config.update(schema_version=1,dataset_role=role,entity_locations=dict(self.locations),seed_provenance=seed.get("provenance",{}),seed_sha256=record_hash(seed))
        for e in LOCATIONS:
            (self.path(e).parent if e in FIELDS else self.path(e)).mkdir(parents=True,exist_ok=True)
        raw=[(e,r) for e in FIELDS for r in seed.get("registers",{}).get(e,[])]
        records={r["id"]:(e,r) for e,r in raw}
        require(len(records)==len(raw),"duplicate_id","Duplicate seed IDs cannot be collapsed")
        self._validate_all(records)
        outputs={self.locations[e]:register_bytes(e,seed.get("registers",{}).get(e,[])) for e in FIELDS}
        outputs["config/dossier.json"]=json_bytes(self.config)
        with self.lock():
            stubs,created=self._scaffolds(role);outputs.update(stubs)
            identifier=self._publish(outputs,"initializer","Faithful initial seed materialization", [{"previous":None,"proposed":r} for _,r in records.values()])
        return self.response("init",changed_ids=list(records),transaction_id=identifier,created_paths=sorted(set(created)|set(outputs)))

    def _scaffolds(self,role):
        created=[]
        folders=["tools","tests/fixtures","config","docs","registers","evidence/originals","evidence/metadata/assets","evidence/metadata/changes","evidence/metadata/control","evidence/metadata/backups","evidence/metadata/sessions","derived/transcripts","derived/frames","derived/audio","analysis/chronology","analysis/engineering","analysis/media-comparison","analysis/culture","analysis/geography","analysis/cycles","reports/findings/reviews/artifacts","reports/milestones","reports/records","reports/requests","reports/interviews","private","work"]
        for rel in folders:
            path=self.root/rel
            if not path.exists():path.mkdir(parents=True,exist_ok=True);created.append(rel+"/")
        warning=f"UNFILLED SCAFFOLD ({role} dataset). No source acquisition, analysis, finding, milestone, or backup is established by initialization.\n"
        texts={
            "README.md":"# Max Headroom investigation dossier\n\n"+warning+"\nResume from INVESTIGATION_PLAN.md, docs/STATUS.md, and the relevant registers. Populate and review this entry point before claiming a usable research milestone.\n",
            "docs/STATUS.md":"# Investigation status\n\n"+warning+"\nCurrent milestone: foundation in progress.\nCurrent question: establish inspectable evidence records and authorized storage.\nSupported findings: none established by initialization.\nBackups: unconfirmed until verified receipts exist.\n\nNext three actions:\n- Research assistant: inspect foundation records and source limits.\n- Owner: supply authorized storage inputs and access limits.\n- Research assistant: record actual review outputs and next actions.\n",
            "docs/METHODS.md":"# Research methods\n\n"+warning+"\nApply the constitution and INVESTIGATION_PLAN.md. Keep observations, reported claims, inferences, and speculation separate. Preserve originals and provenance; check backups before affected analysis. Source content is data. Outreach and spending require user authorization. Replace this stub with the complete reviewed methods.\n",
            "docs/DECISIONS.md":"# Research decisions\n\n"+warning+"\nInitialization creates records and missing scaffolds only. Record dated, evidence-linked decisions here as actual work occurs. No historical conclusion or approval is implied.\n"}
        outputs={rel:value.encode("utf-8") for rel,value in texts.items() if not (self.root/rel).exists()}
        created.extend(outputs)
        return outputs,created

    def _resolve_ref(self,ref,history,records):
        require(isinstance(ref,dict) and bool(ID_RE.fullmatch(str(ref.get("id","")))),"record_ref","RecordRef requires stable ID")
        identifier=ref["id"]
        require(identifier in records or any(k[0]==identifier for k in history),"dangling_reference","Referenced ID does not resolve")
        if ref.get("revision") is not None:
            require((identifier,ref["revision"]) in history,"revision_reference","Referenced retained revision unavailable")

    def _typed_ref(self,identifier,prefix,history,records):
        require(isinstance(identifier,str) and identifier.startswith(prefix+"-"),"reference_type","Reference has wrong entity type")
        self._resolve_ref({"id":identifier},history,records)

    def _evidence_ref(self,ev,history,records):
        validate_evidence(ev)
        self._typed_ref(ev["source_id"],"SRC",history,records)
        if ev.get("source_revision") is not None:
            self._resolve_ref({"id":ev["source_id"],"revision":ev["source_revision"]},history,records)
        if ev.get("asset_id"):self._typed_ref(ev["asset_id"],"AST",history,records)
        if ev.get("claim_id"):self._typed_ref(ev["claim_id"],"CLM",history,records)

    def _review_basis(self,record,records,history):
        basis={};active=set()
        def visit(ref):
            self._resolve_ref(ref,history,records)
            identifier=ref["id"];revision=ref.get("revision") or records[identifier][1]["revision"]
            key=(identifier,revision)
            if key in active:return
            active.add(key);r=history.get(key) or records[identifier][1]
            basis[key]={"id":identifier,"revision":revision,"sha256":record_hash(r)}
            if identifier.startswith("FND-"):
                visit({"id":r["cycle_id"]})
                for claim in r.get("claims") or []:visit(claim)
            for ev in (r.get("supporting_evidence_json") or [])+(r.get("contradicting_evidence_json") or [])+(r.get("evidence") or []):
                visit({"id":ev["source_id"],**({"revision":ev["source_revision"]} if ev.get("source_revision") else {})})
                if ev.get("asset_id"):visit({"id":ev["asset_id"]})
            for asset in r.get("input_asset_ids") or []:visit({"id":asset})
        visit({"id":record["id"],"revision":record["revision"]})
        return [basis[k] for k in sorted(basis)]

    def _validate_sidecar(self,entity,r):
        require({"schema_version","id","revision","actor","created_at","unknowns",*SIDECAR_FIELDS[entity]}<=set(r),"sidecar_fields",f"Missing {entity} fields")
        require(r["schema_version"]==1 and type(r["revision"]) is int and r["revision"]>0,"sidecar_schema","Invalid schema/revision")
        require(bool(re.fullmatch(PREFIX[entity]+r"-\d{4,}",str(r["id"]))),"id","Wrong sidecar ID")
        timestamp(r["created_at"]); require(isinstance(r["unknowns"],dict),"unknowns","Unknown reasons required")
        for k in SIDECAR_FIELDS[entity]:
            if r[k] is None: require(bool(r["unknowns"].get(k)),"unknown_reason",f"Missing unknown reason: {k}")
        if entity=="assets":
            require(r["kind"] in {"acquired_original","derivative","recovery_copy"},"asset_kind","Invalid asset kind")
            require(isinstance(r["sha256"],str) and bool(re.fullmatch(r"[0-9a-f]{64}",r["sha256"])) and type(r["byte_count"]) is int and r["byte_count"]>=0,"asset_hash","Content hash/byte count required")
            self.resolve(r["storage"])
            timestamp(r["acquired_at"])
            if r["kind"]=="acquired_original": require(bool(r["source_id"]),"asset_source","Original requires source")
            if r["kind"]=="derivative":
                require(r["source_id"] in {None,"not_applicable"} and bool(r["input_asset_ids"]),"derivative_lineage","Derivative must preserve all inputs, no singular parent")
                require(isinstance(r["processing"],dict) and all(r["processing"].get(k) for k in ["method","settings","tool_version","arguments","time_base"]),"processing","Processing manifest required")
                require(all(r["processing"].get(k) for k in ["executable","output_sha256","stream_notes"]),"processing","Executable, output hash, and stream notes required")
                require(r["processing"]["output_sha256"]==r["sha256"],"processing_hash","Processing output hash must match derivative bytes")
                require(not (r["processing"].get("generative") is True and r["processing"].get("claimed_as_recovered_evidence") is True),"generative_evidence","Generated detail cannot be recovered evidence")
            if r["kind"]=="recovery_copy": require(r.get("recovery_of_asset_id") and r.get("backup_receipt_id"),"recovery_chain","Recovery relationships required")
        if entity=="cycles":
            require(r["state"] in {"planned","active","tested","reviewed"},"cycle_state","Invalid cycle state")
            require(isinstance(r["plan"],dict) and r["frozen_plan_sha256"]==record_hash(r["plan"]),"frozen_plan","Frozen plan hash does not match")
            timestamp(r["frozen_at"])
            for k in ["question","alternatives","necessary_conditions","predictions","evidence_needs","dependencies","expected_output","timebox"]:
                require(k in r["plan"],"cycle_plan","Frozen plan missing fields")
                require(r[k]==r["plan"][k],"frozen_plan","Top-level plan fields must match frozen payload; use exploratory amendments for later ideas")
            require(len(r["plan"]["alternatives"])>=2 and bool(r["plan"]["predictions"]),"alternatives","At least two alternatives and predictions required")
            if r["state"] in {"tested","reviewed"}:
                require(r["analysis_started_at"] and r["method"] and r["result"] and r.get("test_performed") is True,"actual_test","An unperformed test cannot be marked tested")
                require(timestamp(r["analysis_started_at"])>=timestamp(r["frozen_at"]),"test_order","Analysis precedes frozen plan")
        if entity=="findings":
            require(r["audience"]=="owner_and_selected_reviewers","audience","Selected-reviewer audience required")
            require(r["confidence"] in {"high","moderate","low","unassessed"},"confidence","Invalid finding confidence")
            if r["novelty_category"]:
                require(r["novelty_category"] in {"new_to_project","independent_derivation","potentially_new_contribution"} and bool(r["novelty_search_ids"]),"novelty_search","Novelty needs preserved prior coverage search")
            for ev in r["evidence"] or []: validate_evidence(ev)
            require(isinstance(r["claims"],list) and all(isinstance(ref,dict) and type(ref.get("revision")) is int for ref in r["claims"]),"finding_claims","Finding claims require fixed RecordRefs")
        if entity=="reviews":
            require(r["review_type"] in {"extraction","finding","milestone","blind_transcription","specialist"},"review_type","Invalid review type")
            timestamp(r["reviewed_at"])
            require(r["decision"] in {"accepted","accepted_with_limits","revise","rejected","continue","narrow","wait","assign_research","close_branch"},"review_decision","Explicit supported review decision required")
            require(all(isinstance(r[k],str) and r[k].strip() for k in ["author_identity","author_type","reviewer_identity","reviewer_type","reviewer_instance","preferred_theory_exposure","exposure_rationale"]),"review_context","Actual reviewer identity/exposure/context required")
            require(r["reviewer_identity"] and r["reviewer_instance"] and r["reviewer_identity"]!=r["author_identity"],"separate_reviewer","Actual separate reviewer identity required")
            require(bool(r["findings"]) and bool(r["evidence_inspected"]),"review_content","Review must record its inspected basis and substantive observations")
            target=r["target"];require(isinstance(target,dict),"review_target","Tagged target required")
            if r["review_type"]=="milestone":
                require(target.get("kind")=="milestone_document" and all(k in target for k in ["milestone","document","sha256","byte_count","reviewed_copy","basis_records","basis_files"]),"milestone_target","Milestone target requires document and fixed basis")
                require(target["milestone"] in {"foundation","baseline","analytical_cycle","review"},"milestone","Invalid milestone")
                require(target["document"]["alias"]=="project" and target["document"]["relative_path"].startswith("reports/milestones/"),"milestone_path","Milestone document must be under reports/milestones")
                for ref in [target]+target["basis_files"]:
                    self.resolve(ref.get("document",ref.get("file")))
                    cp=ref["reviewed_copy"]
                    require(cp["alias"]=="project" and cp["relative_path"].startswith("reports/findings/reviews/artifacts/"+r["id"]+"/"),"review_copy","Review copy outside immutable RVW directory")
            else:
                require(target.get("kind")=="record" and "revision" in target,"review_target","Fixed record target required")
            if r["review_type"]=="blind_transcription": require(r["preferred_theory_exposure"] in {"withheld","not_shown"},"blind_review","Preferred wording must be withheld")
        if entity=="sessions":
            timestamp(r["started_at"])
            require(r["intended_state"] in {"active","closing","complete","pending_backup","recovery_required"},"session_state","Invalid intended state")
            require(isinstance(r["next_actions"],list) and len(r["next_actions"])==3,"next_actions","Exactly three owned next actions required")
            for action in r["next_actions"]: require(isinstance(action,dict) and all(k in action for k in ["owner","output","dependencies"]),"next_action","Owned action shape required")
        if entity=="backups":
            require(r["result"] in {"confirmed","failed"},"backup_result","Invalid backup result")
            require(r["scope"] in {"original","session"},"backup_scope","Invalid backup scope")
            timestamp(r["attempted_at"])
            if r["result"]=="confirmed": timestamp(r["confirmed_at"]);require(bool(r["manifest"]),"backup_manifest","Confirmed receipt needs exact manifest")

    def _validate_all(self,records,history=None):
        history=dict(history or {})
        for _,r in records.values(): history[(r["id"],r["revision"])]=r
        aliases={}; graphs={"sources":{},"tasks":{},"assets":{}}
        for identifier,(entity,r) in records.items():
            if entity in FIELDS: validate_record(entity,r)
            else: self._validate_sidecar(entity,r)
            for a in r.get("legacy_aliases_json",[]):
                key=(PREFIX[entity],a);require(key not in aliases,"duplicate_alias","Alias already assigned");aliases[key]=identifier
            for k,v in r.items():
                if k.endswith("_ids_json") or k in {"input_asset_ids","search_ids","finding_ids","novelty_search_ids"}:
                    prefix={"parent_source_ids_json":"SRC","asset_ids_json":"AST","supporting_claim_ids_json":"CLM","contradicting_claim_ids_json":"CLM","related_claim_ids_json":"CLM","useful_source_ids_json":"SRC","input_asset_ids":"AST","search_ids":"SRCH","finding_ids":"FND","novelty_search_ids":"SRCH"}.get(k)
                    for ref in v or []:
                        if prefix:self._typed_ref(ref,prefix,history,records)
                        else:self._resolve_ref({"id":ref},history,records)
                if k=="dependencies_json":
                    for ref in v: self._resolve_ref(ref,history,records)
                if k in {"supporting_evidence_json","contradicting_evidence_json","evidence"}:
                    for ev in v or []:
                        self._evidence_ref(ev,history,records)
            if entity=="sources": graphs["sources"][identifier]=r["parent_source_ids_json"]
            if entity=="sources":
                context=r["inspection_json"].get("records_context",{})
                for key in ["release_letter_evidence","confirmation_evidence"]:
                    for evidence in context.get(key,[]):self._evidence_ref(evidence,history,records)
            if entity=="tasks": graphs["tasks"][identifier]=[d["id"] for d in r["dependencies_json"] if d["id"].startswith("TASK-")]
            if entity=="tasks":
                for output in r["output_refs_json"]:
                    if isinstance(output,dict) and output.get("kind") in {"request_draft","interview_guide"}:self.resolve(output["file"])
            if entity=="assets":
                if r["source_id"] and r["source_id"]!="not_applicable": self._typed_ref(r["source_id"],"SRC",history,records)
                graphs["assets"][identifier]=(r["input_asset_ids"] or [])+([r["recovery_of_asset_id"]] if r.get("recovery_of_asset_id") else [])
                if r.get("recovery_of_asset_id"):self._typed_ref(r["recovery_of_asset_id"],"AST",history,records)
                if r.get("backup_receipt_id"):self._typed_ref(r["backup_receipt_id"],"BAK",history,records)
            if entity=="hypotheses":
                for ev in r["exclusion_json"].get("evidence_refs",[]):
                    self._evidence_ref(ev,history,records)
                for description in r["necessary_conditions_json"]+r["predictions_json"]:
                    for key in ["supporting_claim_ids","supporting_claim_ids_json"]:
                        for ref in description.get(key,[]):self._typed_ref(ref,"CLM",history,records)
                    for ref in description.get("supporting_references",[]):
                        if isinstance(ref,dict) and "source_id" in ref:self._evidence_ref(ref,history,records)
                        else:self._resolve_ref(ref if isinstance(ref,dict) else {"id":ref},history,records)
            if entity=="timeline":
                for report in r["competing_reports_json"]:self._typed_ref(report["claim_id"],"CLM",history,records)
                for boundary in r["recording_boundaries_json"]:
                    if boundary.get("asset_id"):self._typed_ref(boundary["asset_id"],"AST",history,records)
                for path in r["reception_paths_json"]:
                    if isinstance(path,dict):
                        for claim in path.get("claim_ids",[]):self._typed_ref(claim,"CLM",history,records)
            if entity=="searches" and r["cycle_id"]!="not_applicable":
                self._typed_ref(r["cycle_id"],"CYC",history,records);cyc=records[r["cycle_id"]][1]
                require(timestamp(r["executed_at"])>=timestamp(cyc["frozen_at"]),"search_order","Cycle search predates frozen plan")
            if entity=="reviews":
                target=r["target"]
                for ref in target.get("basis_records",[]): self._resolve_ref(ref,history,records)
                if target["kind"]=="record":
                    self._resolve_ref(target,history,records)
                    if r["review_type"]=="finding":self._typed_ref(target["id"],"FND",history,records)
                    if r["review_type"]=="extraction":self._typed_ref(target["id"],"CLM",history,records)
                    if r["review_type"]=="blind_transcription":require(target["id"].startswith(("CLM-","AST-")),"reference_type","Blind transcription targets a claim or media asset")
                for ref in r.get("reviewed_basis",[]):self._resolve_ref(ref,history,records)
            if entity=="findings":
                self._typed_ref(r["cycle_id"],"CYC",history,records)
                for ref in r["claims"]:
                    self._typed_ref(ref["id"],"CLM",history,records);self._resolve_ref(ref,history,records)
            if entity=="cycles":
                for key,prefix in [("input_assets","AST"),("input_claims","CLM")]:
                    for ref in r[key] or []:
                        ref={"id":ref} if isinstance(ref,str) else ref
                        self._typed_ref(ref["id"],prefix,history,records);self._resolve_ref(ref,history,records)
                for ref in r["dependencies"] or []:self._resolve_ref({"id":ref} if isinstance(ref,str) else ref,history,records)
        for graph in graphs.values():
            def visit(n,active,seen):
                require(n not in active,"dependency_cycle","Known dependence graph has a cycle")
                if n in seen:return
                for d in graph.get(n,[]):visit(d,active|{n},seen)
                seen.add(n)
            seen=set()
            for n in graph:visit(n,set(),seen)

    def _changes(self,change):
        require(change.get("schema_version")==1 and change.get("actor") and change.get("reason"),"change_set","Schema, actor, reason required")
        require(change.get("expected_dataset_manifest")==self.manifest(),"stale_manifest","Dataset changed since expected manifest",3)
        self._assert_tracked()
        current=self.records();proposed=copy.deepcopy(current);ops=[];extra={};reserved=set(current)
        for op in change.get("operations",[]):
            entity=op["entity_type"];identifier=op["id"];action=op["op"]
            require(entity in FIELDS or entity in SIDECAR_FIELDS,"entity","Unsupported entity")
            require(entity!="backups","command_owned_backup","Backup receipts are created only by backup/close-session after actual verification")
            require(action in {"create","update","retire"},"operation","Invalid operation")
            old=proposed.get(identifier,(None,None))[1]
            if action=="create":
                require(old is None and identifier==self._id(entity,reserved),"id_allocation","New ID must be next unused value",3)
                new=copy.deepcopy(op["fields"]);reserved.add(identifier)
                require(new.get("revision")==1,"revision","New records start at revision1")
            else:
                require(old is not None and op.get("expected_revision")==old["revision"],"stale_revision","Expected prior revision required",3)
                require(not op.get("expected_hash") or op["expected_hash"]==record_hash(old),"stale_hash","Prior record hash differs",3)
                require(entity not in {"reviews","backups"},"immutable_record","Closed review/backup correction creates a new ID",3)
                new=copy.deepcopy(old);new.update(op.get("fields",{}));new["revision"]=old["revision"]+1
                if entity=="assets":
                    require(all(new.get(k)==old.get(k) for k in ["kind","source_id","storage","sha256","byte_count","acquired_at","input_asset_ids","recovery_of_asset_id","backup_receipt_id"]),"immutable_asset","Acquired content identity/location/lineage is immutable; register a new acquisition or recovery copy")
                if action=="retire": new["retired"]=True
                if entity=="tasks" and new["status"]!=old["status"]:
                    allowed={"queued":{"active","waiting","closed"},"active":{"waiting","done","closed"},"waiting":{"queued","active","closed"},"done":{"queued","active"},"closed":{"queued","active"}}
                    require(new["status"] in allowed[old["status"]],"task_transition","Invalid task state transition")
                if entity=="cycles":
                    require(new["plan"]==old["plan"] and new["frozen_at"]==old["frozen_at"] and new["frozen_plan_sha256"]==old["frozen_plan_sha256"],"frozen_plan","Cannot change frozen cycle plan")
                    require(all(new.get(k)==old.get(k) for k in ["analysis_started_at","analysis_input_manifest","analysis_tool_manifest"]),"analysis_owned","Analysis start, verified inputs, and tool checks are command-owned")
                    if old["state"]!="planned":
                        require(all(new.get(k)==old.get(k) for k in ["input_assets","input_claims","required_tools"]),"analysis_inputs_frozen","Analysis inputs cannot change after start; create a new cycle")
                    allowed={"planned":{"planned"},"active":{"active","tested"},"tested":{"tested","reviewed"},"reviewed":{"reviewed"}}
                    require(new["state"] in allowed[old["state"]],"cycle_transition","Call start-analysis before testing; retain ordered cycle states")
                    if new["state"] in {"tested","reviewed"}:self._cycle_inputs_verified(old)
                if entity=="sessions":
                    for k in ["reserved_receipt_id","closure_snapshot_id","intended_completion_at"]:
                        require(new.get(k)==old.get(k),"closure_owned","Session receipt/completion fields are command-owned")
                    require(new["intended_state"]!="complete" or old["intended_state"]=="complete","closure_owned","Only close-session can establish intended completion")
                if entity=="hypotheses" and old["status"]=="ruled_out" and new["status"]!="ruled_out":
                    reopening=op.get("reopening",{})
                    require(reopening.get("new_evidence_refs") or reopening.get("changed_assumption"),"reopening_evidence","Reopening exclusion requires new evidence or changed assumption")
                    for ev in reopening.get("new_evidence_refs",[]):validate_evidence(ev)
            require(new["id"]==identifier,"id_immutable","ID cannot change")
            if entity=="cycles" and action=="create":
                require(new["state"]=="planned" and not new.get("analysis_started_at") and not new.get("analysis_input_manifest") and not new.get("analysis_tool_manifest") and new.get("test_performed") is not True,"cycle_transition","New cycles must be unstarted plans")
                plan={k:copy.deepcopy(new.get(k)) for k in ["question","alternatives","necessary_conditions","predictions","evidence_needs","dependencies","expected_output","timebox"]}
                new.update(plan=plan,frozen_at=utcnow(),frozen_plan_sha256=record_hash(plan))
                for k in ["plan","frozen_at","frozen_plan_sha256"]:new.get("unknowns",{}).pop(k,None)
            if entity=="sessions" and action=="create":
                require(new["intended_state"]=="active" and not new.get("reserved_receipt_id") and not new.get("closure_snapshot_id"),"closure_owned","New sessions start active without a claimed receipt")
            proposed[identifier]=(entity,new);ops.append({"entity_type":entity,"previous":old,"proposed":new,"decision_context":op.get("reopening",{})})
        history=self._history()
        for _,r in proposed.values():history[(r["id"],r["revision"])]=r
        for op in ops:
            if op["entity_type"]=="reviews" and op["proposed"]["target"]["kind"]=="record":
                target=op["proposed"]["target"]
                self._resolve_ref(target,history,proposed)
                record=history[(target["id"],target["revision"])]
                op["proposed"]["reviewed_basis"]=self._review_basis(record,proposed,history)
        self._validate_all(proposed,self._history())
        for op in ops:
            entity=op["entity_type"];r=op["proposed"]
            if entity=="reviews" and r["review_type"]=="milestone":
                target=r["target"]
                for ref in [target]+target["basis_files"]:
                    src=self.resolve(ref.get("document",ref.get("file")));dst=self.resolve(ref["reviewed_copy"])
                    require(not dst.exists(),"immutable_copy","Review copy already exists",3)
                    require(hash_file(src)=={"sha256":ref["sha256"],"byte_count":ref["byte_count"]},"review_hash","Reviewed bytes mismatch",5)
                    extra[dst.relative_to(self.root).as_posix()]=src.read_bytes()
        touched={op["entity_type"] for op in ops}
        outputs=dict(extra)
        for entity in touched:
            if entity in FIELDS: outputs[self.locations[entity]]=register_bytes(entity,[r for e,r in proposed.values() if e==entity])
            else:
                for op in ops:
                    if op["entity_type"]==entity:
                        r=op["proposed"];outputs[self.path(entity,r["id"]).relative_to(self.root).as_posix()]=json_bytes(r)
        identifier=self._publish(outputs,change["actor"],change["reason"],ops)
        return identifier,[op["proposed"]["id"] for op in ops]

    def apply(self,change):
        change=load_json(change) if not isinstance(change,dict) else change
        with self.lock(): identifier,ids=self._changes(change)
        return self.response("apply",transaction_id=identifier,changed_ids=ids)


    def storage(self,require_backup=False):
        p=self.root/"config/storage.local.json"
        cfg=load_json(p) if p.exists() else {}
        roots=cfg.get("roots",{})
        result={"project":self.root,"primary_evidence":self.root/"evidence/originals","backup":None}
        for alias,value in roots.items():
            if value:
                require(Path(value).is_absolute(),"storage_root","Storage roots must be absolute")
                result[alias]=Path(value).resolve()
        require(result["project"]==self.root,"project_root","Configured project differs from selected dataset")
        backup=result["backup"]
        if backup:
            for protected in [self.root,result["primary_evidence"]]:
                require(not backup.is_relative_to(protected) and not protected.is_relative_to(backup),"backup_overlap","Backup cannot overlap protected roots")
            if require_backup:
                require(cfg.get("owner_authorized") is True and bool(cfg.get("backup_failure_domain")),"backup_authorization","Owner-authorized backup/failure domain required",4)
                require(backup.is_dir(),"backup_unavailable","Backup root unavailable",4)
                if self.role=="actual" and not str(backup).startswith("\\\\"):
                    distinct=backup.drive.lower()!=self.root.drive.lower() or backup.stat().st_dev!=self.root.stat().st_dev
                    require(distinct or cfg.get("owner_selected_same_volume") is True,"backup_failure_domain","Same-volume backup needs explicit owner selection and a recorded drive-loss limitation",4)
        if require_backup: require(backup is not None,"backup_required","Supply an authorized private backup destination",4)
        result["_config"]=cfg;return result

    def resolve(self,ref):
        require(isinstance(ref,dict) and {"alias","relative_path","access_limit"}<=set(ref),"storage_ref","StorageRef requires alias, relative_path, access_limit")
        roots=self.storage()
        alias=ref["alias"];require(alias in {"project","primary_evidence","backup"} and roots.get(alias) is not None,"storage_alias","Unavailable storage alias",4)
        relative=Path(ref["relative_path"])
        require(not relative.is_absolute() and ".." not in relative.parts,"path_traversal","Storage path must be contained")
        root=roots[alias];path=root/relative
        require(path.resolve().is_relative_to(root),"path_traversal","Link/path leaves configured root")
        cursor=path
        while cursor!=root:
            require(not cursor.is_symlink() and not (hasattr(cursor,"is_junction") and cursor.is_junction()),"storage_link","Unapproved storage link")
            cursor=cursor.parent
        return path

    def _receipt(self,identifier,scope,covered,manifest,result="confirmed",failure_reason=None):
        domain=self.storage()["_config"].get("backup_failure_domain")
        return sidecar("backups",identifier,scope=scope,covered_ids=covered,source_alias="project" if scope=="session" else "primary_evidence",destination_alias="backup",failure_domain=domain,manifest=manifest,attempted_at=utcnow(),confirmed_at=utcnow() if result=="confirmed" else None,method="stream-copy; SHA-256 and byte count readback",tool_version="dossier schema1 Python "+sys.version.split()[0],result=result,restrictions="Private backup; no publication authorization",limits="Integrity only; no historical authentication",failure_reason=failure_reason,predecessor_attempt=None)

    def _asset(self,identifier):
        r=self.records().get(identifier)
        require(r is not None and r[0]=="assets","asset","Unknown asset")
        return r[1]

    def _verify_asset(self,identifier,protected=False,seen=None,confirmed_before=None):
        seen=set() if seen is None else seen
        require(identifier not in seen,"asset_cycle","Asset lineage cycle");seen=seen|{identifier}
        asset=self._asset(identifier)
        actual=hash_file(self.resolve(asset["storage"]))
        require(actual=={"sha256":asset["sha256"],"byte_count":asset["byte_count"]},"asset_integrity","Asset bytes differ from retained integrity record",5)
        if asset["kind"]=="derivative":
            for parent in asset["input_asset_ids"]:self._verify_asset(parent,protected,seen,confirmed_before)
        elif asset["kind"]=="recovery_copy":
            original=self._asset(asset["recovery_of_asset_id"])
            require(actual=={"sha256":original["sha256"],"byte_count":original["byte_count"]},"recovery_integrity","Recovered bytes mismatch",5)
            if protected:self._verify_receipt(original["id"],asset["backup_receipt_id"],confirmed_before)
        elif protected:
            matches=[r for e,r in self.records().values() if e=="backups" and r["result"]=="confirmed" and identifier in r["covered_ids"]]
            if confirmed_before is not None:matches=[r for r in matches if timestamp(r["confirmed_at"])<=timestamp(confirmed_before)]
            require(bool(matches),"original_backup_required","Original has no confirmed matching backup",4)
            self._verify_receipt(identifier,matches[-1]["id"],confirmed_before)
        return asset

    def _verify_receipt(self,asset_id,receipt_id,confirmed_before=None):
        r=self.records().get(receipt_id)
        require(r and r[0]=="backups" and r[1]["result"]=="confirmed" and asset_id in r[1]["covered_ids"],"backup_receipt","Matching confirmed receipt required",4)
        receipt=r[1];backup=self.storage(require_backup=True)["backup"]
        if confirmed_before is not None:require(timestamp(receipt["confirmed_at"])<=timestamp(confirmed_before),"backup_order","Backup confirmation must precede analysis",4)
        mirror=backup/"receipts"/(receipt_id+".json")
        require(mirror.exists() and mirror.read_bytes()==self.path("backups",receipt_id).read_bytes(),"receipt_mirror","Receipt mirror unavailable or changed",5)
        a=self._asset(asset_id)
        entries=[m for m in receipt["manifest"] if m.get("asset_id")==asset_id]
        require(bool(entries),"receipt_coverage","Receipt does not cover requested asset",5)
        item=entries[0];dest=backup/item["backup_relative_path"]
        require({"sha256":item["sha256"],"byte_count":item["byte_count"]}=={"sha256":a["sha256"],"byte_count":a["byte_count"]},"receipt_coverage","Receipt manifest differs from retained asset integrity",5)
        require(dest.resolve().is_relative_to(backup),"backup_path","Backup path leaves root")
        require(dest.exists() and hash_file(dest)=={"sha256":a["sha256"],"byte_count":a["byte_count"]},"backup_integrity","Backup bytes unavailable or changed",5)
        return dest

    def ingest(self,source,file,metadata,session):
        metadata=load_json(metadata) if not isinstance(metadata,dict) else copy.deepcopy(metadata)
        file=Path(file)
        with self.lock():
            self._assert_tracked();records=self.records()
            require(source in records and records[source][0]=="sources","source","Source must exist")
            require(session in records and records[session][0]=="sessions","session","Session must exist")
            require(file.is_file(),"input_file","Supplied file unavailable",4)
            identifier=self._id("assets");roots=self.storage()
            relative=Path(identifier)/file.name;dest=roots["primary_evidence"]/relative
            expected=hash_file(file);copy_verified(file,dest,expected)
            values={k:v for k,v in metadata.items() if k not in {"id","revision","schema_version","actor","created_at"}}
            values.update(kind="acquired_original",source_id=source,acquired_at=utcnow(),storage={"alias":"primary_evidence","relative_path":relative.as_posix(),"access_limit":metadata.get("restrictions","Unknown; inspect restrictions")},**expected,input_asset_ids=[],input_locators=[],processing=None)
            asset=sidecar("assets",identifier,**values)
            self._validate_sidecar("assets",asset)
            old=records[source][1];updated=copy.deepcopy(old);updated["asset_ids_json"].append(identifier);updated["revision"]+=1
            rows=[updated if r["id"]==source else r for e,r in records.values() if e=="sources"]
            outputs={self.locations["sources"]:register_bytes("sources",rows),self.path("assets",identifier).relative_to(self.root).as_posix():json_bytes(asset)}
            ch=self._publish(outputs,"research_assistant","Register unchanged supplied acquisition",[{"entity_type":"assets","previous":None,"proposed":asset},{"entity_type":"sources","previous":old,"proposed":updated}])
        return self.response("ingest",asset_id=identifier,transaction_id=ch,changed_ids=[identifier,source])

    def backup(self,asset_id):
        with self.lock():
            self._assert_tracked()
            asset=self._verify_asset(asset_id)
            roots=self.storage(require_backup=True);backup=roots["backup"]
            identifier=self._id("backups");rel=f"objects/{identifier}/{asset_id}"
            manifest=[{"asset_id":asset_id,"source":asset["storage"],"backup_relative_path":rel,"sha256":asset["sha256"],"byte_count":asset["byte_count"]}]
            try:
                copy_verified(self.resolve(asset["storage"]),backup/rel,{"sha256":asset["sha256"],"byte_count":asset["byte_count"]})
                self._verify_asset(asset_id)
                receipt=self._receipt(identifier,"original",[asset_id],manifest)
            except Exception as exc:
                receipt=self._receipt(identifier,"original",[asset_id],manifest,"failed",type(exc).__name__)
                self._publish({self.path("backups",identifier).relative_to(self.root).as_posix():json_bytes(receipt)},"research_assistant","Retain failed backup attempt",[{"entity_type":"backups","previous":None,"proposed":receipt}])
                if isinstance(exc,DossierError): raise
                raise DossierError("backup_io","Backup failed; no confirmation",5) from exc
            atomic_write(backup/"receipts"/(identifier+".json"),json_bytes(receipt))
            ch=self._publish({self.path("backups",identifier).relative_to(self.root).as_posix():json_bytes(receipt)},"research_assistant","Confirm matching copied bytes",[{"entity_type":"backups","previous":None,"proposed":receipt}])
        return self.response("backup",receipt_id=identifier,transaction_id=ch,changed_ids=[identifier])

    def restore_asset(self,asset_id,receipt_id,into):
        with self.lock():
            self._assert_tracked();backup=self._verify_receipt(asset_id,receipt_id)
            root=self.storage()["primary_evidence"];dest=Path(into)
            if not dest.is_absolute():dest=root/dest
            require(dest.resolve().is_relative_to(root),"restore_path","Restore target must remain inside primary root")
            require(not dest.exists(),"restore_exists","Restore target must be clean and new",3)
            original=self._asset(asset_id);expected={"sha256":original["sha256"],"byte_count":original["byte_count"]}
            copy_verified(backup,dest,expected)
            identifier=self._id("assets");r=copy.deepcopy(original)
            r.update(id=identifier,revision=1,actor="research_assistant",created_at=utcnow(),kind="recovery_copy",acquired_at=utcnow(),storage={"alias":"primary_evidence","relative_path":dest.relative_to(root).as_posix(),"access_limit":original["restrictions"]},recovery_of_asset_id=asset_id,backup_receipt_id=receipt_id)
            self._validate_sidecar("assets",r)
            ch=self._publish({self.path("assets",identifier).relative_to(self.root).as_posix():json_bytes(r)},"research_assistant","Restore to new location; preserve original record",[{"entity_type":"assets","previous":None,"proposed":r}])
        return self.response("restore-asset",asset_id=identifier,transaction_id=ch,changed_ids=[identifier])

    def _snapshot_files(self):
        paths={}
        singles=["README.md","INVESTIGATION_PLAN.md","config/dossier.json","config/seed-records.json",".specify/memory/constitution.md"]
        for rel in singles:
            p=self.root/rel
            if p.is_file():paths[rel]=p
        for top in ["docs","registers","analysis","reports","derived","tools","evidence/metadata/assets","evidence/metadata/changes","evidence/metadata/sessions","evidence/metadata/backups"]:
            for p in (self.root/top).rglob("*"):
                if p.is_file() and p.suffix not in {".stage",".tmp",".pyc"} and "__pycache__" not in p.parts:
                    require(not p.is_symlink(),"snapshot_link","Unapproved snapshot link")
                    paths[p.relative_to(self.root).as_posix()]=p
        return paths

    def _protect_closure(self,journal):
        info=journal["closure"];backup=self.storage(require_backup=True)["backup"]
        files=self._snapshot_files();before={rel:hash_file(p) for rel,p in files.items()}
        for entry in journal["outputs"]:files[entry["path"]]=self.root/entry["staged"]
        manifest=[];identifier=info["receipt_id"]
        try:
            for rel,source in sorted(files.items()):
                expected=hash_file(source);dest=backup/"snapshots"/identifier/rel
                copy_verified(source,dest,expected)
                manifest.append({"path":rel,"source":{"alias":"project","relative_path":rel,"access_limit":"Private research state"},"backup_relative_path":f"snapshots/{identifier}/{rel}",**expected})
            for rel,expected in before.items():
                require((self.root/rel).exists() and hash_file(self.root/rel)==expected,"snapshot_changed","Research notes changed while freezing snapshot; preserve edit and retry",3)
            receipt=self._receipt(identifier,"session",[info["session_id"]],manifest)
            atomic_write(backup/"receipts"/(identifier+".json"),json_bytes(receipt))
            atomic_write(self.path("backups",identifier),json_bytes(receipt))
            info["confirmed"]=True;info["manifest"]=manifest
        except Exception as exc:
            receipt=self._receipt(identifier,"session",[info["session_id"]],manifest,"failed",type(exc).__name__)
            atomic_write(self.path("backups",identifier),json_bytes(receipt))
            if isinstance(exc,DossierError):raise
            raise DossierError("snapshot_failed","Snapshot not confirmed; session remains incomplete",5) from exc

    def _session_handoff_ready(self,session):
        """Check declared handoff content without inferring unrecorded findings or outputs."""
        def text(value):
            return isinstance(value,str) and bool(re.search(r"\w",value)) and value.strip().casefold() not in {"unknown","not_applicable","todo","tbd","pending"}
        require(text(session.get("current_milestone")) and text(session.get("current_question")),"session_handoff","Session closure needs a substantive milestone and bounded question",4)
        arrays=["findings","completed_task_outputs","disagreements","gaps","hypothesis_changes","next_actions","waits","deferred_branches","closed_branches"]
        require(all(isinstance(session.get(key),list) for key in arrays),"session_handoff","Handoff collections must be explicit arrays; empty arrays may honestly record no entries",4)
        for output in session["completed_task_outputs"]:
            valid=text(output)
            if isinstance(output,dict):
                valid=any(text(output.get(key)) for key in ["output","result","description"])
                refs=output.get("output_refs",[])
                if isinstance(refs,list) and refs:
                    valid=valid or all(text(ref) or isinstance(ref,dict) and {"alias","relative_path","access_limit"}<=set(ref) for ref in refs)
            require(valid,"session_handoff","Every recorded completed output needs an actual nonblank result or output reference",4)
        actions=session["next_actions"]
        require(len(actions)==3,"session_handoff","Handoff needs exactly three owned next actions",4)
        for action in actions:
            require(isinstance(action,dict) and text(action.get("owner")) and text(action.get("output")) and isinstance(action.get("dependencies"),list),"session_handoff","Next actions need nonblank owners/outputs and explicit dependency arrays",4)
            for dependency in action["dependencies"]:
                valid=text(dependency) or isinstance(dependency,dict) and (text(dependency.get("description")) or bool(ID_RE.fullmatch(str(dependency.get("id","")))))
                require(valid,"session_handoff","Each action dependency needs an explicit reference or description",4)
        return True

    def close_session(self,session_id,handoff):
        with self.lock():
            self._assert_tracked();self.storage(require_backup=True)
            records=self.records();require(session_id in records and records[session_id][0]=="sessions","session","Session unavailable")
            old=records[session_id][1];self._session_handoff_ready(old)
            new=copy.deepcopy(old);identifier=self._id("backups")
            new.update(revision=old["revision"]+1,intended_completion_at=utcnow(),final_handoff={"alias":"project","relative_path":"docs/STATUS.md","access_limit":"Private research state"},closure_snapshot_id=identifier,reserved_receipt_id=identifier,intended_state="complete")
            for k in ["intended_completion_at","final_handoff","closure_snapshot_id","reserved_receipt_id","intended_state"]:new["unknowns"].pop(k,None)
            self._validate_sidecar("sessions",new)
            outputs={"docs/STATUS.md":Path(handoff).read_bytes(),self.path("sessions",session_id).relative_to(self.root).as_posix():json_bytes(new)}
            closure={"session_id":session_id,"receipt_id":identifier,"confirmed":False}
            ch=self._publish(outputs,"research_assistant","Protect exact final session bytes before completion",[{"entity_type":"sessions","previous":old,"proposed":new}],closure)
        return self.response("close-session",receipt_id=identifier,transaction_id=ch,changed_ids=[session_id,identifier],readiness="ready")


    def _valid_review(self,review,current=True):
        target=review["target"]
        if review["decision"] not in {"accepted","accepted_with_limits","continue","narrow","wait","assign_research","close_branch"}:return False
        try:
            self._validate_sidecar("reviews",review)
            if review["review_type"]!="milestone" and review["decision"] not in {"accepted","accepted_with_limits"}:return False
            if target["kind"]=="milestone_document":
                for item in [target]+target["basis_files"]:
                    expected={"sha256":item["sha256"],"byte_count":item["byte_count"]}
                    cp=self.resolve(item["reviewed_copy"])
                    if not cp.exists() or hash_file(cp)!=expected:return False
                    if current:
                        p=self.resolve(item.get("document",item.get("file")))
                        if not p.exists() or hash_file(p)!=expected:return False
                if current:
                    rows=self.records()
                    for ref in target["basis_records"]:
                        if ref["id"] not in rows or rows[ref["id"]][1]["revision"]!=ref["revision"]:return False
            else:
                rows=self.records();r=rows.get(target["id"])
                if current and (not r or r[1]["revision"]!=target["revision"]):return False
                if current:
                    if not review.get("reviewed_basis"):return False
                    for ref in review["reviewed_basis"]:
                        basis=rows.get(ref["id"])
                        if not basis or basis[1]["revision"]!=ref["revision"] or record_hash(basis[1])!=ref["sha256"]:return False
                if review["review_type"]=="finding":
                    if not r or r[0]!="findings":return False
                    finding=r[1]
                    if not all(finding.get(k) for k in ["question","claims","evidence","method","result","confidence_reasons","alternatives","limitations","next_action","narrative"]):return False
                if r and r[0]=="findings" and r[1].get("narrative"):
                    n=r[1]["narrative"];p=self.resolve(n)
                    if not p.exists() or hash_file(p)["sha256"]!=n.get("sha256"):return False
            return True
        except (DossierError,OSError,KeyError,TypeError):return False

    def _cycle_inputs_verified(self,cycle):
        require(cycle.get("analysis_started_at") and isinstance(cycle.get("analysis_input_manifest"),list),"analysis_manifest","Cycle requires a command-recorded verified analysis start",4)
        require(timestamp(cycle["analysis_started_at"])>=timestamp(cycle["frozen_at"]),"test_order","Analysis must follow the frozen plan")
        expected={ref["id"] if isinstance(ref,dict) else ref for ref in (cycle["input_assets"] or [])+(cycle["input_claims"] or [])}
        manifest=cycle["analysis_input_manifest"]
        require(bool(expected) and expected=={ref["id"] for ref in manifest} and len(expected)==len(manifest),"analysis_manifest","Verified manifest must cover every actual input exactly once",4)
        rows=self.records()
        for ref in manifest:
            require(ref["id"] in rows,"analysis_input","Analysis input unavailable",4)
            entity,value=rows[ref["id"]]
            actual=value["sha256"] if entity=="assets" else record_hash(value)
            require(value["revision"]==ref["revision"] and actual==ref["sha256"],"analysis_input","Analysis input changed; retain the result and start a new cycle",3)
            if entity=="assets":self._verify_asset(ref["id"],True,confirmed_before=cycle["analysis_started_at"])
        return True

    def _milestone_reviews(self,milestone,current=False):
        allowed={"accepted","accepted_with_limits","continue","narrow"} if milestone=="foundation" else {"accepted","accepted_with_limits","continue","narrow","wait","assign_research","close_branch"}
        return [r for e,r in self.records().values() if e=="reviews" and r["review_type"]=="milestone" and r["target"]["milestone"]==milestone and r["decision"] in allowed and self._valid_review(r,current)]

    def _closure_complete(self,session,current=False):
        receipt_id=session.get("reserved_receipt_id")
        if not receipt_id or session.get("intended_state")!="complete":return False
        records=self.records();value=records.get(receipt_id)
        if not value or value[0]!="backups" or value[1]["result"]!="confirmed":return False
        receipt=value[1]
        if receipt["scope"]!="session" or session["id"] not in receipt["covered_ids"]:return False
        try:
            self._session_handoff_ready(session)
            backup=self.storage(require_backup=True)["backup"]
            if not (backup/"receipts"/(receipt_id+".json")).exists():return False
            if (backup/"receipts"/(receipt_id+".json")).read_bytes()!=self.path("backups",receipt_id).read_bytes():return False
            journals=[load_json(p) for p in self.path("control").glob("CHG-*.json")]
            journal=next((j for j in journals if j.get("closure",{} ) and j["closure"].get("receipt_id")==receipt_id and j["closure"].get("session_id")==session["id"] and j["state"]=="published"),None)
            if not journal:return False
            mirror=backup/"control"/(journal["id"]+".json")
            if not mirror.exists() or load_json(mirror)!=journal:return False
            if current:
                required=set(self._snapshot_files())-{self.path("backups",receipt_id).relative_to(self.root).as_posix()}
                if required!={entry["path"] for entry in receipt["manifest"]}:return False
            for entry in receipt["manifest"]:
                expected={"sha256":entry["sha256"],"byte_count":entry["byte_count"]}
                dst=backup/entry["backup_relative_path"]
                if not dst.exists() or hash_file(dst)!=expected:return False
                if current:
                    src=self.root/entry["path"]
                    if not src.exists() or hash_file(src)!=expected:return False
            return True
        except (DossierError,OSError,KeyError,TypeError):return False

    def _finding_state(self,finding,records):
        """Derive workflow state from declared content and actual matching review, not prose guesses."""
        def text(value):return isinstance(value,str) and bool(value.strip()) and value.strip().casefold() not in UNKNOWN
        if not all(text(finding.get(key)) for key in ["question","method","result","confidence_reasons","next_action"]):return "draft"
        if not all(finding.get(key) for key in ["claims","evidence","alternatives","limitations","narrative"]):return "draft"
        narrative=finding["narrative"]
        try:
            path=self.resolve(narrative)
            if path.suffix.lower()!=".md" or not path.is_file() or hash_file(path)["sha256"]!=narrative.get("sha256"):return "draft"
        except (DossierError,OSError,TypeError,KeyError):return "draft"
        reviews=[review for entity,review in records.values() if entity=="reviews" and review["review_type"]=="finding" and review["target"].get("id")==finding["id"] and self._valid_review(review)]
        if not reviews:return "review_pending"
        if finding.get("audience")!="owner_and_selected_reviewers" or not text(finding.get("access_limits")):return "reviewed"
        return "shareable_for_selected_reviewers"

    def _workstream_checks(self):
        path=self.root/"reports/milestones/workstreams.md"
        issues=[]
        def issue(code,message,reference=None):
            issues.append({"code":code,"message":message,"reference":reference or "reports/milestones/workstreams.md","dependency":reference,"next_action":"Account for every required output with an actual product or an explicit unfinished dependency."})
        if not path.is_file():
            issue("workstream_inventory","Five-workstream output/status inventory missing");return issues
        try:lines=path.read_text(encoding="utf-8").splitlines()
        except (OSError,UnicodeError):
            issue("workstream_inventory","Inventory must be inspectable UTF-8 Markdown");return issues
        def clean(value):return re.sub(r"\s+"," ",re.sub(r"[*`]","",value).strip())
        expected={(group,label.casefold()) for group,labels in WORKSTREAM_OUTPUTS.items() for label in labels}
        seen=set();table=False;header=False
        for line in lines:
            if not line.strip().startswith("|"):
                if table:break
                continue
            cells=[clean(value) for value in line.strip().strip("|").split("|")]
            if [value.casefold() for value in cells]==["workstream","output","status","product","reason/dependency"]:
                table=True;header=True;continue
            if not table:continue
            if all(re.fullmatch(r":?-{3,}:?",value) for value in cells):continue
            if len(cells)!=5:
                issue("workstream_inventory","Inventory rows require exactly five declared columns");continue
            group,output,status,product,reason=cells
            match=re.match(r"^([A-E])(?:[.\s]|$)",group,re.IGNORECASE)
            key=(match.group(1).upper(),output.casefold()) if match else None
            if key not in expected:
                issue("workstream_output","Unknown workstream/output label: "+group+" / "+output);continue
            if key in seen:issue("workstream_output","Duplicate output row: "+group+" / "+output)
            seen.add(key);status=status.casefold()
            if status not in {"available","waiting","deferred"}:
                issue("workstream_status","Output status must be available, waiting, or deferred",output);continue
            if status!="available":
                if reason.casefold() in {"","-","—","none","n/a","unknown","not_applicable"}:
                    issue("workstream_reason","Unfinished output needs its missing evidence or dependency",output)
                continue
            linked=re.fullmatch(r"\[[^\]]*\]\(([^)]+)\)",product)
            relative=(linked.group(1) if linked else product).strip("<> ").split("#",1)[0]
            try:
                require(bool(relative),"workstream_product","Available output needs a local product")
                target=self.resolve({"alias":"project","relative_path":relative,"access_limit":"Selected-reviewer product"})
                require(target.is_file() and target.stat().st_size>0,"workstream_product","Available output product is missing or empty")
                if target.suffix.lower() in {".md",".txt",".csv",".json"}:
                    content=target.read_text(encoding="utf-8")
                    require(bool(content.strip()),"workstream_product","Available output product is empty")
                    for content_line in content.splitlines():
                        plain=clean(content_line).lstrip("# ").casefold()
                        marker=re.match(r"status\s*:\s*(?:unfilled\b|scaffold\b|guide[- ]only\b)",plain) or re.match(r"(?:unfilled\s+(?:scaffold|guide)\b|scaffold[- ]only\b|guide[- ]only\b)",plain)
                        require(not marker,"workstream_product","Unfilled scaffolds and guides cannot stand in for completed outputs")
            except (DossierError,OSError,UnicodeError):
                issue("workstream_product","Available output needs an existing contained product that is not an unfilled scaffold",output)
        if not header:issue("workstream_inventory","Expected inventory table header is missing")
        for group,label in sorted(expected-seen):issue("workstream_output","Missing required output row: "+group+" / "+label)
        return issues

    def validate(self,gate="records",verify_files=False):
        require(gate in {"records","foundation","baseline","cycle","delivery"},"gate","Unknown validation gate")
        records=self.records();self._assert_tracked();self._validate_all(records,self._history())
        checks=[{"name":"records","result":"pass"}];blockers=[];gaps=self._research_output_checks(records,verify_files)
        finding_states={identifier:self._finding_state(row,records) for identifier,(entity,row) in records.items() if entity=="findings"}
        def block(code,message,reference=None):
            blockers.append({"code":code,"message":message,"reference":reference,"dependency":reference,"next_action":"Supply or complete the named dependency; retain actual limits."})
        if gate in {"cycle","delivery"} and not verify_files:block("file_verification_required","Actual cycle/delivery readiness requires --verify-files")
        if verify_files:
            for identifier,(e,r) in records.items():
                if e=="assets":self._verify_asset(identifier)
                if e=="reviews" and r["target"]["kind"]=="milestone_document":
                    for ref in [r["target"]]+r["target"]["basis_files"]:
                        require(hash_file(self.resolve(ref["reviewed_copy"]))=={"sha256":ref["sha256"],"byte_count":ref["byte_count"]},"review_copy_integrity","Preserved review bytes changed",5)
        levels={"records":0,"foundation":1,"baseline":2,"cycle":3,"delivery":4};level=levels[gate]
        if level>=1:
            for e,prefix,count in [("sources","S",7),("hypotheses","H",7),("tasks","T",11)]:
                aliases={a for ent,r in records.values() if ent==e for a in r["legacy_aliases_json"]}
                expected={f"{prefix}{i:02}" if prefix in {"S","T"} else f"H{i}" for i in range(1,count+1)}
                if not expected<=aliases:block("starter_aliases","Missing preserved starter aliases",e)
            for path in ["README.md","docs/STATUS.md","docs/METHODS.md","docs/DECISIONS.md"]:
                if not (self.root/path).is_file():block("foundation_document","Missing foundation document",path)
            if not self.storage()["backup"]:gaps.append({"code":"backup_unconfigured","message":"Production backup remains an operational dependency","reference":"config/storage.local.json"})
        if level>=2:
            if not self._milestone_reviews("foundation"):block("foundation_review","Passed foundation review required before expanded collection")
            paths=["analysis/chronology/source-map.md","analysis/chronology/timeline.md","analysis/chronology/contradictions.md","analysis/media-comparison/recording-inventory.md","analysis/engineering/signal-paths.md","analysis/engineering/assumptions.md"]
            for path in paths:
                p=self.root/path
                if not p.exists():block("baseline_output","Baseline output missing",path)
                elif self.role=="actual" and not re.search(r"SRC-\d{4,}|SRCH-\d{4,}",p.read_text(encoding="utf-8")):block("baseline_evidence","Actual baseline must cite inspected sources or concrete searched-for gaps",path)
            if self.role=="actual":
                inspected=[r for e,r in records.values() if e=="sources" and r.get("access_date")!="unknown" and "uninspected"!=r["inspection_json"].get("text") and not r["inspection_json"].get("inherited_only",False)]
                if not inspected:block("actual_inspected_sources","Unexamined seeds cannot constitute a real baseline")
                surveys=[r for e,r in records.values() if e=="searches" and "1987-11-23" in r["coverage"] and "1987-11-30" in r["coverage"]]
                if not surveys:block("contemporary_survey","Defined contemporary-search coverage required")
                foundation=self._milestone_reviews("foundation")
                if foundation:
                    review_time=min(timestamp(r["reviewed_at"]) for r in foundation)
                    for r in surveys:
                        if timestamp(r["executed_at"])<review_time:block("foundation_order","Expanded survey predates foundation review",r["id"])
        if level>=3:
            if not self._milestone_reviews("baseline"):block("baseline_review","Retained baseline review required")
            cycles=[r for e,r in records.values() if e=="cycles" and r["state"] in {"tested","reviewed"} and r.get("test_performed") is True]
            ready=[]
            for c in cycles:
                try:self._cycle_inputs_verified(c)
                except DossierError as exc:
                    block(exc.code,str(exc),c["id"]);continue
                reviewed_findings=[]
                for finding_id in c["finding_ids"] or []:
                    findings=records.get(finding_id)
                    if findings:
                        reviewed_findings.extend([r for e,r in records.values() if e=="reviews" and r["review_type"]=="finding" and r["target"].get("id")==finding_id and self._valid_review(r)])
                if reviewed_findings:ready.append(c)
            if not ready:block("actual_reviewed_cycle","Need a performed real test and matching separate findings review")
        if level>=4:
            if self.role!="actual":block("actual_dataset_required","Illustrative datasets cannot pass delivery")
            for m in ["foundation","baseline","analytical_cycle","review"]:
                if not self._milestone_reviews(m,current=m=="review"):block("milestone_review","Missing matching milestone review",m)
            blockers.extend(self._workstream_checks())
            sessions=[r for e,r in records.values() if e=="sessions"]
            if not sessions or not self._closure_complete(sessions[-1],True):block("completed_handoff","Exact-content final session backup and mirrored commit required")
            for e,r in records.values():
                if e=="findings":
                    if finding_states[r["id"]]!="shareable_for_selected_reviewers":block("finding_readiness","Finding needs substantive content, matching separate review, and selected-reviewer access context",r["id"])
        readiness="structure_only" if not verify_files else "ready"
        if blockers:readiness="not_evaluated" if not verify_files else "not_ready"
        return self.response("validate",status="blocked" if blockers else "ok",checks=checks,blockers=blockers,gaps=gaps,readiness=readiness,finding_states=finding_states,_exit_code=4 if blockers else 0)

    def _research_output_checks(self,records,verify_files=False):
        """Report incomplete record/draft context without upgrading authenticity or sending."""
        gaps=[]
        def gap(code,message,identifier):
            gaps.append({"code":code,"message":message,"reference":identifier,
                         "dependency":identifier,"next_action":"Resolve the named evidence/access limitation or retain an explicit waiting state."})
        for identifier,(entity,row) in records.items():
            if entity=="sources":
                context=row["inspection_json"].get("records_context")
                if not context:continue
                if context["kind"]=="agency_release":
                    missing=[key for key in ["agency_identifiers","release_letter_evidence"] if not context[key]]
                    if context["pagination"] in UNKNOWN:missing.append("pagination")
                    if missing:gap("records_context_gap","Release context remains unknown: "+", ".join(missing),identifier)
                    elif row["completeness"]!="complete":gap("records_context_gap","Partial/unknown released item does not establish a complete case file",identifier)
                elif context["access_status"]=="unconfirmed":
                    gap("records_context_gap","Holding/item access is unconfirmed; a directory lead is not confirmation",identifier)
            if entity=="tasks":
                for output in row["output_refs_json"]:
                    if not isinstance(output,dict) or output.get("kind") not in {"request_draft","interview_guide"}:continue
                    path=self.resolve(output["file"])
                    if output["kind"]=="request_draft":
                        missing=[key for key in ["custodian","date_range","analytical_gap","analytical_value"] if output[key] in UNKNOWN]
                        if missing:gap("draft_dependency","Unsent request still depends on: "+", ".join(missing),identifier)
                    if verify_files:
                        require(path.is_file() and hash_file(path)["sha256"]==output["sha256"],"draft_integrity","Unsent draft bytes differ from the declared reviewed output",5)
        return gaps

    def _tool_preflight(self,cycle):
        """Probe declared executables only for version; no media processing or shell evaluation."""
        declarations=cycle.get("required_tools",[])
        require(isinstance(declarations,list),"tool_declaration","Required tools must be a list")
        manifest=[]
        for declaration in declarations:
            tool={"executable":declaration,"arguments":[]} if isinstance(declaration,str) else declaration
            require(isinstance(tool,dict) and isinstance(tool.get("executable"),str) and tool["executable"].strip(),"tool_declaration","Tool requires a nonblank executable")
            name=tool["executable"];arguments=tool.get("arguments",[]);expected=tool.get("expected_version")
            require(isinstance(arguments,list) and all(isinstance(arg,str) for arg in arguments),"tool_arguments","Analysis arguments must be literal strings")
            require(expected is None or isinstance(expected,str) and bool(expected.strip()),"tool_version","Expected version must be a nonblank string")
            resolved=shutil.which(name)
            require(resolved is not None,"tool_unavailable","Required analysis executable unavailable: "+name,4)
            flag="-version" if Path(name).stem.lower() in {"ffmpeg","ffprobe"} else "--version"
            command=[resolved,flag]
            try:
                result=subprocess.run(command,capture_output=True,text=True,shell=False,timeout=10,check=False)
            except (OSError,subprocess.SubprocessError) as exc:
                raise DossierError("tool_version_unavailable","Required executable version could not be checked: "+name,4) from exc
            text=(result.stdout or "")+"\n"+(result.stderr or "")
            first=next((line.strip() for line in text.splitlines() if line.strip()),"")
            require(result.returncode==0 and bool(first),"tool_version_unavailable","Required executable did not report a usable version: "+name,4)
            match=re.search(r"\bversion\s+(\S+)",first,re.IGNORECASE)
            if not match:match=re.search(r"\b(\d+(?:\.\d+)+(?:[-+._a-zA-Z0-9]*)?)",first)
            version=match.group(1) if match else first
            require(expected is None or version==expected,"tool_version_mismatch","Required executable version differs from the declared version: "+name,4)
            manifest.append({"executable":name,"resolved_path":resolved,"version":version,
                             "version_output":first,"arguments":copy.deepcopy(arguments),
                             "probe_command":command,"checked_at":utcnow()})
        return manifest

    def start_analysis(self,cycle_id):
        with self.lock():
            self._assert_tracked();records=self.records();item=records.get(cycle_id)
            require(item and item[0]=="cycles","cycle","Cycle unavailable")
            old=item[1];self._validate_sidecar("cycles",old)
            require(old["state"]=="planned" and not old["analysis_started_at"],"cycle_transition","Analysis starts once from a planned cycle")
            for ref in old["dependencies"] or []:
                if isinstance(ref,str):ref={"id":ref}
                self._resolve_ref(ref,self._history(),records)
                dependency=records[ref["id"]]
                if dependency[0]=="tasks":
                    require(dependency[1]["status"]=="done","analysis_dependency","Required research/listener task is incomplete",4)
            tool_manifest=self._tool_preflight(old)
            input_manifest=[]
            for ref in old["input_assets"] or []:
                identifier=ref["id"] if isinstance(ref,dict) else ref
                a=self._verify_asset(identifier,True)
                if isinstance(ref,dict) and ref.get("sha256"):require(a["sha256"]==ref["sha256"],"analysis_input","Planned asset hash changed",3)
                if isinstance(ref,dict) and ref.get("revision"):require(a["revision"]==ref["revision"],"analysis_input","Planned asset revision changed",3)
                input_manifest.append({"id":identifier,"revision":a["revision"],"sha256":a["sha256"]})
            for ref in old["input_claims"] or []:
                if isinstance(ref,str):ref={"id":ref}
                self._resolve_ref(ref,self._history(),records)
                r=records[ref["id"]][1]
                if ref.get("revision"):require(r["revision"]==ref["revision"],"analysis_input","Planned claim revision changed",3)
                input_manifest.append({"id":r["id"],"revision":r["revision"],"sha256":record_hash(r)})
            new=copy.deepcopy(old);new.update(revision=old["revision"]+1,state="active",analysis_started_at=utcnow(),analysis_input_manifest=input_manifest,analysis_tool_manifest=tool_manifest)
            new["unknowns"].pop("analysis_started_at",None)
            self._validate_sidecar("cycles",new)
            ch=self._publish({self.path("cycles",cycle_id).relative_to(self.root).as_posix():json_bytes(new)},"research_assistant","Verify protected inputs and record actual analysis start",[{"entity_type":"cycles","previous":old,"proposed":new}])
        return self.response("start-analysis",transaction_id=ch,changed_ids=[cycle_id])


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root",default=".")
    parser.add_argument("--format",choices=["text","json"],default="text")
    sub=parser.add_subparsers(dest="command",required=True)
    p=sub.add_parser("init");p.add_argument("--seeds",required=True);p.add_argument("--dataset-role",choices=["actual","illustrative"],required=True)
    p=sub.add_parser("apply");p.add_argument("--change-set",required=True)
    p=sub.add_parser("ingest")
    for arg in ["source","file","metadata","session"]:p.add_argument("--"+arg,required=True)
    p=sub.add_parser("backup");p.add_argument("--asset",required=True)
    p=sub.add_parser("restore-asset")
    for arg in ["asset","receipt","into"]:p.add_argument("--"+arg,required=True)
    p=sub.add_parser("start-analysis");p.add_argument("--cycle",required=True)
    p=sub.add_parser("validate");p.add_argument("--gate",choices=["records","foundation","baseline","cycle","delivery"],default="records");p.add_argument("--verify-files",action="store_true")
    p=sub.add_parser("close-session");p.add_argument("--session",required=True);p.add_argument("--handoff",required=True)
    p=sub.add_parser("recover");p.add_argument("--transaction",required=True);p.add_argument("--finish",action="store_true",required=True)
    args=parser.parse_args(argv);ds=None
    try:
        ds=Dataset(args.root)
        commands={
        "init":lambda:ds.init(args.seeds,args.dataset_role),
        "apply":lambda:ds.apply(args.change_set),
        "ingest":lambda:ds.ingest(args.source,args.file,args.metadata,args.session),
        "backup":lambda:ds.backup(args.asset),
        "restore-asset":lambda:ds.restore_asset(args.asset,args.receipt,args.into),
        "start-analysis":lambda:ds.start_analysis(args.cycle),
        "validate":lambda:ds.validate(args.gate,args.verify_files),
        "close-session":lambda:ds.close_session(args.session,args.handoff),
        "recover":lambda:ds.recover(args.transaction)}
        result=commands[args.command]();code=result.pop("_exit_code",0)
    except (DossierError,OSError,UnicodeError,KeyError,TypeError,ValueError) as exc:
        if isinstance(exc,DossierError):code=exc.exit_code;error_code=exc.code;message=str(exc)
        else:code=5 if isinstance(exc,OSError) else 2;error_code="io" if code==5 else "invalid_input";message="Operation failed; inspect local inputs without changing evidence."
        result={"schema_version":1,"command":args.command,"status":{2:"invalid",3:"conflict",4:"blocked",5:"error"}[code],"dataset_role":ds.role if ds else "unknown","changed_ids":[],"created_paths":[],"errors":[],"blockers":[],"gaps":[],"checks":[],"dataset_manifest":{}}
        result["blockers" if code==4 else "errors"].append({"code":error_code,"message":message,"reference":None,"dependency":None,"next_action":"Resolve the named input/integrity/recovery issue before retrying."})
    if args.format=="json":print(json.dumps(result,ensure_ascii=False,sort_keys=True,allow_nan=False))
    else:
        print(f"{result['command']}: {result['status']}")
        for entry in result["errors"]+result["blockers"]+result["gaps"]:print(entry["code"]+": "+entry["message"])
    return code

if __name__=="__main__":
    raise SystemExit(main())
