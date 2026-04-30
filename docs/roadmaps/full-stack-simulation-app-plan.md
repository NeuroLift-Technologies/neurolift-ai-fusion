# Full-Stack Simulation App Plan (Web + Android + iOS)

## Objective

Evolve `neurolift-ai-fusion` from a Python-first simulation codebase into a product-ready full-stack platform with:

- a web application,
- a shared mobile app (Android + iOS),
- and a simulation API layer backed by existing Python domain logic.

## Current implementation baseline (2026-04-25)

- **API starter live** in `services/api/app/` using FastAPI and the existing `SessionOrchestrator`.
- **Web starter live** in `apps/web/` with buttons to call `/health` and `/sessions/demo-run`.
- **Mobile starter live** in `apps/mobile/` as an Expo app for Android and iOS.
- **Shared SDK starter live** in `packages/simulation-sdk/` with TypeScript contracts + client wrapper.

## Target Monorepo Layout

```text
apps/
  web/                  # Browser app (participant + coach dashboards)
  mobile/               # Cross-platform mobile app (Android/iOS)
services/
  api/                  # Simulation API (session orchestration, auth, telemetry)
packages/
  simulation-sdk/       # Shared contracts/types/client SDK for app consumption
src/                    # Existing Python simulation domain (current engine)
```

## Product Surface Areas

### 1) Web App (`apps/web`)
- session setup and scenario launch
- live simulation timeline and interventions
- post-session review with progress metrics

### 2) Mobile App (`apps/mobile`)
- run and review sessions on Android/iOS
- in-session prompts and coaching nudges
- push notifications for reflection checkpoints

### 3) API Layer (`services/api`)
- secure APIs for session creation, retrieval, and analytics
- gateway between clients and `src/` simulation domain
- event ingestion and audit-ready logs

### 4) Shared Contracts (`packages/simulation-sdk`)
- API request/response schemas
- event models used by web + mobile
- typed client utilities to reduce drift across frontends

## Migration Phases

1. **Foundation (complete):** repository cleanup + app/service/package scaffolding.
2. **Starter implementation (complete):** API + web + mobile + SDK starter code connected.
3. **API hardening:** authentication, persistence integration, and robust error contracts.
4. **Product UX:** richer web/mobile flows for session management and analytics.
5. **Convergence:** unified telemetry, identity, and release workflows across all surfaces.

## Guardrails for Implementation

- Keep provider-agnostic AI integration boundaries.
- Preserve human-in-the-loop review for critical decisions.
- Keep simulation domain in `src/` as source-of-truth during migration.
- Avoid direct client access to persistence layers; use service APIs.
