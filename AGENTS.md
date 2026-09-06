# AGENTS.md — Guardrails for AI Agents in this Repo

This file applies to **any** AI coding agent working in this repository (Claude
Code, Codex, Cursor, Copilot, etc.). Tool-specific instructions live in their
own files (e.g. `CLAUDE.md`); those files must not contradict this one.

## What this project is

Numia is an early-stage personal finance tool (Python). It parses bank
statement exports in **OFX** (via `ofxparse`) and **CSV** (via pandas) formats,
stores transactions in a database (SQLAlchemy), and produces reports/
dashboards (pandas, plotly, Streamlit). There are two CLI entry points:
`numia` (`src/numia/cli.py`) and `pytrato` (`src/numia/report.py`). The
codebase is currently a bootstrap skeleton — expect a lot of the architecture
to still be undecided.

Bank CSV exports have no standard schema — column names/order/date formats
vary per bank. Don't assume a single hardcoded layout works for all inputs;
if you build CSV parsing, make the column mapping explicit and easy to adapt
per source, and confirm the target format(s) with the user rather than
guessing.

## 1. Sensitive financial data — hard rules

This project's entire purpose is to ingest real bank/financial data. Treat
that as the highest-risk part of the repo.

- **Never commit real financial data**: OFX/QFX/CSV bank exports, account
  numbers, balances, transaction histories, statements, screenshots of bank
  websites, or any file that looks like it came from a real account. If you
  find such a file staged or already tracked, stop and flag it instead of
  committing/pushing it.
- **Never commit credentials or secrets**: bank logins, API keys, DB
  connection strings with passwords, `.env` files. Check file contents before
  `git add`, not just filenames.
- **Sample/test data must be synthetic.** When you need fixtures for tests or
  demos, generate fake data (fake names, round/randomized amounts, fake
  account numbers) — never anonymize-by-editing a real export.
- **Local databases and data files are not build artifacts to clean up
  carelessly.** A `*.db`, `*.sqlite`, or data directory may contain a real
  user's imported financial history. Don't delete, truncate, or overwrite one
  without checking with the user first.
- If you're unsure whether something is real or synthetic data, ask before
  acting on it (committing, printing full contents to logs, uploading it
  anywhere).

## 2. Dependencies & environment

- This project uses **uv** (`pyproject.toml` + `uv.lock`), Python `>=3.14`.
- Use `uv add <pkg>` / `uv remove <pkg>` to change dependencies — don't
  hand-edit `pyproject.toml`'s dependency list or `uv.lock` directly.
- Don't add a new dependency for something the standard library or an
  existing dependency (pandas, sqlalchemy, plotly, streamlit, ofxparse,
  pyyaml) already covers.
- Don't upgrade/downgrade pinned versions or change `requires-python` unless
  the task specifically calls for it — ask first.

## 3. Scope discipline

- This is a bootstrap-stage project with almost no code yet. Resist the urge
  to scaffold a "full" architecture (layers, abstractions, config systems,
  plugin frameworks) that nothing has asked for. Build the thing that was
  requested; let structure emerge from real needs.
- Don't introduce a web framework, task queue, ORM alternative, or new major
  dependency to solve a problem the current stack already handles.
- Keep changes scoped to what was asked. Don't refactor unrelated files,
  rename things, or "clean up" code you weren't asked to touch.

## 4. Database & migrations

- SQLAlchemy is the persistence layer. Any schema change is effectively
  irreversible for a user with real data already imported.
- Don't run destructive operations (`DROP TABLE`, bulk `DELETE`, dropping a
  local dev DB file) without explicit confirmation, even in "just testing"
  contexts.
- If a schema/migration approach doesn't exist yet and you need one, propose
  it before writing it — don't silently pick a migration framework.

## 5. Code style

- **Language: English, always.** Code, identifiers, comments, docstrings,
  commit messages, and all documentation (this file, `CLAUDE.md`, `README.md`,
  requirements docs, etc.) must be written in English — regardless of what
  language the conversation with the user happens in.
- Follow PEP 8; use type hints for new functions.
- No docstrings/comments explaining *what* code does — only add a comment
  when there's a non-obvious *why* (a workaround, a subtle invariant).
- Tests use `pytest` — see § Testing strategy below for how/where.

## 5b. Testing strategy

Every test's subject must be code in `src/numia`. We don't re-test our
dependencies (`ofxparse`, `pandas`, `sqlalchemy`, `streamlit`, `plotly`,
`playwright`) — they have their own test suites and we trust their
documented behavior. If a test's only assertions are about a third-party
library's output with no `numia` code in the call path, it isn't testing
this project and shouldn't be added — including as a way to "prove a fixture
works" ahead of the code that will consume it. Write the test once the
project code it's meant to exercise exists, not before.

This follows the classic **test pyramid** — three levels, most tests at the
bottom, fewest at the top — as described by Mike Cohn (*Succeeding with
Agile: Software Development Using Scrum*, 2009) and popularized by Martin
Fowler ([martinfowler.com/bliki/TestPyramid.html](https://martinfowler.com/bliki/TestPyramid.html)):
**Unit → Integration → End-to-end (E2E/UI)**. Fowler is explicit that teams
name the middle/top layers differently ("service", "component",
"acceptance"...) — what matters is the shape, not the label — so we're
picking the mainstream three names rather than inventing our own.

Separately, "functional" is **not a level of this pyramid at all** — per the
[ISTQB Glossary](https://glossary.istqb.org/), functional testing is a test
*type* (verifying the system does what its functional requirements say),
orthogonal to unit/integration/E2E (which are test *levels*, about scope and
real-vs-fake dependencies). A unit test can be functional; so can an E2E
test. We don't use "functional" as a separate layer name for that reason —
an earlier draft of this document did, incorrectly implying it was a
standard term for "integration test without a browser," and that's been
removed.

Three layers, mapped to `tests/<layer>/` (each has its own README with more
detail). Every layer runs via `uv run pytest`; see `CLAUDE.md` for exact
commands.

- **Unit** (`tests/unit/`, no marker needed): isolated functions/classes,
  everything external mocked (no real files, DB, network, subprocess,
  browser). Mirrors `src/numia/` module paths (`test_<module>.py`).
  **This is the only layer the 90% coverage gate applies to**
  (`[tool.coverage]` in `pyproject.toml`, `fail_under = 90`), measured by
  running *only* this directory with coverage on: `uv run pytest tests/unit
  --cov`. It applies to core logic only: parsers, classification, DB layer,
  report/data-generation code. Streamlit UI modules (convention:
  `src/numia/ui/*`) and `if __name__ == "__main__":` blocks are excluded
  from the coverage calculation (`coverage.omit` / `exclude_also`), not from
  testing — they're covered by integration/E2E instead.
  Integration and E2E tests must pass, but are **not** counted toward the
  90% number and are never run together with `--cov` for gating purposes —
  they exist to catch defects across real boundaries (parser libs, DB,
  browser), not to inflate a coverage percentage. Don't treat a passing
  integration/E2E suite as a substitute for unit coverage on the same code.
- **Integration** (`tests/integration/`, `@pytest.mark.integration`): real
  collaborators, no browser. Two shapes:
  - *Parsers*: the project's own parser modules — not mocked, so they do
    exercise the real third-party library underneath — run against real
    synthetic fixture files (`tests/fixtures/{ofx,csv}/`), asserting on
    *our* normalized output. The library call is incidental; the thing
    under test is always our code.
  - *Pipelines/DB*: multi-module flows through our own code with real
    collaborators wired together — e.g. raw fixture file in, report
    DataFrame/object out (parse → classify → persist → report), or real
    SQLAlchemy models/queries against a throwaway SQLite DB (`tmp_path`
    file or `:memory:`, never the user's real local `.db`).
- **E2E** (`tests/e2e/`, `@pytest.mark.e2e`): Playwright drives the real
  Streamlit app in a real browser, launched as a subprocess against a
  throwaway DB seeded with synthetic data. Covers "does the dashboard/chart
  actually render," which no other layer can.

Rules for agents adding features:

- New parser/classification/report logic needs a unit test in the same
  change. A new file format or column layout needs a new fixture under
  `tests/fixtures/` plus an integration test. A change to the pipeline
  wiring (parse → classify → persist → report) needs an integration test
  covering the new path.
- A change to what the UI shows the user needs an e2e check for the golden
  path — don't rely on "the unit tests pass" as proof the dashboard works.
- Fixture data must always be synthetic (see § Sensitive financial data) —
  this is the one place in the repo where committing bank-statement-shaped
  files is correct and expected.
- Don't lower `fail_under`, add `# pragma: no cover`, or widen
  `coverage.omit` to dodge the gate — if core logic is genuinely hard to
  cover, say so and ask instead of quietly excluding it.
- Playwright tests must tear down their app subprocess/temp DB even on
  failure (fixture with `yield` + cleanup). Don't commit
  screenshots/traces/videos — they're `.gitignore`d as debugging artifacts,
  not assertions.

## 6. Git hygiene

- Never force-push, `git reset --hard`, or rewrite history on `main` without
  explicit instruction.
- Review `git status`/`git diff` before every commit — especially after a
  broad `git add` — and double-check file contents (not just names) for
  anything that looks like real financial data or secrets.
- Don't push to the remote or open PRs unless asked.

## 7. When in doubt, ask

Prefer asking over guessing when the decision involves: real user data,
schema/migration design, a new major dependency, or deleting/overwriting
anything that isn't clearly disposable output you created this session.
