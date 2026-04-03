# TOI-OTOI Integration Framework

## Overview

This repository implements the TOI-OTOI (Terms of Interaction - Orchestrated Terms of Interaction) framework to ensure privacy-preserving, human-controlled AI agency across all business operations.

## Core Principles

### 1. Privacy Protection
- **Data Retention**: Ephemeral by default, with human-controlled overrides
- **Context Sharing**: Selective and purposeful information exchange
- **Override Rights**: Humans maintain complete control over data usage

### 2. Human Agency Preservation
- **Task Initiation**: Human-approved for all strategic decisions
- **Interruptibility**: Agents can always be paused or redirected
- **Decision Authority**: Advisory-only with clear escalation paths

### 3. Cognitive Alignment
- **Modular Scaffolding**: Agents adapt to human cognitive styles
- **Parallel Threading**: Maintain context across multiple conversations
- **Selective Context Sharing**: Relevant information flows between agents

## Implementation Architecture

### Global Configuration
Located in `config/global-toi-config.json`:

```json
{
  "otoi": {
    "version": "1.2.0",
    "global_settings": {
      "privacy": {
        "data_retention": "ephemeral",
        "override_rights": "human-controlled",
        "context_window": "adaptive"
      },
      "agency": {
        "task_initiation": "human-approved",
        "interruptibility": "always",
        "decision_authority": "advisory-only"
      },
      "cognitive_alignment": {
        "scaffolding_style": "modular",
        "threading": "parallel-preserving",
        "context_sharing": "selective"
      }
    }
  }
}
```

### Agent-Level Configuration

Each agent includes a `toi-profile.json` that defines:

- **Privacy Settings**: Data retention and sharing preferences
- **Agency Level**: Autonomy level and approval requirements
- **Cognitive Style**: Processing approach and output format

### Human Oversight Integration

#### CEO Oversight
- **Approval Required**: Strategic decisions, financial commitments, executive recommendations
- **Notification Required**: All agent outputs, escalated issues, performance metrics

#### COO Oversight  
- **Approval Required**: Operational changes, resource allocation, process modifications
- **Notification Required**: Department outputs, operational metrics, escalation events

## Communication Protocol

### Inter-Agent Communication
- **Method**: Message queue with structured JSON format
- **Logging**: Comprehensive logging with full human visibility
- **Escalation**: Clear triggers and routing for human intervention

### Escalation Triggers
- Conflicting recommendations between agents
- Decision uncertainty beyond agent capabilities
- Resource conflicts requiring human arbitration
- Ethical concerns or policy violations
- Capability limitations requiring human expertise

### Context Sharing Rules
- **Between Executives**: Full context sharing
- **Between Departments**: Relevant information only
- **Sub-Agent to Parent**: Comprehensive reporting
- **To Humans**: Summarized with detailed information available on request

## Privacy Controls

### Data Retention Policies
- **Ephemeral**: Default for all agent conversations
- **Session**: For ongoing projects requiring context
- **Persistent**: Only for critical business records (with human approval)

### Override Mechanisms
- **Immediate Override**: Humans can stop any agent action
- **Data Deletion**: Complete removal of specified data
- **Context Isolation**: Prevent information sharing between agents
- **Decision Reversal**: Override any agent recommendation

## Ethical Guidelines

### Decision Making
- All significant decisions require human approval
- Agents provide transparent reasoning for recommendations
- Ethical considerations are explicitly evaluated
- Human values and company culture are prioritized

### Transparency
- Complete audit trail of all agent activities
- Human-readable explanations for all decisions
- Regular reporting on agent performance and behavior
- Open communication about AI capabilities and limitations

## Monitoring and Compliance

### Performance Metrics
- Response accuracy and quality
- Decision approval rates
- Escalation frequency and patterns
- Human override frequency and reasons

### Compliance Tracking
- TOI-OTOI principle adherence
- Privacy policy compliance
- Human oversight effectiveness
- Ethical guideline adherence

## Integration Points

### External Systems
- CRM and business systems
- Financial and accounting platforms
- Communication and collaboration tools
- Monitoring and analytics platforms

### Human Interfaces
- CEO Dashboard for strategic oversight
- COO Dashboard for operational management
- Real-time notifications and alerts
- Comprehensive reporting and analytics

## Best Practices

### For Humans
1. **Regular Review**: Monitor agent performance and decision quality
2. **Clear Communication**: Provide explicit instructions and feedback
3. **Ethical Oversight**: Ensure all decisions align with company values
4. **Continuous Learning**: Adapt oversight based on agent performance

### For Agents
1. **Transparent Reasoning**: Always explain decision rationale
2. **Proactive Escalation**: Raise concerns before they become problems
3. **Context Preservation**: Maintain relevant information across interactions
4. **Human Alignment**: Adapt communication style to human preferences

## Troubleshooting

### Common Issues
- **Agent Conflicts**: Use escalation protocols to resolve disagreements
- **Decision Uncertainty**: Escalate to appropriate human authority
- **Performance Issues**: Review configuration and provide additional training
- **Privacy Concerns**: Use override mechanisms to control data usage

### Support Resources
- Configuration guides in `docs/architecture/`
- Troubleshooting playbooks in `docs/playbooks/`
- Agent training materials in `docs/training/`

---

*This framework ensures that AI agents enhance human capabilities while maintaining human control, privacy, and ethical standards across all business operations.*

---

## Documentation Update Note

**Updated: November 23, 2025**

The TOI-OTOI framework terminology has been standardized across all repository documentation. 

**Proper Verbiage**: TOI-OTOI = **Terms of Interaction - Orchestrated Terms of Interaction**

This framework defines how AI agents interact with users and each other through structured, orchestrated interaction patterns that ensure:
- Privacy-preserving operations
- Human-controlled agency
- Ethical alignment
- Transparent decision-making

All references throughout the repository now use this consistent terminology.

---

*Author: Joshua Dorsey (via GitHub Copilot)*  
*Date: November 23, 2025*  
*Update: Repository verbiage standardization*