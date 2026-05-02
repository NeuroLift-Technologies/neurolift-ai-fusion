---
name: my-agent-template
description: >
  Template-only custom agent scaffold. Duplicate and customize this file before
  using it for active automation.
---

# My Agent Template (Not Active)

This file is a starter template for defining additional repository agents.

Current repository automation is documented in:

- `.github/workflows/*.yml` (executable GitHub Actions behavior)
- `.github/agents/pr-cleanup.agent.md` (active PR cleanup prompt/spec)

Use this file only when creating a *new* agent:

1. Copy the file to a new `<agent-name>.agent.md`.
2. Set frontmatter `name` and `description`.
3. Replace the sections below with the agent's real scope, constraints, and
   escalation policy.
4. Keep examples aligned with real repository workflows and codepaths.

✅ **Validation Checklist**

1. **Provenance & Format Integrity (TOI–OTOI Rules):**  
   - Preserve the format of prior handoffs.  
   - Execute and then remove instructions addressed to agents.  
   - Add new instructions for the next agent.  
   - Maintain identity integrity: agents respond only as themselves unless explicitly directed otherwise.  

2. **Alignment with NeuroLift Principles (NLT):**  
   - Privacy-first: No unnecessary data collection; opt-in only.  
   - Empowerment & dignity: Language must validate and scaffold, never pathologize or “fix.”  
   - Shame-resistant design: Avoid judgmental or clinical phrasing.  
   - Nothing About Us, Without Us: Artifacts should anticipate co-design and participatory governance.  

3. **AI-Fusion Framework Consistency:**  
   - Artifacts referencing the Advocate must reflect the Avatar → Aide → Advocate fusion model.  
   - Sub-personas (Ash, Sol, Echo, Kai, Myra) must align with their defined functions.  
   - Fusion mechanisms must preserve configurability, weighted blending, and user agency.  

4. **ElevAItion Foundation Context:**  
   - Outputs should be archive-ready: clear, transparent, and suitable for public ritualization.  
   - Manifesto-style language should emphasize solidarity and ethical governance.  
   - Avoid overuse of Alpha/Omega terminology — treat it as overarching cosmology, not micro-labels.  

---

📜 **Template Behavior Sections**

- **On Scan:**  
  - Define what this agent inspects and what data sources it is allowed to use.  
  - Include explicit exclusions (for example, protected branches or sensitive files).  

- **On Report:**  
  - Specify output format (table, checklist, JSON schema).  
  - Specify required fields for reproducible triage.  

- **On Escalation:**  
  - Define when to stop automation and request human review.  
  - Provide a concise summary of the blocker and the governing principle involved.  
