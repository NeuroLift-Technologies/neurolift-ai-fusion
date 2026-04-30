# Platform API

FastAPI service for the PR #37 full-stack platform surface. It wraps the Python
simulation engine for the Next.js web app and Expo mobile app.

## Intent and architecture

`apps/api/` is the current platform API entrypoint documented by the root
quick start:

```text
apps/api/main.py              # FastAPI app, CORS, router registration
apps/api/routers/avatars.py   # static Avatar catalog
apps/api/routers/aides.py     # static Aide catalog
apps/api/routers/sessions.py  # in-memory async session runner + WebSocket updates
apps/api/routers/advocates.py # static Advocate catalog
apps/api/schemas/models.py    # Pydantic request/response models
src/simulation/session_orchestrator.py
```

The older `services/api/` service is still present as a simulation demo API
(`GET /sessions/demo-run`, `POST /sessions/run`). Do not mix its unversioned
routes with this service's `/api/v1/*` routes when wiring clients.

## Local run

```bash
cd apps/api
pip install -r requirements.txt
PYTHONPATH=../.. uvicorn main:app --reload
```

Open:

- API health: <http://localhost:8000/health>
- OpenAPI docs: <http://localhost:8000/docs>

## Environment

Copy `.env.example` when running outside the shell:

```bash
cp .env.example .env
```

| Variable | Purpose | Local default |
| --- | --- | --- |
| `ALLOWED_ORIGINS` | Comma-separated CORS allow-list. Empty falls back to `*`. | unset / `*` |
| `SUPABASE_URL`, `SUPABASE_KEY` | Reserved for future persistence integration. Current routers use in-memory/static data. | example values |
| `ENVIRONMENT` | Runtime label for deployment tooling. | `development` |

## Route contract

All platform routes except `/health` are registered under `/api/v1`.

| Route | Method | Behavior |
| --- | --- | --- |
| `/health` | `GET` | Returns service status and resolved CORS origins. |
| `/api/v1/avatars/` | `GET` | Lists `stay_alert` and `task_kickstart` Avatar summaries. |
| `/api/v1/avatars/{avatar_id}` | `GET` | Returns Avatar detail or `404`. |
| `/api/v1/aides/` | `GET` | Lists `stay_alert_aide` and `task_kickstart_aide` summaries. |
| `/api/v1/aides/{aide_id}` | `GET` | Returns Aide detail or `404`. |
| `/api/v1/advocates/` | `GET` | Lists current Advocate placeholders. |
| `/api/v1/sessions/` | `POST` | Creates a session, starts the simulation in a background task, and returns a running summary. |
| `/api/v1/sessions/` | `GET` | Lists in-memory session summaries. |
| `/api/v1/sessions/{session_id}` | `GET` | Returns session result/status or `404`. |
| `/api/v1/sessions/{session_id}` | `DELETE` | Removes in-memory session state. |
| `/api/v1/sessions/{session_id}/ws` | WebSocket | Streams session state, waking on state changes. |

Example session request:

```bash
curl -X POST http://localhost:8000/api/v1/sessions/ \
  -H "Content-Type: application/json" \
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

## Developer pitfalls

- Session data is process-local memory (`_sessions`, `_summaries`). Restarting
  Uvicorn or scaling to multiple workers loses existing session state.
- `SessionCreate.scenarios` uses `type`, `difficulty`, and `description`, while
  `SessionOrchestrator` still documents `name`, `task_type`,
  `base_success_rate`, and `cognitive_demand` as its canonical scenario keys.
  Keep the adapter in `routers/sessions.py` aligned when changing either side.
- The WebSocket registry stores one event per session ID; a second active
  listener for the same session replaces the first listener's wake-up event.
- `ALLOWED_ORIGINS=*` is convenient locally but should be narrowed for hosted
  environments.
