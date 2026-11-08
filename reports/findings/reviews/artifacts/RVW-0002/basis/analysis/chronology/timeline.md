# Baseline chronology

**Status: actual partial baseline, 2026-11-08; awaiting separate baseline review.**
This product compares real inspected accounts. It does not measure a broadcast recording,
authenticate a station clock, determine an entry mechanism, or establish participant identity.
The [timeline register](../../registers/timeline.csv), [claim register](../../registers/claims.csv)
and [source register](../../registers/sources.csv) remain canonical.

## Input basis and coverage

Basis: EVT-0001 r2 and EVT-0002–EVT-0004 r1; CLM-0002 r2 and CLM-0001/CLM-0003–CLM-0020 r1. Each claim retains its cited
source revision. Relevant source versions are SRC-0001/0002/0004/0005 r2 and SRC-0008/0009/0010 r3.
SRCH-0010–SRCH-0019 record the bounded 1987-11-23 through 1987-11-30 newspaper/trade-press survey;
this is available-index coverage, not an exhaustive examination of every issue or archive.

[Image/text checks](image-text-check.md) record comparison of the protected Tribune and Sun-Times
clipping images and Electronic Media pages with their extracted/indexed text. Their originals
are AST-0001–AST-0003, protected by BAK-0002–BAK-0004. They are publication scans, **not broadcast
recordings**. Clipping edition/date provenance remains limited; the Electronic Media issue header
was checked. The UPI account remains indexed text with direct-page retrieval blocked.

## Registered event sequence

All times below are attributed Chicago-local reports. The UTC offset remains explicitly unknown
in all four event rows because the inspected basis does not authenticate the clock/offset.

| Event/revision | Station and phase | Local start/end or competing reports | Clock and precision | Evidence and reception limit |
| --- | --- | --- | --- | --- |
| EVT-0001 r2 | WGN-TV; reported disruption during the sportscast | Reported 1987-11-22 21:14; end unknown. Separate accounts give 25/28-second figures and nominal/approximate 30-second descriptions; their qualifiers are itemized below. | Newspaper/account time at minute precision; no station log or synchronized recording clock. | CLM-0010 → SRC-0008 r3, AST-0001, PDF p2 left column, paragraph beginning “The first interruption.” Duration evidence is itemized below. Exact receiver/feed/capture remains unknown. |
| EVT-0002 r1 | WGN-TV; restoration | Local start/end unknown; no restoration timestamp is derived by adding a duration to 21:14. | Attributed recovery account, not a measured boundary. | CLM-0013 → SRC-0008 r3, AST-0001, PDF p2 left column, paragraph beginning “Strutzel said.” It reports a program-link frequency change; this is not an independently verified mechanism. |
| EVT-0003 r1 | WTTW; reported Doctor Who disruption | Canonical start/end unknown. Preserve 23:10 as a reported minute and around 23:15 as a separate listing account. | Attributed newspaper/station-spokesman account versus uploader/listing description; clock origins and offsets unverified. | CLM-0004/0020 versus CLM-0006. Reception/capture path and phase endpoints remain unknown. |
| EVT-0004 r1 | WTTW; restoration | Local start/end unknown; programming reportedly returned. | No authenticated restoration clock or frame boundary. | CLM-0005/0016/0020 support the attributed interruption accounts; their reported lengths cannot supply an exact restoration timestamp. |

The canonical `total_disruption` grouping organizes reports; it does not certify that every
author measured the same start/end phase. No report is averaged into a preferred duration or
converted into an unsupported numerical uncertainty interval.

## Duration accounts and exact locations

| Station | Registered account | Exact source location | Limit |
| --- | --- | --- | --- |
| WGN-TV | About 25 s: CLM-0001 | SRC-0002 r2, indexed UPI paragraph beginning “The first interruption.” | Publisher original/image uninspected; approximate wording. |
| WGN-TV | 25 s: CLM-0015; CLM-0018 | SRC-0009 r3/AST-0002, clipping paragraph beginning “The first interruption”; SRC-0010 r3/AST-0003, printed p4 final paragraph continued on p87 first line (PDF pp6/89). | Image-checked reporting, not independent timing; shared station testimony may underlie separate publications. |
| WGN-TV | 28 s: CLM-0009 | SRC-0008 r3/AST-0001, PDF p1 middle column, paragraph beginning “Two hours earlier.” | Reported figure; measured phase boundaries and method unstated. |
| WGN-TV | Nominal 30 s: CLM-0002 r2 | SRC-0001 r2, main article paragraph 7 excluding sponsor inserts. | The article reports news returning after 30 seconds; it does not explicitly say “about.” Its timing method, precision and common phase endpoints remain unspecified, so this is not an authenticated exact measurement. |
| WGN-TV | About 30 s: CLM-0003 r1 | SRC-0004 r2, printed p2 narrator passage after the station-presenter account. | Retrospective narration includes initial black picture, without a measured separate black interval. This qualifier is not transferred to SRC-0001. |
| WTTW | 1 min 28 s (88 s by unit conversion): CLM-0016 | SRC-0009 r3/AST-0002, clipping paragraph beginning “At the end.” | Printed figure, not a verified start/end measurement. |
| WTTW | About 90 s: CLM-0005; CLM-0020 | SRC-0002 r2, indexed paragraph beginning “The second break-in”; SRC-0010 r3/AST-0003, printed p87 third paragraph of the continuation (PDF p89). | Preserve approximation and station-account dependence; no separate capture clock. |

## Phase coverage and missing boundaries

| Station | Total disruption | Black/static | Visible intrusion | Restoration |
| --- | --- | --- | --- | --- |
| WGN-TV | Reported figures above; common measurement boundaries unknown. | Initial black picture is part of the CLM-0003 narration. Its start, length, and any later black/static interval are unmeasured. | Appearance is reported, but no inspected recording separates its endpoints from black/static or total disruption. | EVT-0002 preserves a recovery account. First restored program frame and exact clock time remain unknown. |
| WTTW | The 88/about-90-second descriptions remain separate. | No separate black/static boundary is established by the registered basis; do not copy WGN's sequence onto WTTW. | No inspected capture supplies a separate visible-intrusion interval or verified first/last frame. | EVT-0004 records the reported return, with its boundary and precise time unknown. |

All `recording_boundaries_json` collections are empty with explicit reasons. This means no
boundaries have been measured, not that a phase was absent. The [recording inventory](../media-comparison/recording-inventory.md)
contains provisional host/copy leads only. A host's file duration, later caption, or restoration
label is not a historical clock or a measured intrusion interval.

## Distribution and clock limits

| Path/account | What the current basis supports | What remains unknown |
| --- | --- | --- |
| Local WGN picture | CLM-0019 reports a distinction involving the local feed. SRC-0010 r3/AST-0003, printed p87 second paragraph of the continuation (PDF p89). | Exact receiver, monitored point, geographic reach, and provenance of a surviving capture. |
| Cable/superstation | The same article qualifies the reported effect; preserve its tentative language. | Neither uniform disruption nor definitely normal reception for every cable/superstation viewer is established. |
| Studio monitor | No station-monitor timing log is present in these event rows. | A studio-output view cannot be equated with off-air reception or used as an authenticated event clock. |
| Satellite distribution | No separately identified satellite-path capture/log has been verified. | Do not turn a cable/superstation qualification into a satellite-path verdict. |
| WTTW reception | Interruption accounts exist, with differing reported clock minutes. | Their exact reception/capture paths and relative clock errors remain unverified. |

No displayed program clock, station/log clock, receiver clock or uploader caption has been
authenticated here. UTC endpoints, second-level start times, numeric error bars and elapsed
times between the two stations cannot be manufactured from the reported figures.

## Open work and review boundary

See [contradictions](contradictions.md) for competing explanations and reopening evidence. Next
work should favor an attainable distinguishing question under TASK-0010. Media-boundary work
requires selected capture files, provenance and confirmed backups; historical path questions
require the dated documents named in [signal paths](../engineering/signal-paths.md).

This narrative is a baseline product awaiting review, not a reviewed finding or a completed
analytical cycle. Later source/claim changes must preserve this basis and trigger appropriate re-review.
