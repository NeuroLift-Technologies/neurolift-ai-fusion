# AI Guidance Documentation

This directory contains documentation and guidance materials specifically designed for AI assistants working on the NeuroLift AI Fusion project.

## Contents

### Claude Code session governance (`.claude/`)

The repository includes a Claude Code session-governance template under
`.claude/`. It is a synced copy from
`NeuroLift-Technologies/.github-private/.claude/`, so agents should read it but
should not edit it in this repo unless explicitly directed by a human.

Key entry points:

| Path | Purpose |
| --- | --- |
| `.claude/README.md` | Explains the synced template, source of truth, and repo-specific override path. |
| `.claude/settings.json` | Wires the `SessionStart` hook and Claude Code permission/env defaults. |
| `.claude/hooks/session-start.sh` | Prints mandatory OTOI reading order and checks required governance files; exits `0` even when it warns. |
| `.claude/commands/` | Slash-command guidance for session registration, handoff, escalation, intent logs, and governance checks. |
| `.claude/skills/` | Task-specific OTOI guidance that can be loaded on demand. |
| `.claude/agents/` | NLT Governance Steward, NLT Code Reviewer, and SWE subagent profiles. |

Repo-specific Claude Code overrides belong in `.claude/settings.local.json`;
the propagation workflow is documented not to overwrite that file.

### Staged governance validation proposals

`.nltotoi/proposals/*.yml.proposed` contains proposed GitHub Actions workflow
definitions for agent commit-format, session handoff, agent-profile, and
skill-profile validation. These files are source material only while they keep
the `.proposed` suffix. They do not run in CI unless a human/governance-approved
change moves them into `.github/workflows/`.

### GEMINI_TOPOGRAPHY.py

A comprehensive Python file that provides:
- Complete repository structure mapping
- TOI-OTOI Framework specifications
- Avatar-Aide-Advocate architecture details
- Development phases and roadmap
- Business model integration
- Integration points with other systems
- Utility functions for AI assistants

This file serves as the primary reference for AI assistants (particularly Gemini) to understand the project structure, conventions, and implementation details.

## Purpose

These files help AI assistants:
1. Understand the repository organization
2. Navigate the codebase effectively
3. Implement features consistently with the architecture
4. Maintain privacy-first and community-driven principles
5. Follow the TOI-OTOI framework correctly

## Usage

AI assistants should reference these files when:
- Starting work on any new feature
- Understanding the project structure
- Implementing Avatar, Aide, or Advocate components
- Integrating with other NeuroLift systems
- Validating implementations against specifications
- Beginning a Claude Code session that must follow OTOI registration, handoff,
  escalation, or governance-check protocols
