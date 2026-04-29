import { useEffect, useState } from "react";
import { fusionApi, avatarsApi, aidesApi, type FusionReport, type Avatar, type Aide } from "../api/client";

export default function FusionPage() {
  const [reports, setReports] = useState<FusionReport[]>([]);
  const [avatars, setAvatars] = useState<Avatar[]>([]);
  const [aides, setAides] = useState<Aide[]>([]);
  const [avatarId, setAvatarId] = useState("");
  const [aideId, setAideId] = useState("");
  const [loading, setLoading] = useState(true);
  const [attempting, setAttempting] = useState(false);

  const load = () => {
    setLoading(true);
    Promise.all([fusionApi.list(), avatarsApi.list(), aidesApi.list()])
      .then(([r, a, ai]) => {
        setReports(r);
        setAvatars(a);
        setAides(ai);
        if (a.length) setAvatarId(a[0].avatar_id);
        if (ai.length) setAideId(ai[0].aide_id);
      })
      .finally(() => setLoading(false));
  };

  useEffect(load, []);

  const handleFusion = async () => {
    if (!avatarId || !aideId) return;
    setAttempting(true);
    try {
      const report = await fusionApi.attempt(avatarId, aideId);
      setReports((prev) => [report, ...prev]);
    } finally {
      setAttempting(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto">
      <div className="mb-6">
        <h1 className="text-3xl font-bold mb-1">Fusion</h1>
        <p className="text-[#8888aa]">Fuse a trained Avatar + Aide into an Advocate.</p>
      </div>

      {/* Fusion form */}
      <div className="bg-[#1a1a2e] border border-[#2e2e4e] rounded-xl p-5 mb-6">
        <h2 className="font-semibold mb-4">Attempt Fusion</h2>
        <div className="flex flex-wrap gap-3 items-end">
          <div>
            <label className="block text-xs text-[#8888aa] mb-1">Avatar</label>
            <select
              className="bg-[#0f0f1a] border border-[#2e2e4e] rounded-lg px-3 py-2 text-sm text-[#e8e8f0]"
              value={avatarId}
              onChange={(e) => setAvatarId(e.target.value)}
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
              value={aideId}
              onChange={(e) => setAideId(e.target.value)}
            >
              {aides.map((a) => (
                <option key={a.aide_id} value={a.aide_id}>
                  {a.expertise_area} ({a.aide_id.slice(0, 6)})
                </option>
              ))}
            </select>
          </div>
          <button
            onClick={handleFusion}
            disabled={attempting || !avatarId || !aideId}
            className="bg-gradient-to-r from-[#6c63ff] to-[#48cfad] text-white px-5 py-2 rounded-lg text-sm font-semibold transition-opacity disabled:opacity-50"
          >
            {attempting ? "Fusing…" : "⚡ Attempt Fusion"}
          </button>
        </div>
      </div>

      {/* Reports */}
      {loading ? (
        <p className="text-[#8888aa]">Loading…</p>
      ) : reports.length === 0 ? (
        <div className="bg-[#1a1a2e] border border-[#2e2e4e] rounded-xl p-10 text-center text-[#8888aa]">
          No fusion attempts yet.
        </div>
      ) : (
        <div className="flex flex-col gap-3">
          {reports.map((r) => (
            <div
              key={r.fusion_id}
              className={`bg-[#1a1a2e] border rounded-xl p-5 ${
                r.success ? "border-[#48cfad]/40" : "border-[#fc5c65]/40"
              }`}
            >
              <div className="flex items-center justify-between mb-2">
                <div className="font-mono text-sm text-[#8888aa]">{r.fusion_id.slice(0, 12)}…</div>
                <span
                  className={`text-xs font-bold px-2 py-0.5 rounded-full ${
                    r.success
                      ? "bg-[#48cfad]/20 text-[#48cfad]"
                      : "bg-[#fc5c65]/20 text-[#fc5c65]"
                  }`}
                >
                  {r.success ? "SUCCESS — Advocate Created" : "NOT READY"}
                </span>
              </div>
              <div className="text-sm text-[#8888aa]">
                Readiness Score:{" "}
                <span
                  className="font-semibold"
                  style={{ color: r.readiness_score >= 0.75 ? "#48cfad" : "#fc5c65" }}
                >
                  {(r.readiness_score * 100).toFixed(1)}%
                </span>
              </div>
              {r.failure_reason && (
                <div className="mt-2 text-xs text-[#fc5c65]">{r.failure_reason}</div>
              )}
              {r.advocate_id && (
                <div className="mt-2 text-xs text-[#48cfad]">
                  Advocate ID: <span className="font-mono">{r.advocate_id}</span>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
