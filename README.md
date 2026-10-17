# NeuroLift AI Fusion

**Full-Stack Avatar-Aide-Advocate Training Platform**

A full-stack web and mobile platform backed by a Python AI simulation engine. AI Avatars with ADHD traits experience authentic life struggles in a Sims/RPG-style environment while AI Aides provide real-time coaching. After sufficient training they fuse into Advocates that combine lived understanding with expert solutions.

> **Sibling repo:** [`nlt-world-engine`](https://github.com/NeuroLift-Technologies/nlt-world-engine) owns the **physical simulation layer**. Godot 4.7.2 is the target runtime; `WorldEngine/` is the retained UE reference implementation. This repo owns the **intelligence**—ADHD trait models, Aide coaching, session orchestration, and fusion. The closed-loop agent contract is defined, but the live Fusion ↔ Godot runtime connection is not yet wired.

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

### Simulation Engine (Python)
```bash
pip install -r requirements.txt
pytest
```

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
**Environment:** Sims/RPG-style virtual world — the target physical runtime is **[Godot 4.7.2 in `nlt-world-engine`](https://github.com/NeuroLift-Technologies/nlt-world-engine/tree/main/world-engine-godot)**. `WorldEngine/` retains the UE 5.8 reference implementation. The transport-neutral agent-loop contract is defined, and Fusion exposes a loopback HTTP endpoint at `POST /agent-loop/perception`. Live Godot ↔ Fusion transport and runtime dispatch are not yet wired.

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

> Canonical persona catalog (spec): `StayAlert` → `RSDShield` (20 advocates). These are **catalog entries**, not an implementation status claim — this repo implements the generic `base_advocate` + prototype pairs (see [`docs/implementation_summary.md`](docs/implementation_summary.md)); the [`nlt-adhd`](https://github.com/NeuroLift-Technologies/nlt-adhd) App scaffolds all 20 dirs in `src/advocates/` (MVP wires 6: 01, 04, 05, 07, 09, 20 — the remaining 14 are stubs).

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
18. **SensorySeeker** - Sensory-seeking behavior
19. **ConfidenceCoach** - Self-esteem and identity
20. **RSDShield** - Rejection sensitivity dysphoria

## 🏆 Success Criteria

1. **Structure Complete:** Repository organized exactly as specified
2. **Documentation Clear:** Any neurodivergent developer can understand the system
3. **Prototype Working:** At least one Avatar-Aide pair trains successfully
4. **Progress Measurable:** Can track Avatar learning from struggle to independence
5. **Realistic Simulation:** Scenarios authentically represent ADHD challenges
6. **Fusion Validated:** Resulting Advocate demonstrates both empathy and expertise
7. **Community Ready:** Code is documented well enough for contributors

## 📞 Contact

**Founder:** Joshua W. Dorsey, Sr. (ADHD cognitive profile)
- Multi-threaded thinker — may switch contexts frequently
- Prefers iterative development with frequent check-ins
- Values authentic neurodivergent representation
- **Email:** neuro.edge24@gmail.com
- **Website:** [neuroliftsolutions.com](https://neuroliftsolutions.com)

---

**This project (together with [`nlt-world-engine`](https://github.com/NeuroLift-Technologies/nlt-world-engine)) represents a new paradigm in AI training — learning through experience, not just data. Welcome to building something genuinely innovative.**