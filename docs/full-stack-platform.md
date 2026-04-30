# Full-Stack Platform Guide

**Source-verified:** Apr 30, 2026
**Primary codepaths:** `apps/api/`, `apps/web/`, `apps/mobile/`, `src/simulation/session_orchestrator.py`

This guide documents the full-stack application surface added around the
Avatar-Aide-Advocate simulation engine. Use it when wiring the API to the web or
mobile clients, troubleshooting local setup, or changing the public HTTP session
workflow.

## Architecture at a glance

```
apps/web        Next.js App Router UI
   |            reads NEXT_PUBLIC_API_URL
   v
apps/api        FastAPI service, in-memory session API, WebSocket updates
   |
   v
src/            Python simulation engine and SessionOrchestrator
   ^
   |
apps/mobile     Expo Router UI, intended to read EXPO_PUBLIC_API_URL
```

The API is the boundary between TypeScript clients and the Python simulation
engine. The current API stores sessions in process memory, starts each session in
a FastAPI background task, and streams terminal state changes over WebSocket.

## Local setup

### Install dependencies

```bash
# Python API and simulation engine
python -m pip install -r requirements.txt
python -m pip install -r apps/api/requirements.txt

# TypeScript workspaces
npm install
```

### Run the API

```bash
cd apps/api
PYTHONPATH=../.. uvicorn main:app --reload
```

Open:

- Health check: `http://localhost:8000/health`
- OpenAPI docs: `http://localhost:8000/docs`

Production CORS should be restricted with `ALLOWED_ORIGINS`:

```bash
ALLOWED_ORIGINS=https://app.neuroliftsolutions.com,https://staging.neuroliftsolutions.com
```

Leaving `ALLOWED_ORIGINS` unset defaults to `["*"]` for local development.

### Run the web app

```bash
cp apps/web/.env.local.example apps/web/.env.local
npm run dev:web
```

The web app defaults `NEXT_PUBLIC_API_URL` to `http://localhost:8000` in
`apps/web/next.config.ts`.

### Run the mobile app

```bash
cp apps/mobile/.env.example apps/mobile/.env
npm run dev:mobile
```

For a physical device, set `EXPO_PUBLIC_API_URL` to a host reachable from that
device, such as your LAN IP rather than `localhost`.

## Workspace commands

Root `package.json` defines these workspace scripts:

| Command | Runs |
| --- | --- |
| `npm run dev:web` | `next dev` in `apps/web` |
| `npm run dev:mobile` | `expo start` in `apps/mobile` |
| `npm run build:web` | `next build` in `apps/web` |
| `npm run lint` | workspace lint scripts when present |
| `npm run type-check` | workspace TypeScript checks when present |

`turbo.json` defines `build`, `dev`, `lint`, and `type-check` tasks, but the
root scripts currently call npm workspaces directly. `apps/mobile` defines a
lint script, but `apps/web` currently calls `next lint`; Next.js 14 removed that
subcommand, so web linting needs an ESLint script/config update before root
`npm run lint` is a reliable full-workspace check.

## API contract

All versioned endpoints are rooted at `/api/v1`.

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/health` | Service health and active CORS origins |
| `GET` | `/api/v1/avatars/` | List available Avatar summaries |
| `GET` | `/api/v1/avatars/{avatar_id}` | Get Avatar detail by id |
| `GET` | `/api/v1/aides/` | List available Aide summaries |
| `GET` | `/api/v1/aides/{aide_id}` | Get Aide detail by id |
| `GET` | `/api/v1/advocates/` | List Advocate summaries |
| `POST` | `/api/v1/sessions/` | Create and start a training session |
| `GET` | `/api/v1/sessions/` | List in-memory session summaries |
| `GET` | `/api/v1/sessions/{session_id}` | Read one session result |
| `DELETE` | `/api/v1/sessions/{session_id}` | Delete one in-memory session |
| `WS` | `/api/v1/sessions/{session_id}/ws` | Stream session result updates |

### Available public types

The API currently exposes two Avatar ids and two Aide ids:

| Domain | Values |
| --- | --- |
| `avatar_type` | `stay_alert`, `task_kickstart` |
| `aide_type` | `stay_alert_aide`, `task_kickstart_aide` |
| `scenario.type` | `workplace`, `personal`, `social` |
| `session.status` | `pending`, `running`, `completed`, `aborted`, `failed` |

### Create a session

```bash
curl -X POST http://localhost:8000/api/v1/sessions/ \
  -H 'Content-Type: application/json' \
  -d '{
    "avatar_type": "stay_alert",
    "aide_type": "stay_alert_aide",
    "scenarios": [
      {
        "type": "workplace",
        "difficulty": 0.5,
        "description": "Workplace productivity task"
      }
    ],
    "max_attempts_per_scenario": 10,
    "max_coaching_per_attempt": 3,
    "independence_target": 0.8
  }'
```

Response shape:

```json
{
  "session_id": "<uuid>",
  "status": "running",
  "avatar_type": "stay_alert",
  "aide_type": "stay_alert_aide",
  "created_at": "2026-04-30T13:40:00+00:00"
}
```

### Read live session updates

After creating a session, clients fetch the current result with:

```bash
curl http://localhost:8000/api/v1/sessions/<session_id>
```

Clients then open:

```text
ws://localhost:8000/api/v1/sessions/<session_id>/ws
```

The WebSocket sends the current session result when connected, waits for the
background task to update the session, then closes after `completed`, `failed`,
or `aborted`.

## Client workflow

### Web (`apps/web`)

The UI contains:

- `/` landing page.
- `/dashboard` session list and "New Session" entry point.
- `/session/new` Avatar/Aide selection and difficulty slider.
- `/session/[id]` session metrics and live updates.

Expected client helper imports:

- `@/lib/api`
- `@/lib/types`

Those files are not present in the current branch, so `next build` and
`npm run type-check --workspace=apps/web` will fail until the API client and
type definitions are added.

### Mobile (`apps/mobile`)

The Expo app contains:

- tabbed dashboard, sessions, and profile screens.
- `/session/new` session creation flow.
- `/session/[id]` session metrics and WebSocket updates.

Expected client helper imports:

- `@/lib/api`
- `@/lib/types`

Those files are not present in the current branch. The mobile app also imports
`@react-native-community/slider`, but `apps/mobile/package.json` does not list
that dependency yet. Add the dependency before running the new-session screen.

## Current constraints and pitfalls

- **Session persistence is in memory.** Restarting the API process clears
  `_sessions`, `_summaries`, and WebSocket notification state.
- **One active WebSocket listener per session.** The API stores a single
  `asyncio.Event` per session id, so multiple listeners can overwrite each
  other's wake event.
- **Background sessions report failures in-band.** `_run_session` catches
  exceptions and stores `status: "failed"` plus `error`; it does not raise the
  exception back to the `POST /sessions/` response.
- **API-to-engine scenario shapes are not identical.** The HTTP schema accepts
  `type`, `difficulty`, and `description`; `SessionOrchestrator.run_session`
  documents `name`, `task_type`, `base_success_rate`, and `cognitive_demand`.
  Keep this mapping explicit when repairing the API session runner.
- **API imports currently point at non-existent module paths.**
  `apps/api/routers/sessions.py` imports `src.avatars.stay_alert_avatar` and
  `src.avatars.task_kickstart_avatar`, while the checked-in implementations live
  under `src/avatars/adhd_traits/`.
- **Result field names differ between API and engine.** The API reads fields
  such as `overall_success_rate`, `final_independence_level`,
  `peak_burnout_risk`, and `fusion_ready`; the current engine result exposes
  `success_rate`, `final_independence`, and `fusion_readiness`.
- **Mobile API URL must be device-reachable.** `localhost` works for simulators
  in some setups but not for a physical phone scanning the Expo QR code.
- **Production CORS must not rely on the local default.** Set
  `ALLOWED_ORIGINS` explicitly before exposing the API outside local dev.

## Verification checklist

Use this checklist after changing API routes, client helpers, or session
runtime wiring:

```bash
# Python import and syntax check
python -m compileall src apps/api

# API route smoke check
cd apps/api
PYTHONPATH=../.. uvicorn main:app --reload
# in another terminal: curl http://localhost:8000/health

# Web static verification
npm run type-check --workspace=apps/web
npm run build:web

# Mobile static verification
npm run type-check --workspace=apps/mobile
```

If the TypeScript checks fail with missing `@/lib/api` or `@/lib/types`, add the
shared client modules before treating the web or mobile apps as runnable.
