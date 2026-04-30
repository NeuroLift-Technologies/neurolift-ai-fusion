import type { SessionRunRequest, SessionRunResponse } from "./types";

export class SimulationApiClient {
  constructor(private readonly baseUrl: string) {}

  async health(): Promise<Record<string, unknown>> {
    const response = await fetch(`${this.baseUrl}/health`);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return response.json();
  }

  async runSession(payload: SessionRunRequest): Promise<SessionRunResponse> {
    const response = await fetch(`${this.baseUrl}/sessions/run`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return response.json();
  }
}
