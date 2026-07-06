#!/usr/bin/env python3
"""CLI entry points for pip-installed modelboosting."""

import os, sys, json, subprocess

_WD = os.path.dirname(os.path.abspath(__file__))
# Resolve watchdog scripts relative to package location
_ROOT = os.path.normpath(os.path.join(_WD, "..", "watchdog"))
CONFIG = os.path.join(_ROOT, "config.json")


def _python():
    """Best-effort Python resolution: config.json > sys.executable."""
    try:
        with open(CONFIG, "r", encoding="utf-8") as f:
            return json.load(f)["paths"]["python_exe"]
    except Exception:
        return sys.executable


def _run(script, *args):
    """Run a watchdog script via subprocess and stream output."""
    py = _python()
    cmd = [py, os.path.join(_ROOT, script)] + list(args)
    return subprocess.run(cmd, capture_output=False)


def gate():
    """Pre-execution gate — blocks ambiguous EXECUTE on DeepSeek."""
    task = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""
    if not task:
        print("Usage: modelboost-gate <task description>")
        sys.exit(1)
    proc = _run("deepseek_gate.py", task, _ROOT)
    sys.exit(proc.returncode)


def detect():
    """Model self-detection — sqlite > toml > config.json > settings.json."""
    proc = _run("model_detect.py", ".", "--persist", _ROOT)
    sys.exit(proc.returncode)


def check():
    """Full gate check — boot + fuse + integrity + heartbeat + mode + scope."""
    proc = _run("enforce.py", "check-all")
    sys.exit(proc.returncode)


def classify():
    """Complexity scoring for a task (1-5)."""
    task = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""
    if not task:
        print("Usage: modelboost-classify <task description>")
        sys.exit(1)
    proc = _run("deepseek_compensation.py", "classify", task)
    sys.exit(proc.returncode)
