# Mobile App (Expo Router)

This is the React Native client for the PR #37 full-stack platform. It uses
Expo Router and talks to the platform API in `apps/api/`.

## Intent and architecture

Current source path:

```text
apps/mobile/app/_layout.tsx          # Expo Router stack
apps/mobile/app/(tabs)/dashboard.tsx # session list
apps/mobile/app/session/new.tsx      # Avatar/Aide picker + session creation
apps/mobile/app/session/[id].tsx     # session result/live status view
apps/mobile/src/api/client.ts        # older REST client kept for prototype screens
apps/api/main.py                     # FastAPI platform API
```

The Expo entrypoint is configured by `package.json` as `expo-router/entry`.
`App.tsx` and `index.ts` are older demo entrypoints that call `/health` and
`/sessions/demo-run`; they are not the current router path.

## Current capabilities

- list sessions through `GET /api/v1/sessions/`
- create a session through `POST /api/v1/sessions/`
- view a session through `GET /api/v1/sessions/{session_id}`
- open a WebSocket for live updates at `/api/v1/sessions/{session_id}/ws`

## Local run

From the repository root:

```bash
npm install
npm run dev:mobile
```

Or from this workspace:

```bash
cd apps/mobile
npm install
cp .env.example .env
npm run start
```

Then launch Android, iOS, or web from Expo.

## API configuration

Set the base API URL in `EXPO_PUBLIC_API_URL`:

```bash
EXPO_PUBLIC_API_URL=http://localhost:8000 npm run start
```

The router screens expect the platform API root (`http://localhost:8000`) and
append `/api/v1/...` paths for session, avatar, and aide calls.

If the app runs on a physical device or emulator that cannot resolve the host
machine's `localhost`, use the host LAN IP or the emulator-specific host
address. Keep `ALLOWED_ORIGINS` in `apps/api` aligned with that origin if CORS
is restricted.

## Developer pitfalls

- Start `apps/api` first with `PYTHONPATH=../.. uvicorn main:app --reload`
  from `apps/api`, or run its Dockerfile from the repo root.
- Current router screens import `@/lib/api` and `@/lib/types`, but this checkout
  does not include `apps/mobile/lib/`; either restore those files or update the
  imports before expecting `npm run type-check` or Expo bundling to pass.
- The current session store is in-memory. Restarting the API clears sessions and
  makes old detail links return `404`.
- Mobile and web both depend on `apps/api`'s `/api/v1` routes. The older
  `services/api` demo routes (`/sessions/demo-run`, `/sessions/run`) are a
  separate surface.
- The app is included in the root npm workspace (`apps/mobile`), so root
  scripts such as `npm run dev:mobile` and `npm run type-check` can target it.
- Mobile dependency security overrides live in `apps/mobile/package.json` under
  `overrides`; PR #65 pins vulnerable transitive `@xmldom/xmldom` and `uuid`
  ranges while the upstream dependency tree catches up.
- When dependency overrides or direct dependencies change, update and review
  `apps/mobile/package.json` and `apps/mobile/package-lock.json` together, then
  verify with `npm audit --prefix apps/mobile --audit-level=moderate`.
