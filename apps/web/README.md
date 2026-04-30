# Web App

A runnable browser starter for checking the simulation API and running a demo session.

## Intent and current architecture

`apps/web/` is the first browser client surface for simulation control. It currently contains
two browser paths with different levels of backend support:

```text
apps/web/index.html, main.js, style.css  # source-verified API smoke console
apps/web/src/                            # Vite/React product dashboard prototype
```

The static console calls the FastAPI starter in `services/api/app/` and renders raw JSON
responses for quick integration checks. The Vite/React dashboard prototype is useful for UI
development, but several of its data calls target routes that do not exist in the current
FastAPI starter yet.

## Current capabilities

Static console:

- check simulation API health with `GET /health`
- trigger a demo session with `GET /sessions/demo-run`
- inspect returned JSON payloads in the browser

Vite/React prototype:

- provides dashboard, avatar, aide, session, fusion, and scenario screens under `apps/web/src/pages/`
- reads its API base URL from `VITE_API_URL` and otherwise uses `/api`
- proxies `/api` to `http://localhost:8000` during `npm run dev` through `vite.config.ts`

## Local run

### Source-verified static smoke console

Start the API first:

```bash
python3 -m pip install -r requirements.txt
uvicorn services.api.app.main:app --reload
```

In another terminal, serve the static console:

```bash
python3 -m http.server 4173 --directory apps/web
```

Then open `http://localhost:4173`.

### Vite/React prototype

```bash
cd apps/web
npm install
npm run dev
```

This starts the React dashboard on the Vite dev server, typically `http://localhost:5173`.
It expects API routes under `/api/*`; only use it against a backend that implements those routes,
or expect empty/error states in screens that call unimplemented endpoints.

## API base URL

The console reads `window.NEUROLIFT_API_URL` and falls back to `http://localhost:8000`:

```html
<script>
  window.NEUROLIFT_API_URL = "http://localhost:8000";
</script>
<script src="./main.js" defer></script>
```

Define that global before loading `main.js` if the API runs somewhere else.

## Developer pitfalls

- The API currently has no CORS middleware. Browser requests from `http://localhost:4173` to
  `http://localhost:8000` may be blocked until CORS support is added to `services/api/app/main.py`.
- The static console uses `GET /sessions/demo-run`; it does not exercise the SDK client or
  `POST /sessions/run` yet.
- `npm run dev` starts the separate Vite/React surface under `apps/web/src/`, not the static
  smoke console described above.
- The Vite/React API client currently calls `/api/avatars/`, `/api/aides/`, `/api/sessions/`,
  `/api/fusion/`, and `/api/scenarios/`. Those routes are not implemented by
  `services/api/app/main.py`, whose verified routes are `/health`, `/sessions/demo-run`, and
  `/sessions/run`.
