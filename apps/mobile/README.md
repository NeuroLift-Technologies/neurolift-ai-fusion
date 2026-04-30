# Mobile App (Android + iOS)

This is now a runnable Expo starter app connected to the simulation API.

## Intent and architecture

`apps/mobile/` is the cross-platform client starter for Android and iOS. It currently uses
Expo + React Native and calls the same API endpoints as the web starter:

```text
apps/mobile/App.tsx
  -> GET /health
  -> GET /sessions/demo-run
  -> services/api/app/main.py
```

The app renders raw JSON responses so mobile developers can verify connectivity before richer
session workflows are implemented.

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
- `npm install` is local to `apps/mobile/`; this directory is not wired into a root workspace yet.
