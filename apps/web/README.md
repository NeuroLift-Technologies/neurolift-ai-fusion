# Web App

Browser surfaces for the NeuroLift simulation platform. This package currently
contains multiple entrypoints that target different API contracts; choose the
one that matches the backend you are running.

## Entrypoint map

| Entrypoint | Source | API contract | Local status |
| --- | --- | --- | --- |
| Next.js app | `apps/web/app/**` | `NEXT_PUBLIC_API_URL`, defaulting to `http://localhost:8000/api/v1` in `next.config.mjs` | Package scripts (`pnpm dev`, `pnpm build`) run this surface |
| Simulation Lab | `apps/web/app/simulation-lab/page.tsx` plus `apps/web/src/simulation/**` | Fixture-driven; no backend required | Available through the Next.js app at `/simulation-lab` |
| Static console | `apps/web/index.html`, `main.js`, `style.css` | `services/api/` routes: `GET /health`, `GET /sessions/demo-run` | Serve with `python3 -m http.server` |
| PR #32 React Router source | `apps/web/src/App.tsx`, `apps/web/src/pages/**`, `apps/web/src/api/client.ts` | `backend/` routes under `/api/*` through the Vite proxy in `vite.config.ts` | Source is present, but `package.json` has no Vite script or Vite dependencies in this snapshot |

## Next.js local run

```bash
corepack enable
pnpm --dir apps/web install --frozen-lockfile
cp apps/web/.env.local.example apps/web/.env.local
pnpm --dir apps/web dev
```

Open `http://localhost:3000`. The platform dashboard/session routes import
`@/lib/api` and `@/lib/types`; those modules are not present in this snapshot,
so verify the route you are changing before relying on a full app build.

## PR #32 backend-aligned source

The React Router source under `apps/web/src/` models the full PR #32 dashboard:

- `/` dashboard
- `/avatars`
- `/aides`
- `/sessions`
- `/fusion`
- `/scenarios`

Its API client uses `const BASE_URL = "/api"` and request paths such as
`/avatars/`, `/sessions/`, and `/fusion/`. `vite.config.ts` proxies `/api` to
`http://localhost:8000`, so the matching backend command is:

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Because `apps/web/package.json` currently runs Next.js and does not include a
Vite script, treat this source tree as a contract reference until a runnable
Vite package path is restored.

## Static console run

Start the demo API:

```bash
python3 -m pip install -r requirements.txt
uvicorn services.api.app.main:app --reload
```

In another terminal, serve the static files:

```bash
python3 -m http.server 4173 --directory apps/web
```

Then open `http://localhost:4173`.

The console reads `window.NEUROLIFT_API_URL` and falls back to
`http://localhost:8000`:

```html
<script>
  window.NEUROLIFT_API_URL = "http://localhost:8000";
</script>
<script src="./main.js" defer></script>
```

## Developer pitfalls

- Do not mix `backend/` (`/api/*`), `apps/api/` (`/api/v1/*`), and
  `services/api/` (unversioned demo routes) request shapes.
- `npm run dev --workspace=apps/web` and `pnpm --dir apps/web dev` start the
  Next.js surface, not the PR #32 React Router source or the static console.
- The web package currently has both `apps/web/pnpm-lock.yaml` and
  `apps/web/package-lock.json`. Routine web development uses pnpm, while the
  npm lockfile supports the npm audit workflow documented at the repo root.
  Keep both files intentional when changing dependencies.
- Root npm workspace scripts can start the web package, but they do not update
  the web pnpm lockfile. If a dependency manifest changes, update and review
  `apps/web/package.json` and `apps/web/pnpm-lock.yaml` together.
- `/simulation-lab` is fixture-driven. Its state model lives in
  `apps/web/src/simulation/lab/stayAlertMorningRoutine.ts` so a future renderer
  can project the same state without becoming the source of truth.
