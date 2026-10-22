# Specification Quality Checklist: Structural exclusions and the T4 sign gate

**Purpose**: Validate specification completeness and quality before planning.
**Created**: 2026-10-22
**Feature**: [spec.md](../spec.md)

## Content Quality

- [x] No implementation details prescribing languages, frameworks or APIs.
- [x] Focused on user value and business needs.
- [x] Written for stakeholders; runner-specific terms are defined under Key Entities.
- [x] All mandatory sections completed.

## Requirement Completeness

- [x] No clarification markers remain.
- [x] Requirements are testable and unambiguous.
- [x] Success criteria are measurable.
- [x] Success criteria describe observable outcomes without prescribing implementation.
- [x] Acceptance scenarios are defined for all three stories.
- [x] Edge cases are identified.
- [x] Scope is clearly bounded; excluded findings are listed under Assumptions.
- [x] Dependencies and assumptions identified.

## Feature Readiness

- [x] All functional requirements have clear acceptance criteria.
- [x] User scenarios cover primary flows.
- [x] Feature meets measurable outcomes defined in Success Criteria.
- [x] No implementation details leak into specification.

## Notes

- Like specs 008–010, this spec names reason codes, patterns, the canonical regex and file paths.
  They are the observable contract of a developer tool and the canonical rule text, not
  implementation choices. How label–value lines are recognized and how exclusions are generated
  belongs in the plan.
- The scores in Background come from the session that opened feature 009 (live service, private
  note). They are not re-measured; the private note is not used.
- The eight patterns naming titles, labels or tables in **Không flag** were found by a text search
  of `SKILL.md` at `2670959`. Which of them exclude a structure as a whole is a planning task
  (FR-006), not settled here.
- User Stories 1 and 2 change no rule text; User Story 3 is the rule maintenance the owner
  authorized.
- Re-validated on 2026-10-22 after the owner answered Q1 with B: Status, Clarifications, User
  Story 3 (new scenario 4 on what the runner detects), FR-011 and SC-001 were updated. All items
  pass. Captions, tables of contents and checklist items are named in V11's rule but not detected
  by the runner in this feature; scenario 4 says so.
- Re-validated on 2026-10-22 after the planning revision accepted by the owner (research R3): User
  Story 2 scenario 2 and SC-001 now use bold labels or field lists of at least two items. All items
  still pass.
