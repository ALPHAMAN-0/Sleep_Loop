#!/usr/bin/env bash
# BLOCK 1: AUTOMATIONS — the heartbeat. Runs on a schedule, not on you.
# Wire it once and walk away. Example cron entry (nightly at 2am):
#
#   0 2 * * *  /path/to/sleep-loop/run_loop.sh >> /path/to/sleep-loop/.loop/cron.log 2>&1
#
set -euo pipefail
cd "$(dirname "$0")"
echo "=== sleep-loop run @ $(date) ==="
python3 loop.py
