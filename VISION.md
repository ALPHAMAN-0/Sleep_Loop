# VISION — what "done" means

GOAL: `target/string_utils.py::slugify` must turn any human string into a clean URL slug.

A slug must:
- be lowercase
- have leading/trailing whitespace removed
- replace runs of spaces or underscores with a single hyphen
- drop every character that is not a-z, 0-9, or hyphen
- collapse runs of hyphens into one
- have no leading or trailing hyphen

DEFINITION OF DONE (checked automatically, never by vibes):
- every test in target/test_string_utils.py passes
- the file still compiles (syntax + parses)
- no lint violation from the bundled checker

This is a CLOSED loop: fixed goal, fixed steps, automatic validation.
A wrong attempt is cheap (we work on a throwaway copy), the task has a
machine-checkable definition of done, and it is worth wiring because the
same loop guards this function forever.
