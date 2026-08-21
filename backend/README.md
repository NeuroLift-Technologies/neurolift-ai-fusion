# NeuroLift AI-Fusion — Backend API

FastAPI backend that exposes the simulation engine as a REST API consumed by the web and mobile apps.

## Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI 0.110+ |
| Runtime | Python 3.10+ |
| Database | Supabase (PostgreSQL) |
| Auth | Supabase Auth (JWT) |
| Deployment | Docker / Cloudflare Workers (planned) |

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
# Edit .env with your Supabase credentials

# Run development server
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.

Interactive docs: `http://localhost:8000/api/docs`

## API Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/api/health` | Health check |
| GET/POST | `/api/avatars/` | List / create Avatars |
| GET/PATCH/DELETE | `/api/avatars/{id}` | Get / update / delete Avatar |
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
| GET | `/api/world/state` | Get full world snapshot (time, rooms, Sims, entities) |
| GET | `/api/world/sims` | List all Sims (name, needs, activity, position) |
| GET | `/api/world/sims/{sim_id}` | Get detailed Sim state (needs, mood, relationships, schedule) |
| GET | `/api/world/rooms` | List all rooms (furniture, occupants) |
| POST | `/api/world/time/advance` | Advance simulation clock by N minutes |
| POST | `/api/world/time/set` | Set the simulation clock to a specific hour:minute |
| POST | `/api/world/time/speed` | Set time speed (realtime=1x, fast=5x, ultra=20x, hyper=100x) |
| POST | `/api/world/save` | Save world state to a JSON file |
| POST | `/api/world/load` | Load a previously saved world state |

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
│   │   ├── scenarios.py
│   │   └── world.py      # World-state router (time, Sims, rooms, save/load)
│   ├── schemas/
│   │   └── world.py      # Pydantic models for the world router
│   ├── models/           # Shared Pydantic models (future)
│   └── services/         # Business logic services (future)
├── requirements.txt
├── .env.example
└── README.md
```
