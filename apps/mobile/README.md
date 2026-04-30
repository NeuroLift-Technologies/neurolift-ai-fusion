# Mobile App (Android + iOS)

This directory contains a runnable Expo smoke-test app plus an earlier tabbed prototype.

## Intent and architecture

`apps/mobile/` is the cross-platform client starter for Android and iOS. The source-verified
smoke-test entrypoint is `App.tsx`, registered by `index.ts`, which calls the same implemented
FastAPI endpoints as the static web console:

```text
apps/mobile/App.tsx
  -> GET /health
  -> GET /sessions/demo-run
  -> services/api/app/main.py
```

The app renders raw JSON responses so mobile developers can verify connectivity before richer
session workflows are implemented.

A richer Expo Router prototype also exists under `apps/mobile/app/` with shared helpers in
`apps/mobile/src/api/client.ts`. That prototype points at `/api/avatars`, `/api/aides`,
`/api/sessions`, `/api/fusion`, and `/api/scenarios`, which are not implemented by the current
FastAPI starter.

## Current capabilities

- check API health
- run demo simulation session from mobile UI

## Local run

```bash
cd apps/mobile
npm install
npm run start
```

Then launch Android or iOS from Expo.

## API configuration

The API base URL is read from `EXPO_PUBLIC_API_URL`:

```bash
EXPO_PUBLIC_API_URL=http://localhost:8000 npm run start
```

If the app runs on a physical device or an emulator that cannot resolve the host machine's
`localhost`, use the host LAN IP or the emulator-specific host address.

## Developer pitfalls

- Start the FastAPI service first: `uvicorn services.api.app.main:app --reload`.
- Browser/mobile cross-origin access still depends on API CORS support, which is not configured
  in the starter yet.
- The starter calls only the demo endpoint. Custom session payloads should use
  `POST /sessions/run` after the UI adds scenario editing.
- The tabbed Expo Router files under `apps/mobile/app/` are prototype screens for a broader API
  contract. They should be treated as design/reference code until the corresponding FastAPI
  routers exist.
- `apps/mobile/src/api/client.ts` currently defaults to `http://localhost:8000/api`, unlike
  `App.tsx`, which defaults to `http://localhost:8000`. Keep this difference in mind when
  moving from the smoke-test app to the tabbed prototype.
- `npm install` is local to `apps/mobile/`; this directory is not wired into a root workspace yet.
