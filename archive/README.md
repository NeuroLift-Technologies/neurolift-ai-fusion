# Archive

This directory contains files and directories that were removed from the active codebase because they do not belong in the NeuroLift AI-Fusion simulation/app repository. All items are preserved here for historical reference.

## Archived Items

| Directory / File | Reason Archived |
|---|---|
| `wordpress/` | WordPress marketing site theme for `neuroliftsolutions.com` — belongs in a separate marketing repo, not the simulation engine |
| `cloudflare/` | Cloudflare Workers and config scoped to the WordPress site — not relevant to the simulation or app |
| `nlt-business-agents/` | Duplicate of `2-person-business-structure/` already in archive — business org docs, not code |
| `business-structure/` | Business organisational documents — not part of the technical codebase |
| `ai-agent-docs/` | AI agent handoff logs (`docs/handoffs/`), agent registration logs (`docs/agent-log/`), AI-specific guidance (`docs/ai-guidance/`), PR review notes (`docs/reviews/`), `CLAUDE.md`, `AGENTS.md` — operational notes for AI coding assistants, not project documentation |
| `azure-ci/` | `azure-pipelines.yml` — the project uses GitHub Actions; Azure Pipelines config is unused |
| `idx-config/` | `.idx/dev.nix` — Firebase IDX development environment config, not needed for the app stack |
| `package-lock.json` | Orphaned lock file with no corresponding `package.json` at the root |

## What Belongs in the Active Repo

The active repository now contains only:

- `src/` — Python simulation engine (Avatars, Aides, Advocates, Fusion, World Engine, NPCs, DB client)
- `apps/web/` — React + TypeScript + TailwindCSS full-stack web application
- `apps/mobile/` — Expo React Native app (iOS + Android)
- `backend/` — FastAPI backend exposing the simulation engine as a REST API
- `supabase/` — Database migrations
- `tests/` — Python test suite
- `configs/` — Simulation and training YAML configs
- `config/` — Global TOI config
- `data/` — Data templates
- `scripts/` — Setup and utility scripts
- `docs/` — Architecture and active documentation
- `.github/` — GitHub Actions CI/CD workflows
