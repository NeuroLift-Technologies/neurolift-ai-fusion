# NeuroLift AI-Fusion — Mobile App (iOS & Android)

Expo React Native app for the NeuroLift simulation environment, targeting iOS and Android.

## Stack

| Layer | Technology |
|---|---|
| Framework | Expo SDK 56 + React 19 + React Native 0.85 |
| Language | TypeScript |
| Navigation | Expo Router (file-based) |
| Styling | React Native StyleSheet |
| HTTP | Native `fetch` |
| Backend | PR #32 FastAPI surface in `backend/` (`/api/*`) |

## Quick Start

```bash
cd apps/mobile

# Install dependencies
npm install

# Configure backend URL for devices/emulators
cp .env.example .env

# Start Expo development server
npx expo start
```

Then press:
- `i` — open iOS Simulator (macOS only)
- `a` — open Android Emulator
- `w` — open in browser
- Scan QR code with Expo Go on a physical device

## Screens

These tabs are registered in `app/(tabs)/_layout.tsx`:

| Tab file | Label | Description |
|---|---|
| `index.tsx` | Home | Stats overview and process summary |
| `avatars.tsx` | Avatars | Create and monitor Avatar instances |
| `aides.tsx` | Aides | Create and manage Aide coaching instances |
| `sessions.tsx` | Sessions | Start and track training sessions |
| `fusion.tsx` | Fusion | Attempt Avatar + Aide to Advocate fusion |

## Environment Variables

Create a `.env` file from the checked-in template:

```bash
cp .env.example .env
```

The API client reads `EXPO_PUBLIC_API_URL` and appends endpoint paths such as
`/avatars/` and `/sessions/`. Include the `/api` prefix in the value:

```env
EXPO_PUBLIC_API_URL=http://your-backend-host:8000/api
```

> **Note:** When running on a physical device, replace `localhost` with your machine's local IP address.

For Android emulators, `http://10.0.2.2:8000/api` often reaches a backend on
the host machine; iOS simulators can usually use `http://localhost:8000/api`.

## API contract

The active tab screens import `apps/mobile/src/api/client.ts`, which mirrors the
PR #32 web source. The helper exposes:

- `GET/POST /api/avatars/`
- `GET /api/avatars/traits/list`
- `DELETE /api/avatars/{id}`
- `GET/POST /api/aides/`
- `DELETE /api/aides/{id}`
- `GET/POST /api/sessions/`
- `POST /api/sessions/{session_id}/complete`
- `GET/POST /api/fusion/`
- `GET /api/fusion/advocates/`
- `GET /api/scenarios/`

Current tab usage is narrower than the helper: Dashboard lists counts,
Avatars/Aides create and delete records, Sessions creates/completes sessions
with the hard-coded `workplace_email_overload` scenario, and Fusion lists and
attempts fusions. No registered tab renders the scenario catalogue yet.

Start the matching backend with:

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Build for Production

```bash
# Install EAS CLI
npm install -g eas-cli

# Configure EAS
eas build:configure

# Build for iOS
eas build --platform ios

# Build for Android
eas build --platform android
```

## Project Structure

```
apps/mobile/
├── app/
│   ├── _layout.tsx          # Root stack layout
│   └── (tabs)/
│       ├── _layout.tsx      # Tab bar layout
│       ├── index.tsx        # Dashboard
│       ├── avatars.tsx      # Avatars
│       ├── aides.tsx        # Aides
│       ├── sessions.tsx     # Sessions
│       └── fusion.tsx       # Fusion
├── src/
│   └── api/
│       └── client.ts        # API client
├── assets/                  # Icons, splash screen
├── app.json                 # Expo config
└── package.json
```

## Developer pitfalls

- Additional route files such as `app/(tabs)/dashboard.tsx`,
  `app/(tabs)/session.tsx`, and `app/session/*` import `@/lib/api` and
  `@/lib/types`, but no `apps/mobile/lib/` modules are present in this
  snapshot. Do not wire those screens into navigation until the missing modules
  are implemented or the routes are retired.
- Do not point this client at `apps/api/` without changing request shapes:
  `apps/api/` uses `/api/v1/*`, `avatar_type`, `aide_type`, and scenario arrays,
  while this client uses PR #32 ID-based payloads.
- `backend/` stores data in process memory. Restarting the backend clears
  created Avatars, Aides, sessions, fusion reports, and Advocate placeholders.
