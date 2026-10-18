# Specification Analysis Report — 2026-10-16

Read-only analysis was completed before remediation. Owner explicitly authorized fixing deviations
and implementing; no extra permission was needed. Constitution 2.0.0 retained unchanged.

| ID | Category | Severity | Location | Finding | Resolution |
|---|---|---|---|---|---|
| U1 | Underspecification | MEDIUM | contracts/cli.md raw input | Annotation/link/review field shapes were descriptive rather than concrete | Added concrete host-field schema, coordinates and malformed/unresolved rules |
| U2 | Verification ambiguity | MEDIUM | tasks.md RED rules | New modules can fail only by import error, which is not behavioral RED | Exercise v2 input/automatic-target behavior at existing core entry points before adding modules; record module-unit checks separately |

All 16 FR and 6 SC have mapped tasks (100% structural coverage); 45 tasks, no unmapped tasks.
No constitution issue, critical issue or duplicate requirement found. Requirement mapping is the
explicit table in tasks.md; it is design coverage, not implementation proof. Source/structure,
context, batching, fallback, protection and package consumers all have test obligations.
No extension hooks configured. Remediation is separate from the read-only analysis invocation.
Proceed through speckit-implement and preserve all missing proof as pending.
