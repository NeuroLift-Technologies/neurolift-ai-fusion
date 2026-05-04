# NeuroLift AI Fusion

**Full-Stack Avatar-Aide-Advocate Training Platform**

A full-stack web and mobile platform backed by a Python AI simulation engine. AI Avatars with ADHD traits experience authentic life struggles in a Sims/RPG-style environment while AI Aides provide real-time coaching. After sufficient training they fuse into Advocates that combine lived understanding with expert solutions.

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
npm install
cp .env.local.example .env.local   # set NEXT_PUBLIC_API_URL
npm run dev
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


## 🧹 Repository Cleanup Update (2026-04-25)

To reduce scope drift and support productization, non-core assets were archived and a new full-stack app layout was introduced:

- Archived legacy folders into `archive/legacy-content/` (including business structures, WordPress assets, and older business-agent framework)
- Added app/service/package scaffolds under `apps/`, `services/`, and `packages/`
- Added implementation roadmap: `docs/roadmaps/full-stack-simulation-app-plan.md`

### New Full-Stack Foundation

```text
apps/
  web/
  mobile/
services/
  api/
packages/
  simulation-sdk/
```

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
python3 -m pip install -r requirements.txt

# Run initial setup
python3 scripts/setup_environment.py
```

> ⚠️ `scripts/setup_environment.py` creates default configs/data templates **and currently overwrites root `.gitignore` and `LICENSE`**. Run it in a fresh clone or sandbox, then review changes with `git diff` before committing.  
> Note: the script currently prints a reference to `docs/avatar-aide-advocate-process.md`, which is not present in this repository.

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

This repository currently has ten automation workflows in `.github/workflows/`.
The table below groups the developer-facing CI and operations workflows most
likely to affect pull requests:

| Workflow file | Actions UI name | Role | Job flow |
| --- | --- | --- | --- |
| `.github/workflows/shared-ci.yml` | **Shared CI** | Organization-standard checks via reusable workflows in `NeuroLift-Technologies/.github-private` | `lint` -> (`test`, `security`) |
| `.github/workflows/python-app.yml` | **Python — Simulation Engine** | Local Python/API checks for `src/`, `tests/`, `requirements.txt`, `pytest.ini`, and `apps/api/` changes | single `test` job (checkout -> setup Python 3.11 -> install -> flake8 -> pytest) |
| `.github/workflows/redteam-ci.yml` | **Red Team CI — Clearance Rubric** | Progressive 3-level clearance harness for syntax/lint/tests, coverage/type checks, and security baseline | `clearance-level-1` -> `clearance-level-2` -> `clearance-level-3` -> PR summary comment |
| `.github/workflows/pgsa-portability-gate.yml` | **PGSA Portability Gate** | Required-check aggregator for secrets scanning and provenance validation | (`secrets-scan`, `provenance-check`) -> `pgsa-gate` |
| `.github/workflows/pr-cleanup.yml` | **PR Cleanup** | Repository hygiene: marks stale PRs, auto-closes stale PRs, and deletes merged source branches | `stale-prs` + `delete-merged-branches` |
| `.github/workflows/sync-governance-public.yml` | **Sync Governance (Public)** | Syncs governance documents (for example `NLT-DEV-OTOI.md`) from `NeuroLift-Technologies/.github-private` via `repository_dispatch`, and runs weekly presence validation | single `sync-governance` job (checkout -> apply payload doc -> validate -> optional commit/PR) |

Other workflow files are subsystem-specific (`web.yml`, `mobile.yml`,
`test-cloudflare.yml`, `validate-governance.yml`) or support repository
maintenance. Python versions are workflow-specific: `shared-ci.yml` currently
requests Python 3.10 from reusable workflows, while `python-app.yml`,
`redteam-ci.yml`, and `pgsa-portability-gate.yml` set up Python 3.11 directly.

### Trigger behavior and constraints

`shared-ci.yml`, `redteam-ci.yml`, and `pgsa-portability-gate.yml` run on:

- `push` to `main`
- `pull_request` targeting `main`
- `workflow_dispatch` (manual run from the Actions tab)

`redteam-ci.yml` also exposes a `clearance_level` manual-dispatch input, but
the current workflow jobs invoke fixed levels (`1`, `2`, and `3`) rather than
threading that input into the script commands.

`python-app.yml` runs on the same event types when Python/API paths change:

- `src/**`
- `tests/**`
- `requirements.txt`
- `pytest.ini`
- `apps/api/**`

`pr-cleanup.yml` runs on:

- a daily schedule (`cron: 0 6 * * *`, 06:00 UTC)
- `workflow_dispatch` with optional inputs:
  - `days_before_stale` (default `30`)
  - `days_before_close` (default `7`)

`sync-governance-public.yml` runs on:

- `repository_dispatch` with type `governance-sync` (document sync path)
- `workflow_dispatch` (manual validation-only run)
- weekly schedule (`cron: 0 8 * * 1`, Monday 08:00 UTC validation-only run)

Important constraints:

- A push to a non-`main` branch does **not** auto-run CI unless you open a PR to `main` or trigger manually.
- Because several CI workflows subscribe to PRs targeting `main`, a qualifying PR can run shared CI, Python/API checks, Red Team clearance, and PGSA checks in parallel.
- `redteam-ci.yml` uploads `clearance-level-<N>-report` artifacts with `actions/upload-artifact@v4.6.2`; the PR summary comment links back to the workflow artifacts.
- `pgsa-portability-gate.yml` uploads `pgsa-secrets-report` and `pgsa-provenance-report` artifacts with `actions/upload-artifact@v4.6.2`; branch protection should use `PGSA Gate — Required Status Check` if the portability gate is enforced.
- Provenance validation passes when no `provenance.json` or `*.provenance.json` manifests are present; missing manifests are reported as "nothing to validate," not as a failure.
- PGSA whitelist misses are advisory warnings; blacklisted sources, malformed manifests, and missing required provenance fields fail validation.
- PR cleanup staleness currently uses defaults of **30 inactive days** before `stale`, then **7 more days** before auto-close (overridable via manual dispatch inputs).
- Draft PRs are explicitly exempt from staleness in `pr-cleanup.yml` (`exempt-draft-pr: true`).
- PR cleanup only targets pull requests (issue staleness is disabled via `days-before-issue-stale: -1` and `days-before-issue-close: -1`).
- Branch deletion only applies to branches merged from this repository (not forks), and skips protected/default branches.
- Governance sync requires `document_name` and base64-encoded `content` in `repository_dispatch.client_payload`; optional fields are `version` and `checksum`.
- Governance sync only writes documents matching `NLT-*.md` or `docs/governance/NLT-*.md`; other paths are rejected.
- Governance sync checksum verification currently supports only `sha256:<hex>` values; unsupported checksum algorithms are warned and skipped.
- Governance sync creates a PR only on `repository_dispatch` runs that produce an actual file diff; scheduled/manual validation runs do not commit or open PRs.

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

### Governance sync runbook (`.github/workflows/sync-governance-public.yml`)

**Subsystems covered:**

1. **Inbound sync ingestion** (`repository_dispatch`)
   - Reads `document_name`, `content` (base64), `version`, and `checksum` from `github.event.client_payload`.
   - Rejects requests that do not include required fields (`document_name`, `content`).
   - Restricts writable targets to `NLT-*.md` and `docs/governance/NLT-*.md`.
2. **Content verification and validation**
   - Decodes payload content from base64 and writes to the requested file.
   - Optionally verifies checksum when `checksum` is provided.
   - Weekly/manual validation checks presence of `NLT-DEV-OTOI.md` and emits warnings if missing.
3. **Automated PR creation**
   - Runs only for `repository_dispatch` events with actual file changes.
   - Creates branch `governance-sync/<UTC timestamp>`, commits the synced document, pushes branch, and opens a PR with `gh pr create`.

**Codepath map (source-verified):**

| Behavior | Workflow codepath | Notes |
| --- | --- | --- |
| Required payload fields | `if [ -z "$DOCUMENT_NAME" ] \|\| [ -z "$DOCUMENT_CONTENT" ]` | Missing fields fail the run. |
| Allowed destination paths | `case "$DOCUMENT_NAME" in NLT-*.md \| docs/governance/NLT-*.md)` | Any other path is rejected. |
| Base64 decode write path | `echo "$DOCUMENT_CONTENT" \| base64 --decode > "$DOCUMENT_NAME"` | Parent dir is created first with `mkdir -p`. |
| Checksum verification | `case "$ALGO" in sha256)` | Expects `sha256:<hex>` format. Mismatches fail the run; unsupported algorithm prefixes are skipped with a warning (not enforced). |
| Validation document check | `for doc in NLT-DEV-OTOI.md; do ...` | Missing docs warn, not fail. |
| PR creation gate | `if: github.event_name == 'repository_dispatch' && steps.changes.outputs.changed == 'true'` | Manual/scheduled runs do not open PRs. |

**Operational constraints and pitfalls:**

- Governance sync requires `contents: write` and `pull-requests: write` to push branches and create PRs.
- Document content must be base64-safe text; malformed base64 causes decode failure.
- A valid dispatch can still produce no PR if the decoded content is identical to the existing file.
- The validation step currently checks only `NLT-DEV-OTOI.md`; additional required governance docs must be added explicitly in workflow code.

### Manual usage

From GitHub UI:

1. Open **Actions**.
2. Select the workflow to run (for example **Shared CI**, **Python — Simulation Engine**, **Red Team CI — Clearance Rubric**, **PGSA Portability Gate**, **PR Cleanup**, or **Sync Governance (Public)**).
3. Click **Run workflow**.
4. Choose the branch and set any workflow-specific inputs.

For manual Red Team clearance:

1. Open **Actions** -> **Red Team CI — Clearance Rubric** -> **Run workflow**.
2. Choose a branch and, if needed, select `clearance_level`.
3. Inspect the `clearance-level-<N>-report` artifacts and the PR summary comment.

For manual PGSA validation:

1. Open **Actions** -> **PGSA Portability Gate** -> **Run workflow**.
2. Inspect `pgsa-secrets-report`, `pgsa-provenance-report`, and the final `PGSA Gate — Required Status Check` job.

For manual PR cleanup tuning (`PR Cleanup` only):

1. Open **Actions** -> **PR Cleanup** -> **Run workflow**.
2. Set `days_before_stale` (default `30`) and `days_before_close` (default `7`) if needed.
3. Run and inspect logs for the `stale-prs` and `delete-merged-branches` jobs.

For governance validation (`Sync Governance (Public)`):

1. Open **Actions** -> **Sync Governance (Public)** -> **Run workflow**.
2. Run on the target branch (normally `main`).
3. Inspect logs for:
   - `Validate governance documents` (presence/warnings)
   - `Apply synced governance document` and `Create pull request for governance update` on repository-dispatch runs.

PR cleanup verification checklist:

1. Confirm the run used the expected `days_before_stale` and `days_before_close` values.
2. In `stale-prs` logs, verify labels/actions align with the current policy (`stale`, `auto-closed`, draft PR exemption).
3. In `delete-merged-branches` logs, verify each skip/delete outcome is expected (fork PR, protected branch, or already deleted branch).
4. If merged branches remain, check whether the relevant PRs fall outside the current `per_page: 100` query window.

For manual governance validation (`Sync Governance (Public)` only):

1. Open **Actions** -> **Sync Governance (Public)** -> **Run workflow**.
2. Choose the branch (usually `main`) and start the run.
3. Review `Validate governance documents` logs for missing-file warnings.

For automated governance ingestion (from tooling/private repo), dispatch `repository_dispatch` with this payload contract:

```json
{
  "event_type": "governance-sync",
  "client_payload": {
    "document_name": "NLT-DEV-OTOI.md",
    "content": "<base64-encoded markdown>",
    "version": "optional-version-string",
    "checksum": "sha256:<hex-digest>"
  }
}
```

`document_name` and `content` are required. `checksum` is optional but recommended for tamper detection.

To reproduce `python-app.yml` locally:

```bash
python -m pip install --upgrade pip
pip install flake8 pytest
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
pytest
```

To reproduce the Red Team and PGSA harness locally:

```bash
# Clearance Level 1 only: syntax, fatal lint errors, unit tests
python scripts/run_clearance_tests.py --level 1 --verbose

# Full clearance through Level 3. Requires flake8, pytest, pytest-cov, mypy,
# and at least one installed secret scanner for meaningful secret results.
python scripts/run_clearance_tests.py --level 3 --verbose

# PGSA secrets scan. Install gitleaks locally for parity with CI.
python scripts/scan_secrets.py \
  --gitleaks-config .github/gitleaks.toml \
  --fail-on-findings \
  --skip-trufflehog \
  --verbose

# PGSA provenance validation.
python scripts/validate_provenance.py \
  --scan-root . \
  --config config/pgsa-allowlists.json \
  --verbose
```

### Maintenance checklist

- **Update Python version in both CI workflows together** to avoid drift:
  - `.github/workflows/shared-ci.yml` -> `with.python-version`
  - `.github/workflows/python-app.yml` -> `with.python-version`
- **Keep Red Team/PGSA workflow docs aligned** when changing the harness:
  - `.github/workflows/redteam-ci.yml` (job graph, artifact names, manual inputs)
  - `.github/workflows/pgsa-portability-gate.yml` (required check name, report artifacts)
  - `scripts/run_clearance_tests.py`, `scripts/scan_secrets.py`, and `scripts/validate_provenance.py` (CLI flags, exit behavior, report formats)
  - `docs/CI_HARNESS_README.md` and this README section
- **Keep branch trigger filters aligned** in both CI files when changing branch policy.
- **Treat `shared-ci.yml` behavior as externally defined**: it calls reusable workflows from `.github-private` at `@main`.
- **Do not remove `security-events: write` from `shared-ci.yml`** unless the reusable security workflow no longer needs upload permissions.
- **When changing PR retention policy, update both code and docs together**:
  - `.github/workflows/pr-cleanup.yml` (`days-before-stale`, `days-before-close`)
  - this README section (trigger behavior + runbook defaults)
- **When changing governance document policy, update both code and docs together**:
  - `.github/workflows/sync-governance-public.yml` (allowed path patterns + validation document list)
  - this README section (payload contract + runbook constraints)
- **Protect long-lived branches in GitHub settings** so `delete-merged-branches` can safely skip them using the protected-branch API check.
- **Do not reduce PR Cleanup write permissions** unless stale labeling/closing and branch deletion behavior is intentionally being disabled.
- **Keep cleanup intent aligned in two places** when requirements change:
  - `.github/workflows/pr-cleanup.yml` (enforced behavior)
  - `.github/agents/pr-cleanup.agent.md` (agent runbook + reporting expectations)
- **Keep governance source-of-truth explicit**:
  - upstream governance authoring lives in `NeuroLift-Technologies/.github-private`
  - this repository consumes synced copies (for example `NLT-DEV-OTOI.md`) via `Sync Governance (Public)`
- **If checksum algorithms change**, update both workflow verification logic and this runbook's payload guidance at the same time.

### Troubleshooting and common pitfalls

- **CI did not run:** confirm the event targets `main`, or run with `workflow_dispatch`.
- **`Shared CI` fails before local tests run:** inspect reusable workflow logs from `.github-private`; failures there can occur without changes in this repository.
- **Security/test ordering confusion:** in `shared-ci.yml`, both `test` and `security` depend on `lint` and can run in parallel after lint passes.
- **`python-app.yml` lint behavior seems inconsistent:** the first flake8 command fails on syntax/name errors; the second uses `--exit-zero` and is informational for style/complexity reporting.
- **PR branch was not deleted after merge:** check whether the PR came from a fork, whether the branch is protected, or whether it was already deleted (422 is treated as non-fatal in workflow logs).
- **PR expected to stay open got marked stale:** add any activity (comment/commit/review) or convert to draft if it is actively in progress but intentionally paused.
- **Governance sync run fails with "missing required fields":** verify `repository_dispatch.client_payload` includes both `document_name` and `content`.
- **Governance sync run fails with "Disallowed document name":** path must match `NLT-*.md` or `docs/governance/NLT-*.md`.
- **Governance sync logs checksum mismatch:** recompute checksum from the decoded file content and ensure it is sent as `sha256:<hex>`.
- **Governance sync did not open a PR:** confirm event was `repository_dispatch` (not schedule/manual) and that the decoded file content actually changed.
- **Red Team Level 2 or 3 appears to rerun earlier checks:** this is current script behavior. `run_clearance_tests.py --level N` executes every level from `1` through `N`, and the workflow runs each clearance job independently.
- **Secret scan reports no tools available locally:** install Gitleaks or TruffleHog. CI installs Gitleaks before Red Team Level 3 and PGSA secrets scanning.
- **PGSA provenance passed with zero manifests:** this is expected; add `provenance.json` or `*.provenance.json` files for components that need explicit provenance tracking.
- **PGSA provenance shows whitelist warnings but the job passes:** whitelist matches are advisory. Blacklist matches, parse errors, and missing required fields are enforced failures.
- **Expected PGSA branch-protection check is missing:** branch protection should reference `PGSA Gate — Required Status Check`, not the individual `Secrets Scan (Gitleaks)` or `Provenance Validation (PGSA)` jobs.

### Local runtime troubleshooting (scripts)

- **`ImportError: attempted relative import beyond top-level package` from `scripts/run_training_session.py`:**
  `run_training_session.py` imports `avatars.*` after modifying `sys.path`, but modules under `src/avatars` use package-relative imports (`..core`), so direct execution currently fails.
- **`TypeError: CoachingContext.__init__() got an unexpected keyword argument 'avatar'` from `scripts/test_training_loop.py`:**
  this script still uses an older `CoachingContext` call pattern that no longer matches `src/aides/base_aide.py`.
- **`No module named pytest` when running test commands:**
  install dependencies first with `python3 -m pip install -r requirements.txt`.
- **Need a deterministic smoke path while those scripts are being reconciled:**
  run `python3 -m compileall src scripts`, then use `python3 -m pytest tests/test_simulation/test_session_orchestrator.py` as the reference for current orchestration interfaces.

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

See `archive/legacy-content/nlt-business-agents/implementation-guide.md` for historical business-agent instructions.

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
├── archive/legacy-content/business-structure/  # Archived planning assets
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
└── archive/legacy-content/nlt-business-agents/    # Archived business agent framework
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

#### Workers

| Worker | Purpose | Deploy | Visit |
|--------|---------|--------|-------|
| **Main** | Request routing & caching | [![Deploy](https://deploy.workers.cloudflare.com/button)](https://deploy.workers.cloudflare.com/?url=https://github.com/NeuroLift-Technologies/neurolift-ai-fusion) | [![Visit](https://img.shields.io/badge/Visit-neuroliftsolutions.com-F38020?style=flat-square&logo=cloudflare&logoColor=white)](https://neuroliftsolutions.com) |
| **WordPress Optimizer** | Performance & WP caching | [![Deploy](https://deploy.workers.cloudflare.com/button)](https://deploy.workers.cloudflare.com/?url=https://github.com/NeuroLift-Technologies/neurolift-ai-fusion) | [![Visit](https://img.shields.io/badge/Visit-neuroliftsolutions.com-F38020?style=flat-square&logo=cloudflare&logoColor=white)](https://neuroliftsolutions.com) |
| **Security** | Bot protection & headers | [![Deploy](https://deploy.workers.cloudflare.com/button)](https://deploy.workers.cloudflare.com/?url=https://github.com/NeuroLift-Technologies/neurolift-ai-fusion) | [![Visit](https://img.shields.io/badge/Visit-neuroliftsolutions.com-F38020?style=flat-square&logo=cloudflare&logoColor=white)](https://neuroliftsolutions.com) |

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

*Note: The older business-agent framework now lives in `/archive/legacy-content/nlt-business-agents/` for historical reference.*
