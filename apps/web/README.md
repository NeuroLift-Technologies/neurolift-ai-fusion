# NeuroLift AI-Fusion — Web App

React + TypeScript + TailwindCSS dashboard for the NeuroLift simulation environment.

## Stack

| Layer | Technology |
|---|---|
| Framework | React 19 + TypeScript |
| Build tool | Vite 8 |
| Styling | TailwindCSS v4 |
| Routing | React Router v7 |
| HTTP client | Axios |
| Backend | FastAPI (`/backend`) via `/api` proxy |

## Quick Start

```bash
cd apps/web
pnpm install
pnpm dev
```

The app will be available at `http://localhost:5173`.

## Pages

| Route | Description |
|---|---|
| `/` | Dashboard — stats overview and process summary |
| `/avatars` | Create and monitor Avatar instances |
| `/aides` | Create and manage Aide coaching instances |
| `/sessions` | Start and track training sessions |
| `/fusion` | Attempt Avatar + Aide → Advocate fusion |
| `/scenarios` | Browse the scenario library |

## Environment Variables

Create a `.env.local` file:

```env
VITE_API_URL=http://localhost:8000/api
```

## Build for Production

```bash
pnpm build
# Output in dist/
```
