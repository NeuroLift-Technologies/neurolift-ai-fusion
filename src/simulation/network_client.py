import json
import logging
import re
import urllib.request
import urllib.error
from typing import Dict, Any, Optional, Tuple

DEFAULT_BASE_URL = "http://localhost:8765"
DEFAULT_OLLAMA_URL = "http://localhost:11434"
DEFAULT_OLLAMA_MODEL = "qwen2.5:1.5b"

# Observation indices (must match llm_policy.py)
FOCUS_IDX = 0
LOAD_IDX = 1
STRESS_IDX = 2
BURNOUT_IDX = 3
INDEPENDENCE_IDX = 4
FUSION_IDX = 5
SUCCESS_IDX = 6

INTERACTION_NAMES = ["Idle", "StartTask", "RequestHelp", "CompleteTask"]

log = logging.getLogger("NLT-Bridge")


class RemoteAgentInterface:
    """
    Asynchronous communication bridge between UE5 and an LLM (Ollama).

    Flow:
      1. perceive()   — GET /api/avatar/state  from UE5 (world state)
      2. decide()     — POST to Ollama /api/generate  → parse movement JSON
      3. submit_intent() — POST /api/avatar/action  to UE5 (execute move)

    The UE5 world engine (port 8765) exposes the HTTP API.
    Ollama (port 11434) serves the LLM.
    """

    def __init__(
        self,
        agent_id: str,
        base_url: str = DEFAULT_BASE_URL,
        ollama_url: str = DEFAULT_OLLAMA_URL,
        ollama_model: str = DEFAULT_OLLAMA_MODEL,
    ):
        self.agent_id = agent_id
        self.base_url = base_url.rstrip("/")
        self.ollama_url = ollama_url.rstrip("/")
        self.ollama_model = ollama_model
        self.last_perception: Dict[str, Any] = {}
        self.is_busy: bool = False
        self._connected: bool = False

    # -- UE5 connection ---------------------------------------------------

    def connect(self) -> bool:
        """Verify the UE5 world engine is reachable via /api/status."""
        try:
            req = urllib.request.Request(f"{self.base_url}/api/status", method="GET")
            with urllib.request.urlopen(req, timeout=5) as resp:
                body = json.loads(resp.read().decode())
            # The UE5 /api/status endpoint reports {"running": true, "pace": 1, ...}
            self._connected = bool(body.get("running"))
            if self._connected:
                log.info("[%s] Connected to UE5 world engine at %s", self.agent_id, self.base_url)
            return self._connected
        except Exception as e:
            log.error("[%s] UE5 connection failed: %s", self.agent_id, e)
            self._connected = False
            return False

    def perceive(self, radius: int = 10) -> Dict[str, Any]:
        """Fetch avatar state from the UE5 world engine (GET /api/avatar/state)."""
        if not self._connected:
            return {}
        try:
            req = urllib.request.Request(f"{self.base_url}/api/avatar/state", method="GET")
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode())
            self.last_perception = data
            return data
        except Exception as e:
            log.error("[%s] Perceive failed: %s", self.agent_id, e)
            return {}

    # -- LLM inference ----------------------------------------------------

    def decide(self) -> Tuple[float, float, float, int]:
        """
        Send the current observation to the LLM and parse the movement command.

        Returns:
            (move_x, move_y, move_z, interact) — the LLM-generated action.
        """
        metrics = self._extract_metrics()
        if not metrics:
            log.warning("[%s] No metrics available for LLM decision", self.agent_id)
            return 0.0, 0.0, 0.0, 0

        prompt = self._format_prompt(metrics)
        response = self._call_ollama(prompt)
        if not response:
            log.warning("[%s] LLM returned empty response", self.agent_id)
            return 0.0, 0.0, 0.0, 0

        move_x, move_y, move_z, interact = self._parse_response(response)
        log.info(
            "[%s] LLM decision: move=(%.2f, %.2f, %.2f) interact=%d | resp=%s",
            self.agent_id, move_x, move_y, move_z, interact, response.strip()[:80],
        )
        return move_x, move_y, move_z, interact

    def _extract_metrics(self) -> Optional[Dict[str, float]]:
        """Extract the cognitive metrics dict from the last perception."""
        if not self.last_perception:
            return None
        metrics = self.last_perception.get("metrics", {})
        if not metrics:
            return None
        return {
            "focus": float(metrics.get("focus", 0.5)),
            "cognitive_load": float(metrics.get("cognitive_load", 0.2)),
            "stress": float(metrics.get("stress", 0.2)),
            "burnout": float(metrics.get("burnout", 0.1)),
            "independence": float(metrics.get("independence", 0.2)),
            "fusion_ready": float(metrics.get("fusion_ready", 0.0)),
            "success_rate": float(metrics.get("success_rate", 0.5)),
        }

    def _format_prompt(self, metrics: Dict[str, float]) -> str:
        """Format the observation as a prompt for the avatar LLM."""
        obs = [
            metrics.get("focus", 0.5),
            metrics.get("cognitive_load", 0.2),
            metrics.get("stress", 0.2),
            metrics.get("burnout", 0.1),
            metrics.get("independence", 0.2),
            metrics.get("fusion_ready", 0.0),
            metrics.get("success_rate", 0.5),
        ]
        return (
            f"Focus:{obs[FOCUS_IDX]:.1f} Stress:{obs[STRESS_IDX]:.1f} "
            f"Burnout:{obs[BURNOUT_IDX]:.1f} Independence:{obs[INDEPENDENCE_IDX]:.1f} "
            f"Success:{obs[SUCCESS_IDX]:.1f}\n\n"
            f"You are an AI controlling a character in Unreal Engine 5. "
            f"The character has the following metrics. Based on these metrics, "
            f"decide how to move and interact. "
            f"Respond ONLY with this exact format on a single line:\n"
            f"MOVE x y z INTERACT i\n\n"
            f"Where x, y, z are floats in [-1, 1] and i is an integer in [0, 3].\n"
            f"Do NOT add any text before or after the MOVE line.\n"
            f"Move [-1..1] x,y,z. Action: 0=Idle,1=Start,2=Help,3=Complete"
        )

    def _call_ollama(self, prompt: str, max_tokens: int = 32) -> str:
        """Call Ollama's /api/generate endpoint and return the response text."""
        payload = {
            "model": self.ollama_model,
            "prompt": prompt,
            "stream": False,
            "options": {"num_predict": max_tokens, "temperature": 0.3, "top_k": 10},
        }
        try:
            body = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                f"{self.ollama_url}/api/generate",
                data=body,
                method="POST",
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                result = json.loads(resp.read().decode())
            return result.get("response", "")
        except Exception as e:
            log.error("[%s] Ollama call failed: %s", self.agent_id, e)
            return ""

    def _parse_response(self, response: str) -> Tuple[float, float, float, int]:
        """Parse the LLM response to extract MOVE and INTERACT values."""
        move_x, move_y, move_z = 0.0, 0.0, 0.0
        interact = 0

        m = re.search(r"MOVE\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)", response)
        if m:
            move_x = float(m.group(1))
            move_y = float(m.group(2))
            move_z = float(m.group(3))
            # Clamp to [-1, 1]
            move_x = max(-1.0, min(1.0, move_x))
            move_y = max(-1.0, min(1.0, move_y))
            move_z = max(-1.0, min(1.0, move_z))

        i = re.search(r"INTERACT\s+(\d+)", response)
        if i:
            interact = int(i.group(1)) % len(INTERACTION_NAMES)

        return move_x, move_y, move_z, interact

    # -- UE5 action -------------------------------------------------------

    def submit_intent(self, intent_type: str, data: Dict[str, Any] = None) -> bool:
        """Send an avatar action to the UE5 world engine (POST /api/avatar/action)."""
        if self.is_busy or not self._connected:
            return False

        payload = self._build_action(intent_type, data or {})
        try:
            body = json.dumps(payload).encode()
            req = urllib.request.Request(
                f"{self.base_url}/api/avatar/action",
                data=body,
                method="POST",
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=5) as resp:
                result = json.loads(resp.read().decode())
            if result.get("ok"):
                self.is_busy = True
                log.info("[%s] Action submitted: %s → %s", self.agent_id, intent_type, result.get("message", ""))
                return True
            else:
                log.warning("[%s] Action rejected: %s", self.agent_id, result)
                return False
        except Exception as e:
            log.error("[%s] Submit intent failed: %s", self.agent_id, e)
            return False

    def release(self) -> None:
        """Mark the avatar as no longer busy."""
        self.is_busy = False

    def _build_action(self, intent_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert an intent into the UE5 action payload."""
        action: Dict[str, Any] = {"avatar_id": self.agent_id}

        if intent_type in ("move", "goto"):
            action["move_x"] = float(data.get("dx", data.get("move_x", 0.0)))
            action["move_y"] = float(data.get("dy", data.get("move_y", 0.0)))
            action["move_z"] = float(data.get("dz", data.get("move_z", 0.0)))
            if "interact" in data:
                action["interact"] = int(data["interact"])
        elif intent_type == "stop":
            action["move_x"] = 0.0
            action["move_y"] = 0.0
            action["move_z"] = 0.0
            action["interact"] = 0
        elif intent_type == "focus":
            action["interact"] = 1
            action["move_x"] = 0.0
            action["move_y"] = 0.0
            action["move_z"] = 0.0
        elif intent_type == "release":
            action["interact"] = 0
            action["move_x"] = 0.0
            action["move_y"] = 0.0
            action["move_z"] = 0.0
        else:
            action["interact"] = 0
            action["move_x"] = 0.0
            action["move_y"] = 0.0
            action["move_z"] = 0.0

        return action

    # -- convenience ------------------------------------------------------

    def step(self) -> bool:
        """
        Full bridge cycle: perceive → decide → submit.
        Returns True if an action was successfully submitted.
        """
        perception = self.perceive()
        if not perception:
            return False
        move_x, move_y, move_z, interact = self.decide()
        action_data = {"move_x": move_x, "move_y": move_y, "move_z": move_z, "interact": interact}
        return self.submit_intent("move", action_data)


def main():
    """Full bridge demo: connect to UE5 + Ollama, perceive, decide, act."""
    agent = RemoteAgentInterface("Agent_0")
    try:
        if not agent.connect():
            print("Failed to connect to UE5 world engine.")
            return

        # Verify Ollama is reachable
        print("LLM bridge active:", agent.ollama_url, "/", agent.ollama_model)

        print("Perceiving world...")
        perception = agent.perceive(radius=10)
        avatar_id = perception.get("avatar_id", "?")
        metrics = perception.get("metrics", {})
        print(f"Avatar {avatar_id} — metrics:", {k: round(v, 2) for k, v in metrics.items()})

        print("LLM deciding...")
        move_x, move_y, move_z, interact = agent.decide()
        print(f"LLM → move=({move_x:.2f}, {move_y:.2f}, {move_z:.2f}) interact={interact}")

        if interact == 0 and move_x == 0.0 and move_y == 0.0 and move_z == 0.0:
            print("LLM chose Idle.")
        else:
            print("Submitting action to UE5...")
            ok = agent.submit_intent("move", {"move_x": move_x, "move_y": move_y, "move_z": move_z, "interact": interact})
            print("Action submitted:", ok)

        agent.release()
        print("Done.")

    except Exception as e:
        print(f"Bridge failed: {e}")


if __name__ == "__main__":
    main()
