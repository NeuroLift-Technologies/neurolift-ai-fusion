# CLAUDE.md — Repository Context for AI Agents

**Repository:** NeuroLift-Technologies/neurolift-ai-fusion  
**Governance:** ORG-DEV-OTOI-1.0.0  
**Last updated:** 2026-04-25

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
├── apps/                   # Full-stack application layer
│   ├── api/                # FastAPI backend (wraps simulation engine)
│   │   ├── main.py         # App entry point
│   │   ├── routers/        # Route handlers (avatars, aides, sessions, advocates)
│   │   ├── schemas/        # Pydantic request/response models
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   ├── web/                # Next.js 14 web app (TypeScript + Tailwind)
│   │   ├── app/            # App Router pages (dashboard, session)
│   │   ├── components/     # Shared UI components
│   │   └── lib/            # API client + types
│   └── mobile/             # Expo (React Native) — iOS & Android
│       ├── app/            # Expo Router screens
│       │   ├── (tabs)/     # Tab navigation (dashboard, sessions, profile)
│       │   └── session/    # Session detail & new session screens
│       └── lib/            # API client + types
├── src/                    # Python simulation engine
│   ├── avatars/            # Avatar trait implementations
│   ├── aides/              # Aide coaching implementations
│   ├── core/               # Core infrastructure (events, signals, DB)
│   ├── simulation/         # SessionOrchestrator + WorldEngine
│   ├── fusion/             # Fusion engine + readiness assessor
│   └── database/           # Supabase abstraction layer
├── tests/                  # pytest test suite
├── docs/                   # Project documentation
│   ├── architecture.md     # System architecture
│   ├── active-threads.md   # Active work tracking (read before starting)
│   ├── agent-log/
│   │   ├── registrations/  # Agent registration records
│   │   └── handoffs/       # Session handoff records
│   ├── ai-guidance/        # AI assistant reference materials
│   └── cloudflare/         # Cloudflare integration docs
├── config/                 # All configuration (YAML + JSON)
├── supabase/               # Supabase schema and migrations
├── scripts/                # Utility scripts
├── cloudflare/             # Cloudflare Workers infrastructure
├── archive/                # Archived / deprecated content
├── package.json            # Monorepo root (npm workspaces)
├── turbo.json              # Turborepo build pipeline
├── requirements.txt        # Python simulation engine deps
├── pytest.ini              # pytest configuration
├── AGENTS.md               # Agent coordination gateway
├── CLAUDE.md               # This file
└── TOI-OTOI-INTEGRATION.md # TOI-OTOI framework overview
```

---

## Technology Stack

| Layer | Technology |
|-------|-----------|
| Simulation Engine | Python 3.11+ |
| API Backend | FastAPI + uvicorn (`apps/api/`) |
| Web Frontend | Next.js 14 + TypeScript + Tailwind CSS (`apps/web/`) |
| Mobile (iOS + Android) | Expo (React Native) + TypeScript (`apps/mobile/`) |
| Monorepo tooling | npm workspaces + Turborepo |
| Database | Supabase (PostgreSQL) with Row-Level Security |
| Testing | pytest (Python) |
| CI/CD | GitHub Actions (python-app.yml, web.yml, mobile.yml, shared-ci.yml) |
| Infrastructure | Cloudflare (Workers, Pages) |

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

1. `NLT-DEV-OTOI.md` (repo root synced copy) — OTOI constitutional document used by this repository
2. `AGENTS.md` — Agent coordination gateway
3. `CLAUDE.md` — This file ✓
4. `docs/active-threads.md` — Current work and ownership
5. `docs/architecture.md` — System architecture

If `NLT-DEV-OTOI.md` is missing in the repository root, request a run of **Sync Governance (Public)** (`.github/workflows/sync-governance-public.yml`) to refresh governance docs from `NeuroLift-Technologies/.github-private`.

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
