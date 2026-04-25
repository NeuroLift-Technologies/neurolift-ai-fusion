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

Use this verified sequence to confirm your local setup before deeper development:

```bash
# 1) Syntax smoke check for core modules and scripts
python3 -m compileall src scripts

# 2) Run the interactive training loop demo
python3 scripts/test_training_loop.py
```

`test_training_loop.py` currently reaches scenario execution, then fails during coaching context construction (see troubleshooting below). This is useful for validating the setup path and reproducing current integration behavior.

## 🔁 CI and Repository Automation Workflows (GitHub Actions)

### Intent and architecture

This repository currently has four automation workflows in `.github/workflows/`:

| Workflow file | Actions UI name | Role | Job flow |
| --- | --- | --- | --- |
| `.github/workflows/shared-ci.yml` | **Shared CI** | Organization-standard checks via reusable workflows in `NeuroLift-Technologies/.github-private` | `lint` -> (`test`, `security`) |
| `.github/workflows/python-app.yml` | **Python application** | Local baseline checks defined in this repository | single `build` job (checkout -> setup python -> install -> flake8 -> pytest) |
| `.github/workflows/pr-cleanup.yml` | **PR Cleanup** | Repository hygiene: marks stale PRs, auto-closes stale PRs, and deletes merged source branches | `stale-prs` + `delete-merged-branches` |
| `.github/workflows/sync-governance-public.yml` | **Sync Governance (Public)** | Syncs governance documents (for example `NLT-DEV-OTOI.md`) from `NeuroLift-Technologies/.github-private` via `repository_dispatch`, and runs weekly presence validation | single `sync-governance` job (checkout -> apply payload doc -> validate -> optional commit/PR) |

Both CI workflows currently use **Python 3.10**.

### Trigger behavior and constraints

`shared-ci.yml` and `python-app.yml` run on:

- `push` to `master`
- `pull_request` targeting `master`
- `workflow_dispatch` (manual run from the Actions tab)

`pr-cleanup.yml` runs on:

- a daily schedule (`cron: 0 6 * * *`, 06:00 UTC)
- `workflow_dispatch` with optional inputs:
  - `days_before_stale` (default `30`)
  - `days_before_close` (default `7`)

`sync-governance-public.yml` runs on:

- `repository_dispatch` with type `governance-sync` (content sync path)
- `workflow_dispatch` (manual validation/sync testing)
- weekly schedule (`cron: 0 8 * * 1`, Monday 08:00 UTC) for validation-only runs

Important constraints:

- A push to a non-`master` branch does **not** auto-run CI unless you open a PR to `master` or trigger manually.
- Because both CI workflows subscribe to the same events, a PR to `master` runs both pipelines.
- PR cleanup staleness currently uses defaults of **30 inactive days** before `stale`, then **7 more days** before auto-close (overridable via manual dispatch inputs).
- Draft PRs are explicitly exempt from staleness in `pr-cleanup.yml` (`exempt-draft-pr: true`).
- PR cleanup only targets pull requests (issue staleness is disabled via `days-before-issue-stale: -1` and `days-before-issue-close: -1`).
- Branch deletion only applies to branches merged from this repository (not forks), and skips protected/default branches.
- Governance sync only accepts document names matching `NLT-*.md` at repo root or `docs/governance/NLT-*.md`; other filenames are rejected.
- Governance sync weekly/manual validation warns when `NLT-DEV-OTOI.md` is missing; repository-dispatch runs can open a PR only when synced content actually changed.

### Agent automation definitions (`.github/agents/*.agent.md`)

This repository also includes agent prompt definitions under `.github/agents/`:

| Agent file | Purpose | Current status |
| --- | --- | --- |
| `.github/agents/pr-cleanup.agent.md` | Prompt/spec for PR cleanup reporting behavior (stale PR + merged branch hygiene context) | Active prompt asset |
| `.github/agents/my-agent.agent.md` | Generic starter template for defining additional custom agents | Template only |

Important constraint:

- No workflow in `.github/workflows/` currently imports or executes `.agent.md` files directly. Runtime automation behavior is defined by workflow YAML (plus external automation tooling), while `.agent.md` files define prompt/behavior expectations.

### PR Cleanup runbook (`.github/workflows/pr-cleanup.yml`)

**Subsystems covered:**

1. **Stale PR lifecycle** (`actions/stale@v9`)
   - Marks inactive PRs with `stale` after configured inactivity.
   - Closes stale PRs after configured grace period with `auto-closed` label.
   - Exempts draft PRs (`exempt-draft-pr: true`).
2. **Merged branch deletion** (`actions/github-script@v7`)
   - Scans closed PRs and keeps only merged PRs from this repository (not forks).
   - Skips protected/default branches (`master`, `main`, `develop`, `dev`, `release`) and any branch returned by `repos.listBranches(protected: true)`.
   - Deletes `refs/heads/<branch>` and treats HTTP 422 as "already deleted."

**Codepath map (source-verified):**

| Behavior | Workflow codepath | Notes |
| --- | --- | --- |
| Stale threshold input | `github.event.inputs.days_before_stale \|\| 30` | Manual dispatch can override default `30`. |
| Close threshold input | `github.event.inputs.days_before_close \|\| 7` | Manual dispatch can override default `7`. |
| PR-only scope | `days-before-issue-stale: -1`, `days-before-issue-close: -1` | Issues are explicitly excluded. |
| Merged PR branch filter | `pr.merged_at !== null` + `pr.head.repo.full_name === <current repo>` | Excludes fork-origin branches. |
| Protected branch skip | static set + `repos.listBranches(protected: true)` | Includes both default names and API-protected branches. |
| Branch deletion API call | `github.rest.git.deleteRef({ ref: "heads/<branch>" })` | HTTP 422 is logged as already deleted and not fatal. |

**Operational constraints and pitfalls:**

- Branch deletion requires `contents: write`; stale/close operations require `pull-requests: write` and `issues: write`.
- The merged-branch cleanup loop reads up to `per_page: 100` closed PRs per run.
- Fork-origin PR branches are not deleted by design.
- Schedule times are UTC; if cleanup appears "late", verify timezone conversion before changing cron.

### Governance Sync runbook (`.github/workflows/sync-governance-public.yml`)

**Subsystems covered:**

1. **Inbound governance payload application** (`repository_dispatch`)
   - Reads `github.event.client_payload.document_name`, `content`, `version`, and optional `checksum`.
   - Restricts allowed targets to `NLT-*.md` or `docs/governance/NLT-*.md`.
   - Decodes base64 content and writes the document to the requested path.
2. **Governance presence validation**
   - Verifies `NLT-DEV-OTOI.md` is present and emits warnings (not hard failure) when missing.
3. **Conditional commit and PR creation**
   - Runs only for `repository_dispatch` events with real file changes.
   - Creates branch `governance-sync/<timestamp>`, commits synced document, and opens a PR with governance metadata.

**Codepath map (source-verified):**

| Behavior | Workflow codepath | Notes |
| --- | --- | --- |
| Trigger type gate | `if: github.event_name == 'repository_dispatch'` | Content-writing steps are skipped for schedule/manual validation-only runs. |
| Allowed filename filter | `case "$DOCUMENT_NAME" in NLT-*.md \| docs/governance/NLT-*.md)` | Rejects non-governance paths to prevent arbitrary writes. |
| Base64 payload decode | `echo "$DOCUMENT_CONTENT" \| base64 --decode > "$DOCUMENT_NAME"` | Keeps transport safe for multiline markdown. |
| Optional checksum verification | `sha256sum` block when `DOCUMENT_CHECKSUM` is set | Expects `sha256:<hex>` format. Fails run on mismatch; unsupported algorithm formats are skipped with a warning (not enforced). |
| Weekly validation target | `for doc in NLT-DEV-OTOI.md` | Ensures required constitutional doc presence in this repo. |
| PR creation condition | `steps.changes.outputs.changed == 'true'` | Avoids no-op governance sync PRs. |

**Operational constraints and pitfalls:**

- The workflow uses `gh pr create` and requires `pull-requests: write` + `contents: write` in the job permission block.
- Validation-only runs can succeed with warnings when governance docs are absent; they are observability checks, not strict enforcement gates.
- If dispatch payload omits `document_name` or `content`, the sync step exits with an explicit error.
- Filename allow-list is intentionally strict; if governance scope expands, update both workflow code and this runbook together.

### Manual usage

From GitHub UI:

1. Open **Actions**.
2. Select **Shared CI**, **Python application**, **PR Cleanup**, or **Sync Governance (Public)**.
3. Click **Run workflow**.
4. Choose the branch and (for PR Cleanup) optionally override stale/close thresholds.

For manual PR cleanup tuning (`PR Cleanup` only):

1. Open **Actions** -> **PR Cleanup** -> **Run workflow**.
2. Set `days_before_stale` (default `30`) and `days_before_close` (default `7`) if needed.
3. Run and inspect logs for the `stale-prs` and `delete-merged-branches` jobs.

For governance validation (`Sync Governance (Public)`):

1. Open **Actions** -> **Sync Governance (Public)** -> **Run workflow**.
2. Run on the target branch (normally `master`).
3. Inspect logs for:
   - `Validate governance documents` (presence/warnings)
   - `Apply synced governance document` and `Create pull request for governance update` on repository-dispatch runs.

PR cleanup verification checklist:

1. Confirm the run used the expected `days_before_stale` and `days_before_close` values.
2. In `stale-prs` logs, verify labels/actions align with the current policy (`stale`, `auto-closed`, draft PR exemption).
3. In `delete-merged-branches` logs, verify each skip/delete outcome is expected (fork PR, protected branch, or already deleted branch).
4. If merged branches remain, check whether the relevant PRs fall outside the current `per_page: 100` query window.

To reproduce `python-app.yml` locally:

```bash
python -m pip install --upgrade pip
pip install flake8 pytest
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
pytest
```

### Maintenance checklist

- **Update Python version in both CI workflows together** to avoid drift:
  - `.github/workflows/shared-ci.yml` -> `with.python-version`
  - `.github/workflows/python-app.yml` -> `with.python-version`
- **Keep branch trigger filters aligned** in both CI files when changing branch policy.
- **Treat `shared-ci.yml` behavior as externally defined**: it calls reusable workflows from `.github-private` at `@main`.
- **Do not remove `security-events: write` from `shared-ci.yml`** unless the reusable security workflow no longer needs upload permissions.
- **When changing PR retention policy, update both code and docs together**:
  - `.github/workflows/pr-cleanup.yml` (`days-before-stale`, `days-before-close`)
  - this README section (trigger behavior + runbook defaults)
- **When changing governance sync scope, update both code and docs together**:
  - `.github/workflows/sync-governance-public.yml` (allow-list, validation targets, PR behavior)
  - this README section (trigger behavior + governance runbook)
- **Protect long-lived branches in GitHub settings** so `delete-merged-branches` can safely skip them using the protected-branch API check.
- **Do not reduce PR Cleanup write permissions** unless stale labeling/closing and branch deletion behavior is intentionally being disabled.
- **Keep cleanup intent aligned in two places** when requirements change:
  - `.github/workflows/pr-cleanup.yml` (enforced behavior)
  - `.github/agents/pr-cleanup.agent.md` (agent runbook + reporting expectations)
- **Keep governance source-of-truth explicit**:
  - upstream governance authoring lives in `NeuroLift-Technologies/.github-private`
  - this repository consumes synced copies (for example `NLT-DEV-OTOI.md`) via `Sync Governance (Public)`

### Troubleshooting and common pitfalls

- **CI did not run:** confirm the event targets `master`, or run with `workflow_dispatch`.
- **`Shared CI` fails before local tests run:** inspect reusable workflow logs from `.github-private`; failures there can occur without changes in this repository.
- **Security/test ordering confusion:** in `shared-ci.yml`, both `test` and `security` depend on `lint` and can run in parallel after lint passes.
- **`python-app.yml` lint behavior seems inconsistent:** the first flake8 command fails on syntax/name errors; the second uses `--exit-zero` and is informational for style/complexity reporting.
- **PR branch was not deleted after merge:** check whether the PR came from a fork, whether the branch is protected, or whether it was already deleted (422 is treated as non-fatal in workflow logs).
- **PR expected to stay open got marked stale:** add any activity (comment/commit/review) or convert to draft if it is actively in progress but intentionally paused.
- **Governance sync did not write a file:** verify the event was `repository_dispatch` with `governance-sync`, and that payload included both `document_name` and base64 `content`.
- **Governance sync rejected the file path:** ensure the payload target matches `NLT-*.md` or `docs/governance/NLT-*.md`.
- **No governance sync PR was created:** check whether there were actual file changes (`Check for changes` may evaluate to `false` on identical content).

### Local runtime troubleshooting (scripts)

- **`ImportError: attempted relative import beyond top-level package` from `scripts/run_training_session.py`:**
  `run_training_session.py` imports `avatars.*` after modifying `sys.path`, but modules under `src/avatars` use package-relative imports (`..core`), so direct execution currently fails.
- **`TypeError: CoachingContext.__init__() got an unexpected keyword argument 'avatar'` from `scripts/test_training_loop.py`:**
  this script still uses an older `CoachingContext` call pattern that no longer matches `src/aides/base_aide.py`.
- **Need a deterministic smoke path while those scripts are being reconciled:**
  run `python3 -m compileall src scripts`, then use `tests/test_simulation/test_session_orchestrator.py` as the reference for current orchestration interfaces.

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

See `nlt-business-agents/implementation-guide.md` for detailed instructions.

## Support

- **Architecture**: See `docs/architecture.md`
- **Implementation summary**: See `docs/implementation_summary.md`
- **Cloudflare setup**: See `docs/cloudflare/CLOUDFLARE_SETUP.md`

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
├── .github/                           # GitHub workflows + custom agent prompt definitions
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

Formal `CONTRIBUTING.md` guidance is being drafted; for now, follow the CI workflow and documentation standards in this README.

## 📚 Documentation

- [Architecture Overview](docs/architecture.md)
- [Quick Start Guide](QUICKSTART.md)
- [TOI-OTOI Integration](TOI-OTOI-INTEGRATION.md)
- [Implementation Summary](docs/implementation_summary.md)
- [Cloudflare Setup Guide](docs/cloudflare/CLOUDFLARE_SETUP.md)

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
