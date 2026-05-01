import { useEffect, useState } from "react";
import { scenariosApi, type Scenario } from "../api/client";

const CATEGORY_COLORS: Record<string, string> = {
  workplace: "#6c63ff",
  personal: "#48cfad",
  social: "#fed330",
};

export default function ScenariosPage() {
  const [scenarios, setScenarios] = useState<Scenario[]>([]);
  const [category, setCategory] = useState<string>("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    scenariosApi
      .list(category || undefined)
      .then(setScenarios)
      .finally(() => setLoading(false));
  }, [category]);

  return (
    <div className="max-w-5xl mx-auto">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-3xl font-bold mb-1">Scenarios</h1>
          <p className="text-[#8888aa]">Training scenarios available in the simulation environment.</p>
        </div>
        <div className="flex gap-2">
          {["", "workplace", "personal", "social"].map((cat) => (
            <button
              key={cat}
              onClick={() => setCategory(cat)}
              className={`text-sm px-3 py-1.5 rounded-lg transition-colors ${
                category === cat
                  ? "bg-[#6c63ff]/20 text-[#6c63ff] font-semibold"
                  : "text-[#8888aa] hover:text-[#e8e8f0]"
              }`}
            >
              {cat === "" ? "All" : cat.charAt(0).toUpperCase() + cat.slice(1)}
            </button>
          ))}
        </div>
      </div>

      {loading ? (
        <p className="text-[#8888aa]">Loading…</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {scenarios.map((s) => (
            <div key={s.scenario_id} className="bg-[#1a1a2e] border border-[#2e2e4e] rounded-xl p-5">
              <div className="flex items-start justify-between mb-2">
                <div className="font-semibold">{s.name}</div>
                <span
                  className="text-xs px-2 py-0.5 rounded-full capitalize"
                  style={{
                    background: `${CATEGORY_COLORS[s.category] ?? "#8888aa"}22`,
                    color: CATEGORY_COLORS[s.category] ?? "#8888aa",
                  }}
                >
                  {s.category}
                </span>
              </div>
              <p className="text-sm text-[#8888aa] mb-3">{s.description}</p>
              <div className="grid grid-cols-3 gap-2 text-xs text-[#8888aa]">
                <div>
                  Complexity
                  <div className="text-[#e8e8f0] capitalize">{s.complexity}</div>
                </div>
                <div>
                  Cognitive Demand
                  <div className="text-[#fed330]">{(s.cognitive_demand * 100).toFixed(0)}%</div>
                </div>
                <div>
                  Base Success
                  <div className="text-[#48cfad]">{(s.base_success_rate * 100).toFixed(0)}%</div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
