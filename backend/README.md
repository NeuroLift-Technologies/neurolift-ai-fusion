# NeuroLift AI-Fusion — Backend API

FastAPI backend that exposes the simulation engine as a REST API consumed by the web and mobile apps.

## Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI 0.110+ |
| Runtime | Python 3.10+ |
| Current persistence | Process-local in-memory dictionaries in router modules |
| Planned persistence | Supabase/PostgreSQL fields are present in `.env.example`, but this source tree does not initialize Supabase from `backend/app/` |
| Deployment | Local Uvicorn development server; hosted deployment is not defined in source |

## Runtime model

`backend/` is the PR #32 REST surface for the `apps/web/src/` and
`apps/mobile/src/` API clients. It registers every public route under `/api`
from `backend/app/main.py` and exposes OpenAPI at `/api/docs`.

The routers currently store Avatars, Aides, sessions, fusion reports, and
Advocate placeholders in module-level dictionaries. Restarting Uvicorn or
running multiple worker processes loses or splits that state. Treat Supabase
settings in `.env.example` as future integration placeholders unless source code
under `backend/app/` starts reading them.

## Quick Start

```bash
cd backend

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Optional: set NEUROLIFT_CORS_ALLOW_ORIGINS for browser clients

# Run development server
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.

Interactive docs: `http://localhost:8000/api/docs`

## Environment

| Variable | Purpose | Source-verified default |
|---|---|---|
| `NEUROLIFT_CORS_ALLOW_ORIGINS` | Comma-separated browser/mobile development origins allowed by FastAPI CORS middleware. | `http://localhost:3000,http://localhost:4173,http://localhost:5173,http://localhost:8081` |
| `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY` | Reserved for future persistence/auth integration. | Not read by current `backend/app/` source |
| `API_SECRET_KEY`, `ENVIRONMENT` | Template values for future API/runtime configuration. | Not read by current `backend/app/` source |

Example:

```env
NEUROLIFT_CORS_ALLOW_ORIGINS=http://localhost:3000,http://localhost:5173,http://localhost:8081
```

For hosted environments, narrow this list to the exact deployed web origins.

## API Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/api/health` | Health check |
| GET/POST | `/api/avatars/` | List / create Avatars |
| GET/DELETE | `/api/avatars/{id}` | Get / delete Avatar |
| PATCH | `/api/avatars/{id}/state` | Update Avatar emotional state, cognitive load, or stress level |
| GET | `/api/avatars/traits/list` | List valid ADHD trait names |
| GET/POST | `/api/aides/` | List / create Aides |
| GET/DELETE | `/api/aides/{id}` | Get / delete Aide |
| GET/POST | `/api/sessions/` | List / start training sessions |
| GET | `/api/sessions/{id}` | Get session details |
| POST | `/api/sessions/{id}/task-result` | Record task attempt result |
| POST | `/api/sessions/{id}/complete` | Mark session complete |
| GET/POST | `/api/fusion/` | List fusions / attempt fusion |
| GET | `/api/fusion/{id}` | Get fusion report |
| GET | `/api/fusion/advocates/` | List Advocates |
| GET | `/api/scenarios/` | List scenarios (filter by category) |
| GET | `/api/scenarios/categories` | List categories |
| GET | `/api/scenarios/{id}` | Get scenario |

### Request shape examples

Create an Avatar:

```bash
curl -X POST http://localhost:8000/api/avatars/ \
  -H "Content-Type: application/json" \
  -d '{"trait_name":"stay_alert","trait_config":{}}'
```

Create a session after selecting an Avatar, Aide, and scenario:

```bash
curl -X POST http://localhost:8000/api/sessions/ \
  -H "Content-Type: application/json" \
  -d '{
    "avatar_id": "<avatar_id>",
    "aide_id": "<aide_id>",
    "scenario_id": "workplace_email_overload",
    "session_type": "standard"
  }'
```

Attempt fusion:

```bash
curl -X POST http://localhost:8000/api/fusion/ \
  -H "Content-Type: application/json" \
  -d '{"avatar_id":"<avatar_id>","aide_id":"<aide_id>"}'
```

Fusion readiness is placeholder logic in this router: it samples a readiness
score between `0.5` and `1.0` and succeeds at `0.75` or higher. The production
fusion engine contract remains documented in `docs/architecture.md`.

### Known pitfalls

- Created objects live only in the current backend process. Restarting Uvicorn
  clears Avatars, Aides, sessions, fusion reports, and Advocate placeholders.
- The backend route contract is not the same as `apps/api/` (`/api/v1/*`) or
  `services/api/` (`/sessions/demo-run`, `/sessions/run`).

## Project Structure

```
backend/
├── app/
│   ├── main.py           # FastAPI app, CORS, router registration
│   ├── routers/
│   │   ├── health.py
│   │   ├── avatars.py
│   │   ├── aides.py
│   │   ├── sessions.py
│   │   ├── fusion.py
│   │   └── scenarios.py
│   ├── models/           # Shared Pydantic models (future)
│   └── services/         # Business logic services (future)
├── requirements.txt
├── .env.example
└── README.md
```
