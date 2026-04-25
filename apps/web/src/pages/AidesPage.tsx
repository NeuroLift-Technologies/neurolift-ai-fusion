import { useEffect, useState } from "react";
import { aidesApi, type Aide } from "../api/client";

export default function AidesPage() {
  const [aides, setAides] = useState<Aide[]>([]);
  const [area, setArea] = useState("attention");
  const [loading, setLoading] = useState(true);
  const [creating, setCreating] = useState(false);

  const load = () => {
    setLoading(true);
    aidesApi.list().then(setAides).finally(() => setLoading(false));
  };

  useEffect(load, []);

  const handleCreate = async () => {
    setCreating(true);
    try {
      const aide = await aidesApi.create(area);
      setAides((prev) => [...prev, aide]);
    } finally {
      setCreating(false);
    }
  };

  const handleDelete = async (id: string) => {
    await aidesApi.delete(id);
    setAides((prev) => prev.filter((a) => a.aide_id !== id));
  };

  return (
    <div className="max-w-5xl mx-auto">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-3xl font-bold mb-1">Aides</h1>
          <p className="text-[#8888aa]">AI coaching Aides paired with Avatars.</p>
        </div>
        <div className="flex gap-3 items-center">
          <input
            className="bg-[#1a1a2e] border border-[#2e2e4e] rounded-lg px-3 py-2 text-sm text-[#e8e8f0] w-48"
            placeholder="Expertise area"
            value={area}
            onChange={(e) => setArea(e.target.value)}
          />
          <button
            onClick={handleCreate}
            disabled={creating}
            className="bg-[#48cfad] hover:bg-[#3ab89a] text-[#0f0f1a] px-4 py-2 rounded-lg text-sm font-semibold transition-colors disabled:opacity-50"
          >
            {creating ? "Creating…" : "+ New Aide"}
          </button>
        </div>
      </div>

      {loading ? (
        <p className="text-[#8888aa]">Loading…</p>
      ) : aides.length === 0 ? (
        <div className="bg-[#1a1a2e] border border-[#2e2e4e] rounded-xl p-10 text-center text-[#8888aa]">
          No aides yet. Create one to pair with an Avatar.
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {aides.map((aide) => (
            <div key={aide.aide_id} className="bg-[#1a1a2e] border border-[#2e2e4e] rounded-xl p-5">
              <div className="flex items-start justify-between mb-3">
                <div>
                  <div className="font-semibold text-lg capitalize">{aide.expertise_area}</div>
                  <div className="text-xs text-[#8888aa] font-mono">{aide.aide_id.slice(0, 8)}</div>
                </div>
                <button
                  onClick={() => handleDelete(aide.aide_id)}
                  className="text-[#8888aa] hover:text-[#fc5c65] text-xs transition-colors"
                >
                  Remove
                </button>
              </div>
              <div className="grid grid-cols-4 gap-2 text-xs text-[#8888aa]">
                <div>
                  <div className="text-[#e8e8f0] font-semibold">{aide.total_interventions}</div>
                  Total
                </div>
                <div>
                  <div className="text-[#48cfad] font-semibold">{aide.successful_interventions}</div>
                  Successful
                </div>
                <div>
                  <div className="text-[#fc5c65] font-semibold">{aide.crisis_interventions}</div>
                  Crisis
                </div>
                <div>
                  <div className="text-[#6c63ff] font-semibold">{aide.independence_achievements}</div>
                  Independence
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
