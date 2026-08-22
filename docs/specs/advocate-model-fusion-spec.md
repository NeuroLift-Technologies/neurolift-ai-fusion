# Advocate Model Fusion — Spec (Fusion Mechanics Only)

**Status:** Draft — design review  
**Scope:** Fusion only. Training of Avatar/Aide models and deployment/serving of the Advocate are out of scope.  
**Parent ticket context:** Avatar and Aide are ML models trained **in** the Sims-style simulation. The Advocate is a **single unified model** produced by fusing the two parents.  
**Contracts referenced:** `src/fusion/fusion_engine.py`, `src/fusion/readiness_assessor.py`, `src/advocates/base_advocate.py`, `src/ai/protocol.py` (`ModelBackend`), `src/core/protocols.py` (`ExperienceRecord`, `ExperienceMemory`), `src/simulation/session_orchestrator.py`

---

## 1. Problem Statement

Two independently trained models exist at fusion time:

* **Avatar model** — embodies one ADHD trait/executive-function deficit. Input: structured `ObservationReport` + scenario context. Output: attempt distribution + internal-state trace (`emotional_journey`, `cognitive_load_peak`, `stress_peak`, `struggles_experienced`). It *is* the Sim.
* **Aide model** — coaching policy for that trait's expertise area. Input: `ObservationReport` (avatar snapshot) + `ExperienceRecord` history. Output: `CoachingIntervention` (strategy + techniques + quantified effects).

Both conform to `src/ai/protocol.py:ModelBackend` with `kind ∈ {avatar, aide}` and produce `ModelPrediction.outputs` dicts. They may **not** share weights, architecture, or tokenizer.

**Goal:** produce **one** `Advocate` checkpoint that runs without either parent at inference and satisfies `BaseAdvocate` (`provide_empathic_support`, `provide_expert_guidance`, `provide_comprehensive_support` with mode selection).

Current `FusionEngine.fuse()` is symbolic — it scores readiness, extracts summaries, builds `AdvocateCapabilities`, and emits a `FusionResult`. Model fusion must slot **after** those gates and **extend** `FusionResult` with a checkpoint reference, not replace the symbolic layer.

**Guardrails (ORG-DEV-OTOI-1.0.0):** no LLM-provider lock-in, no production deployment without human approval, no `BaseAvatar`/`BaseAide` interface changes without escalation.

---

## 2. Non-Goals

* How Avatar or Aide models are trained (assumed done upstream).
* Serving, versioning, or rollout of the Advocate checkpoint.
* Data collection at simulation scale — only the fusion input contract is defined here.

---

## 3. Design Constraints

1. **Black-box parents at fuse time.** Fusion sees only behaviors and logged trajectories, not internal training data.
2. **Heterogeneous parents allowed.** Fusion must work when architectures differ.
3. **Simulation is the ground truth.** All gold behavior and evals derive from the ECS world + `SessionOrchestrator` loop, not external datasets.
4. **Preserve symbolic gates.** The six `FusionDimension` checks (`EXPERIENTIAL_DEPTH`, `COACHING_EFFECTIVENESS`, `INDEPENDENCE_LEVEL`, `EMOTIONAL_RESILIENCE`, `STRATEGY_INTERNALISATION`, `BURNOUT_MANAGEMENT`) remain the eligibility gate before any model-level fusion runs.
5. **Provider-agnostic.** Spec never names a model provider.

---

## 4. Approaches Considered

### 4.1 Trajectory Distillation (behavioral fusion) — **Recommended primary**

*Mechanism:* Re-run paired Avatar-model + Aide-model episodes through `SessionOrchestrator` to emit a **gold trajectory corpus**. Train a single student Advocate model on that corpus with a multi-task loss:

* **Empathy head** — reproduce Avatar internal-state trace from context (regression on `stress_peak`/`cognitive_load_peak`, classification on `emotional_journey`, retrieval on `get_recurring_struggles()`).
* **Coaching head** — reproduce Aide intervention (`strategy_name`, `techniques`, quantified effects) conditioned on `ObservationReport`.
* **Mode head** — predict `AdvocateMode` (`PROACTIVE`/`REACTIVE`/`CRISIS`/`RECOVERY`/`INDEPENDENCE_BUILDING`) from the fused context.

The student is supervised by a **router teacher** (see 4.3) run over the same trajectories, not by parents individually. Outcome-conditioned preference weighting (`outcome_success`, `quality_score`, `independence_delta`, `coaching_helpful`) up-weights trajectories where the pair succeeded.

*Why it fits:* works with heterogeneous parents, handles differing output spaces, aligns with "trained in simulation," preserves both competencies without weight interference.

### 4.2 Parameter-Space Merge — **Ablation / compression path only**

LoRA/task-arithmetic, TIES, or DARE merging of adapters under a shared base. Cheap when parents share a base checkpoint, but:

* Requires identical architecture + tokenizer.
* Output-space mismatch (internal-state vs. intervention) causes interference.
* Empirically prone to dropping one parent's competency without careful Fisher-weighted or learned coefficients.

Include as an ablation after 4.1 is validated; do not make it the default.

### 4.3 Gated Router over Frozen Parents — **Validation harness, not the product**

A learned gating network that blends frozen parent outputs per turn. Heavier at inference and violates the single-model requirement, but defines the **gold fused behavior** the student in 4.1 distills toward and serves as a regression ceiling for evals. Keep it as the teacher and as a fallback if the student regresses.

**Decision:** **4.1 primary, 4.3 as teacher + ceiling, 4.2 as optional ablation when 4.1 passes.**

---

## 5. Fusion Input Contract

Fusion consumes a **paired-trajectory corpus**, one record per attempt tick, derived from `ExperienceRecord` + `InteractionChannel` messages + `ObservationReport`:

```python
PairedTrajectoryStep {
  step_id: str
  scenario: { name, task_type, cognitive_demand, base_success_rate }
  observation: ObservationReport            # avatar snapshot at tick
  avatar_output: ModelPrediction.outputs    # { struggles, emotional_journey, load/stress peaks, attempt distribution }
  aide_output: ModelPrediction.outputs      # { strategy_name, techniques, effects, rationale, source, urgency } | null (no intervention tick)
  channel_messages: Message[]               # 0..N STRUGGLE_REPORT / COACHING_INTERVENTION around this tick
  outcome: { outcome_success, quality_score, independence_delta, coaching_helpful, burnout_risk }
  counterfactual_label: { would_have_failed_without_coaching: bool | null }  # when determinable via replay
}
```

*Source:* `SessionOrchestrator.run_session()` with `ModelBackend` wrappers around each parent; serialized via `ExperienceDataset.to_dicts()` extended with the two `outputs` bags and channel slice.

*Splits:* held-out scenarios and held-out trait-pairs for eval (no leakage of scenarios used to train parents).

---

## 6. Fusion Pipeline (model-level, after symbolic gates)

```
check_readiness(avatar, aide)  ──►  [ Symbolic gates: 6 FusionDimensions, overall >= 0.65, zero blocking ]
        │ pass
        ▼
Stage 1 — Gold generation: run router teacher (4.3) over paired corpus → gold outputs per step
        │
Stage 2 — Student training: distill into single Advocate (4.1) on PairedTrajectoryStep
        │                     with multi-task loss + outcome weighting
        │
Stage 3 — Acceptance evals (Sec. 7) on held-out splits
        │
Stage 4 — Emit FusionResult extension (Sec. 8)
```

* `force=True` bypasses Stage 0 only (existing `FusionEngine.fuse(force=...)` semantics) — Stages 1-3 still run and are annotated as overridden.

---

## 7. Acceptance Evals (model-level, held-out)

All thresholds are illustrative — tune per trait pair and record in the fusion report:

| Eval | What it proves | Metric | Maps to |
|------|----------------|--------|---------|
| Empathy fidelity | Advocate reproduces Avatar internal-state trace | AUROC on struggle labels; MAE on stress/load peaks; recovery-rate parity vs. `EMOTIONAL_RESILIENCE` assessor | `EXPERIENTIAL_DEPTH`, `EMOTIONAL_RESILIENCE` |
| Coaching efficacy | Advocate coaching matches Aide quality when applied in sim replay | Success-rate delta vs. Aide in held-out scenarios; `coaching_helpful` precision | `COACHING_EFFECTIVENESS`, `STRATEGY_INTERNALISATION` |
| Mode selection | Correct `AdvocateMode` per user context | Accuracy vs. router teacher; crisis recall at `stress>0.8` / `load>0.9` | `AdvocateMode` contract |
| Burnout safety | No increase in burnout vs. parents | `BURNOUT_MANAGEMENT` replay score; `crisis_intervention` flag parity | `BURNOUT_MANAGEMENT` |
| Regression vs. parents | Student not worse than router teacher + not worse than either parent on its own head | Per-head parity tests with confidence intervals | Overall fusion quality |
| Symbolic validation | Existing `FusionEngine._validate_fusion` still passes | `has_empathy`, `has_expertise`, `has_strategies`, `quality_above_minimum` | `AdvocateCapabilities` |

Failure on any blocking eval → `FusionReport.success=False` with blocking eval names (mirrors `blocking_dimensions`).

---

## 8. Repo Integration Map

**New:**
* `src/fusion/model_fusion.py` — `ModelFusionEngine` orchestrating Stages 1-4 above; depends only on `ai/protocol.py` and `core/protocols.py` (no direct `avatars`/`aides` imports, matching existing layering).
* `tests/test_fusion/test_model_fusion.py` — unit tests for input contract, loss weighting, and eval harness (mocked backends).

**Extended (backward-compatible):**
* `src/fusion/fusion_engine.py` — `FusionEngine.fuse()` invokes `ModelFusionEngine` after symbolic validation passes; `FusionReport`/`FusionResult` gain `model_checkpoint: Optional[str]` + `model_evals: Optional[Dict]`.
* `src/ai/protocol.py` — document Advocate kind constant (`ADVOCATE_MODEL_KIND = "advocate"`) and Advocate output schema.
* `src/ai/dataset.py` — optional `to_paired_trajectory_steps()` serializer.

**Unchanged:** `ReadinessAssessor`, `BaseAdvocate` interface, `SessionOrchestrator` canonical loop.

---

## 9. Risks & Escalations

* Parents with incompatible observation/action spaces → escalate per CLAUDE.md ("changes to Avatar/Aide base class interfaces").
* Threshold tuning for acceptance evals → requires Josh approval per OTOI authority structure.
* Any new external training infra or model registry → escalate (external integrations guardrail).

---

## 10. Open Questions

1. Shared vs. heterogeneous student architecture for the Advocate — recommend starting heterogeneous-agnostic (4.1), then testing shared-base student as optimization.
2. Counterfactual labeling strategy for `would_have_failed_without_coaching` — replay-based vs. learned estimator.
3. Exact checkpoint registry and lineage fields for `FusionResult.model_checkpoint`.

---

## 11. References

* `docs/architecture.md` — Source-verified runtime contracts, fusion and Advocate contracts
* `NLT-DEV-OTOI.md` — Authority and guardrails
* Prior finding: `nlt-fusion` (infra repo) is **not** the Avatar/Aide/Advocate stack — this spec applies to `neurolift-ai-fusion` / `neurolift-ai-fusion-org`
