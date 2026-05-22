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
corepack prepare pnpm@10 --activate
pnpm --dir apps/web install --frozen-lockfile
pnpm --dir apps/web dev
```

Then open `http://localhost:3000/simulation-lab`.

## Dependency and security override workflow

The Next.js dependency graph is locked with pnpm:

```text
apps/web/package.json
apps/web/pnpm-workspace.yaml
apps/web/pnpm-lock.yaml
```

`apps/web/pnpm-workspace.yaml` is the pnpm override source for current web
security pins. PR #66 regenerated `pnpm-lock.yaml` so the lockfile records these
overrides and resolves the affected transitive packages to safe lines:

| Package | Override |
| --- | --- |
| `postcss` | `>=8.5.14` |
| `glob` | `>=10.5.0` |
| `minimatch` | `>=9.0.7` |

When Dependabot or an audit requires changing these pins:

1. Update `apps/web/pnpm-workspace.yaml`.
2. Keep `apps/web/package.json` `overrides` aligned if npm-based tooling still
   needs the same constraints.
3. Regenerate the lockfile from the web package:

   ```bash
   corepack enable
   corepack prepare pnpm@10 --activate
   pnpm --dir apps/web install --lockfile-only
   pnpm --dir apps/web install --frozen-lockfile
   ```

4. Review the top-level `overrides:` block in `apps/web/pnpm-lock.yaml` before
   committing.

Verified package-manager constraints:

- Use `pnpm@10` for the current lockfile workflow until the repo pins a
  `packageManager` field.
- `pnpm@9.15.9` rejects the current override-only `pnpm-workspace.yaml` because
  it has no `packages` field.
- Unpinned Corepack can select newer pnpm majors; pnpm 11 may fail frozen
  installs on minimum-release-age supply-chain policy checks for very recent
  lockfile entries.

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
- The checked-in web lockfile is `apps/web/pnpm-lock.yaml`. Use pnpm for web
  dependency changes and avoid generating `apps/web/package-lock.json`.
- For pnpm security override changes, edit `apps/web/pnpm-workspace.yaml`; the
  nested `pnpm.overrides` block in `package.json` is not sufficient by itself
  for the current lockfile workflow.
- Root npm workspace scripts can start the web package, but they do not update
  the web pnpm lockfile. If a dependency manifest changes, update and review
  `apps/web/package.json` and `apps/web/pnpm-lock.yaml` together.
- `.github/workflows/web.yml` currently runs `npm install` from `apps/web`, so
  pnpm lockfile-only changes should be verified locally with the pnpm commands
  above until CI is aligned.
- `/simulation-lab` is fixture-driven. Its state model lives in
  `apps/web/src/simulation/lab/stayAlertMorningRoutine.ts` so a future renderer can
  project the same state without becoming the source of truth.
