# Web App

A runnable browser starter for checking the simulation API and running a demo session.

## Intent and current architecture

`apps/web/` is the first client surface for simulation control. The current runnable entrypoint
is the static console in:

```text
apps/web/index.html
apps/web/main.js
apps/web/style.css
```

It calls the FastAPI service in `services/api/app/` and renders raw JSON responses for quick
integration checks. A Vite/React application also exists under `apps/web/src/`, but the static
console is the source-verified starter documented here.

## Current capabilities

- check simulation API health with `GET /health`
- trigger a demo session with `GET /sessions/demo-run`
- inspect returned JSON payloads in the browser
- view the fixture-driven `/simulation-lab` observer surface in the Next.js app

## Local run

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

To review the Next.js app and Simulation Lab route:

```bash
corepack enable
pnpm --dir apps/web install --frozen-lockfile
pnpm --dir apps/web dev
```

Then open `http://localhost:3000/simulation-lab`.

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
- `npm run dev --workspace=apps/web` starts the Next.js surface, not the static
  console described above.
- The Next.js workflow uses `apps/web/pnpm-lock.yaml`; use pnpm for routine web
  dependency installs and development.
- `apps/web/package-lock.json` is also checked in for npm audit coverage after
  PR #65. If security overrides change, review `apps/web/package.json`,
  `apps/web/pnpm-lock.yaml`, and `apps/web/package-lock.json` together.
- Web dependency security overrides currently live in both `overrides` and
  `pnpm.overrides` in `apps/web/package.json` so npm audit and pnpm installs
  resolve the same safe transitive minimums.
- Verify web dependency security changes with
  `npm audit --prefix apps/web --audit-level=moderate`.
- `/simulation-lab` is fixture-driven. Its state model lives in
  `apps/web/src/simulation/lab/stayAlertMorningRoutine.ts` so a future renderer can
  project the same state without becoming the source of truth.
