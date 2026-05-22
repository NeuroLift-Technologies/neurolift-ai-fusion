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

It calls the FastAPI service in `services/api/app/` and renders raw JSON
responses for quick integration checks. The active package scripts in
`apps/web/package.json` start the Next.js app under `apps/web/app/`. A Vite/React
prototype also exists under `apps/web/src/`; its historical npm lockfile remains
tracked as `apps/web/package-lock.json`, but that lockfile is not the source of
truth for the current Next.js dependency graph.

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

## Dependency and workflow boundaries

- Current Next.js dependency changes should update `apps/web/package.json` and
  `apps/web/pnpm-lock.yaml` together with pnpm:
  `pnpm --dir apps/web install --frozen-lockfile` for verification, or the
  equivalent pnpm update command when intentionally changing versions.
- `apps/web/package-lock.json` is tracked, but it reflects the older Vite/React
  prototype dependency graph rather than the active Next.js app. Leave it
  unchanged unless the Vite prototype is intentionally restored and given a
  matching manifest.
- Root npm workspace scripts can start the web package, but they do not refresh
  the web pnpm lockfile. If a dependency manifest changes, review the manifest
  and the intended lockfile in the same diff.
- `.github/workflows/web.yml` currently runs `npm install` in `apps/web` and is
  scoped to the `master` branch. If that workflow is re-enabled for `main`,
  align it with the pnpm lockfile before treating it as the authoritative web
  CI path.

## Developer pitfalls

- The API currently has no CORS middleware. Browser requests from `http://localhost:4173` to
  `http://localhost:8000` may be blocked until CORS support is added to `services/api/app/main.py`.
- The static console uses `GET /sessions/demo-run`; it does not exercise the SDK client or
  `POST /sessions/run` yet.
- `npm run dev --workspace=apps/web` starts the Next.js surface, not the static
  console described above.
- `/simulation-lab` is fixture-driven. Its state model lives in
  `apps/web/src/simulation/lab/stayAlertMorningRoutine.ts` so a future renderer can
  project the same state without becoming the source of truth.
