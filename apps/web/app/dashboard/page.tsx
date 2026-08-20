"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { api } from "../../lib/api";
import type { SessionSummary } from "../../lib/types";

const statusColors: Record<string, string> = {
  pending: "bg-yellow-100 text-yellow-800",
  running: "bg-blue-100 text-blue-800",
  completed: "bg-green-100 text-green-800",
  failed: "bg-red-100 text-red-800",
  aborted: "bg-gray-100 text-gray-800",
};

export default function DashboardPage() {
  const [sessions, setSessions] = useState<SessionSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api.sessions
      .list()
      .then(setSessions)
      .catch((e: Error) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Dashboard</h1>
        <Link
          href="/session/new"
          className="px-4 py-2 bg-brand-600 text-white rounded-lg text-sm font-medium hover:bg-brand-700 transition-colors"
        >
          + New Session
        </Link>
      </div>

      {loading && <p className="text-gray-500">Loading sessions...</p>}
      {error && <p className="text-red-600">Error: {error}</p>}

      {!loading && !error && sessions.length === 0 && (
        <div className="text-center py-16 border border-dashed border-gray-300 dark:border-gray-700 rounded-xl">
          <p className="text-gray-500 mb-4">No training sessions yet.</p>
          <Link href="/session/new" className="text-brand-600 hover:underline font-medium">
            Start your first session →
          </Link>
        </div>
      )}

      {sessions.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {sessions.map((s) => (
            <Link
              key={s.session_id}
              href={`/session/${s.session_id}`}
              className="border border-gray-200 dark:border-gray-700 rounded-xl p-5 bg-white dark:bg-gray-900 hover:shadow-md transition-shadow"
            >
              <div className="flex items-start justify-between mb-3">
                <span className="text-sm font-mono text-gray-500 truncate max-w-[60%]">
                  {s.session_id.slice(0, 8)}…
                </span>
                <span className={`text-xs px-2 py-1 rounded-full font-medium ${statusColors[s.status] ?? "bg-gray-100 text-gray-800"}`}>
                  {s.status}
                </span>
              </div>
              <p className="font-medium text-gray-900 dark:text-white capitalize">
                {s.avatar_type.replace(/_/g, " ")}
              </p>
              <p className="text-sm text-gray-500 capitalize">
                {s.aide_type.replace(/_/g, " ")}
              </p>
              <p className="text-xs text-gray-400 mt-3">
                {new Date(s.created_at).toLocaleString()}
              </p>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
