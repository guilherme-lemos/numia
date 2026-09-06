# E2E tests (Playwright)

Marked `@pytest.mark.e2e`. Drive the real Streamlit app through a real
browser: launch it as a subprocess on a fixed local test port against a
throwaway DB seeded with synthetic data, then use Playwright to load the
page, interact, and assert on rendered content (including that plotly charts
actually render).

Rules:

- Never point these at a real user database or real bank export — seed a
  temp DB with synthetic fixtures from `tests/fixtures/`.
- Always tear down the app subprocess and temp DB after the test, even on
  failure (use a fixture with `yield` + cleanup, not a bare `subprocess.run`).
- Screenshots/videos/traces are debugging artifacts, not test assertions —
  don't commit them; they're covered by `.gitignore`.

See `AGENTS.md` § Testing strategy for the full rationale.
