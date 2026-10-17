"use client";

import { useRef } from "react";
import { motion, useInView } from "framer-motion";
import type { Variants } from "framer-motion";
import { Brain, Earth, ArrowUpRight } from "lucide-react";
import { cn } from "@/lib/utils";
import { WORLD_ENGINE_URL } from "@/lib/links";

const fadeUp: Variants = {
  hidden: { opacity: 0, y: 24 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.6, ease: "easeOut" },
  },
};

// Mirrors the repo boundary: Fusion owns semantic decisions, the World Engine
// owns physical reality.
const roles = [
  {
    icon: Brain,
    name: "AI Fusion",
    role: "Decides what to do",
    description: "ADHD trait models, Aide coaching, and the intent behind every move an Avatar makes.",
    textColor: "text-orange-500",
    circleColor: "bg-orange-500/15",
    borderColor: "border-orange-500/30",
    bgTint: "bg-orange-500/[0.03]",
  },
  {
    icon: Earth,
    name: "World Engine",
    role: "Makes it happen",
    description: "A persistent 3D world with space, time, and physics, where every move plays out and has consequences.",
    textColor: "text-teal-500",
    circleColor: "bg-teal-500/15",
    borderColor: "border-teal-500/30",
    bgTint: "bg-teal-500/[0.03]",
  },
];

export function WorldEngineSection() {
  const sectionRef = useRef<HTMLElement>(null);
  const isInView = useInView(sectionRef, { once: true, margin: "-80px 0px" });

  return (
    <section
      id="world-engine"
      ref={sectionRef}
      className="relative w-full px-4 py-20 sm:py-28"
      aria-labelledby="world-engine-heading"
    >
      <motion.div
        className="mx-auto flex max-w-4xl flex-col items-center text-center"
        variants={fadeUp}
        initial="hidden"
        animate={isInView ? "visible" : "hidden"}
      >
        <p className="text-xs font-semibold uppercase tracking-widest text-orange-500 sm:text-sm">
          Where the Avatars live
        </p>
        <h2
          id="world-engine-heading"
          className="mt-2 text-3xl font-bold tracking-tight text-foreground sm:text-4xl md:text-5xl"
        >
          NLT World Engine
        </h2>
        <p className="mt-4 max-w-2xl text-base leading-relaxed text-muted-foreground sm:text-lg">
          Avatars don&rsquo;t learn ADHD from a script. They live it in the NLT World Engine, an AI
          habitat where models perceive their surroundings, act, and learn from what happens next.
        </p>

        <div className="mt-10 grid w-full gap-4 text-left sm:grid-cols-2">
          {roles.map((r) => (
            <div key={r.name} className={cn("flex gap-4 rounded-2xl border p-5", r.borderColor, r.bgTint)}>
              <div
                className={cn(
                  "flex h-11 w-11 shrink-0 items-center justify-center rounded-full",
                  r.circleColor,
                  r.textColor,
                )}
              >
                <r.icon className="h-5 w-5" strokeWidth={1.8} aria-hidden="true" />
              </div>
              <div>
                <h3 className="font-bold text-foreground">{r.name}</h3>
                <p className={cn("text-xs font-semibold uppercase tracking-widest", r.textColor)}>{r.role}</p>
                <p className="mt-2 text-sm leading-relaxed text-muted-foreground">{r.description}</p>
              </div>
            </div>
          ))}
        </div>

        <a
          href={WORLD_ENGINE_URL}
          target="_blank"
          rel="noopener noreferrer"
          className="mt-10 inline-flex items-center gap-2 rounded-full border-2 border-orange-500/60 px-6 py-3 text-sm font-semibold text-foreground transition-all duration-300 hover:scale-[1.03] hover:bg-orange-500/10 hover:shadow-[0_0_20px_rgba(243,128,32,0.35)] sm:px-8 sm:py-3.5 sm:text-base"
        >
          Visit the World Engine
          <ArrowUpRight className="h-4 w-4" aria-hidden="true" />
          <span className="sr-only">(opens in a new tab)</span>
        </a>
      </motion.div>
    </section>
  );
}
