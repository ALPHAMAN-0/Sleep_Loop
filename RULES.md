# RULES.md — the loop must follow these, and it grows them itself

## Rules for RULES.md
- Add a rule whenever the agent repeats a mistake.
- Curate it yourself; you own this file.
- Prefer deterministic checks over a plain note.
- Don't let the loop auto-fill it with noise — one rule per real failure.

## Seeded rules (written by a human once)
- A fix is not done until the checker runs the FULL test suite green.
- Never widen behaviour to make one test pass while breaking another.

## Learned rules (appended by the loop, newest last)
<!-- the loop writes below this line -->
- strategy 'spaces-only' fails because test_strip_whitespace failed the suite — keep handling it
- strategy 'handle-underscores-and-trim' fails because test_drops_punctuation failed the suite — keep handling it
- strategy 'drop-punctuation' fails because test_collapses_hyphens failed the suite — keep handling it
