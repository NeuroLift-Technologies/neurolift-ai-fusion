# NeuroLift AI Fusion

**Full-Stack Avatar-Aide-Advocate Training Platform**

A full-stack web and mobile platform backed by a Python AI simulation engine. AI Avatars with ADHD traits experience authentic life struggles in a Sims/RPG-style environment while AI Aides provide real-time coaching. After sufficient training they fuse into Advocates that combine lived understanding with expert solutions.

> **Sibling repo:** [`nlt-world-engine`](https://github.com/NeuroLift-Technologies/nlt-world-engine) owns the **authoritative simulation training environment** — the UE 5.8 Unreal WorldEngine (rooms, objects, NPCs, tick loop, Mass Entity entities). This repo owns the **intelligence** that drives it: ADHD trait models, Aide coaching, session orchestration, and the fusion process. If `nlt-world-engine` is the **Sims game**, this repo is the **AI mod + web/mobile wrapper**.

```yaml
ai_assistant_directive:
  priority: 1
  instruction: "Before performing any development or coding tasks, read NLT-DEV-OTOI.md."
  description: "NLT-DEV-OTOI.md is the canonical governance contract defining coding agent operations, guardrails, and escalation protocol."
  required_file: "NLT-DEV-OTOI.md"
```

## Quick Start

### API (FastAPI — Python)
```bash
cd apps/api
pip install -r requirements.txt
PYTHONPATH=../../src uvicorn main:app --reload
# → http://localhost:8000/docs
```

### Web App (Next.js)
```bash
cd apps/web
corepack enable
pnpm install --frozen-lockfile
cp .env.local.example .env.local   # set NEXT_PUBLIC_API_URL
pnpm dev
# → http://localhost:3000
```

### Mobile App (Expo — iOS & Android)
```bash
cd apps/mobile
npm install
cp .env.example .env
npx expo start
# → scan QR with Expo Go on your device
```

### Simulation Engine (Python — Intelligence Layer)
```bash
pip install -r requirements.txt
pytest
```

> **Note:** The simulation *runtime* (world, rooms, objects, tick loop) is the **Unreal WorldEngine in [`nlt-world-engine`](https://github.com/NeuroLift-Technologies/nlt-world-engine)**, not this repo. This repo provides the Python intelligence (Avatar trait models, Aide coaching, session orchestration) that drives that world via the agent interface. The legacy lightweight Python world in `src/simulation/environment/` is for testing and reference only.

### JavaScript dependency boundaries

The repository currently has multiple JavaScript package-manager surfaces:

| Path | Lockfile | Use for |
| --- | --- | --- |
| `apps/web/` | `pnpm-lock.yaml` | Next.js web surface and `/simulation-lab` |
| `apps/mobile/` | `package-lock.json` | Expo mobile starter |
| `cloudflare-engine/` | `package-lock.json` | World Engine Worker and local Wrangler CLI |

Use the lockfile in the package you are changing. For web-only dependency work,
run pnpm inside `apps/web/` so the checked-in `pnpm-lock.yaml` stays in sync and
avoid creating an `apps/web/package-lock.json`. For the Cloudflare worker, run
`npm ci` from `cloudflare-engine/` so local `npx wrangler ...` commands use the
repo-pinned Wrangler v4 dependency instead of a global install.

---

[![Deploy to Cloudflare Workers](https://deploy.workers.cloudflare.com/button)](https://deploy.workers.cloudflare.com/?url=https://github.com/NeuroLift-Technologies/neurolift-ai-fusion)
[![Visit Site](https://img.shields.io/badge/Visit%20Site-neuroliftsolutions.com-F38020?style=for-the-badge&logo=cloudflare&logoColor=white)](https://neuroliftsolutions.com)

## 🎯 Project Vision

**Mission:** "Nothing About Us Without Us" - neurodivergent voices lead development

This project implements **experiential learning** for AI systems, not traditional data training. Avatars don't just analyze patterns about ADHD - they actually live through the struggles, experience real stress, make mistakes, and learn through doing with Aide support.

### Core Innovation

Nobody else is training AI this way. While the industry has solved infrastructure (MCP, A2A protocols), two critical gaps remain:
- **User preference enforcement: UNSOLVED** ← OTOI addresses this
- **AI capability reliability: UNSOLVED** (38.1% computer use accuracy, 85% agentic AI failure rate)

This simulation approach addresses both gaps through authentic experiential learning.

## 🏗️ Architecture Overview

### The Avatar-Aide-Advocate Process

#### Phase 1: Avatar Creation
- Each Avatar embodies a specific ADHD trait/executive function deficit
- Experiences authentic stress, frustration, and failure patterns
- Lives through simulated everyday scenarios where their specific trait creates challenges
- Makes real mistakes with real consequences in the virtual environment

#### Phase 2: Aide Development
**Foundation Components:**
1. **RRT (Rapid Response Team) Core** - Pre-existing therapeutic knowledge with dormant burnout response
2. **PhD-Level Expertise** - Deep academic research on specific executive functions
3. **Real-World Feedback** - Input from people with ADHD who've mastered that specific area

**Role:** Coach, therapist, and assistant operating IN the simulation environment alongside the Avatar

#### Phase 3: Simulation Training
**Environment:** Sims/RPG-style virtual world — rendered and simulated by the **[UE 5.8 Unreal WorldEngine in `nlt-world-engine`](https://github.com/NeuroLift-Technologies/nlt-world-engine)** (rooms, objects, NPCs, deterministic tick loop). This repo's Avatar/Aide intelligence connects to it through the agent interface (HTTP/WebSocket API).

**Scenario Categories:**
- **Workplace:** HR compliance, meetings, project management, performance reviews
- **Personal:** Household management, social relationships, financial tasks, self-care
- **Social Dynamics:** Rejection sensitivity, emotional regulation, social cues

**Key Environmental Features:**
- **Neurotypical NPCs:** Complete same tasks easily, creating realistic social comparison
- **Biased NPCs:** Exhibit workplace discrimination, microaggressions, ableism
- **Random Dysfunction Injection:** Suddenly adds new executive function challenges
- **Real Consequences:** Failed tasks have meaningful impact, creating authentic learning pressure

#### Phase 4: Fusion into Advocate
**When:** After Avatar demonstrates consistent independence across scenarios  
**How:** Combine Avatar's experiential struggle awareness with Aide's proven expertise  
**Result:** An Advocate that both understands what ADHD struggles feel like AND knows what actually works

## 🎮 The 20 Avatar-Aide-Advocate Pairs

> Canonical persona catalog: `StayAlert` → `RSDShield` (20 advocates). The App delivery runtime in [`nlt-adhd`](https://github.com/NeuroLift-Technologies/nlt-adhd) ships these 1:20 (20 advocate dirs in `src/advocates/`, mirroring this list).

### Executive Function Focused (14 pairs):
1. **StayAlert** - Sustained attention deficit
2. **ImpulseGuard** - Impulsivity control
3. **FocusFlow** - Hyperfocus management
4. **Timely** - Time blindness
5. **MemoryMate** - Working memory deficits
6. **MoodEase** - Emotional regulation
7. **TaskKickstart** - Task initiation difficulty
8. **CalmCore** - Low frustration tolerance
9. **Planner Pro** - Prioritization and planning
10. **SmoothSwitch** - Transition difficulties
11. **AwareMate** - Self-monitoring challenges
12. **SteadyMind** - Poor impulse control
13. **FocusRecharge** - Effortful focus fatigue
14. **EffortAlign** - Effort vs. productivity perception

### Non-Executive Function (6 pairs):
15. **StressShield** - Stress sensitivity
16. **SensoryBalance** - Sensory sensitivity
17. **SocialSync** - Social challenges
18. **SensorySeeker** - Sensory seeking behavior
19. **ConfidenceCoach** - Self-esteem and identity
20. **RSDShield** - Rejection sensitivity dysphoria

## 🎮 Unreal Engine AI Tools

> **Note:** The Unreal Engine 5.8 project — and therefore all UE plugin configuration, RL/PPO training, and UE AI tooling — lives in [`nlt-world-engine/WorldEngine`](https://github.com/NeuroLift-Technologies/nlt-world-engine). This catalog was historically kept here as reference context for the AI layer; it is now maintained in the sibling repo only.

**What this repo needs to know:**

- The WorldEngine (UE 5.8) is the **authoritative simulation training environment** — Mass Entity population, StateTree behavior, Smart Objects, deterministic tick, and RL/PPO training (Learning Agents plugin).
- The in-engine **LLM control path** (`UMLInferenceBridgeSubsystem` in nlt-world-engine) drives `AAvatarAIController::ExecuteLLMCommand` directly — the model controls the actor inside the engine, not through the public web server.
- Fusion's intelligence connects over the agent interface (HTTP/WebSocket API) — see [`docs/architecture.md`](docs/architecture.md) and the fusion-unreal domain mapping in nlt-world-engine.

UE-side plugin/tooling details: see the **UE Plugins Enabled** table and subsystem docs in [`nlt-world-engine/README.md`](https://github.com/NeuroLift-Technologies/nlt-world-engine).

---

## 🔁 CI and Repository Automation

### Workflows

| Workflow | Role | Trigger |
|----------|------|---------|
| `shared-ci.yml` | Org-standard checks via reusable workflows | push to main, PR to main |
| `python-app.yml` | Python/API checks for `src/`, `tests/`, `apps/api/` | push to main, PR to main (when Python paths change) |
| `redteam-ci.yml` | Progressive 3-level clearance (syntax → coverage → security) | push to main, PR to main |
| `pgsa-portability-gate.yml` | Secrets scanning + provenance validation | push to main, PR to main |
| `pr-cleanup.yml` | Stale PR marking, auto-close, merged branch deletion | daily schedule + manual |
| `sync-governance-public.yml` | Syncs governance docs from `.github-private` | repository_dispatch + weekly schedule |

### Key constraints

- Pushes to non-`main` branches do not auto-run CI unless a PR targets `main`
- `shared-ci.yml` calls reusable workflows from `NeuroLift-Technologies/.github-private` at `@main`
- `pr-cleanup.yml` exempts draft PRs from staleness; branch deletion skips protected branches and forks
- Governance sync requires `document_name` + base64-encoded `content` in `repository_dispatch` payload

Full CI/CD documentation: [`docs/CI_HARNESS_README.md`](docs/CI_HARNESS_README.md)

### 🌐 Cloudflare Integration

Our infrastructure leverages Cloudflare for:
- **WordPress Hosting**: Optimized performance and caching
- **Cloudflare Workers**: Serverless edge computing
- **Cloudflare Pages**: Static site hosting for documentation and app interfaces
- **CDN**: Global content delivery for fast access
- **Security**: DDoS protection, WAF, and bot mitigation

| Worker | Purpose |
|--------|---------|
| **Main** | Request routing & caching |
| **WordPress Optimizer** | Performance & WP caching |
| **Security** | Bot protection & headers |

Deployment details: [`docs/cloudflare/CLOUDFLARE_SETUP.md`](docs/cloudflare/CLOUDFLARE_SETUP.md)

## 🛡️ Privacy-First Design

<!-- 
NON-NEGOTIABLES FOR PRODUCTION & END USER USE:
The following 4 principles are mandatory requirements for any production 
deployment or end-user facing application of this framework.

Note: "Local Processing" does not apply during development and training phases,
where cloud/remote processing may be used for Avatar-Aide simulation training.
-->

- **Local Processing:** All processing happens locally *(exempt during development/training)*
- **No Data Collection:** No external data transmission without explicit consent
- **No Monetization:** User data never monetized
- **Transparent:** Clear about what data exists and where

> **⚠️ Production Requirements:** The above 4 principles are **non-negotiable** for production and end-user use. "Local Processing" may be relaxed during development and training phases only.

## 🏆 Success Criteria

1. **Structure Complete:** Repository organized exactly as specified
2. **Documentation Clear:** Any neurodivergent developer can understand the system
3. **Prototype Working:** At least one Avatar-Aide pair trains successfully
4. **Progress Measurable:** Can track Avatar learning from struggle to independence
5. **Realistic Simulation:** Scenarios authentically represent ADHD challenges
6. **Fusion Validated:** Resulting Advocate demonstrates both empathy and expertise
7. **Community Ready:** Code is documented well enough for contributors

## 🤝 Contributing

This project follows "Nothing About Us Without Us" principles. We welcome contributions from:
- Neurodivergent developers and researchers
- ADHD specialists and therapists
- AI/ML researchers interested in experiential learning
- Anyone committed to authentic representation

Formal `CONTRIBUTING.md` guidance is being drafted; for now, follow the CI workflow and documentation standards in this README.

## 📚 Documentation

- [Architecture Overview](docs/architecture.md)
- [Quick Start Guide](QUICKSTART.md)
- [TOI-OTOI Integration](TOI-OTOI-INTEGRATION.md)
- [Implementation Summary](docs/implementation_summary.md)
- [Cloudflare Setup Guide](docs/cloudflare/CLOUDFLARE_SETUP.md)

## 📞 Contact

**Founder:** Joshua W. Dorsey, Sr. (ADHD cognitive profile)
- Multi-threaded thinker — may switch contexts frequently
- Prefers iterative development with frequent check-ins
- Values authentic neurodivergent representation
- **Email:** neuro.edge24@gmail.com
- **Website:** [neuroliftsolutions.com](https://neuroliftsolutions.com)

## 📄 License

[License TBD - Open Source]

## 🎯 Current Status

**Development Phase:** Fusion & AI Model Layer (Phases 5–6) — intelligence layer driving the UE WorldEngine (in `nlt-world-engine`) ✅  
**Last Updated:** September 2026  
**Next Milestone:** Expand remaining 16 Avatar-Aide pairs → real-world testing with neurodivergent community  
**Spec:** [`docs/specs/advocate-model-fusion-spec.md`](docs/specs/advocate-model-fusion-spec.md) + [`docs/research/Trajectory Distillation for Behavioral AI Fusion.md`](docs/research/Trajectory%20Distillation%20for%20Behavioral%20AI%20Fusion.md)

---

**This project (together with [`nlt-world-engine`](https://github.com/NeuroLift-Technologies/nlt-world-engine)) represents a new paradigm in AI training — learning through experience, not just data. Welcome to building something genuinely innovative.**
