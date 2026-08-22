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

## 11. Research Basis — Trajectory Distillation vs. Parameter-Space Merge

*Evidence from `docs/research/Trajectory Distillation for Behavioral AI Fusion.md` (full study, 100+ citations). Summary below is distilled; see that file for full bibliography.*

**Why trajectory, not weights, for the Advocate:** The study classifies “Trajectory Distillation” as an umbrella for techniques that distill *multi-step reasoning processes*, not static outputs — directly applicable to fusing Avatar lived-experience traces with Aide coaching trajectories. Three validated paradigms:

| Paradigm | Mechanism | Training | Key Innovation | Demonstrated Use |
|---|---|---|---|---|
| **Trajectory-aware On-Policy Distillation (TOPD)** | Corrects student’s self-generated trajectories under teacher supervision via Optimal Transport (OT) over short-window continuations | Requires training (modified loss) | Identifies genuine divergence points, injects future-trajectory signal, down-weights “false alarm” tokens; 46.7%→53.3% on AIME25 | DeepSeek-V4, MiMo, Qwen-3 alignment |
| **Training-Free Experience Distillation (TED)** | Extracts generalized experiences (principles, strategies, failure patterns) from teacher evaluation of student trajectories; stores in context, no weight updates | No parameter updates (frozen student) | Compression (merge/rewrite/prune) to prevent unbounded growth; 20× training-cost reduction on MathVision | Edge / black-box API, low-data multimodal |
| **Multi-Agent Dynamics Distillation (AgentArk/PAD)** | Step-level RL via Process Reward Model (PRM) + GRPO on corrective patterns from multi-agent debates | Significant offline cost (e.g., 20h on 8×H100 for 7B) | Model-agnostic reasoning patterns (text→MLLM transfer), improved generalization | Single agent from team of specialists |

*Takeaway:* All three are technically viable and **behavior-first** — they teach the *how* of reasoning, not just the *what*.

**Parameter-space merge — high-risk aggregation:**

| Technique | Core Principle | Strengths | Weaknesses |
|---|---|---|---|
| Model Soups | Linear weight averaging of same-arch fine-tunes | Simple, improves generalization on related tasks | Fails if not in connected low-loss region |
| Task Arithmetic | Algebra on task vectors (fine-tune − base) | Only method that consistently gains in large systematic eval | No explicit interference handling |
| TIES-Merging | Trim + elect sign + disjoint merge | Designed for many-model scaling | Catastrophic degradation on heterogeneous checkpoints (0% success as N grows) |
| Subspace Boosting | Low-rank compression of task vectors | Seeks coherent directions | Steady accuracy decline as more models merged |
| SLERP/NuSLERP | Spherical interpolation on weight manifold | More stable than linear | Expensive angle computation, arch-incompatible |
| AlignMerge | Fisher-metric, geometry-constrained merge preserving alignment as invariant (AQI penalty) | Preserves safety/helpfulness while matching best expert on utility; multimodal via joint Fisher | Complex, requires aligned base |
| Passthrough Merge | Dynamic routing, no weight fusion | Avoids interference (Goliath-120B) | Latency, no single efficient model |

*Current evidence:* naive merging of heterogeneous LLMs frequently violates its own assumptions (mode connectivity, task orthogonality, sparsity) and causes catastrophic forgetting. AlignMerge is the only merging method that explicitly preserves alignment and is multimodal-capable — relevant if we later merge vision/audio encoders.

**Comparative lens for Advocate fusion:**

| Aspect | Trajectory Distillation | Parameter-Space Merge |
|---|---|---|
| Primary goal | Behavioral refinement — coherence, logic, empathy over multi-turn trajectories | Capability aggregation — broad skill set in one chassis |
| Ideal use | Multi-step coaching, empathetic tone maintenance, cross-modal reasoning alignment (X-OPD: 11.29%→0.97% drop on BIG Bench Audio) | Combining complementary specialists (e.g., factual + sentiment + creative) |
| Conflict handling | Corrects divergent paths via OT / PRM | Prone to destructive interference without Fisher/OT |
| Suitability for empathy | Excellent (process-level) | Poor unless alignment-preserving |

**Spec decision reaffirmed:** **Trajectory Distillation primary (4.1), router as TED-style teacher (4.3), parameter merge as AlignMerge-tracked ablation (4.2).** The study’s recommended *hybrid two-stage* — **AlignMerge (breadth) → TOPD/X-OPD (depth)** — is adopted as the *future* track when Avatar/Aide diverge to distinct backbones or modalities (e.g., VLM + LLM with 60/40 VLM-dominant selective attention merging). A future `TOPDTeacher` can add OT divergence detection to our `RouterTeacher` to suppress false-alarm tokens.

Implementation note: our `RouterTeacher` today is a *TED* teacher (frozen parents, experience in `PairedTrajectoryStep.gold_weight`); a follow-up `TOPDTeacher` would add Optimal Transport short-window comparison.

## 12. References

* `docs/architecture.md` — Source-verified runtime contracts, fusion and Advocate contracts
* `docs/research/Trajectory Distillation for Behavioral AI Fusion.md` — Full feasibility study (TOPD, TED, AgentArk/PAD vs. Model Soups/TIES/AlignMerge; 100+ refs)
* `NLT-DEV-OTOI.md` — Authority and guardrails
* Prior finding: `nlt-fusion` (infra repo) is **not** the Avatar/Aide/Advocate stack — this spec applies to `neurolift-ai-fusion` / `neurolift-ai-fusion-org`
