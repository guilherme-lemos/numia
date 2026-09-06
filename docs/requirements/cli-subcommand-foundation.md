# Requirements: CLI Subcommand Foundation (init & report)

**Status:** Implemented
**Date:** 2026-09-06
**Implemented:** 2026-09-06
**Author:** guilherme@lemos.tec.br

## 1. Context

The `numia` CLI currently exposes a single `main()` function that prints one
line, with no subcommand structure. Report functionality lives in a separate
script entry point, `pytrato` (`numia.report:main`), unrelated to `numia` at
the command-line level.

Before any real feature (project/ledger initialization, reporting, etc.) is
implemented, the CLI needs a subcommand-based structure so that future
features can be added consistently as new subcommands rather than as ad-hoc
entry points.

**5W2H**
- **What**: refactor the `numia` CLI to route to subcommands via `argparse`,
  and introduce the first two subcommands: `init` (placeholder) and `report`
  (migrated from the standalone `pytrato` entry point).
- **Why**: establish the CLI subcommand pattern before real functionality is
  built on top of it.
- **Who**: the project owner/developer only — `numia` is a personal,
  single-user project with no other stakeholders.
- **Where**: local CLI, terminal usage only — no server component involved.
- **When**: now, as foundational work ahead of implementing real features.
- **How**: `argparse` (standard library), using `add_subparsers`.

**Business goal**: establish the CLI subcommand pattern that all future
`numia` commands will follow.

**Out of scope**:
- Real `init` behavior (actually creating a project/ledger — files, schema,
  config). Deferred to a future requirements document.
- Real `report` behavior beyond what already exists today (still a
  placeholder print).
- Validation/error handling for an invalid `init` path.
- Custom `--help` text — the default `argparse`-generated help/usage output
  is sufficient.

## 2. Functional Requirements & Acceptance Criteria

### US-1: CLI subcommand routing (Must)

As a developer, I want the `numia` CLI to route to subcommands via
`argparse`, so that future features can be added as new subcommands without
redesigning the entry point each time.

**Acceptance Criteria:**
- Given the CLI, When I run `numia` with no arguments, Then it prints
  `🚀 Numia v26.09.0` and exits with code 0 (existing fallback behavior is
  preserved).
- Given the CLI, When I run `numia init .`, Then it dispatches to the `init`
  subcommand handler.
- Given the CLI, When I run `numia foo` (an unknown subcommand), Then
  `argparse` rejects it with a usage error on stderr and exits with a
  non-zero status code.

### US-2: `init` placeholder command (Must)

As a user, I want to run `numia init <path>`, so that I have a starting
point that will later become full project/ledger initialization at that
location.

**Acceptance Criteria:**
- Given the CLI, When I run `numia init .`, Then it prints `.` and exits
  with code 0.
- Given the CLI, When I run `numia init /some/path`, Then it prints
  `/some/path` and exits with code 0.
- Given the CLI, When I run `numia init` without a path argument, Then
  `argparse` reports a missing required argument error and exits with a
  non-zero status code.

### US-3: `report` command migrated from `pytrato` (Must)

As a user, I want to run `numia report` instead of the separate `pytrato`
command, so that all functionality lives under one consistent CLI entry
point.

**Acceptance Criteria:**
- Given the CLI, When I run `numia report`, Then it prints `🚀 Report` and
  exits with code 0 (identical output to what `pytrato` prints today).
- Given the project is installed, When I try to run `pytrato` directly,
  Then the command is not found (its entry point has been removed from
  `pyproject.toml`).

## 3. Non-Functional Requirements

- **Portability**: the implementation must not use any OS-specific path
  syntax or OS-specific calls — use `pathlib.Path`, no `os.name`/
  `sys.platform` branching, no `subprocess` calls with `shell=True`.
  Verified by code review and unit tests; no CI matrix change (single
  `ubuntu-latest` runner stays as-is).
- **Maintainability**: adding a new subcommand in the future must require at
  most (1) one new handler function and (2) one new
  `subparsers.add_parser(...)` registration call — with no changes to the
  existing `init`/`report` handler code.

## 4. Risks & Assumptions

| Risk | Probability | Impact | Mitigation/Owner |
|------|-------------|--------|------------------|
| Removing the `pytrato` entry point breaks something depending on it | Low | Low | Pre-release, single-user project — no external consumers to protect |
| The `argparse` refactor regresses the current no-args fallback (`numia` printing the banner) | Low | Medium | Unit test explicitly covering the no-subcommand case |
| New CLI code drops the 90% unit coverage gate | Low | Medium | Unit tests for `init`, `report`, and the no-subcommand case are part of this change (already required by `AGENTS.md`) |

**Assumptions:**
- `argparse` with subparsers is sufficient for the next real subcommands
  (e.g. import, classify) without needing to switch to a different CLI
  library later.
- `numia report`'s output stays byte-identical to what `pytrato` prints
  today (`🚀 Report`) — the migration does not change the message.

**Open questions / dependencies:**
- None. Real `init`/`report` behavior is deferred to a future requirements
  document, out of scope here.

## 5. Definition of Ready

- [x] Every functional requirement has at least one Given/When/Then
      acceptance criterion, including a negative/edge case.
- [x] No requirement contains an undefined vague term.
- [x] Applicable NFRs have measurable thresholds.
- [x] Out-of-scope is stated explicitly.
- [x] All open questions/dependencies are either resolved or have an
      assigned owner.
- [x] Stakeholders/approvers for this requirement set are identified.
