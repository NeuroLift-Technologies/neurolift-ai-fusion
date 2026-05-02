import Link from "next/link";

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[70vh] text-center gap-8">
      <div>
        <h1 className="text-5xl font-bold text-gray-900 dark:text-white mb-4">
          NeuroLift <span className="text-brand-600">AI Fusion</span>
        </h1>
        <p className="text-xl text-gray-600 dark:text-gray-300 max-w-2xl">
          Avatar-Aide-Advocate experiential learning platform for evidence-based
          ADHD coaching through AI simulation.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full max-w-3xl">
        <FeatureCard
          title="Avatars"
          description="AI entities that simulate specific ADHD trait profiles — attention drift, task initiation difficulty, and more."
          icon="🧠"
        />
        <FeatureCard
          title="Aides"
          description="Coaching agents with domain expertise in attention science, task management, and emotional regulation."
          icon="🤝"
        />
        <FeatureCard
          title="Advocates"
          description="Higher-level agents that coordinate Avatar-Aide pairs and escalate to human oversight when needed."
          icon="🌟"
        />
      </div>

      <div className="flex gap-4">
        <Link
          href="/dashboard"
          className="px-6 py-3 bg-brand-600 text-white rounded-lg font-medium hover:bg-brand-700 transition-colors"
        >
          Go to Dashboard
        </Link>
        <Link
          href="/session/new"
          className="px-6 py-3 border border-brand-600 text-brand-600 rounded-lg font-medium hover:bg-brand-50 transition-colors"
        >
          Start New Session
        </Link>
      </div>
    </div>
  );
}

function FeatureCard({
  title,
  description,
  icon,
}: {
  title: string;
  description: string;
  icon: string;
}) {
  return (
    <div className="border border-gray-200 dark:border-gray-700 rounded-xl p-6 bg-white dark:bg-gray-900 text-left">
      <div className="text-3xl mb-3">{icon}</div>
      <h3 className="font-semibold text-gray-900 dark:text-white mb-2">{title}</h3>
      <p className="text-sm text-gray-600 dark:text-gray-400">{description}</p>
    </div>
  );
}
