---
name: nlt-agent-registration
description: 'Complete an NLT agent self-registration record (OTOI Section 3). Use when an agent is starting a new session and needs to register, when asked to fill out agent-registration.json, when logging agent session start details, or when recording agent capabilities and limitations before beginning work.'
nlt-otoi-version: ORG-DEV-OTOI-1.0.2
nlt-solidarity-framework: true
nlt-haief: true
nlt-authority: Joshua W. Dorsey, Sr.
---

# NLT Agent Self-Registration (OTOI Section 3)

This skill guides agents through completing the **agent self-registration** record required by ORG-DEV-OTOI-1.0.2 Section 3 at the start of every NLT session.

The `/register-session` slash command automates this workflow.

## Where to Store the Registration

Save the completed registration to:
```
docs/agent-log/registrations/[date]-[agent-name].json
```

## Registration Template

```json
{
  "agent_registration": {
    "agent_name":         "Claude Code",
    "platform":           "Claude Code",
    "version":            "[Model version]",
    "session_id":         "[Branch name]",
    "entry_date":         "[YYYY-MM-DD]",
    "entry_point":        "[Task that started this session]",
    "acknowledged_otoi":  true,
    "otoi_version":       "ORG-DEV-OTOI-1.0.2",
    "working_repo":       "NeuroLift-Technologies/neurolift-ai-fusion",
    "working_branch":     "[branch]",
    "capabilities_self_reported": [],
    "known_limitations": [],
    "preferred_handoff_format": "[Description]"
  }
}
```

## Field Guidance

- `acknowledged_otoi`: Must be `true` — confirms you have read the contract
- `otoi_version`: Must be `"ORG-DEV-OTOI-1.0.2"`
- `entry_date`: ISO 8601 `YYYY-MM-DD`
- All fields except `version`, `session_id`, `preferred_handoff_format` are required

## References

- `templates/agent-registration.json` — Blank template
- `NLT-DEV-OTOI.md` Section 3 — Canonical spec
- `SOPs/new-agent-onboarding.md` — Full onboarding procedure
