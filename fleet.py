#!/usr/bin/env python3
"""
fleet.py — section 4, the FLEET variant.

The single-agent loop in loop.py is enough for most tasks: cheap, simple, one
brain improving its own work. Reach for a fleet only when one agent isn't
enough — then specialists run under an orchestrator and EVERY agent still runs
its own loop.

Here three specialists each own one slice of the goal. The orchestrator decides
when the whole job is done. Same closed-loop, gate, and memory machinery.
"""
from __future__ import annotations
from loop import Maker, Checker, notify


class ResearchAgent:
    """Reads the spec and tests, states the contract in plain terms."""
    def work(self) -> str:
        return "slug = lowercase, trim, [\\s_]->-, drop non-[a-z0-9-], collapse -, strip -"


class EngineeringAgent:
    """Writes the code. Wraps the same Maker subagent from the single loop."""
    def __init__(self):
        self.maker = Maker()

    def work(self, failed: set[str]) -> tuple[str, str]:
        return self.maker.propose(failed)


class QAAgent:
    """Runs the quality gate. Wraps the same Checker — never the maker."""
    def __init__(self):
        self.checker = Checker()

    def work(self, workdir):
        return self.checker.gate(workdir)


class FleetOrchestrator:
    """Owns the goal; decides when the fleet is done. Use only if one agent
    can't hold the whole job. For slugify, the single loop is the right call —
    this is here to show the shape, not because the task needs it."""
    def __init__(self):
        self.research = ResearchAgent()
        self.engineering = EngineeringAgent()
        self.qa = QAAgent()

    def run(self):
        notify("fleet started under orchestrator")
        contract = self.research.work()
        notify(f"research agent fixed the contract: {contract}")
        notify("orchestrator hands off to engineering, then QA — each runs its own loop")
        # In practice the orchestrator would now drive the same run() cycle as
        # SingleAgentLoop, fanning work out to specialists in parallel worktrees.


if __name__ == "__main__":
    FleetOrchestrator().run()
