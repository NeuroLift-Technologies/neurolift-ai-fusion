import { useEffect, useState } from "react";
import { avatarsApi, type Avatar } from "../api/client";

const STATE_COLORS: Record<string, string> = {
  idle: "#8888aa",
  attempting_task: "#6c63ff",
  struggling: "#fc5c65",
  receiving_coaching: "#48cfad",
  applying_strategy: "#fed330",
  learning: "#48cfad",
  independent: "#48cfad",
  burnout_risk: "#fc5c65",
  burnout: "#fc5c65",
  recovering: "#fed330",
};

export default function AvatarsPage() {
  const [avatars, setAvatars] = useState<Avatar[]>([]);
  const [traits, setTraits] = useState<string[]>([]);
  const [selected, setSelected] = useState("");
  const [loading, setLoading] = useState(true);
  const [creating, setCreating] = useState(false);

  const load = () => {
    setLoading(true);
    Promise.all([avatarsApi.list(), avatarsApi.traits()])
      .then(([avs, ts]) => {
        setAvatars(avs);
        setTraits(ts);
        if (ts.length) setSelected(ts[0]);
      })
      .finally(() => setLoading(false));
  };

  useEffect(load, []);

  const handleCreate = async () => {
    if (!selected) return;
    setCreating(true);
    try {
      const av = await avatarsApi.create(selected);
      setAvatars((prev) => [...prev, av]);
    } finally {
      setCreating(false);
    }
  };

  const handleDelete = async (id: string) => {
    await avatarsApi.delete(id);
    setAvatars((prev) => prev.filter((a) => a.avatar_id !== id));
  };

  return (
    <div className="max-w-5xl mx-auto">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-3xl font-bold mb-1">Avatars</h1>
          <p className="text-[#8888aa]">AI Avatars embodying specific ADHD traits.</p>
        </div>
        <div className="flex gap-3 items-center">
          <select
            className="bg-[#1a1a2e] border border-[#2e2e4e] rounded-lg px-3 py-2 text-sm text-[#e8e8f0]"
            value={selected}
            onChange={(e) => setSelected(e.target.value)}
          >
            {traits.map((t) => (
              <option key={t} value={t}>{t.replace(/_/g, " ")}</option>
            ))}
          </select>
          <button
            onClick={handleCreate}
            disabled={creating}
            className="bg-[#6c63ff] hover:bg-[#5a52e0] text-white px-4 py-2 rounded-lg text-sm font-semibold transition-colors disabled:opacity-50"
          >
            {creating ? "Creating…" : "+ New Avatar"}
          </button>
        </div>
      </div>

      {loading ? (
        <p className="text-[#8888aa]">Loading…</p>
      ) : avatars.length === 0 ? (
        <div className="bg-[#1a1a2e] border border-[#2e2e4e] rounded-xl p-10 text-center text-[#8888aa]">
          No avatars yet. Create one to begin training.
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {avatars.map((av) => (
            <div
              key={av.avatar_id}
              className="bg-[#1a1a2e] border border-[#2e2e4e] rounded-xl p-5"
            >
              <div className="flex items-start justify-between mb-3">
                <div>
                  <div className="font-semibold text-lg capitalize">
                    {av.trait_name.replace(/_/g, " ")}
                  </div>
                  <div
                    className="text-xs mt-0.5 font-mono"
                    style={{ color: STATE_COLORS[av.current_state] ?? "#8888aa" }}
                  >
                    {av.current_state}
                  </div>
                </div>
                <button
                  onClick={() => handleDelete(av.avatar_id)}
                  className="text-[#8888aa] hover:text-[#fc5c65] text-xs transition-colors"
                >
                  Remove
                </button>
              </div>
              <div className="grid grid-cols-3 gap-2 text-xs text-[#8888aa]">
                <div>
                  <div className="text-[#e8e8f0] font-semibold">{av.total_tasks_attempted}</div>
                  Tasks Attempted
                </div>
                <div>
                  <div className="text-[#48cfad] font-semibold">{av.total_tasks_completed}</div>
                  Completed
                </div>
                <div>
                  <div className="text-[#fed330] font-semibold">{av.total_coaching_sessions}</div>
                  Coaching
                </div>
              </div>
              <div className="mt-3 grid grid-cols-3 gap-2 text-xs">
                {[
                  { label: "Stress", value: av.stress_level, color: "#fc5c65" },
                  { label: "Cognitive Load", value: av.cognitive_load, color: "#fed330" },
                  { label: "Burnout Risk", value: av.burnout_risk_level, color: "#fc5c65" },
                ].map(({ label, value, color }) => (
                  <div key={label}>
                    <div className="flex justify-between mb-0.5 text-[#8888aa]">
                      <span>{label}</span>
                      <span style={{ color }}>{(value * 100).toFixed(0)}%</span>
                    </div>
                    <div className="h-1.5 bg-[#2e2e4e] rounded-full overflow-hidden">
                      <div
                        className="h-full rounded-full transition-all"
                        style={{ width: `${value * 100}%`, background: color }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
