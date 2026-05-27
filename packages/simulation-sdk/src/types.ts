export type ScenarioInput = {
  name: string;
  task_type?: string;
  base_success_rate?: number;
  cognitive_demand?: number;
};

export type SessionRunRequest = {
  avatar_id?: string;
  aide_id?: string;
  scenarios: ScenarioInput[];
};

export type SessionRunResponse = {
  session_id: string;
  avatar_id: string;
  aide_id: string;
  total_attempts: number;
  total_successes: number;
  total_coaching: number;
  success_rate: number;
  final_independence: number;
  fusion_ready: boolean;
  scenarios: Array<Record<string, unknown>>;
};
