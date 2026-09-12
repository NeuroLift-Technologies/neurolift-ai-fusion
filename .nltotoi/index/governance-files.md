# Governance File Index — NeuroLift Technologies `neurolift-ai-fusion`

**Last updated:** 2026-09-12
**Maintained by:** `.nltotoi/` namespace tooling
**Scope:** `NeuroLift-Technologies/neurolift-ai-fusion`
**Governance version:** ORG-DEV-OTOI-1.0.3

---

## Core Governance Files

| File | Type | Purpose | Required |
|---|---|---|---|
| `NLT-DEV-OTOI.md` | Contract | Org-level coding agent contract (ORG-DEV-OTOI-1.0.3) | ✅ |
| `AGENTS.md` | Gateway | Internal agent coordination gateway | ✅ |
| `REVIEW.md` | Format | Canonical agent review format | ✅ |
| `nltotoi.json` | Manifest | Machine-readable discovery manifest | ✅ |
| `README.md` | Overview | Repository overview and purpose | ✅ |

---

## .nltotoi Namespace

| File | Purpose | Required |
|---|---|---|
| `.nltotoi/README.md` | Namespace overview | ✅ |
| `.nltotoi/index/governance-files.md` | This file — governance registry | ✅ |
| `.nltotoi/contracts/README.md` | Contract namespace and versioning | ✅ |
| `.nltotoi/scripts/validate-governance.sh` | Automated compliance validation | ✅ |
| `.nltotoi/proposals/validation-roadmap.md` | Planned validation improvements | ✅ |

---

## Templates

| File | Purpose | Source |
|---|---|---|
| `templates/agent-registration.json` | Agent self-registration format | OTOI Section 3 |
| `templates/handoff-record.json` | Session handoff format | OTOI Section 5 |
| `templates/escalation.md` | Escalation record format | OTOI Section 4.3 |
| `templates/intent-log.md` | Intent logging before action | OTOI Section 7 |
| `templates/commit-message.md` | Commit message format reference | OTOI Section 4.2, SOP-NLT-001 Step 7 |
| `templates/review-record.md` | Fillable review record template | OTOI Section 4.5 |

---

## GitHub Templates

| File | Purpose |
|---|---|
| `ISSUE_TEMPLATE/agent-escalation.md` | GitHub issue form for agent escalations |
| `ISSUE_TEMPLATE/governance-proposal.md` | GitHub issue form for OTOI amendment proposals |
| `PULL_REQUEST_TEMPLATE/agent-contribution.md` | Agent PR checklist with governance requirements |

---

## CI Workflows

| File | Purpose | Trigger |
|---|---|---|
| `.github/workflows/validate-governance.yml` | Governance validation (runs validate-governance.sh) | push, pull_request |
| `.github/workflows/shared-ci.yml` | Organization-standard checks (lint, test, security) | push, pull_request |
| `.github/workflows/python-app.yml` | Python/API simulation engine checks | push, pull_request |
| `.github/workflows/redteam-ci.yml` | Progressive 3-level clearance harness | push, pull_request |
| `.github/workflows/pgsa-portability-gate.yml` | Secrets scanning + provenance validation | push, pull_request |
| `.github/workflows/pr-cleanup.yml` | Stale PR + merged branch hygiene | schedule, workflow_dispatch |
| `.github/workflows/sync-governance-public.yml` | Sync governance docs from `.github-private` | repository_dispatch, schedule |
| `.github/workflows/web.yml` | Next.js web app build/test | push, pull_request |
| `.github/workflows/mobile.yml` | Expo mobile app build/test | push, pull_request |
| `.github/workflows/test-cloudflare.yml` | Cloudflare Workers deployment test | push, pull_request |
| `.github/workflows/ai-tests.yml` | AI/ML model tests | push, pull_request |

---

## SOPs (Standard Operating Procedures)

| File | Purpose |
|---|---|
| `SOPs/new-agent-onboarding.md` | How to onboard a new coding agent |
| `SOPs/repo-governance-setup.md` | How to add governance stubs to a new NLT repo |
| `SOPs/incident-response.md` | What to do when an agent goes off-rails |

---

## File Count Summary

| Category | Count |
|---|---|
| Core governance | 5 |
| .nltotoi namespace | 5 |
| Templates | 6 |
| GitHub templates | 3 |
| CI workflows | 11 |
| SOPs | 3 |
| **Total** | **33** |

---

*Generated from `.nltotoi/index/governance-files.md` | NeuroLift Technologies | ORG-DEV-OTOI-1.0.3*
