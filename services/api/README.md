# Simulation API Service

This service now includes a runnable FastAPI starter wired to the existing Python simulation domain.

## Intent and architecture

`services/api/` is the service boundary between client applications and the Python simulation
domain in `src/`. Client surfaces should call this API instead of importing Avatar, Aide, or
orchestrator classes directly.

Current source path:

```text
services/api/app/main.py             # FastAPI routes
services/api/app/schemas.py          # Pydantic request/response models
services/api/app/session_service.py  # Adapter into src.simulation.session_orchestrator
src/simulation/session_orchestrator.py
```

The starter currently runs `StayAlertAvatar` with `AttentionCoaching` through
`SessionOrchestrator`. It does not yet provide authentication, persistence, CORS middleware,
or multi-avatar selection.

## Implemented route surface

`services/api/app/main.py` currently defines only these routes:

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/health` | Liveness check for local clients and orchestration probes. |
| `GET` | `/sessions/demo-run` | Runs the built-in `DEFAULT_SCENARIOS` list from `session_service.py`. |
| `POST` | `/sessions/run` | Runs caller-provided scenarios through the current session adapter. |

The React dashboard prototypes under `apps/web/src/` and `apps/mobile/app/` reference broader
resource routes such as `/api/avatars/`, `/api/aides/`, `/api/sessions/`, `/api/fusion/`, and
`/api/scenarios/`. Those routes are not implemented in this FastAPI starter yet. Treat those
client paths as forward-looking UI scaffolding until API routers are added.

## Endpoints

- `GET /health` — service health
- `GET /sessions/demo-run` — run built-in demo scenarios
- `POST /sessions/run` — run a custom session payload

## Request and response contract

`POST /sessions/run` accepts:

```json
{
  "avatar_id": "stay_alert_api",
  "aide_id": "stay_alert_aide_api",
  "scenarios": [
    {
      "name": "Morning planning sprint",
      "task_type": "planning",
      "base_success_rate": 0.55,
      "cognitive_demand": 0.65
    }
  ]
}
```

Scenario constraints are enforced by `ScenarioInput`:

- `name` is required.
- `task_type` defaults to `focus_task`.
- `base_success_rate` and `cognitive_demand` must be between `0.0` and `1.0`.

Responses are serialized `SessionResult` payloads with:

- session and participant IDs (`session_id`, `avatar_id`, `aide_id`)
- aggregate metrics (`total_attempts`, `total_successes`, `total_coaching`, `success_rate`)
- final state (`final_independence`, `fusion_ready`)
- per-scenario result dictionaries under `scenarios`

## Local run

```bash
python3 -m pip install -r requirements.txt
uvicorn services.api.app.main:app --reload
```

Smoke checks:

```bash
curl http://localhost:8000/health
curl http://localhost:8000/sessions/demo-run
curl -X POST http://localhost:8000/sessions/run \
  -H "Content-Type: application/json" \
  -d '{"scenarios":[{"name":"Quick focus drill"}]}'
```

## Developer pitfalls

- Browser clients served from another origin, such as `http://localhost:4173`, will need CORS
  support before their fetches can succeed in a real browser. No CORS middleware is configured
  in `services/api/app/main.py` yet.
- `GET /sessions/demo-run` and `POST /sessions/run` execute an in-process simulation on each
  request; there is no job queue or persisted session store yet.
- The current API adapter always uses the sustained-attention Avatar/Aide pair. `avatar_id` and
  `aide_id` label the returned run but do not select different implementations yet.
- Keep API schemas aligned with `packages/simulation-sdk/src/types.ts` when request or response
  fields change.
- Do not point clients at `/api/...` resource routes until matching FastAPI routers exist. The
  current smoke-test clients call the root-level route paths listed above.

## Why this matters

This API is the integration seam for both web and mobile applications, so clients do not directly couple to `src/` internals.
