#!/usr/bin/env bash
# validate-governance.sh
# NeuroLift Technologies — Governance Compliance Validation
set -uo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PASS=0
FAIL=0
WARN=0
STRICT=0

for _arg in "$@"; do
  case "${_arg}" in
    --strict) STRICT=1 ;;
    *) echo "Unknown flag: ${_arg}" >&2; exit 1 ;;
  esac
done

check_file() {
  local file="$1"
  if [[ -f "${REPO_ROOT}/${file}" ]]; then
    echo "  ✅ EXISTS: ${file}"
    ((PASS++)) || true
  else
    echo "  ❌ MISSING: ${file}"
    ((FAIL++)) || true
  fi
}

check_content() {
  local file="$1"
  local pattern="$2"
  local label="$3"
  if [[ -f "${REPO_ROOT}/${file}" ]] && grep -q "${pattern}" "${REPO_ROOT}/${file}"; then
    echo "  ✅ CONTENT OK: ${label} in ${file}"
    ((PASS++)) || true
  else
    echo "  ❌ CONTENT MISSING: ${label} in ${file}"
    ((FAIL++)) || true
  fi
}

echo "=============================================="
echo "  NLT Governance Validation"
echo "  Repo: ${REPO_ROOT}"
echo "  Date: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "=============================================="
echo ""

# --- Required Files ---
echo "[ Required Files ]"
required_files=(
  "NLT-DEV-OTOI.md"
  "AGENTS.md"
  "REVIEW.md"
  "nltotoi.json"
  ".nltotoi/README.md"
  ".nltotoi/index/governance-files.md"
  ".nltotoi/contracts/README.md"
  ".nltotoi/scripts/validate-governance.sh"
  ".nltotoi/proposals/validation-roadmap.md"
  "templates/agent-registration.json"
  "templates/handoff-record.json"
  "templates/escalation.md"
  "templates/intent-log.md"
  "templates/commit-message.md"
  "templates/review-record.md"
  "ISSUE_TEMPLATE/agent-escalation.md"
  "ISSUE_TEMPLATE/governance-proposal.md"
  "PULL_REQUEST_TEMPLATE/agent-contribution.md"
  ".github/workflows/validate-governance.yml"
  "SOPs/new-agent-onboarding.md"
  "SOPs/repo-governance-setup.md"
  "SOPs/incident-response.md"
)

for f in "${required_files[@]}"; do
  check_file "$f"
done

echo ""

# --- Content Checks ---
echo "[ Content Validation ]"
check_content "NLT-DEV-OTOI.md"  "ORG-DEV-OTOI-1.0.3"           "Document ID"
check_content "NLT-DEV-OTOI.md"  "Joshua W. Dorsey"              "Authority marker"
check_content "NLT-DEV-OTOI.md"  "Solidarity Framework"          "Solidarity Framework reference"
check_content "NLT-DEV-OTOI.md"  "HAIEF"                         "HAIEF reference"
check_content "REVIEW.md"        "ORG-DEV-OTOI-1.0.3"             "OTOI version referenced in REVIEW.md"
check_content "REVIEW.md"        "NLT-DEV-OTOI.md"               "OTOI reference in REVIEW.md"
check_content "AGENTS.md"        "NLT-DEV-OTOI.md"               "OTOI reference in AGENTS.md"
check_content "AGENTS.md"        "ORG-DEV-OTOI-1.0.3"            "Document ID in AGENTS.md"
check_content "nltotoi.json"     "NeuroLift-Technologies/neurolift-ai-fusion" "Repository name in manifest"
check_content "nltotoi.json"     "ORG-DEV-OTOI-1.0.3"            "Document ID in manifest"
check_content "nltotoi.json"     "NLT-DEV-OTOI.md"               "Canonical contract path in manifest"

echo ""

# --- Summary ---
echo "=============================================="
echo "  Results: ${PASS} passed, ${FAIL} failed, ${WARN} warned"
if [[ "${STRICT}" -eq 1 ]]; then
  echo "  Mode: strict (warnings treated as failures)"
fi
echo "=============================================="

if [[ "${FAIL}" -gt 0 ]]; then
  echo ""
  echo "GOVERNANCE VALIDATION FAILED — ${FAIL} check(s) did not pass."
  exit 1
else
  echo ""
  echo "GOVERNANCE VALIDATION PASSED — all ${PASS} checks passed."
  exit 0
fi
