# NeuroLift AI-Fusion — Mobile App (iOS & Android)

Expo React Native app for the NeuroLift simulation environment, targeting iOS and Android.

## Stack

| Layer | Technology |
|---|---|
| Framework | Expo SDK 52 + React Native |
| Language | TypeScript |
| Navigation | Expo Router (file-based) |
| Styling | React Native StyleSheet |
| HTTP | Native `fetch` |
| Backend | FastAPI (`/backend`) |

## Quick Start

```bash
cd apps/mobile

# Install dependencies
npm install

# Start Expo development server
npx expo start
```

Then press:
- `i` — open iOS Simulator (macOS only)
- `a` — open Android Emulator
- `w` — open in browser
- Scan QR code with Expo Go on a physical device

## Screens

| Tab | Description |
|---|---|
| Dashboard | Stats overview and process summary |
| Avatars | Create and monitor Avatar instances |
| Aides | Create and manage Aide coaching instances |
| Sessions | Start and track training sessions |
| Fusion | Attempt Avatar + Aide → Advocate fusion |

## Environment Variables

Create a `.env.local` file:

```env
EXPO_PUBLIC_API_URL=http://your-backend-host:8000/api
```

> **Note:** When running on a physical device, replace `localhost` with your machine's local IP address.

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
