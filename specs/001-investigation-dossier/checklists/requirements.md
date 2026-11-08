# Specification Quality Checklist: Max Headroom Investigation Dossier

**Purpose**: Validate specification completeness and quality before proceeding to planning.
**Created**: 2026-11-06
**Feature**: [spec.md](../spec.md)

**Note**: This built-in checklist is maintained by the speckit-specify and speckit-clarify workflows.
**Review Ownership**: Requirements quality was reviewed by the author and a separate AI reviewer.
**Marker Semantics**: A checked item means requirements quality was reviewed and satisfied;
it does not mean the dossier is implemented or research milestones are complete.

## Content Quality

- [x] CHK001 No implementation details (languages, frameworks, APIs).
- [x] CHK002 Focused on user value and business needs.
- [x] CHK003 Written for non-technical stakeholders.
- [x] CHK004 All mandatory sections completed.

## Requirement Completeness

- [x] CHK005 No unresolved clarification markers remain.
- [x] CHK006 Requirements are testable and unambiguous.
- [x] CHK007 Success criteria are measurable.
- [x] CHK008 Success criteria are technology-agnostic (no implementation details).
- [x] CHK009 All acceptance scenarios are defined.
- [x] CHK010 Edge cases are identified.
- [x] CHK011 Scope is clearly bounded.
- [x] CHK012 Dependencies and assumptions identified.

## Feature Readiness

- [x] CHK013 All functional requirements have clear acceptance criteria.
- [x] CHK014 User scenarios cover primary flows.
- [x] CHK015 Feature meets measurable outcomes defined in Success Criteria.
- [x] CHK016 No implementation details leak into specification.

## Notes

- Validation iteration 2: all 16 criteria pass; no unresolved clarification markers remain.
  The specification is ready for speckit-plan. CHK015 confirms that the specified behavior maps
  to measurable outcomes; actual achievement is assessed after implementation and research.
- Review iteration 1 found FR-028's wording, "private contact details and personal allegations,"
  broader than the foundation. It now specifies "uncorroborated personal allegations."
- Review iteration 1 also requested explicit scenarios for claim category/confidence, verified
  source extraction, and shared/backed-up evidence. These were added as US1 scenarios 5-6 and
  US5 scenario 4. US4 scenario 5 makes privacy and source-instruction controls explicit.
- SHA-256, stable record identifiers, historical signal paths, and processing provenance are
  required evidence standards from the plan and constitution, not software design choices.

| Requirements | Acceptance coverage | Outcome coverage |
| --- | --- | --- |
| FR-001-FR-003 | US1 scenarios 1 and 5; required Key Entities | SC-001 |
| FR-004-FR-006 | US1 scenarios 3 and 5; US4 scenario 4 | SC-003, SC-008 |
| FR-007-FR-008 | US1 scenario 2; US5 scenarios 1-2; integrity and lost-information edge cases | SC-002, SC-007 |
| FR-009 | US1 scenario 4; blocked-source and timebox edge cases | SC-008 |
| FR-010-FR-011 | US2 scenarios 1-3 | SC-004 |
| FR-012 | US3 scenario 3; historical-equipment edge case | SC-005 |
| FR-013-FR-015 | US5 scenarios 1-4; waiting-listener edge case | SC-007 |
| FR-016-FR-018 | US3 scenarios 1-4; blocked-branch edge case | SC-005, SC-006 |
| FR-019-FR-021 | US4 scenarios 1 and 4-5 | SC-003, SC-009 |
| FR-022-FR-024 | US4 scenarios 2-3; US1 scenario 1; US3 scenario 4 | SC-001, SC-005, SC-006, SC-009 |
| FR-025-FR-027 | US6 scenarios 1-3 | SC-008, SC-009 |
| FR-028-FR-029 | US4 scenario 5; US3 scenario 4; US6 scenario 3 | SC-003, SC-008 |
| FR-030 | US1 scenario 6; unavailable-storage edge case | SC-002, SC-006 |
| FR-031 | US4 scenario 3; scope assumptions | SC-005, SC-009 |

- Foundation coverage: workstreams A-E are represented by US1-US3 and US5-US6; the four
  milestones and durable handoff are covered by US4 and FR-022-FR-024.
- A later quality failure requires the affected item to be reopened and the specification
  corrected before planning proceeds. No operational milestones are claimed complete here.
