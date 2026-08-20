"use client";

import { useEffect, useRef, useState } from "react";
import { useParams } from "next/navigation";
import { api } from "../../../lib/api";
import type { SessionResult, ScenarioResult } from "../../../lib/types";

function Metric({ label, value, unit = "" }: { label: string; value: number | string; unit?: string }) {
  return (
    <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-xl p-4">
      <p className="text-xs text-gray-500 uppercase tracking-wide mb-1">{label}</p>
      <p className="text-2xl font-bold text-gray-900 dark:text-white">
        {typeof value === "number" ? `${Math.round(value * 100)}${unit}` : value}
      </p>
    </div>
  );
}

function ScenarioCard({ sr }: { sr: ScenarioResult }) {
  const pct = Math.round(sr.success_rate * 100);
  return (
    <div className="border border-gray-200 dark:border-gray-700 rounded-xl p-4 bg-white dark:bg-gray-900">
      <div className="flex justify-between items-center mb-2">
        <span className="font-medium capitalize">{sr.scenario_type} scenario {sr.scenario_index + 1}</span>
        <span className={`text-xs px-2 py-0.5 rounded-full ${sr.completed ? "bg-green-100 text-green-800" : "bg-yellow-100 text-yellow-800"}`}>
          {sr.completed ? "done" : "incomplete"}
        </span>
      </div>
      <div className="w-full bg-gray-100 dark:bg-gray-800 rounded-full h-2 mb-3">
        <div className="bg-brand-600 h-2 rounded-full transition-all" style={{ width: `${pct}%` }} />
      </div>
      <div className="grid grid-cols-3 gap-2 text-sm text-gray-600 dark:text-gray-400">
        <span>Success: {pct}%</span>
        <span>Attempts: {sr.attempts}</span>
        <span>Coached: {sr.coaching_events}×</span>
      </div>
      {sr.peak_burnout_risk > 0.7 && (
        <p className="text-xs text-red-600 mt-2">⚠ High burnout risk: {Math.round(sr.peak_burnout_risk * 100)}%</p>
      )}
    </div>
  );
}

export default function SessionPage() {
  const id = useParams<{ id: string }>()?.id ?? "";
  const [session, setSession] = useState<SessionResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    api.sessions
      .get(id)
      .then((s) => {
        setSession(s);
        if (s.status === "running" || s.status === "pending") {
          wsRef.current = api.sessions.connectWs(id, setSession);
        }
      })
      .catch((e: Error) => setError(e.message));

    return () => wsRef.current?.close();
  }, [id]);

  if (error) return <p className="text-red-600">Error: {error}</p>;
  if (!session) return <p className="text-gray-500">Loading session…</p>;

  const isLive = session.status === "running" || session.status === "pending";

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="flex items-center gap-4">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
          Session <span className="font-mono text-base text-gray-400">{id.slice(0, 8)}…</span>
        </h1>
        <span className={`px-3 py-1 rounded-full text-sm font-medium ${
          isLive ? "bg-blue-100 text-blue-800 animate-pulse" :
          session.status === "completed" ? "bg-green-100 text-green-800" :
          "bg-red-100 text-red-800"
        }`}>
          {isLive ? "● Live" : session.status}
        </span>
        {session.fusion_ready && (
          <span className="px-3 py-1 rounded-full text-sm font-medium bg-purple-100 text-purple-800">
            ✦ Fusion Ready
          </span>
        )}
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <Metric label="Success Rate" value={session.overall_success_rate} unit="%" />
        <Metric label="Independence" value={session.final_independence_level} unit="%" />
        <Metric label="Peak Burnout" value={session.peak_burnout_risk} unit="%" />
        <Metric label="Duration" value={`${session.duration_seconds.toFixed(1)}s`} />
      </div>

      {session.scenario_results.length > 0 ? (
        <div className="space-y-3">
          <h2 className="font-semibold text-gray-700 dark:text-gray-300">Scenario Results</h2>
          {session.scenario_results.map((sr) => (
            <ScenarioCard key={sr.scenario_index} sr={sr} />
          ))}
        </div>
      ) : (
        isLive && (
          <div className="border border-dashed border-blue-300 rounded-xl p-8 text-center text-blue-600">
            <p className="animate-pulse">Training in progress…</p>
          </div>
        )
      )}

      {session.error && (
        <div className="bg-red-50 border border-red-200 rounded-xl p-4 text-red-700 text-sm">
          <strong>Error:</strong> {session.error}
        </div>
      )}
    </div>
  );
}
