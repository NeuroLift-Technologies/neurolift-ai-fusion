import { useEffect, useState } from "react";
import { avatarsApi, aidesApi, sessionsApi, fusionApi } from "../api/client";

interface Stats {
  avatars: number;
  aides: number;
  sessions: number;
  advocates: number;
}

const STAT_CARDS = [
  { key: "avatars", label: "Avatars", color: "#6c63ff" },
  { key: "aides", label: "Aides", color: "#48cfad" },
  { key: "sessions", label: "Sessions", color: "#fed330" },
  { key: "advocates", label: "Advocates", color: "#fc5c65" },
] as const;

export default function Dashboard() {
  const [stats, setStats] = useState<Stats>({ avatars: 0, aides: 0, sessions: 0, advocates: 0 });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      avatarsApi.list(),
      aidesApi.list(),
      sessionsApi.list(),
      fusionApi.advocates(),
    ])
      .then(([avatars, aides, sessions, advocates]) => {
        setStats({
          avatars: avatars.length,
          aides: aides.length,
          sessions: sessions.length,
          advocates: advocates.length,
        });
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="max-w-5xl mx-auto">
      <h1 className="text-3xl font-bold mb-2">Simulation Dashboard</h1>
      <p className="text-[#8888aa] mb-8">
        Monitor Avatar training progress, Aide coaching effectiveness, and Fusion outcomes.
      </p>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-10">
        {STAT_CARDS.map(({ key, label, color }) => (
          <div
            key={key}
            className="bg-[#1a1a2e] border border-[#2e2e4e] rounded-xl p-5 flex flex-col gap-2"
          >
            <span className="text-sm text-[#8888aa]">{label}</span>
            <span
              className="text-4xl font-bold"
              style={{ color }}
            >
              {loading ? "—" : stats[key]}
            </span>
          </div>
        ))}
      </div>

      {/* Mission statement */}
      <div className="bg-[#1a1a2e] border border-[#2e2e4e] rounded-xl p-6 mb-6">
        <h2 className="text-lg font-semibold mb-2 text-[#6c63ff]">Mission</h2>
        <p className="text-[#8888aa] leading-relaxed">
          <em>"Nothing About Us Without Us"</em> — neurodivergent voices lead development. NeuroLift
          trains AI Avatars with ADHD traits through authentic experiential learning in a Sims/RPG-style
          simulation. Paired Aides coach them through real struggles until they are ready to fuse into
          Advocates that combine lived understanding with expert solutions.
        </p>
      </div>

      {/* Process overview */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {[
          { step: "1", title: "Avatar", desc: "Embodies a specific ADHD trait and lives through authentic struggles." },
          { step: "2", title: "Aide", desc: "Coaches the Avatar in real-time with PhD-level expertise and lived experience." },
          { step: "3", title: "Training", desc: "Repeated scenario attempts with real consequences build genuine resilience." },
          { step: "4", title: "Fusion", desc: "Avatar + Aide merge into an Advocate once readiness thresholds are met." },
        ].map(({ step, title, desc }) => (
          <div
            key={step}
            className="bg-[#1a1a2e] border border-[#2e2e4e] rounded-xl p-5"
          >
            <div className="text-[#6c63ff] font-bold text-2xl mb-1">Phase {step}</div>
            <div className="font-semibold mb-2">{title}</div>
            <p className="text-sm text-[#8888aa]">{desc}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
