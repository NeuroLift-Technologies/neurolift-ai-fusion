# NeuroLift Technologies Simulation Environment

**NeuroLift AI-Fusion Framework - Simulation Training Environment**

A Sims/RPG-style simulation environment where AI Avatars with ADHD traits experience authentic life struggles while AI Aides provide real-time coaching. After sufficient training through repeated scenarios, they fuse into Advocates that combine lived understanding with expert solutions.

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
**Environment:** Sims/RPG-style virtual world with realistic consequences

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

## 🎮 The 19 Avatar-Aide-Advocate Pairs

### Executive Function Focused (16 pairs):
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

### Non-Executive Function (3 pairs):
15. **StressShield** - Stress sensitivity
16. **SensoryBalance** - Sensory sensitivity
17. **SocialSync** - Social challenges
18. **SensorySeeker** - Sensory seeking behavior
19. **ConfidenceCoach** - Self-esteem and identity

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Git

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd neurolift-ai-fusion

# Install dependencies
pip install -r requirements.txt

# Run initial setup
python scripts/setup_environment.py
```

### Running Your First Training Session
```bash
# Start a training session with StayAlert Avatar
python scripts/run_training_session.py --avatar stay_alert --scenarios workplace.meeting_dynamics
```

## 📂 Business Structure

### 1-Person Structure (Sole Proprietorship)

This structure is designed for a single founder (CEO) who manages all aspects of the business. The three divisions are managed as separate projects under the founder's direct oversight.

- **neurodivergent-adhd-ai-fusion-system/**: The core product division.
- **toi-otoi-framework/**: The division for the TOI-OTOI framework.
- **rrt-aidvocai-te/**: The division for mental distress and burnout support.

### 2-Person Structure (Partnership)

This structure is designed for a two-person team (CEO + COO) to orchestrate a complete business operation through specialized AI agents.

- **executive-agents/**: 3 core executive agents (CFO, CTO, CMO).
- **department-agents/**: 12 department-level agents.
- **human-interfaces/**: CEO and COO dashboards.

## Agent Hierarchy

### Executive Level (3 Agents)
- **CFO Agent** - Financial strategy, planning, and oversight
- **CTO Agent** - Technical strategy, architecture, and innovation  
- **CMO Agent** - Brand strategy, marketing, and growth

### Department Level (12 Agents)
- **Business Development** (4): Sales, Marketing, Partnership, Investor Relations
- **Operations** (4): Legal, HR, Project Management, Customer Success
- **Technical** (4): Product Manager, QA, DevOps, Security

## Key Features

- **TOI-OTOI Integration** - Privacy-preserving, human-controlled AI agency
- **Human Oversight** - CEO and COO maintain strategic and operational control
- **Agent Coordination** - Structured communication and escalation protocols
- **Performance Monitoring** - Real-time tracking of agent effectiveness
- **Scalable Architecture** - Modular design for easy expansion and customization

## Getting Started

1. **Phase 1**: Foundation setup (Weeks 1-2)
2. **Phase 2**: Executive layer deployment (Weeks 3-4)  
3. **Phase 3**: Department layer deployment (Weeks 5-8)
4. **Phase 4**: Optimization and tuning (Weeks 9-12)

See `docs/playbooks/implementation-guide.md` for detailed instructions.

## Support

- **Architecture**: See `docs/architecture/`
- **Playbooks**: See `docs/playbooks/`
- **Training**: See `docs/training/`

---

*This framework enables two humans to effectively run a billion-dollar operation by orchestrating specialized AI agents while maintaining strategic control and operational oversight.*

## 📁 Repository Structure

```
neurolift-ai-fusion/
business-agents-repo/
├── README.md                           # This file
├── TOI-OTOI-INTEGRATION.md            # TOI-OTOI framework documentation
├── HUMAN-OVERSIGHT-PROTOCOLS.md       # Human control and oversight guidelines
├── AGENT-ORCHESTRATION-GUIDE.md       # How agents coordinate and communicate
├── .github/                           # GitHub workflows and automation
├── config/                            # Global configuration files
├── business-structure/
│   ├── 1-person-structure/
│   │   ├── neurodivergent-adhd-ai-fusion-system/
│   │   ├── toi-otoi-framework/
│   │   └── rrt-aidvocai-te/
│   └── 2-person-structure/
│       ├── executive-agents/
│       ├── department-agents/
│       └── human-interfaces/
├── shared-resources/                  # Templates, prompts, knowledge bases
├── monitoring/                        # Agent performance and decision tracking
└── docs/                             # Architecture and implementation guides

src/
├── avatars/         # Individual Avatar implementations
├── aides/           # Aide support systems
├── advocates/       # Fused Advocate intelligences
└── fusion/          # TOI-OTOI fusion algorithms

cloudflare/          # Cloudflare integration (NEW)
├── connector.py     # Cloudflare API connector
├── workers/         # Cloudflare Workers
├── config/          # Configuration files
└── utils/           # Deployment and helper scripts

docs/
├── framework/       # TOI-OTOI framework documentation
├── architecture/    # System architecture and design
├── business/        # Business plans and strategy
└── cloudflare/      # Cloudflare setup guide

config/
├── avatars.yaml     # Avatar configurations
├── fusion.yaml      # TOI-OTOI fusion parameters
└── privacy.yaml     # Privacy and security settings

assets/
├── diagrams/        # Architecture diagrams
├── mockups/         # UI/UX designs
└── presentations/   # Business presentations
neuroLift-simulation/
├── docs/                    # Comprehensive documentation
├── src/                     # Core implementation
│   ├── avatars/            # Avatar system and ADHD traits
│   ├── aides/              # Aide system and expertise modules
│   ├── simulation/         # Simulation environment and scenarios
│   ├── advocates/          # Fusion engine and Advocate system
│   └── utils/              # Utilities and shared components
├── tests/                  # Comprehensive test suite
├── scripts/                # Setup and execution scripts
├── configs/                # All configuration files
├── data/                   # Local storage (privacy-first)
├── archive/                # Archived content for reference
└── nlt-business-agents/    # Business agent framework (1-person setup)
```

## 🔬 Development Phases

### Phase 1: Foundation ✅
- [x] Repository structure
- [x] Documentation framework
- [x] Base classes implementation
- [x] Configuration schemas

### Phase 2: Simulation Core
- [ ] World engine
- [ ] Time and consequence systems
- [ ] NPC base classes

### Phase 3: First Avatar-Aide Pair (Prototype)
- [x] StayAlert Avatar implementation
- [x] Corresponding Aide expertise
- [ ] Basic training scenarios
- [ ] Training loop validation

### Phase 4: Expand and Validate
- [ ] Remaining 18 Avatar-Aide pairs
- [ ] Full scenario library
- [ ] NPC variety and social dynamics
- [ ] Random dysfunction injection
- [ ] RRT burnout response system

### Phase 5: Fusion and Testing
- [ ] Fusion engine implementation
- [ ] Fused Advocate validation
- [ ] Real-world testing with neurodivergent community
- [ ] Iteration based on feedback

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

## 🤝 Contributing

This project follows "Nothing About Us Without Us" principles. We welcome contributions from:
- Neurodivergent developers and researchers
- ADHD specialists and therapists
- AI/ML researchers interested in experiential learning
- Anyone committed to authentic representation

See [CONTRIBUTING.md](docs/contributing.md) for detailed guidelines.

## 📚 Documentation

- [Architecture Overview](docs/architecture.md)
- [Avatar-Aide-Advocate Process](docs/avatar-aide-advocate-process.md)
- [Executive Functions Theory](docs/executive-functions.md)
- [Simulation Scenarios](docs/simulation-scenarios.md)
- [Training Metrics](docs/training-metrics.md)
- [RRT Foundation](docs/rrt-foundation.md)
- [TOI-OTOI Integration](TOI-OTOI-INTEGRATION.md)
- [Implementation Summary](docs/implementation_summary.md)

## Infrastructure & Deployment

### 🌐 Cloudflare Integration
**Website**: neuroliftsolutions.com (Registered with Northwest Registered Agent)

Our infrastructure leverages Cloudflare for:
- **WordPress Hosting**: Optimized performance and caching
- **Cloudflare Workers**: Serverless edge computing
- **Cloudflare Pages**: Static site hosting for documentation and app interfaces
- **CDN**: Global content delivery for fast access
- **Security**: DDoS protection, WAF, and bot mitigation
- **SSL/TLS**: Automatic HTTPS and encryption

#### Quick Start
```bash
# Configure environment
cp cloudflare/.env.example cloudflare/.env

# Deploy everything
cd cloudflare/utils
./deploy.sh --all
```

**Documentation**: See [Cloudflare Setup Guide](docs/cloudflare/CLOUDFLARE_SETUP.md)

## Business Model
## 🏆 Success Criteria

We'll know we've succeeded when:

1. **Structure Complete:** Repository organized exactly as specified
2. **Documentation Clear:** Any neurodivergent developer can understand the system
3. **Prototype Working:** At least one Avatar-Aide pair trains successfully
4. **Progress Measurable:** Can track Avatar learning from struggle to independence
5. **Realistic Simulation:** Scenarios authentically represent ADHD challenges
6. **Fusion Validated:** Resulting Advocate demonstrates both empathy and expertise
7. **Community Ready:** Code is documented well enough for contributors

- **Founder**: Joshua Dorsey
- **Email**: neuro.edge24@gmail.com
- **Website**: neuroliftsolutions.com
- **Previous Domains**: neurolifttechnologies.com, .org, .info
## 📞 Contact

**Primary Developer:** Joshua W. Dorsey, Sr. (ADHD cognitive profile)
- Multi-threaded thinker - may switch contexts frequently
- Prefers iterative development with frequent check-ins
- Values authentic neurodivergent representation

## 📄 License

[License TBD - Open Source]

---

**This project represents a new paradigm in AI training - learning through experience, not just data. Welcome to building something genuinely innovative.**

## 🎯 Current Status

**Development Phase:** Foundation (Phase 1)
**Last Updated:** January 2026
**Next Milestone:** Complete base classes and first Avatar-Aide pair prototype

---

*Note: The business agent framework has been reorganized into `/nlt-business-agents/` with a 1-person business setup.*
