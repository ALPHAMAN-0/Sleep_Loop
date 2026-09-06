# Sleep_Loop

## Run (no build/test/lint manifest found — these are the only executable commands with direct evidence, from README.md)
- `python3 loop.py` — single-agent loop
- `./run_loop.sh` — same, via the automation entrypoint (cron entry inside)
- `python3 fleet.py` — fleet shape (multi-agent)
- Build / lint / unit-test commands: TODO: verify (no package.json/pyproject.toml/Makefile found)

## Rules observed
- Never treat a passing run as merged: `target/string_utils.py` stays untouched after a pass — the proposed fix is written to `.loop/proposed_fix.py`. The merge is manual, by design (README).
- Don't hand-edit `RULES.md` above the marker: learned rules are appended below the line "the loop writes below this line"; deleting lines under that marker is the documented way to reset memory (README).

## Read first
- REPO_ROOT/README.md
- REPO_ROOT/loop.py
- REPO_ROOT/RULES.md

Architecture: see ARCHITECTURE.md — read before structural changes
