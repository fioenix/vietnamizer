# Tasks: README evidence

## Phase1 Setup
- [x] T001 Read current README/consumers and unchanged source reports018/025; freeze preservation baseline in output/readme-026.
- [x] T002 Record accepted user scope, spec/plan/data/contract and tasks path in specs/026-readme-evidence.

## Phase2 Documentation foundation
- [x] T003 [US3] Add RED tests proving relocated docs must preserve all55patterns/seven cards/latest version and root guide links in tests/test_distribution.py; update fixture inventory in both package test modules.
- [x] T004 [US3] Relocate docs and adapt scripts/validate-package.py/AGENTS.md ownership checks without changing canonical payload, IDs or version.

## Phase3 Reader page
- [x] T005 [US2] Move installation, usage, voice/style, architecture, patterns, benchmark details, sources and changelog into docs/*.md; rebase relative links and preserve old material with a section map.
- [x] T006 [US1] Rewrite README.md<=220lines with use cases, real examples, visible quality-related evidence, short install/use and detailed-doc navigation; retain key public entry headings.

## Phase4 Evidence figures
- [x] T007 [US1] Add source-derived evidence.json/check-data renderer under docs/figures; verify report hashes and all outcome/missing counts with no provider calls.
- [x] T008 [US1] Render two publication figures using isolated/pinned optional Matplotlib tooling, stable SVG output and local PDF/PNG exports; visually inspect desktop/narrow readability.

## Phase5 Verification and delivery
- [x] T009 Run only affected documentation/distribution/package-security checks plus metadata/registry checks; audit links, section preservation, immutable source/raw/release archive hashes.
- [x] T010 Record final verification/limits and deliver reviewable files/figure previews. Do not publish, retag or rerun benchmark/model work under this task.

## Dependencies
T001->T002->T003->T004/T005->T006->T007->T008->T009->T010. One writer; no parallel implementation required. Independent final review only if an applicable required review gate triggers.

## Implementation Strategy
Keep source0.13.2/payload/release immutable. First preserve documentation integrity checks, then move details, then render only observed evidence. Test fixture failures are not permission to weaken inventories. Publication is separate from local delivery.
