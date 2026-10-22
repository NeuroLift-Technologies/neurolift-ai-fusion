import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Avatar-Aide Pairs — NeuroLift AI Fusion",
  description:
    "Browse the Avatar-Aide pair roster: lived ADHD challenges paired with focused coaching responses.",
  openGraph: {
    title: "Avatar-Aide Pairs — NeuroLift AI Fusion",
    description:
      "Browse the Avatar-Aide pair roster: lived ADHD challenges paired with focused coaching responses.",
  },
};

export default function PairsLayout({ children }: { children: React.ReactNode }) {
  return children;
}
