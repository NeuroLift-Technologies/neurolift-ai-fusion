# Simulation API Service

This service now includes a runnable FastAPI starter wired to the existing Python simulation domain.

## Endpoints

- `GET /health` — service health
- `GET /sessions/demo-run` — run built-in demo scenarios
- `POST /sessions/run` — run a custom session payload

## Local run

```bash
pip install fastapi uvicorn pydantic
uvicorn services.api.app.main:app --reload
```

## Why this matters

This API is the integration seam for both web and mobile applications, so clients do not directly couple to `src/` internals.
