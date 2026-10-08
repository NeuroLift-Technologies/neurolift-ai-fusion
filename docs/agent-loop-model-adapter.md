# Local model decision adapter

`src.fusion.TransformersAgentLoopDecision` is an optional, local Hugging Face Transformers
decision source for `FusionAgentLoop`. It loads a causal language model once from a local directory,
then converts each validated physical observation into a semantic `approach` or `wait` intent. The
adapter does not download model files, return physical coordinates, or mutate engine state. Its
synchronous inference must run in a Fusion worker/service context, not a real-time simulation tick.

## HTTP endpoint

`src.fusion.agent_loop_http` exposes the Fusion decision seam to Godot over loopback HTTP. From the
repository root, run:

```powershell
python -m src.fusion.agent_loop_http
```

The endpoint listens on `127.0.0.1:8001`; its route is `POST /agent-loop/perception`. Set
`FUSION_AGENT_LOOP_PORT` to change the local port. Set `FUSION_GGUF_MODEL` to a local GGUF path to
select llama.cpp inference; otherwise the endpoint uses a deterministic, model-free control
decision. Perceptions and returned intents are validated, each avatar is limited to one
in-flight decision, and synchronous inference runs outside the ASGI event loop. Invalid, stale, or
unavailable decisions return a non-success response with no intent. ASFDK governance, live-world
revalidation, and physical execution remain Godot responsibilities.

## Transformers/Safetensors path

`src.fusion.TransformersAgentLoopDecision` remains available as a separate optional path. The
official Qwen3-0.6B Safetensors checkpoint can be downloaded outside the repository, for example
to `C:\Users\<user>\Local_models\Qwen3-0.6B-Safetensors`:

```powershell
hf download Qwen/Qwen3-0.6B --local-dir "C:\Users\<user>\Local_models\Qwen3-0.6B-Safetensors"
```

In an isolated Python environment, install the optional runtime and test runner with
`python -m pip install -r requirements-ai.txt pytest`. Transformers 4.51.0 or newer is required for
Qwen3. Set `NLT_AGENT_LOOP_MODEL_PATH` to the local directory and run:

```powershell
$env:NLT_AGENT_LOOP_MODEL_PATH = "C:\Users\<user>\Local_models\Qwen3-0.6B-Safetensors"
python -m pytest tests/test_fusion/test_transformers_agent_decision.py -q
```

Fusion code can compose the adapter with the existing protocol seam:

```python
decision = TransformersAgentLoopDecision(model_path)
agent_loop = FusionAgentLoop(decide=decision)
intent = agent_loop.handle_observation(perception)
```

## GGUF/llama.cpp path

`src.fusion.LlamaCppAgentLoopDecision` is an independent CPU GGUF adapter; it does not replace or
modify the Transformers path. Its optional runtime is listed separately in `requirements-gguf.txt`.
The first-run model is Qwen3-0.6B-Q8_0 GGUF (about 640 MB), stored outside Git. Given the existing
file at `C:\Users\<user>\Downloads\Qwen3-0.6B-Q8_0.gguf`, create an isolated environment and
install the CPU runtime:

```powershell
py -3.11 -m venv "C:\Users\<user>\Local_models\fusion-gguf-env"
& "C:\Users\<user>\Local_models\fusion-gguf-env\Scripts\python.exe" -m pip install -r requirements-gguf.txt pytest
```

On Windows, if pip cannot find a compatible prebuilt CPU wheel, install from the llama-cpp-python
CPU wheel index or use the project's documented CMake/Visual Studio build instructions. Set the
GGUF path and run both the mocked contract tests and the opt-in local smoke test:

```powershell
$env:NLT_AGENT_LOOP_GGUF_PATH = "C:\Users\<user>\Downloads\Qwen3-0.6B-Q8_0.gguf"
& "C:\Users\<user>\Local_models\fusion-gguf-env\Scripts\python.exe" -m pytest tests/test_fusion/test_gguf_agent_decision.py -q
```

The GGUF adapter defaults to a 2048-token context, two CPU threads, and no GPU layers to keep the
first run bounded. It constrains model output to `wait` or `approach` with a visible entity that
advertises the `approach` affordance, then validates the result against the perception. Its
real-model test is marked `slow` and skipped unless the environment variable is set. The other
tests use a fake llama.cpp object and require neither the native runtime nor the model file. Both
model paths reject malformed output, unsupported verbs, and ungrounded targets; neither silently
substitutes a fallback intent.

Both model adapters validate Fusion's message contract and target grounding against the supplied
observation. Neither performs ASFDK governance, current-world revalidation, or physical execution.
