#!/usr/bin/env python3
"""
sleep-loop: a closed, self-learning loop that repairs slugify() while you sleep.

It maps 1:1 onto Loop Engineering 101:
  1. THE CYCLE        -> discover / plan / execute / verify / iterate (run())
  2. CLOSED LOOP      -> fixed goal (VISION.md), bounded steps, auto validation
  3. SIX BLOCKS       -> automation, worktree, skill, connector, subagents, memory
  4. SINGLE vs FLEET  -> SingleAgentLoop here; FleetOrchestrator in fleet.py
  5. LOOP IN PRACTICE -> load goal+rules, maker writes, checker verifies, gate, learn
  6. QUALITY GATE     -> parse + lint + full test suite (things you can't argue with)
  7. SELF-LEARNING    -> every failure becomes a permanent rule in RULES.md
"""
from __future__ import annotations
import ast
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent
TARGET = ROOT / "target"
RULES = ROOT / "RULES.md"
NOTIFY_LOG = ROOT / ".loop" / "notifications.log"
PATCH_OUT = ROOT / ".loop" / "proposed_fix.py"
MAX_ATTEMPTS = 8


# --- BLOCK 4: PLUGINS & CONNECTORS -----------------------------------------
# The loop touches your real tools. Here it "pings you" to a log; in production
# this is a Slack message or a GitHub PR. The loop NEVER merges to main itself.
def notify(msg: str) -> None:
    NOTIFY_LOG.parent.mkdir(exist_ok=True)
    line = f"[{datetime.now():%H:%M:%S}] {msg}"
    with open(NOTIFY_LOG, "a") as f:
        f.write(line + "\n")
    print("  📣 " + msg)


# --- BLOCK 6: MEMORY --------------------------------------------------------
# Lessons live outside the conversation, in RULES.md, so the loop never forgets.
def learned_rules() -> list[str]:
    text = RULES.read_text()
    after = text.split("the loop writes below this line -->", 1)[-1]
    return [ln.strip("- ").strip() for ln in after.splitlines() if ln.strip().startswith("-")]


def append_rule(rule: str) -> None:
    if rule in learned_rules():
        return  # a mistake becomes a permanent check the loop can't repeat
    with open(RULES, "a") as f:
        f.write(f"- {rule}\n")
    notify(f"learned a new rule: {rule}")


# --- SUBAGENT A: THE MAKER (block 5) ---------------------------------------
# In production this is an LLM agent that reads VISION + SKILL + RULES and
# writes a patch. Here it's a deterministic stand-in with a ladder of candidate
# fixes so the demo runs with no API. It will not retry a strategy the memory
# already recorded as failed -- that's the learning showing up in behaviour.
class Maker:
    CANDIDATES = {
        "spaces-only": (
            'def slugify(text: str) -> str:\n'
            '    return text.lower().replace(" ", "-")\n'
        ),
        "handle-underscores-and-trim": (
            'import re\n\n'
            'def slugify(text: str) -> str:\n'
            '    s = text.strip().lower()\n'
            '    return re.sub(r"[\\s_]+", "-", s)\n'
        ),
        "drop-punctuation": (
            'import re\n\n'
            'def slugify(text: str) -> str:\n'
            '    s = text.strip().lower()\n'
            '    s = re.sub(r"[\\s_]+", "-", s)\n'
            '    return re.sub(r"[^a-z0-9-]", "", s)\n'
        ),
        "collapse-and-trim-hyphens": (
            'import re\n\n'
            'def slugify(text: str) -> str:\n'
            '    s = text.strip().lower()\n'
            '    s = re.sub(r"[\\s_]+", "-", s)\n'
            '    s = re.sub(r"[^a-z0-9-]", "", s)\n'
            '    s = re.sub(r"-+", "-", s)\n'
            '    return s.strip("-")\n'
        ),
    }
    ORDER = ["spaces-only", "handle-underscores-and-trim",
             "drop-punctuation", "collapse-and-trim-hyphens"]

    def __init__(self):
        self.goal = (ROOT / "VISION.md").read_text()
        self.skill = (ROOT / "SKILL.md").read_text()

    def propose(self, failed: set[str]) -> tuple[str, str]:
        rules = learned_rules()  # the maker is informed by memory every run
        print(f"  🤖 maker reads {len(rules)} learned rule(s), avoids {len(failed)} dead end(s)")
        for name in self.ORDER:
            if name not in failed:
                return name, self.CANDIDATES[name]
        raise RuntimeError("maker is out of ideas")


# --- SUBAGENT B: THE CHECKER (block 5, never the same agent as the maker) ---
# It owns the QUALITY GATE (section 6): three things the maker can't argue with.
class Checker:
    def gate(self, workdir: Path) -> tuple[bool, str]:
        src = workdir / "string_utils.py"

        # GATE 1 — the compiler / parser
        try:
            ast.parse(src.read_text())
        except SyntaxError as e:
            return False, f"does not parse: {e}"

        # GATE 2 — the linter (deterministic, opinion-free)
        for i, line in enumerate(src.read_text().splitlines(), 1):
            if line.rstrip() != line:
                return False, f"lint: trailing whitespace on line {i}"
            if "eval(" in line:
                return False, "lint: eval() is forbidden"

        # GATE 3 — the full test suite
        proc = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", "--no-header", "-x"],
            cwd=workdir, capture_output=True, text=True,
        )
        if proc.returncode != 0:
            failing = re.findall(r"(test_\w+)", proc.stdout)
            first = failing[0] if failing else "a test"
            return False, f"{first} failed the suite"
        return True, "all gates green"


# --- THE LOOP: discover, plan, execute, verify, iterate (sections 1 & 5) ----
class SingleAgentLoop:
    def __init__(self):
        self.maker = Maker()
        self.checker = Checker()
        # MEMORY across runs: recover dead ends from past nights' RULES.md so
        # the loop literally cannot repeat a mistake it already made.
        self.failed_strategies: set[str] = {
            m.group(1) for r in learned_rules()
            if (m := re.search(r"strategy '([^']+)' fails", r))
        }
        if self.failed_strategies:
            print(f"  🧠 recovered {len(self.failed_strategies)} dead end(s) from memory")

    # BLOCK 2: WORKTREES — every attempt runs on an isolated throwaway copy,
    # so parallel agents never collide and a wrong attempt costs nothing.
    def _worktree(self) -> Path:
        wt = Path(tempfile.mkdtemp(prefix="worktree-"))
        for f in TARGET.glob("*.py"):
            shutil.copy(f, wt / f.name)
        return wt

    def run(self) -> bool:
        notify("loop started")
        for attempt in range(1, MAX_ATTEMPTS + 1):
            print(f"\n── attempt {attempt} ──")
            wt = self._worktree()
            try:
                # EXECUTE: maker writes work
                name, code = self.maker.propose(self.failed_strategies)
                print(f"  ✍️  maker tries strategy: {name}")
                (wt / "string_utils.py").write_text(code)

                # VERIFY: a *different* agent checks it against the gate
                ok, reason = self.checker.gate(wt)
                if ok:
                    print(f"  ✅ {reason}")
                    self._open_pr(code, name, attempt)
                    return True

                # ITERATE: turn the failure into a permanent rule, then retry
                print(f"  ❌ {reason}")
                self.failed_strategies.add(name)
                append_rule(f"strategy '{name}' fails because {reason} — keep handling it")
            finally:
                shutil.rmtree(wt, ignore_errors=True)
        notify("loop gave up — needs a human")
        return False

    # The loop PROPOSES the fix and pings you. It does not ship on its own.
    def _open_pr(self, code: str, strategy: str, attempt: int) -> None:
        PATCH_OUT.write_text(code)
        notify(f"PASSED via '{strategy}' on attempt {attempt}. "
               f"Proposed fix written to {PATCH_OUT.name}. Review & merge — the merge is yours.")


if __name__ == "__main__":
    ok = SingleAgentLoop().run()
    print("\n" + ("🎉 done — your move" if ok else "🛑 escalated to you"))
    sys.exit(0 if ok else 1)
