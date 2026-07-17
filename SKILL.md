# SKILL — project knowledge the loop reads on every run

- The function under repair lives in `target/string_utils.py`.
- Tests are the contract; read them before editing — they ARE the spec.
- Python's `re` module is available. `re.sub` is the right tool here.
- Order matters: lowercase and strip FIRST, then substitute, then collapse,
  then strip stray hyphens LAST.
- Keep the public signature `slugify(text: str) -> str` unchanged.
