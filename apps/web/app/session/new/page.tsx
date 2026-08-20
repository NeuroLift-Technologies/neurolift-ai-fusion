"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { api } from "../../../lib/api";
import type { AvatarSummary, AideSummary, AvatarType, AideType } from "../../../lib/types";

export default function NewSessionPage() {
  const router = useRouter();
  const [avatars, setAvatars] = useState<AvatarSummary[]>([]);
  const [aides, setAides] = useState<AideSummary[]>([]);
  const [selectedAvatar, setSelectedAvatar] = useState<AvatarType>("stay_alert");
  const [selectedAide, setSelectedAide] = useState<AideType>("stay_alert_aide");
  const [difficulty, setDifficulty] = useState(0.5);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([api.avatars.list(), api.aides.list()]).then(([a, ai]) => {
      setAvatars(a);
      setAides(ai);
    });
  }, []);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setSubmitting(true);
    setError(null);
    try {
      const session = await api.sessions.create({
        avatar_type: selectedAvatar,
        aide_type: selectedAide,
        scenarios: [
          { type: "workplace", difficulty, description: "Workplace productivity task" },
          { type: "personal", difficulty: difficulty * 0.8, description: "Personal organisation task" },
        ],
      });
      router.push(`/session/${session.session_id}`);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Unknown error");
      setSubmitting(false);
    }
  }

  return (
    <div className="max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">New Training Session</h1>

      <form onSubmit={handleSubmit} className="space-y-6">
        <fieldset>
          <legend className="font-semibold text-gray-700 dark:text-gray-300 mb-3">Select Avatar</legend>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {avatars.map((a) => (
              <label
                key={a.id}
                className={`border rounded-xl p-4 cursor-pointer transition-all ${
                  selectedAvatar === a.type
                    ? "border-brand-600 bg-brand-50 dark:bg-brand-900/20"
                    : "border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900"
                }`}
              >
                <input
                  type="radio"
                  name="avatar"
                  value={a.type}
                  checked={selectedAvatar === a.type}
                  onChange={() => setSelectedAvatar(a.type)}
                  className="sr-only"
                />
                <p className="font-medium text-gray-900 dark:text-white">{a.display_name}</p>
                <p className="text-sm text-gray-500 mt-1">{a.description}</p>
                <div className="flex flex-wrap gap-1 mt-2">
                  {a.traits.map((t) => (
                    <span key={t} className="text-xs bg-gray-100 dark:bg-gray-800 px-2 py-0.5 rounded">
                      {t.replace(/_/g, " ")}
                    </span>
                  ))}
                </div>
              </label>
            ))}
          </div>
        </fieldset>

        <fieldset>
          <legend className="font-semibold text-gray-700 dark:text-gray-300 mb-3">Select Aide</legend>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {aides.map((a) => (
              <label
                key={a.id}
                className={`border rounded-xl p-4 cursor-pointer transition-all ${
                  selectedAide === a.type
                    ? "border-brand-600 bg-brand-50 dark:bg-brand-900/20"
                    : "border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900"
                }`}
              >
                <input
                  type="radio"
                  name="aide"
                  value={a.type}
                  checked={selectedAide === a.type}
                  onChange={() => setSelectedAide(a.type)}
                  className="sr-only"
                />
                <p className="font-medium text-gray-900 dark:text-white">{a.display_name}</p>
                <p className="text-sm text-gray-500 mt-1">{a.description}</p>
              </label>
            ))}
          </div>
        </fieldset>

        <div>
          <label className="block font-semibold text-gray-700 dark:text-gray-300 mb-2">
            Difficulty: <span className="text-brand-600">{Math.round(difficulty * 100)}%</span>
          </label>
          <input
            type="range"
            min="0.1"
            max="1.0"
            step="0.05"
            value={difficulty}
            onChange={(e) => setDifficulty(parseFloat(e.target.value))}
            className="w-full accent-brand-600"
          />
          <div className="flex justify-between text-xs text-gray-400 mt-1">
            <span>Easy</span><span>Hard</span>
          </div>
        </div>

        {error && <p className="text-sm text-red-600 bg-red-50 p-3 rounded-lg">{error}</p>}

        <button
          type="submit"
          disabled={submitting}
          className="w-full py-3 bg-brand-600 text-white rounded-lg font-medium hover:bg-brand-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {submitting ? "Starting session…" : "Start Session"}
        </button>
      </form>
    </div>
  );
}
