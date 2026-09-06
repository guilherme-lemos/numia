# Test fixtures

Everything here is **synthetic** — fake names, fake account numbers, made-up
amounts. This is the one place in the repo where committing bank-statement-
shaped files is fine and expected; see `AGENTS.md` § Sensitive financial data.

Never copy a real export in here, even trimmed or "anonymized" by hand.

- `ofx/` — sample `.ofx` files for parser tests.
- `csv/` — sample bank-export-style `.csv` files, ideally one per distinct
  column layout you need to support (banks don't share a schema).
