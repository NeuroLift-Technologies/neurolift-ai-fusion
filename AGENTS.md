# AGENTS.md — NLT Agent Coordination Gateway

**Governance Version:** ORG-DEV-OTOI-1.0.0  
**Repository:** NeuroLift-Technologies/neurolift-ai-fusion  
**Maintained by:** Joshua W. Dorsey, Sr.

---

## Purpose

This file is the internal coordination gateway for all AI agents working in this repository. It defines how agents coordinate, what the non-negotiable guardrails are, and how multi-agent sessions are managed.

All agents **must** read this file before beginning any work. Reading `AGENTS.md` is Step 2 of the SOP-NLT-001 onboarding process.

---

## Solidarity Framework

All agents operating in this repository commit to the **Solidarity Framework** — a set of principles ensuring consistent, ethical, and human-aligned behavior across all AI contributors:

1. **Human primacy** — Humans retain final decision authority. Agents advise, implement, and flag; they never decide unilaterally on strategic, architectural, or resource questions.
2. **Transparency** — All work must be traceable: commits are formatted, sessions are logged, handoffs are written.
3. **No silent failures** — Blockers, ambiguities, and out-of-scope requests are escalated immediately rather than worked around.
4. **Escalation over assumption** — When in doubt, pause and escalate to Joshua W. Dorsey, Sr. via `info@neuroliftsolutions.com`.
5. **Continuity** — Every session ends with a handoff record so the next agent can pick up without loss of context.

---

## Non-Negotiable Guardrails

The following are absolute constraints for all agents in this repository:

| Guardrail | Rule |
|-----------|------|
| **No credentials in code** | Never commit API keys, passwords, tokens, or secrets to VCS |
| **No LLM lock-in** | Do not hard-code a specific LLM provider without Joshua's written approval |
| **No unilateral architecture changes** | Any changes to system design, data models, or external integrations require escalation |
| **No production deployments** | Agents do not deploy to production — humans do |
| **No scope expansion** | Work only within the confirmed task scope; escalate additions |
| **Commit format required** | All commits must use `[AGENT_NAME] type(scope): description` |

---

## Commit Format

Every commit from an agent **must** follow this exact format:

```
[AGENT_NAME] type(scope): description
```

**Valid types:** `feat`, `fix`, `docs`, `refactor`, `chore`, `test`, `ci`

**Examples:**
```
[CLAUDE] feat(avatar): add task initiation simulation for StayAlertAvatar
[COPILOT] fix(api): resolve null pointer in training session endpoint
[CODEX] docs(readme): update environment setup instructions
[GEMINI] chore(governance): add agent coordination stubs (ORG-DEV-OTOI-1.0.0)
```

---

## Multi-Agent Coordination

This repository may have multiple agents working across sessions. To coordinate:

1. **Check `docs/active-threads.md`** before starting — it lists active work and who owns it.
2. **Register yourself** in `docs/agent-log/registrations/` at session start (SOP-NLT-001 Step 5).
3. **Write a handoff record** in `docs/agent-log/handoffs/` at session end (SOP-NLT-001 Step 8).
4. **Do not duplicate work** in progress — coordinate through handoff records and active threads.

---

## Escalation Protocol

Escalate **immediately** (do not proceed) if the task involves any of:

- Architecture or system design decisions
- New external service integrations (Supabase, OpenAI, Cloudflare, etc.)
- Production deployments or infrastructure changes
- LLM provider selection or switching
- Changes to privacy policy or data retention rules
- Any request that conflicts with ORG-DEV-OTOI-1.0.0

**Escalation contact:** Joshua W. Dorsey, Sr. — `info@neuroliftsolutions.com`

---

## Key Files for Agents

| File | Purpose |
|------|---------|
| `NLT-DEV-OTOI.md` (repo root, synced copy) | Constitutional document — the OTOI contract used by this repository |
| `NeuroLift-Technologies/.github-private` (upstream repo) | Upstream governance source used by sync automation — not a path in this repository |
| `AGENTS.md` | This file — coordination gateway |
| `CLAUDE.md` | Repo-specific context for this repository |
| `docs/active-threads.md` | Active work tracking |
| `docs/agent-log/registrations/` | Agent session registration records |
| `docs/agent-log/handoffs/` | Session handoff records |
| `TOI-OTOI-INTEGRATION.md` | TOI-OTOI framework overview |
| `docs/architecture.md` | System architecture reference |

---

## Onboarding Reference

New agents must complete all 8 steps of **SOP-NLT-001** before writing code:

1. Read `NLT-DEV-OTOI.md` (repo root). If unavailable, request a governance sync from the upstream repo `NeuroLift-Technologies/.github-private` by triggering `.github/workflows/sync-governance-public.yml`.
2. Read `AGENTS.md` ← **you are here**
3. Read `CLAUDE.md`
4. Read `docs/active-threads.md`
5. Complete self-registration (`docs/agent-log/registrations/`)
6. Confirm task scope with human
7. Begin work with correct commit format
8. End session with handoff record (`docs/agent-log/handoffs/`)
