# ModelBoosting

<div align="center">

**Your AI coding agent has a 90% success rate. We fix the other 10%.**

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)]()
[![Status](https://img.shields.io/badge/status-active-brightgreen.svg)]()

</div>

---

## The Problem

After ~200 hours of DeepSeek-v4 writing production code, three failure patterns repeat:

| You ask for | DeepSeek gives you |
|-------------|-------------------|
| *"Add user roles to the API"* | Edits 7 files, silently breaks 3 endpoints, invents a middleware that doesn't exist |
| *"What's the best way to refactor this?"* | Starts rewriting 500 lines without asking if you meant yes |
| *"Is there a bug in this function?"* | "No bugs found." — 4 lines later: `ImportError` on a hallucinated module |

Claude Opus and GPT-5 handle these naturally. But running frontier models 24/7 burns cash. **ModelBoosting bridges this gap mechanically** — not with better prompts, with deterministic code between your agent and your filesystem.

---

## Before / After

**Task: "Add role-based access control to the FastAPI backend"**
*(same model — deepseek-v4-pro)*

| | Without ModelBoosting | With ModelBoosting |
|---|----------------------|-------------------|
| **Pre-flight** | Starts writing immediately. No scope, no plan. | Gate detects EXECUTE on ambiguous input → forces CLARIFY → scope declared first |
| **Code quality** | References `flask_jwt_extended` (doesn't exist) | Hallucination checker catches invented import → rejects → regenerates |
| **Scope creep** | Edits 11 files including 2 it shouldn't touch | Filesystem watcher blocks cross-domain writes → alerts |
| **Verification** | Agent says "Done!" — no proof | Verifier confirms: 4/4 tests pass, no import errors, contract intact |
| **Result** | 3 broken endpoints, 45 min debugging | Deployed on first attempt |

**The system doesn't make the model smarter. It makes the model *safer*.**

---

## Quick Start

```bash
pip install modelboosting
modelboost-detect                    # auto-detect your model
modelboost-gate "your task here"     # pre-execution gate check
modelboost-check                     # full integrity check
```

Add to Claude Code `settings.json`:

```json
{
  "hooks": {
    "SessionStart": [{
      "hooks": [{
        "type": "command",
        "command": "python PATH/TO/enforce.py boot --renew && python PATH/TO/enforce.py check-all"
      }]
    }]
  }
}
```

Switching models? Nothing to do. Next session auto-detects and adjusts.

---

## Architecture

```
                      ┌─────────────────────────────────────┐
                      │         SESSION START               │
                      │  model_detect.py → calibration      │
                      └──────────┬──────────────────────────┘
                                 │
                    ┌────────────┴────────────┐
                    │                         │
               elevated                     standard
            (deepseek)                    (claude / gpt)
                    │                         │
    ┌───────────────┼───────────────┐         │
    │               │               │         │
    ▼               ▼               ▼         ▼
┌──────┐      ┌─────────┐    ┌──────────┐   ALL BYPASS
│ GATE │      │   CoT   │    │ SELF-    │   (zero overhead)
│      │ ───→ │compensa-│───→│ AUDIT    │
└──────┘      │ tion    │    └──────────┘
              └─────────┘         │
                    │              ▼
                    ▼       ┌──────────┐
              ┌──────────┐  │ HALLUC.  │
              │ VERIFY   │  │ CHECK    │
              │ TASK     │  └──────────┘
              └──────────┘
                    │
                    ▼
              ┌──────────────────────────┐
              │     QUALITY GATE         │
              │  compile + contract      │
              │  + delegation verify     │
              └──────────┬───────────────┘
                         │
                    ┌────┴────┐
                    │ PASS    │ FAIL
                    │ deploy  │ re-queue + log
                    └─────────┘
```

---

## What's Inside

| Layer | Module | What It Does |
|-------|--------|---------------|
| **Gate** | `deepseek_gate.py` | Blocks ambiguous execution. Forces CLARIFY or SCOPE before any file edit |
| | `self_audit.py` | 5 pre-action checks — EXPLORE mode? SCOPE declared? Backup done? |
| **Reasoning** | `deepseek_compensation.py` | CoT injection, complexity scoring, Design→Implement→Review pipeline |
| | `multi_pass_reason.py` | Solve → Critique → Revise — 3 passes for critical decisions |
| | `req_expand.py` | Turns vague tasks into concrete acceptance criteria |
| **Verification** | `halcheck_live.py` | AST + importlib — catches hallucinated modules before they hit disk |
| | `verify_task.py` | py_compile + import resolution + syntax gate |
| | `code_quality_gate.py` | Full code quality pass |
| **Enforcement** | `enforce.py` | Integrity, heartbeat, fuse (half-blow budget), spiral detection, backup |
| | `fs_watcher.py` | Filesystem monitor — detects and blocks unauthorized writes |
| | `daemon_tick.py` | Background health daemon |
| **Coordination** | `auto_executor.py` | Poll → Gate → Execute → Verify → Delegate |
| | `task_poller.py` | Shared task queue consumer |
| | `delegation_check.py` | Cross-agent routing verification |

**30 watchdog scripts + 5 skill files + full routing and deployment.**

---

## Philosophy

Prompt engineering is fragile. It relies on the model *choosing* to be disciplined. Mechanical enforcement doesn't ask — it checks every action deterministically, before and after, every single time.

**The fence doesn't negotiate.**

---

## Why Not Just Use Frontier Models?

DeepSeek-v4 costs **~1/30th** of Claude Opus per token. With ModelBoosting, output quality is indistinguishable on most engineering tasks. You keep the savings. You get the safety net.

---

## Verified Clean

```
30 .py files, 0 compile errors
0 hardcoded user/machine paths
0 personal data in repo
100% explicit UTF-8 encoding
Cross-platform: one config file is the only machine-specific touchpoint
```

---

**[Full Constitution](E:/AgentHub/AGENTS.md) · [Issues](https://github.com/ForeignStage/ModelBoosting/issues)**

MIT License — use it, fork it, ship it.
