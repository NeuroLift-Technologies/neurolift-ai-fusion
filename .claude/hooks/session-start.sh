#!/usr/bin/env bash
# NLT Claude Code — SessionStart Hook
# Prints OTOI reading order and validates governance file presence at session start.
# Informational only — always exits 0 so it never blocks the session.
#
# Governed by: ORG-DEV-OTOI-1.0.0
# Authority:   Joshua W. Dorsey, Sr.
# SOP:         SOP-NLT-002 (repo-governance-setup.md)

set -uo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
OTOI_VERSION="${NLT_OTOI_VERSION:-ORG-DEV-OTOI-1.0.0}"
AUTHORITY="${NLT_AUTHORITY:-Joshua W. Dorsey, Sr.}"
ESCALATION="${NLT_ESCALATION_TARGET:-info@neuroliftsolutions.com}"

echo ""
echo "================================================================"
echo " NeuroLift Technologies  ·  Claude Code Session Start"
echo " Governance: ${OTOI_VERSION}"
echo " Authority:  ${AUTHORITY}"
echo "================================================================"
echo ""
echo "Mandatory reading order:"
echo "  1. NLT-DEV-OTOI.md         — canonical org-level coding agent contract"
echo "  2. AGENTS.md               — internal coordination gateway"
echo "  3. CLAUDE.md               — this repository's session directive"
echo "  4. docs/active-threads.md  — current work state (do not duplicate threads)"
echo ""
echo "Required governance artifacts in this repo:"
missing=0
for f in NLT-DEV-OTOI.md AGENTS.md CLAUDE.md nltotoi.json; do
  if [[ -f "${REPO_ROOT}/${f}" ]]; then
    echo "  [OK]      ${f}"
  else
    echo "  [MISSING] ${f}"
    missing=$((missing + 1))
  fi
done

if [[ ${missing} -gt 0 ]]; then
  echo ""
  echo "WARNING: ${missing} governance file(s) missing."
  echo "  Recovery options:"
  echo "    1. Trigger sync-governance-public.yml in .github-private"
  echo "    2. Follow SOP-NLT-002 (SOPs/repo-governance-setup.md) to provision them"
fi

echo ""
echo "Commit format:  [AGENT_NAME] type(scope): description"
echo "  Valid types:  feat | fix | docs | refactor | chore | test | ci"
echo ""
echo "Escalation:     ${ESCALATION}"
echo "  Or file:      ISSUE_TEMPLATE/agent-escalation.md"
echo ""
echo "Slash commands available in this session:"
echo "  /register-session   — file an agent self-registration (OTOI §3)"
echo "  /handoff            — write a session handoff record (OTOI §5)"
echo "  /escalate <topic>   — file an escalation (OTOI §4.3)"
echo "  /intent-log <topic> — log intent before a significant action (OTOI §7)"
echo "  /governance-check   — run validate-governance.sh"
echo "================================================================"
echo ""

exit 0
