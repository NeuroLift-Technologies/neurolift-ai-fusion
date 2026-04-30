# Simulation SDK

Shared TypeScript contracts and API client for web + mobile surfaces.

## Intent

`packages/simulation-sdk/` is the shared contract layer for TypeScript clients. Keep these
types aligned with the FastAPI schemas in `services/api/app/schemas.py` so the web and
mobile apps do not drift from the Python API.

This package is currently source-only: it has no `package.json`, build step, or published
artifact yet. Import it by source path during local development, or add package metadata
before treating it as an installable workspace package.

## Included

- `src/types.ts`: session/scenario request-response contracts
- `src/client.ts`: minimal API client wrapper

## Public contract

`ScenarioInput` maps to the API `ScenarioInput` Pydantic model:

- `name` is required.
- `task_type` defaults server-side to `focus_task` when omitted.
- `base_success_rate` and `cognitive_demand` default server-side and must be `0.0` to `1.0`
  when supplied.

`SimulationApiClient` exposes:

- `health()` -> `GET /health`
- `runSession(payload)` -> `POST /sessions/run`

The client throws `Error("HTTP <status>")` for non-2xx responses and returns parsed JSON for
successful responses.

## Example

```ts
const client = new SimulationApiClient("http://localhost:8000");
const result = await client.runSession({ scenarios: [{ name: "Morning planning" }] });
```

## Maintenance notes

- Update `src/types.ts` whenever `services/api/app/schemas.py` changes.
- The web and mobile starters currently call `fetch` directly. Move them to this client when
  the repository has a workspace package/build convention for shared TypeScript code.
