import type {
  AideSummary,
  AvatarSummary,
  SessionCreatePayload,
  SessionResult,
  SessionSummary,
} from "./types";

const API_BASE_URL =
  (process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api/v1").replace(/\/$/, "");

const WS_BASE_URL =
  (process.env.NEXT_PUBLIC_WS_BASE_URL ?? API_BASE_URL.replace(/^http/i, "ws")).replace(/\/$/, "");

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {}),
    },
  });

  if (!response.ok) {
    const detail = await response.text();
    throw new Error(detail || `Request failed with status ${response.status}`);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return response.json() as Promise<T>;
}

export const api = {
  avatars: {
    list: () => request<AvatarSummary[]>("/avatars/"),
  },
  aides: {
    list: () => request<AideSummary[]>("/aides/"),
  },
  sessions: {
    list: () => request<SessionSummary[]>("/sessions/"),
    create: (payload: SessionCreatePayload) =>
      request<SessionSummary>("/sessions/", {
        method: "POST",
        body: JSON.stringify(payload),
      }),
    get: (sessionId: string) => request<SessionResult>(`/sessions/${encodeURIComponent(sessionId)}`),
    connectWs: (sessionId: string, onMessage: (session: SessionResult) => void) => {
      const socket = new WebSocket(`${WS_BASE_URL}/sessions/${encodeURIComponent(sessionId)}/ws`);

      socket.onmessage = (event) => {
        const data = JSON.parse(event.data) as SessionResult | { error: string };
        if ("error" in data) {
          return;
        }
        onMessage(data);
      };

      return socket;
    },
  },
};
