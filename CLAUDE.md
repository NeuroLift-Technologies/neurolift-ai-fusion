# CLAUDE.md — Repository Context for AI Agents

**Repository:** NeuroLift-Technologies/neurolift-ai-fusion  
**Governance:** ORG-DEV-OTOI-1.0.0  
**Last updated:** 2026-04-05

---

## What This Repository Is

`neurolift-ai-fusion` is the core AI training platform for NeuroLift Technologies. It implements the **Avatar-Aide-Advocate** system — an experiential learning framework designed to simulate ADHD traits and provide evidence-based coaching through AI agents.

The system enables:
- **Avatars** — AI entities that simulate specific ADHD trait profiles (attention drift, task initiation difficulty, etc.)
- **Aides** — AI coaching agents with domain expertise (attention science, task management, emotional regulation)
- **Advocates** — Higher-level agents that coordinate Avatar-Aide pairs and escalate to human oversight
- **Training sessions** — Structured interactions that generate learning data and coaching outcomes

---

## Repository Structure

```
neurolift-ai-fusion/
├── src/                    # Core application source
│   ├── avatars/            # Avatar trait implementations
│   ├── aides/              # Aide coaching implementations
│   ├── core/               # Core infrastructure (events, signals, DB)
│   └── simulation/         # Simulation environment (WorldEngine)
├── tests/                  # Test suite (pytest)
├── docs/                   # Project documentation
│   ├── architecture.md     # System architecture
│   ├── active-threads.md   # Active work tracking (read before starting)
│   ├── agent-log/
│   │   ├── registrations/  # Agent registration records
│   │   └── handoffs/       # Session handoff records
│   ├── ai-guidance/        # AI assistant reference materials
│   ├── cloudflare/         # Cloudflare integration docs
│   └── handoffs/           # Legacy handoff format (older sessions)
├── config/                 # Configuration files
├── supabase/               # Supabase schema and migrations
├── scripts/                # Utility scripts
├── AGENTS.md               # Agent coordination gateway
├── CLAUDE.md               # This file
└── TOI-OTOI-INTEGRATION.md # TOI-OTOI framework overview
```

---

## Technology Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.11+ |
| Database | Supabase (PostgreSQL) with Row-Level Security |
| Testing | pytest |
| CI/CD | GitHub Actions (shared-ci.yml, python-app.yml) |
| Infrastructure | Cloudflare (Workers, Pages) |
| Package manager | pip / requirements.txt |

---

## Key Architectural Principles

1. **Privacy-first** — Data retention is ephemeral by default; all overrides require human approval
2. **Human agency** — Agents are advisory; all strategic and architectural decisions belong to humans
3. **Graceful degradation** — All Supabase-dependent features must fall back gracefully when DB is unavailable
4. **TOI-OTOI compliant** — All components implement the Terms of Interaction framework (see `TOI-OTOI-INTEGRATION.md`)
5. **Modular design** — Avatars, Aides, and Advocates are independently swappable

---

## Development Conventions

### Python Style
- Follow PEP 8
- Use type hints on all public functions and methods
- Docstrings on all public classes and methods
- No bare `except:` — always catch specific exceptions

### Testing
- Test file naming: `test_<module_name>.py`
- Run tests: `pytest` (configured in `pytest.ini`)
- Tests live in `tests/`
- Aim for isolation — mock external dependencies (Supabase, etc.)

### Imports
- Use absolute imports from the `src/` root
- No circular imports

### Database
- All DB interactions go through the abstraction layer in `src/core/`
- Never expose raw SQL in business logic layers
- Always handle the case where Supabase is unavailable

---

## Required Reading for New Agents

Before writing any code, read these files in order:

1. `.github-private/NLT-DEV-OTOI.md` — OTOI constitutional document
2. `AGENTS.md` — Agent coordination gateway
3. `CLAUDE.md` — This file ✓
4. `docs/active-threads.md` — Current work and ownership
5. `docs/architecture.md` — System architecture

---

## Escalation

Any of the following **requires escalation** to Joshua W. Dorsey, Sr. before proceeding:

- Changes to the Avatar or Aide base class interfaces
- New external service integrations
- Database schema migrations
- Changes to RLS policies or data retention rules
- LLM provider decisions
- Production deployment steps

**Contact:** `info@neuroliftsolutions.com`

---

## Governance

This repository operates under **ORG-DEV-OTOI-1.0.0**. All agents must:

- Complete SOP-NLT-001 onboarding before writing code
- Use the commit format: `[AGENT_NAME] type(scope): description`
- Register at session start in `docs/agent-log/registrations/`
- Write a handoff record at session end in `docs/agent-log/handoffs/`
