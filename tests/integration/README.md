# Integration tests

Marked `@pytest.mark.integration`. Real collaborators, no browser. Three
shapes:

- **Parsers**: feed a real synthetic file from `tests/fixtures/{ofx,csv}/`
  through the project's own parser module (e.g. `numia.parsers.ofx`) — not
  mocked — and assert on *its* output (the normalized transactions our code
  produces). The subject under test is our wrapper, not `ofxparse`/pandas
  itself. Don't add a test whose only call is directly into the third-party
  library with no `numia` code in between — there's nothing of ours to
  verify yet, so there's nothing to test.
- **Database**: exercise real SQLAlchemy models/queries (our schema, our
  query functions) against a throwaway SQLite database (`tmp_path`-based
  file or `sqlite:///:memory:` — never the user's real local `.db` file).
- **Pipelines**: multi-module flows through our own code with real
  collaborators wired together, no browser — e.g. raw fixture file in,
  report DataFrame/object out (parse → classify → persist → report).

See `AGENTS.md` § Testing strategy for fixture rules and why this is one
level ("integration"), not split into a separate "functional" layer.
