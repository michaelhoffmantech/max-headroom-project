> **Current operational checkpoint — 2026-11-08:** This project is at `C:\dev\max-headroom-project`. The real baseline and CYC-0001 are performed and separately reviewed; first-delivery reviews and the saved handoff are available; the file-verifying delivery gate reports effective completion. See [current status](docs/STATUS.md), [reviewed finding](reports/findings/FND-0001.md), [workstreams](reports/milestones/workstreams.md) and the dated operational checkpoints below. The original November6 ideation text, including its proposed project home and initial-discovery limitations, is retained below as the foundation; it is not the current completion state.

# Max Headroom Incident: Investigation and Project Plan

**Project home:** `C:\dev\max-headroom-analysis-project`  
**Prepared:** November 6, 2026  
**Stage:** Ideation and planning; initial source discovery only  
**Working approach:** Preserve evidence, separate observation from interpretation, and test explanations against alternatives.

## 1. Purpose and definition of success

Build a research project that makes the November 22, 1987 Chicago broadcast intrusions more understandable, testable, and reproducible. Investigate the signal path, production of the video, sequence of events, local media references, and investigation history. Determine what the available evidence can establish and what it cannot.

Identifying the participants is a possible outcome, not a requirement for success. A corrected timeline, an authenticated recording, a narrower technical explanation, or a well-supported rejection of a popular claim would each be useful progress. AI should help find connections and test claims; its conclusions must remain traceable to inspectable evidence.

This document is a living plan. At each checkpoint, update task status, findings, open questions, and the next research priorities. This initial phase creates the plan; the folders, registers, analyses, and research actions below are proposed work, not completed work.

## 2. What kind of project to create

| Project concept | What it provides | When to use it |
| --- | --- | --- |
| **Evidence dossier — recommended starting point** | Markdown notes, CSV registers, preserved source files, a timeline, and linked findings | Start here. Easy to inspect, back up, and use across future research sessions. |
| Reproducible analysis workspace | Small scripts or notebooks for media comparison, measurements, maps, and source processing | Add when a specific question requires a repeatable calculation or transformation. |
| Local research dashboard | Searchable evidence, filters, timeline, hypothesis comparisons, and task status | Add after the evidence model stabilizes and navigating the files becomes a recurring obstacle. |

Use one evidence collection underneath all three. A future dashboard should read the registers rather than create a separate, conflicting account. Avoid spending the initial research effort building a custom application.

Proposed layout under the project home:

```text
README.md                         Entry point and current state
INVESTIGATION_PLAN.md             This living plan
docs/
  STATUS.md                       Current findings and next actions
  METHODS.md                      Evidence and analysis standards
  DECISIONS.md                    Dated reasoning and changes of direction
registers/
  sources.csv
  claims.csv
  timeline.csv
  hypotheses.csv
  tasks.csv
  searches.csv
evidence/
  originals/                      Acquired files, kept unchanged
  metadata/                       Acquisition, provenance, hashes, restrictions
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
reports/                          Dated findings and review snapshots
work/                             Temporary material
```

Keep notes and registers under version control if useful; keep large media in a backed-up evidence store. Keep private contact information and uncorroborated personal allegations outside shareable reports.

## 3. Starting record and uncertainties

The basic event is well documented: WGN-TV's evening news and WTTW's *Doctor Who* broadcast were interrupted on November 22, 1987. WTTW's retrospective includes recollections from its own staff. These are valuable participant accounts, recorded decades later. [S01](https://news.wttw.com/2017/11/21/30-years-later-notorious-max-headroom-incident-remains-mystery)

Do not begin with a supposedly exact timeline. Contemporary UPI reporting describes roughly 25 seconds at WGN and a roughly 90-second WTTW interruption at 11:10 p.m.; WTTW's retrospective describes roughly 30 seconds at WGN. Establish whether these describe different boundaries, approximate recollections, or a genuine contradiction. The UPI page was discoverable in search but blocked direct retrieval during planning. [S02](https://www.upi.com/Archives/1987/11/23/A-video-pirate-struck-two-Chicago-television-stations-briefly/5688564642000), [S01](https://news.wttw.com/2017/11/21/30-years-later-notorious-max-headroom-incident-remains-mystery)

The *Criminal* interview transcript contains recollections from station personnel and an FCC investigator. Use it to identify testable engineering claims and possible record categories, not as a substitute for original logs or equipment documentation. Its publisher explicitly notes that transcription errors are possible. [S04](https://thisiscriminal.com/wp-content/uploads/2020/11/Episode-153-The-Max-Headroom-Incident.pdf)

No broadcast recording was acquired or analyzed during this planning phase. No new technical finding or identification is claimed. The sources below form a starting list, not an exhaustive survey or a verified statement about the case's present investigative status.

## 4. Evidence model and reasoning standards

### Registers

Assign stable identifiers: `SRC-0001` for sources, `CLM-0001` for claims, `EVT-0001` for events, `HYP-0001` for hypotheses, and `TASK-0001` for tasks. The short S01–S07 references in this plan can be mapped into the source register at setup.

| Register | Required information |
| --- | --- |
| Sources | Creator, title, publication/event dates, URL or archive identifier, access date, source type, firsthand/retrospective status, parent source, retrieval status, local file, completeness, known edits, and provenance limits |
| Claims | One precise proposition; observation, reported claim, inference, or speculation; supporting and contradicting source IDs with page/time/frame locations; confidence and reasons; unresolved caveats |
| Timeline | Event, station, time or interval, timezone, clock source, precision, recording boundaries, related claims, and competing reports |
| Hypotheses | Proposition, necessary conditions, distinguishing predictions, evidence for and against, dependencies, next test, current status, and revision history |
| Tasks | Question, owner, priority, dependencies, method, expected output, effort/timebox, status, result, and next action |
| Searches | Question, repository, exact query, filters, date, coverage, useful results, unsuccessful results, and access barriers |

For every acquired file, record an acquisition date and SHA-256 checksum. A checksum detects later changes; it does **not** authenticate the recording or its claimed origin. Record original-media history and digitization history separately when known.

### Rules for assessing claims

1. **Keep observation and interpretation separate.** A sound can be audible while the proposed words remain uncertain. A participant's recollection is evidence of their account, not automatic proof of every technical detail.
2. **Trace source dependence.** Ten articles repeating one interview provide one underlying testimony, not ten independent confirmations. Copies of one tape are also one recording lineage.
3. **Use precise status labels.** Claim confidence: high, moderate, low, or unassessed, with reasons. Hypothesis status: untested, supported, weakened, ruled out, or unresolved. Task status: queued, active, waiting, done, or closed.
4. **Reserve “ruled out” for a failed necessary condition.** Record the evidence, assumptions, and scope of the exclusion. Missing records usually mean unknown, not disproved.
5. **Retain alternatives and negative results.** Preserve uncertain readings, superseded conclusions, unsuccessful searches, and the reason a branch stopped. Do not turn a timeboxed search failure into proof that something never existed.
6. **Separate capability from participation.** Access to equipment, a technical occupation, a cultural reference, or an anecdotal resemblance cannot establish involvement. Avoid facial or speaker identification from masked, distorted material; keep uncorroborated names out of findings.
7. **Make analysis reproducible.** Keep originals unchanged. Save processing settings, tool versions, scripts where used, and links from every derived artifact to its source. Generative enhancement can invent detail and must not serve as recovered evidence.

## 5. Main investigative questions and workstreams

### A. Chronology and broadcast distribution

**Question:** What happened at each station, when, and on which signal paths?

- Build a timeline from surrounding program material, contemporaneous news reports, station statements, and any surviving logs.
- Distinguish total disruption, black/static intervals, visible pirate material, and return to normal programming. Measure each boundary separately.
- Record Chicago local time and its UTC offset explicitly; distinguish a displayed program clock from a later uploader's caption. Preserve time ranges where precision is unsupported.
- Investigate whether local over-the-air, studio-monitor, cable, and satellite-distributed feeds were affected equally. Establish the historical distribution paths before drawing conclusions from differing viewer accounts.

**Output:** A timeline with evidence locations, uncertainty ranges, and a contradiction list.

### B. Recording provenance and audiovisual comparison

**Question:** What survives, and which apparent clues belong to the intrusion rather than a later copy?

- Locate the best available WGN and WTTW recordings, preferably with material before and after the interruption. Ask about capture date, receiver/feed, tape generation, digitization, edits, and prior processing.
- Build a recording family tree. Check whether supposedly independent clips share the same damage, cropping, subtitles, or edit points.
- Compare boundaries, repeated movements, audio continuity, changes in picture quality, and possible edits. Preserve analog interlacing and timing information before making viewing copies.
- Create time-coded transcripts with `[unclear]` and alternative readings. Have a second listener transcribe disputed passages without seeing the preferred interpretation.
- Use conservative processing and side-by-side originals. Treat apparent hum, pitch, distortion, and visual defects as potentially introduced anywhere in the recording chain.

**Output:** Recording inventory, lineage notes, annotated transcript, and a reproducible comparison report.

### C. Radio and television engineering in 1987

**Question:** Which historical signal-chain explanations fit the evidence?

- Reconstruct each station's actual 1987 path from studio output to viewers, including the studio-to-transmitter link (the connection carrying program material to the broadcast transmitter), monitoring, remote control, and alternate feeds.
- Seek dated station engineering descriptions, licensing records, equipment manuals, diagrams, trade reporting, and firsthand engineering accounts. Current facilities are not evidence of the 1987 configuration.
- Test external link interference, an internal feed insertion, and downstream distribution substitution as separate possibilities. Compare what each predicts about studio monitors, over-the-air reception, geographic reach, and recovery actions.
- Separate the source of the program video, any playback equipment, the transmitting location, and the people operating them. They need not all have been at one site or active at the same time.
- Estimate feasibility with parameter ranges only after the architecture is documented. Record unknown receiver behavior, antenna characteristics, obstructions, and equipment access; do not present a single guessed location or power value as a deduction.

**Output:** A dated signal-path diagram, an assumptions table, and a comparison of explanations. Any reconstruction should use records and offline modeling; live broadcast experiments are unnecessary.

### D. Chicago media and 1987 culture

**Question:** Which details were commonplace, and which might actually narrow the possibilities?

- Inventory apparent references to local broadcasters, station branding, advertising, Max Headroom, television programs, music, and other period material. Confirm the underlying words or images before interpreting them.
- Compare each reference with material demonstrably available before November 22, 1987: advertisements, schedules, newspaper pages, recordings, catalogs, and dated community publications.
- Investigate the availability of masks, props, video equipment, and relevant technical knowledge. Widespread availability weakens any claim that possession implies special access.
- Consider broadcasting, amateur radio, video production, college media, computer/BBS communities, and prank culture as research contexts. Membership in one of these communities is not an involvement indicator.
- Keep motive hypotheses broad until evidence distinguishes them. A joke about a station might reflect ordinary audience familiarity, parody, or a personal grievance.

**Output:** A reference catalog with dates, evidence locations, alternative readings, and an assessment of how distinctive each reference is.

### E. Institutional records and human research

**Question:** What did investigators and station staff establish, and what records survive?

- Search contemporaneous coverage first, especially November 23–30, 1987, then expand through 1988 and later follow-ups. Compare article images with searchable text to catch transcription errors and omitted context.
- Search for already released agency records before preparing new requests. Authenticate third-party copies through release letters, agency identifiers, pagination, and record context; do not assume a circulating PDF is a complete case file.
- Prepare narrow record requests for complaints, technical analyses, correspondence, incident logs, and disposition records. Ask for existing records rather than new explanations. Check current agency instructions before submission. [S07](https://www.foia.gov/how-to.html)
- Investigate station, library, broadcast-history, and collector holdings. Confirm access and holdings before travel or paid research; Chicago Public Library's newspaper guide is a starting point, not proof that a particular 1987 issue is immediately available. [S06](https://www.chipublib.org/chicago-newspapers-on-microfilm/)
- Prepare neutral interview questions: What did you personally observe? On which monitor or feed? What did you do? What did you learn later? What surviving record could verify this? Separate recollection from later exposure to reporting.

**Output:** Records inventory, gaps, draft requests or interview guides, and source-linked notes. The user handles or explicitly authorizes any future outreach; creating this plan sends no messages or requests.

## 6. Initial hypothesis register

These are test candidates, not conclusions. H1–H3 concern the entry point; other rows address different questions and may coexist.

| ID | Hypothesis | Distinguishing test or evidence needed |
| --- | --- | --- |
| H1 | An external signal replaced material on a station's studio-to-transmitter path | Historical architecture plus contemporaneous monitoring and recovery evidence consistent with that entry point |
| H2 | Material entered through a studio or other internal program feed | Establish which internal feeds were normal or affected; seek logs and independent observations |
| H3 | Substitution occurred on a downstream distribution path | Compare authenticated recordings from distinct reception paths and locations against the documented distribution network |
| H4 | At least part of the performance was recorded before transmission | Test edits, continuity, playback signatures, and any independently documented production history; edits alone cannot prove the entire event was prerecorded |
| H5 | Both intrusions used one transmitting site | Test whether verified 1987 geometry and equipment constraints permit it; do not confuse the video set with the transmitter site |
| H6 | Unusual references required insider knowledge | Establish their pre-incident public availability; broad availability weakens the claim of privileged knowledge |
| H7 | A proposed clue arose from tape copying, encoding, or later interpretation | Compare independent capture lineages and unprocessed versions; record when independence cannot be established |

Add hypotheses as evidence requires. Keep person-level allegations separate from mechanism testing; naming a candidate is not needed to test these questions.

## 7. The repeatable research cycle

For each investigation session:

1. **Choose one bounded question.** Example: “Why do accounts disagree about the duration of the WGN interruption?”
2. **State alternatives before searching.** Different measurement boundaries, rounded reporting, an edited surviving clip, or a clock error might make different predictions.
3. **Define the distinguishing evidence and timebox.** Identify what result would strengthen, weaken, or leave each explanation unresolved.
4. **Acquire and register sources.** Preserve provenance and exact page or media locations. Log barriers and unsuccessful searches.
5. **Extract observations, then interpret them.** Keep the raw evidence and the reasoning separately reviewable.
6. **Challenge the preferred explanation.** Ask for the strongest alternative, source dependence, hidden assumptions, and evidence that would reverse the conclusion.
7. **Update the registers and write a short finding.** Include the question, evidence, method, result, confidence, alternatives, limitations, and next action.
8. **Choose the next task by information value.** Favor attainable evidence that distinguishes competing explanations. Defer expensive work if it depends on an unresolved assumption.

At a blocked branch, record exactly what is missing and what would justify reopening it. Stop repeating searches that do not add evidence; shift to a different question or assign a concrete archival task.

## 8. Initial task backlog and milestones

Effort ranges below are planning timeboxes, not delivery promises. External archive or records-request waits are separate.

| Task | Priority / owner | Depends on | Deliverable and completion condition |
| --- | --- | --- | --- |
| T01: Set up dossier and registers | P1 / AI | None | Proposed structure exists; status note, ID rules, and register fields are usable; about 1 session |
| T02: Map the starting sources and their dependencies | P1 / AI | T01 | Register S01–S07, identify original sources behind later accounts, and document retrieval limits; 1–2 sessions |
| T03: Collect contemporaneous reporting | P1 / AI + user for restricted archives | T02 | Review a defined November 23–30, 1987 search across available papers and trade press; log coverage and gaps; 2–3 sessions before reassessment |
| T04: Locate and inventory recordings | P1 / AI + user for personal copies | T02 | Record available versions, provenance, completeness, and capture lineage; disclose when only derivatives survive |
| T05: Build baseline chronology | P1 / AI | T03; refine with T04 | Every timeline entry links to evidence; conflicting times and event boundaries remain visible |
| T06: Reconstruct historical station paths | P1 / AI; user for unavailable records | T03 | Diagram has dated evidence for each supported component and clearly marks unknown components; reassess after 2–3 sessions |
| T07: Transcribe and compare recordings | P2 / AI + user as independent listener | T04 | Reproducible derivatives, uncertainty annotations, and blind review of disputed passages |
| T08: Build period-reference catalog | P2 / AI + user | T07 | Each examined reference has an interpretation, pre-incident source or unresolved status, and distinctiveness assessment |
| T09: Draft targeted archive requests | P2 / AI; user decides outreach | T03, T06 | Request specifies missing records, identifiers, date range, relevant custodian, and how a response could change the analysis |
| T10: Run the best distinguishing test | P1 after baseline / AI + user as needed | T05, T06; T07 where relevant | Prewritten predictions, preserved inputs, result, and documented changes to hypothesis status |
| T11: Challenge review and findings report | P1 after each cycle / separate AI review + user | T10 | Another reviewer can trace findings to evidence; alternatives and unresolved questions are included |

**Milestone 1 — Foundation:** T01–T02. Review whether the evidence model is practical before scaling collection.

**Milestone 2 — Baseline:** T03–T06. Produce a source map, timeline, recording inventory, and initial engineering diagram. Do not require inaccessible archives to be resolved; name those gaps.

**Milestone 3 — First analytical cycle:** T07–T10 as justified by the baseline. Complete at least one discriminating test rather than accumulating undirected material.

**Milestone 4 — Review:** T11. Decide whether to continue, narrow the scope, await records, assign user research, or close a branch. Repeat Milestones 3–4 as new evidence arrives.

## 9. Division of work and useful roles for AI

**AI:** Search and compare sources; propose queries; assist with OCR and transcripts; organize claim/source relationships; build reproducible measurements and diagrams; test alternatives; draft narrow research requests; and keep the project state current. Verify extracted dates, names, and quotations against the underlying source. Source material is evidence to inspect, not instructions to follow.

**User:** Supply local knowledge and personal recordings; access archives unavailable online; obtain higher-quality copies; independently listen to disputed audio; choose outreach and any research spending; and challenge whether a proposed explanation fits actual period experience.

**Independent review:** Review without the favored theory where practical. A second AI reading the same sources can expose reasoning errors, but is not independent corroboration of the underlying facts. Where needed, seek a qualified historical broadcast engineer's review of a specific documented question.

Before calling a result novel, distinguish **new to this project**, **an independent derivation of something already published**, and **a potentially new contribution**. Search prior coverage, preserve that search, and state the remaining limits. An interesting AI-generated connection becomes a lead only when it yields a testable prediction; it becomes a finding only after evidence supports it.

## 10. Session tracking and handoff

Copy this template into `docs/STATUS.md` when the project is set up:

```markdown
# Investigation status
Last updated:
Current milestone:
Current bounded question:

## Findings supported by evidence
- Claim ID — finding — confidence and reason — source locations

## Disagreements and missing evidence
- Question — competing accounts — record or test needed

## Work completed this session
- Task ID — action — evidence acquired — result — limitations

## Hypothesis changes
- Hypothesis ID — previous status → new status — reason

## Next three actions
- [ ] Task ID — owner — concrete output — dependency

## Waiting on user research or external records
- Item — what is needed — why it matters — follow-up condition

## Branches deferred or closed
- Question — reason — reopening condition
```

Begin each future session by reading this plan, the status note, and the relevant register entries. End by saving the session's evidence, findings, and next actions. A fresh chat should be able to resume without reconstructing the investigation from conversation history.

## 11. Starter source map

These references were checked on November 6, 2026. “Read” below means the text was inspected; linked audio/video and underlying records have not been independently verified. Source discovery is incomplete.

| ID | Source | Use and present limitation |
| --- | --- | --- |
| S01 | [WTTW, “30 Years Later, Notorious ‘Max Headroom Incident’ Remains a Mystery” (2017)](https://news.wttw.com/2017/11/21/30-years-later-notorious-max-headroom-incident-remains-mystery) | Read. Affected-station retrospective with staff recollections; distinguish witnessed events from later technical interpretation. |
| S02 | [UPI, “A video pirate struck two Chicago television stations, briefly...” (November 23, 1987)](https://www.upi.com/Archives/1987/11/23/A-video-pirate-struck-two-Chicago-television-stations-briefly/5688564642000) | Search excerpts inspected; full page retrieval blocked. Contemporary reporting lead; obtain the complete article or an archival reproduction. |
| S03 | [WBUR / Endless Thread, “The Max Headroom Incident: Revisiting The Masked Mystery, 32 Years Later” (2019)](https://www.wbur.org/endlessthread/2019/11/22/to-the-max-headroom) | Transcript excerpts inspected. Useful map of later reporting and online theories; trace claims to their original speakers and evidence. |
| S04 | [Criminal, Episode 153 transcript (2020)](https://thisiscriminal.com/wp-content/uploads/2020/11/Episode-153-The-Max-Headroom-Incident.pdf) | Read. Interviews with station personnel and an FCC investigator; check audio and original records before relying on disputed wording. |
| S05 | [FuzzyMemories, WTTW “The Max Headroom Pirating Incident” listing](https://fuzzymemories.tv/m/v/214/) | Found in search; page retrieval timed out. Recording-provenance lead, not an authenticated original or verified transcript. |
| S06 | [Chicago Public Library, Chicago Newspapers](https://www.chipublib.org/chicago-newspapers-on-microfilm/) | Search listing inspected; direct page presented a browser verification barrier. Confirm relevant 1987 holdings and access arrangements before a visit. |
| S07 | [FOIA.gov, How to Make a FOIA Request](https://www.foia.gov/how-to.html) | Read. Official process starting point; check the selected agency's current instructions and existing releases when preparing an actual request. |

## 12. Immediate next session

- [ ] Create the proposed dossier structure and registers in the project home (T01).
- [ ] Register the starter sources and the claims they actually support (T02).
- [ ] Begin contemporaneous reporting collection and recording discovery (T03–T04).
- [ ] Select the first bounded question after that inventory: duration discrepancies are a manageable candidate; verifying the historical signal path may provide greater information value if suitable records are available.

The first review should assess whether the evidence is becoming better organized and the uncertainty better constrained. Progress is measured by what the records support, not by how persuasive a story sounds.

## Operational checkpoints

### 2026-11-08 — Foundation

The actual dossier now contains the six registers, seven starter-source mappings, seven untested
hypotheses, eleven original backlog mappings, nine bounded retrieval/search records, and eight
attributed text claims. A separate AI usability review recommends continuing; it establishes no
new historical fact. Source retrieval, editing, shared-witness and original-record limits remain
explicit. No broadcast recording was acquired or measured. The Nov7 usage interruption left
SES-0001 incomplete; closure uses actual Nov8 private-backup confirmation. Next: the defined
contemporary survey, recording inventory, and supported/unknown historical path baseline.

### 2026-11-08 — Baseline

Four real-source baseline product groups are available and separately reviewed: source dependence, recording leads, chronology/contradictions, and dated reported signal paths. Twenty attributed claims retain timing, OCR and distribution-path qualifications. No broadcast recording has yet been acquired or measured; as-built components and capture independence remain unknown. Next: prospectively freeze a bounded WGN candidate-file context test, acquire/protect its inputs, then perform and separately review the result. No historical mechanism or identity conclusion follows.

### 2026-11-08 — Actual analytical cycle

CYC-0001 prospectively froze selected-file context alternatives, acquired/protected two public candidate files and performed conservative decoding/image inspection. Separate review accepts FND-0001 with sampling and capture limits; HYP8weakens, HYP9gains support, original H1-H7 remain untested. Commons lacks recognizable return in inspected sequence; Archive contains post-mask studio/program material. Runtime is not intrusion duration. Partial FBI record/release context and unsent drafts are available; blind transcription/culture remain waiting. Next: saved-file recovery, all-requirement assessment and final cross-output review with protected handoff.

### 2026-11-08 — First-delivery handoff

All34functional requirements and10success outcomes were assessed against actual outputs and explicit conditional states. A separate cross-output source/reasoning/privacy review and two fresh-instance saved-file recoveries are preserved. The actual reviewed file-context finding is useful within its limits; no identity, RF mechanism, original-capture authenticity or novel contribution is claimed. T067blindtranscription/T068culture remain unperformed and waiting, sourceT07/T08notdone. Next: the three owned/dependent research actions in STATUS. Final completion is effective only after the matching current review, exact final snapshot/receipt and mirrored control publish; read-only delivery validation reports that state.
