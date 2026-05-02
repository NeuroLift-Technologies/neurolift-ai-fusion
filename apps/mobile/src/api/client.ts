/**
 * NeuroLift AI-Fusion — Mobile API Client
 * Mirrors the web app API client for React Native.
 */

const BASE_URL = process.env.EXPO_PUBLIC_API_URL ?? "http://localhost:8000/api";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`API ${res.status}: ${text}`);
  }
  return res.json() as Promise<T>;
}

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

export interface Avatar {
  avatar_id: string;
  trait_name: string;
  trait_config: Record<string, unknown>;
  current_state: string;
  emotional_state: string;
  cognitive_load: number;
  stress_level: number;
  burnout_risk_level: number;
  total_tasks_attempted: number;
  total_tasks_completed: number;
  total_coaching_sessions: number;
}

export interface Aide {
  aide_id: string;
  expertise_area: string;
  expertise_config: Record<string, unknown>;
  total_interventions: number;
  successful_interventions: number;
  crisis_interventions: number;
  independence_achievements: number;
}

export interface TrainingSession {
  session_id: string;
  avatar_id: string;
  aide_id: string;
  scenario_id: string;
  session_type: string;
  status: string;
  started_at: string;
  ended_at: string | null;
  task_results: unknown[];
  coaching_actions: unknown[];
}

export interface FusionReport {
  fusion_id: string;
  avatar_id: string;
  aide_id: string;
  success: boolean;
  advocate_id: string | null;
  readiness_score: number;
  failure_reason: string | null;
  timestamp: string;
}

export interface Scenario {
  scenario_id: string;
  name: string;
  category: string;
  task_type: string;
  complexity: string;
  aversiveness: number;
  requires_sustained_focus: boolean;
  cognitive_demand: number;
  base_success_rate: number;
  description: string;
}

// ---------------------------------------------------------------------------
// API helpers
// ---------------------------------------------------------------------------

export const avatarsApi = {
  list: () => request<Avatar[]>("/avatars/"),
  create: (trait_name: string) =>
    request<Avatar>("/avatars/", {
      method: "POST",
      body: JSON.stringify({ trait_name }),
    }),
  traits: () =>
    request<{ traits: string[] }>("/avatars/traits/list").then((r) => r.traits),
  delete: (id: string) =>
    request<void>(`/avatars/${id}`, { method: "DELETE" }),
};

export const aidesApi = {
  list: () => request<Aide[]>("/aides/"),
  create: (expertise_area: string) =>
    request<Aide>("/aides/", {
      method: "POST",
      body: JSON.stringify({ expertise_area }),
    }),
  delete: (id: string) =>
    request<void>(`/aides/${id}`, { method: "DELETE" }),
};

export const sessionsApi = {
  list: (avatar_id?: string) => {
    const q = avatar_id ? `?avatar_id=${avatar_id}` : "";
    return request<TrainingSession[]>(`/sessions/${q}`);
  },
  create: (body: { avatar_id: string; aide_id: string; scenario_id: string }) =>
    request<TrainingSession>("/sessions/", {
      method: "POST",
      body: JSON.stringify(body),
    }),
  complete: (id: string) =>
    request<TrainingSession>(`/sessions/${id}/complete`, { method: "POST" }),
};

export const fusionApi = {
  list: () => request<FusionReport[]>("/fusion/"),
  attempt: (avatar_id: string, aide_id: string) =>
    request<FusionReport>("/fusion/", {
      method: "POST",
      body: JSON.stringify({ avatar_id, aide_id }),
    }),
  advocates: () => request<unknown[]>("/fusion/advocates/"),
};

export const scenariosApi = {
  list: (category?: string) => {
    const q = category ? `?category=${category}` : "";
    return request<Scenario[]>(`/scenarios/${q}`);
  },
};
