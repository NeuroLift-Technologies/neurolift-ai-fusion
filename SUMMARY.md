# Summary

This document describes the implementation plan for the requested changes to the Neurolift AI Fusion project. The changes include code enhancements, documentation updates, and architecture fixes.

## Overview of Changes

### 1. Code Changes

#### A. Transformers Agent Decision Source (transformers_agent_decision.py)
**Current Issues:**
- Only produces "wait" and "approach" verbs
- No seed sampling for reproducible training
- No prompt/token ID recording
- No support for all 7 available verbs (approach, look_at, use, sit, rest, communicate, wait)
- Fixed prompt without Avatar identity/trait/day memory

**Required Changes:**
1. Add support for all 7 verbs: approach, look_at, use, sit, rest, communicate, wait
2. Implement seed-based sampling during training days
3. Maintain greedy decoding for solo-day evaluation
4. Record prompt and generated token IDs for each decision
5. Include Avatar identity, trait, and day memory in system prompt
6. Make decision source selectable in agent_loop_http.build_decision_source()

#### B. Agent Loop Integration
**Current State:**
- SessionOrchestrator runs tasks through avatar.attempt_task()
- Agent loop operates independently
- No integration between the two

**Required Changes:**
1. Connect agent loop to SessionOrchestrator
2. Take outcomes from Godot (world engine)
3. Make success come from world engine's next perception, not attempt_task's probability roll
4. Keep old path for tests only

#### C. Day Log Extension (model_fusion.py)
**Current PairedTrajectoryStep Structure:**
- step_id, scenario, observation, avatar_output, aide_output, channel_messages, outcome, counterfactual_label

**Required Enhancements:**
1. Add token_ids field to record decision tokens
2. Add engine_tick field to track world engine tick
3. Add decision_source field to identify which decision source acted
4. Add solo_day flag to indicate solo training days
5. Add missed_turn flag to track skipped turns

#### D. Solo Days Implementation
**Required Changes:**
1. Implement sessions with no Aide
2. Measure INDEPENDENCE_LEVEL from solo-day outcomes
3. Today it reads the Avatar's own tracked score

#### E. Delayed Credit for Aide
**Required Changes:**
1. Credit strategies when they appear unprompted later
2. Feed credit into STRATEGY_INTERNALISATION
3. Keep trait model fixed during training (Avatar can't succeed by losing trait)

### 2. Documentation Changes

#### A. README.md Fixes
1. Fix: "Says the live Fusion–Godot connection isn't wired. It is, opt-in." - Update to reflect reality
2. Fix: "Calls UE a 'behavioral oracle.' It isn't one." - Update terminology
3. Fix: "Calls Godot the 'target' runtime. It's authoritative." - Update terminology

#### B. architecture.md Fixes
1. Fix wrong pipeline order (World >> Fusion >> App) -> correct order
2. Fix conceptual diagram (puts world, time and consequences inside Fusion)
3. Fix: "19 pairs instead of 20." -> correct to 20 pairs
4. Remove non-existent "A RRTFoundation that doesn't exist"
5. Fix "No cloud dependencies" without the training exemption
6. Fix unverified "26-dim" claim

#### C. CLAUDE.md Fixes
1. Fix OTOI version references conflict between:
   - CLAUDE.md
   - AGENTS.md  
   - NLT-DEV-OTOI.md
   - nltotoi.json
2. Reconcile to canonical version in .github-private
3. Agents read these files first

#### D. implementation_summary.md
1. Mark as historical (Oct 2025, "remaining 18 pairs")
2. Reconcile pair-status counts (code implements 2 Avatars: StayAlert and TaskKickstart)

#### E. docs/ai-agent-docs/ai-guidance/
1. Remove live GEMINI_TOPOGRAPHY.py (archive copy is identical)
2. Repoint README to real sources of truth

## Implementation Priority

### High Priority (Core Functionality)
1. **TransformersAgentLoopDecision** - Core decision making
2. **Agent Loop Integration** - SessionOrchestrator connection
3. **PairedTrajectoryStep Extension** - Day log enhancement
4. **Solo Days Implementation** - Independent training

### Medium Priority (Documentation)
5. **README.md fixes** - User-facing documentation
6. **architecture.md fixes** - System architecture
7. **CLAUDE.md fixes** - Governance and versioning

### Lower Priority (Refinement)
8. **Delayed credit system** - Strategy effectiveness tracking
9. **Implementation summary** - Historical documentation
10. **AI guidance docs** - Developer documentation

## Technical Requirements

### Model Decision Source
- All 7 verbs: approach, look_at, use, sit, rest, communicate, wait
- Token sampling with seed for training days
- Greedy decoding for evaluation/solo days
- Prompt/token ID recording for debugging
- Avatar context in prompts
- Selectable via environment variable

### Session Orchestration
- Integration between agent loop and SessionOrchestrator
- World engine outcome processing
- Backward compatibility for tests
- Clean separation of concerns

### Day Logging
- Comprehensive tracking of decision process
- Multiple decision source identification
- Solo vs. paired training flags
- Missed turn tracking
- Engine tick integration

### Solo Day Training
- Independent Avatar training without Aide
- Autonomy measurement
- Skill development tracking
- Self-sufficiency assessment

## Files to Modify

### Core Code
- `src/fusion/transformers_agent_decision.py`
- `src/fusion/agent_loop.py`
- `src/fusion/model_fusion.py`
- `src/simulation/session_orchestrator.py`

### Documentation
- `README.md`
- `docs/architecture.md`
- `CLAUDE.md`
- `docs/implementation_summary.md`
- `docs/ai-agent-docs/ai-guidance/README.md`

### Configuration
- `.github-private/` canonical OTOI version
- Various config files for environment variables

## Testing Strategy

### Unit Tests
- Decision source functionality
- Verb selection logic
- Token recording
- Solo day behavior

### Integration Tests
- Agent loop integration
- SessionOrchestrator connection
- Day log validation
- End-to-end scenarios

### Documentation Tests
- Documentation consistency
- Version reconciliation
- Architecture diagram validation

## Risk Mitigation

### Technical Risks
1. **Verb expansion** - Ensure all 7 verbs work correctly
2. **Seed sampling** - Maintain reproducibility
3. **Backward compatibility** - Don't break existing tests
4. **Performance** - Token recording shouldn't impact speed

### Documentation Risks
1. **Version conflicts** - OTOI version reconciliation
2. **Outdated information** - Keep docs current
3. **Inconsistent terminology** - Maintain clear language
4. **Missing references** - Ensure all pointers work

## Timeline

### Phase 1: Core Implementation (Weeks 1-2)
1. TransformersAgentLoopDecision enhancements
2. Agent loop integration
3. Day log extension

### Phase 2: Solo Days (Weeks 3-4)
1. Solo day implementation
2. Independence measurement
3. Trait preservation

### Phase 3: Documentation (Weeks 5-6)
1. README.md fixes
2. Architecture.md fixes
3. CLAUDE.md fixes

### Phase 4: Integration & Testing (Weeks 7-8)
1. End-to-end testing
2. Documentation validation
3. Final review

## Success Criteria

### Technical
- All 7 verbs functional
- Seed sampling works for training
- Solo days measure independence
- Delayed credit system operational
- Documentation accurate and consistent

### Quality
- No regression in existing functionality
- Comprehensive test coverage
- Clean code with proper documentation
- Maintained backward compatibility

### Documentation
- All documentation updates applied
- OTOI version conflicts resolved
- Architecture diagrams corrected
- Developer guidance updated

This plan provides a comprehensive roadmap for implementing all requested changes while maintaining code quality and documentation standards.