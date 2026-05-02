import axios from "axios";

const BASE_URL = import.meta.env.VITE_API_URL ?? "/api";

export const api = axios.create({
  baseURL: BASE_URL,
  headers: { "Content-Type": "application/json" },
});

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
  task_results: TaskResult[];
  coaching_actions: unknown[];
}

export interface TaskResult {
  attempt: number;
  success: boolean;
  quality_score: number;
  struggle_indicators: string[];
  aide_interventions: string[];
  emotional_state: string;
  cognitive_load: number;
  recorded_at: string;
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
  list: () => api.get<Avatar[]>("/avatars/").then((r) => r.data),
  create: (trait_name: string) =>
    api.post<Avatar>("/avatars/", { trait_name }).then((r) => r.data),
  get: (id: string) => api.get<Avatar>(`/avatars/${id}`).then((r) => r.data),
  delete: (id: string) => api.delete(`/avatars/${id}`),
  traits: () =>
    api.get<{ traits: string[] }>("/avatars/traits/list").then((r) => r.data.traits),
};

export const aidesApi = {
  list: () => api.get<Aide[]>("/aides/").then((r) => r.data),
  create: (expertise_area: string) =>
    api.post<Aide>("/aides/", { expertise_area }).then((r) => r.data),
  get: (id: string) => api.get<Aide>(`/aides/${id}`).then((r) => r.data),
  delete: (id: string) => api.delete(`/aides/${id}`),
};

export const sessionsApi = {
  list: (avatar_id?: string) =>
    api
      .get<TrainingSession[]>("/sessions/", { params: { avatar_id } })
      .then((r) => r.data),
  create: (body: {
    avatar_id: string;
    aide_id: string;
    scenario_id: string;
  }) => api.post<TrainingSession>("/sessions/", body).then((r) => r.data),
  get: (id: string) =>
    api.get<TrainingSession>(`/sessions/${id}`).then((r) => r.data),
  complete: (id: string) =>
    api.post<TrainingSession>(`/sessions/${id}/complete`).then((r) => r.data),
};

export const fusionApi = {
  list: () => api.get<FusionReport[]>("/fusion/").then((r) => r.data),
  attempt: (avatar_id: string, aide_id: string) =>
    api.post<FusionReport>("/fusion/", { avatar_id, aide_id }).then((r) => r.data),
  advocates: () =>
    api.get<unknown[]>("/fusion/advocates/").then((r) => r.data),
};

export const scenariosApi = {
  list: (category?: string) =>
    api
      .get<Scenario[]>("/scenarios/", { params: { category } })
      .then((r) => r.data),
  get: (id: string) =>
    api.get<Scenario>(`/scenarios/${id}`).then((r) => r.data),
};
