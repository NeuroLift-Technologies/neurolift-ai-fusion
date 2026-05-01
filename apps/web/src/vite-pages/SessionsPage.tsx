import { useEffect, useState } from "react";
import { sessionsApi, avatarsApi, aidesApi, type TrainingSession, type Avatar, type Aide } from "../api/client";

const STATUS_COLORS: Record<string, string> = {
  active: "#48cfad",
  completed: "#6c63ff",
  failed: "#fc5c65",
};

export default function SessionsPage() {
  const [sessions, setSessions] = useState<TrainingSession[]>([]);
  const [avatars, setAvatars] = useState<Avatar[]>([]);
  const [aides, setAides] = useState<Aide[]>([]);
  const [form, setForm] = useState({ avatar_id: "", aide_id: "", scenario_id: "workplace_email_overload" });
  const [loading, setLoading] = useState(true);
  const [creating, setCreating] = useState(false);

  const load = () => {
    setLoading(true);
    Promise.all([sessionsApi.list(), avatarsApi.list(), aidesApi.list()])
      .then(([s, a, ai]) => {
        setSessions(s);
        setAvatars(a);
        setAides(ai);
        if (a.length) setForm((f) => ({ ...f, avatar_id: a[0].avatar_id }));
        if (ai.length) setForm((f) => ({ ...f, aide_id: ai[0].aide_id }));
      })
      .finally(() => setLoading(false));
  };

  useEffect(load, []);

  const handleCreate = async () => {
    if (!form.avatar_id || !form.aide_id) return;
    setCreating(true);
    try {
      const s = await sessionsApi.create(form);
      setSessions((prev) => [...prev, s]);
    } finally {
      setCreating(false);
    }
  };

  const handleComplete = async (id: string) => {
    const s = await sessionsApi.complete(id);
    setSessions((prev) => prev.map((x) => (x.session_id === id ? s : x)));
  };

  return (
    <div className="max-w-5xl mx-auto">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-3xl font-bold mb-1">Training Sessions</h1>
          <p className="text-[#8888aa]">Start and monitor Avatar training sessions.</p>
        </div>
      </div>

      {/* New session form */}
      <div className="bg-[#1a1a2e] border border-[#2e2e4e] rounded-xl p-5 mb-6">
        <h2 className="font-semibold mb-4">Start New Session</h2>
        <div className="flex flex-wrap gap-3 items-end">
          <div>
            <label className="block text-xs text-[#8888aa] mb-1">Avatar</label>
            <select
              className="bg-[#0f0f1a] border border-[#2e2e4e] rounded-lg px-3 py-2 text-sm text-[#e8e8f0]"
              value={form.avatar_id}
              onChange={(e) => setForm((f) => ({ ...f, avatar_id: e.target.value }))}
            >
              {avatars.map((a) => (
                <option key={a.avatar_id} value={a.avatar_id}>
                  {a.trait_name.replace(/_/g, " ")} ({a.avatar_id.slice(0, 6)})
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-xs text-[#8888aa] mb-1">Aide</label>
            <select
              className="bg-[#0f0f1a] border border-[#2e2e4e] rounded-lg px-3 py-2 text-sm text-[#e8e8f0]"
              value={form.aide_id}
              onChange={(e) => setForm((f) => ({ ...f, aide_id: e.target.value }))}
            >
              {aides.map((a) => (
                <option key={a.aide_id} value={a.aide_id}>
                  {a.expertise_area} ({a.aide_id.slice(0, 6)})
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-xs text-[#8888aa] mb-1">Scenario</label>
            <input
              className="bg-[#0f0f1a] border border-[#2e2e4e] rounded-lg px-3 py-2 text-sm text-[#e8e8f0] w-56"
              value={form.scenario_id}
              onChange={(e) => setForm((f) => ({ ...f, scenario_id: e.target.value }))}
            />
          </div>
          <button
            onClick={handleCreate}
            disabled={creating || !form.avatar_id || !form.aide_id}
            className="bg-[#6c63ff] hover:bg-[#5a52e0] text-white px-4 py-2 rounded-lg text-sm font-semibold transition-colors disabled:opacity-50"
          >
            {creating ? "Starting…" : "Start Session"}
          </button>
        </div>
      </div>

      {loading ? (
        <p className="text-[#8888aa]">Loading…</p>
      ) : sessions.length === 0 ? (
        <div className="bg-[#1a1a2e] border border-[#2e2e4e] rounded-xl p-10 text-center text-[#8888aa]">
          No sessions yet. Start one above.
        </div>
      ) : (
        <div className="flex flex-col gap-3">
          {sessions.map((s) => (
            <div key={s.session_id} className="bg-[#1a1a2e] border border-[#2e2e4e] rounded-xl p-5">
              <div className="flex items-center justify-between mb-2">
                <div className="font-mono text-sm text-[#8888aa]">{s.session_id.slice(0, 12)}…</div>
                <div className="flex items-center gap-3">
                  <span
                    className="text-xs font-semibold px-2 py-0.5 rounded-full"
                    style={{ background: `${STATUS_COLORS[s.status] ?? "#8888aa"}22`, color: STATUS_COLORS[s.status] ?? "#8888aa" }}
                  >
                    {s.status}
                  </span>
                  {s.status === "active" && (
                    <button
                      onClick={() => handleComplete(s.session_id)}
                      className="text-xs text-[#48cfad] hover:underline"
                    >
                      Mark Complete
                    </button>
                  )}
                </div>
              </div>
              <div className="text-sm text-[#8888aa]">
                Scenario: <span className="text-[#e8e8f0]">{s.scenario_id}</span> &nbsp;|&nbsp;
                Attempts: <span className="text-[#e8e8f0]">{s.task_results.length}</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
