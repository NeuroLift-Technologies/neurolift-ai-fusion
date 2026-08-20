"use client";

import { useState, useEffect, useRef } from "react";
import { motion, useInView } from "framer-motion";
import type { Variants } from "framer-motion";
import { User, HeartHandshake, Sparkles, ArrowRight } from "lucide-react";
import { cn } from "@/lib/utils";

interface Phase {
  icon: React.ElementType;
  label: string;
  title: string;
  description: string;
  circleColor: string;
  glowColor: string;
  borderColor: string;
  bgTint: string;
  textColor: string;
  gradientBorderColor: string;
  pulseGlowColor: string;
  innerGlowColor: string;
}

const phases: Phase[] = [
  {
    icon: User,
    label: "Phase 1: Experience",
    title: "AVATAR",
    description:
      "AI personas embodying specific ADHD traits live through authentic struggles, experiencing real stress, failure, and frustration.",
    circleColor: "bg-orange-500/15",
    glowColor: "shadow-[0_0_40px_rgba(243,128,32,0.15)]",
    borderColor: "border-orange-500/30",
    bgTint: "bg-orange-500/[0.03]",
    textColor: "text-orange-500",
    gradientBorderColor: "rgba(243,128,32,0.5)",
    pulseGlowColor: "rgba(243,128,32,0.1)",
    innerGlowColor: "rgba(243,128,32,0.05)",
  },
  {
    icon: HeartHandshake,
    label: "Phase 2: Coach",
    title: "AIDE",
    description:
      "PhD-level experts with real-world ADHD strategies provide real-time coaching alongside the Avatar in simulation.",
    circleColor: "bg-teal-500/15",
    glowColor: "shadow-[0_0_40px_rgba(20,184,166,0.15)]",
    borderColor: "border-teal-500/30",
    bgTint: "bg-teal-500/[0.03]",
    textColor: "text-teal-500",
    gradientBorderColor: "rgba(20,184,166,0.5)",
    pulseGlowColor: "rgba(20,184,166,0.1)",
    innerGlowColor: "rgba(20,184,166,0.05)",
  },
  {
    icon: Sparkles,
    label: "Phase 3: Fuse",
    title: "ADVOCATE",
    description:
      "The fused entity combines lived struggle understanding with proven expertise — empathy that truly gets it.",
    circleColor: "bg-violet-500/15",
    glowColor: "shadow-[0_0_40px_rgba(139,92,246,0.15)]",
    borderColor: "border-violet-500/30",
    bgTint: "bg-violet-500/[0.03]",
    textColor: "text-violet-500",
    gradientBorderColor: "rgba(139,92,246,0.5)",
    pulseGlowColor: "rgba(139,92,246,0.1)",
    innerGlowColor: "rgba(139,92,246,0.05)",
  },
];

const cardVariants: Variants = {
  hidden: { opacity: 0, y: 40 },
  visible: (i: number) => ({
    opacity: 1,
    y: 0,
    transition: {
      delay: i * 0.22,
      duration: 0.7,
      ease: "easeOut",
    },
  }),
};

const headerVariants: Variants = {
  hidden: { opacity: 0, y: 24 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.6, ease: "easeOut" },
  },
};

const FLOW_DOTS = [
  { size: 2, opacity: 0.9, delayOffset: 0 },
  { size: 1.5, opacity: 0.5, delayOffset: 0.35 },
  { size: 2.5, opacity: 0.7, delayOffset: 0.7 },
];

function ConnectionLine({ index, isInView }: { index: number; isInView: boolean }) {
  const [isDesktop, setIsDesktop] = useState(false);

  useEffect(() => {
    const update = () => setIsDesktop(window.innerWidth >= 768);
    requestAnimationFrame(update);
    window.addEventListener("resize", update);
    return () => window.removeEventListener("resize", update);
  }, []);

  if (!isDesktop) {
    // Vertical connector for mobile
    return (
      <motion.div
        className="flex flex-col items-center gap-0"
        initial={{ opacity: 0, scaleY: 0 }}
        animate={isInView ? { opacity: 1, scaleY: 1 } : { opacity: 0, scaleY: 0 }}
        transition={{ delay: 0.5 + index * 0.3, duration: 0.5, ease: "easeOut" }}
        style={{ transformOrigin: "top" }}
      >
        <div className="relative h-12 w-0 border-l-2 border-orange-500/30 transition-all duration-500" style={{ borderStyle: isInView ? "solid" : "dashed" }}>
          {/* Animated dots traveling down */}
          {FLOW_DOTS.map((dot) => (
            <motion.div
              key={dot.delayOffset}
              className="absolute -left-[3px] rounded-full bg-orange-400"
              style={{
                width: dot.size,
                height: dot.size,
                opacity: dot.opacity,
                translateX: "-50%",
              }}
              initial={{ top: 0, opacity: 0 }}
              animate={isInView ? { top: "calc(100% - 8px)", opacity: [0, dot.opacity, dot.opacity, 0] } : {}}
              transition={{ delay: 0.7 + index * 0.3 + dot.delayOffset, duration: 0.9, ease: "easeInOut" }}
            />
          ))}
        </div>
        <ArrowRight className="h-4 w-4 -rotate-90 text-muted-foreground/40" />
      </motion.div>
    );
  }

  // Horizontal connector for desktop
  return (
    <motion.div
      className="hidden items-center justify-center md:flex"
      initial={{ opacity: 0, scaleX: 0 }}
      animate={isInView ? { opacity: 1, scaleX: 1 } : { opacity: 0, scaleX: 0 }}
      transition={{ delay: 0.5 + index * 0.3, duration: 0.6, ease: "easeOut" }}
      style={{ transformOrigin: "left" }}
    >
      <div className="relative h-0 w-16 lg:w-24 border-t-2 border-orange-500/30 transition-all duration-500" style={{ borderStyle: isInView ? "solid" : "dashed" }}>
        {/* Animated dots traveling right */}
        {FLOW_DOTS.map((dot) => (
          <motion.div
            key={dot.delayOffset}
            className="absolute -top-1 rounded-full bg-orange-400"
            style={{
              width: dot.size,
              height: dot.size,
              opacity: dot.opacity,
              translateY: "-50%",
            }}
            initial={{ left: 0, opacity: 0 }}
            animate={isInView ? { left: "calc(100% - 8px)", opacity: [0, dot.opacity, dot.opacity, 0] } : {}}
            transition={{ delay: 0.7 + index * 0.3 + dot.delayOffset, duration: 0.9, ease: "easeInOut" }}
          />
        ))}
      </div>
      <ArrowRight className="ml-0.5 h-4 w-4 text-muted-foreground/40" />
    </motion.div>
  );
}

const PHASE_NUMBERS = ["01", "02", "03"];

function PhaseCard({ phase, index, isInView }: { phase: Phase; index: number; isInView: boolean }) {
  const Icon = phase.icon;

  return (
    <motion.article
      className={cn(
        "phase-card-gradient-border phase-card-visible-glow phase-card-inner-glow relative flex flex-1 max-w-sm flex-col items-center rounded-2xl border p-6 text-center transition-shadow duration-500 md:max-w-xs md:p-8",
        phase.borderColor,
        phase.bgTint,
      )}
      style={{
        "--phase-color": phase.gradientBorderColor,
        "--phase-glow-color": phase.pulseGlowColor,
        "--phase-inner-glow": phase.innerGlowColor,
      } as React.CSSProperties}
      custom={index}
      variants={cardVariants}
      initial="hidden"
      animate={isInView ? "visible" : "hidden"}
      whileInView="visible"
      viewport={{ once: true, amount: 0.3 }}
      whileHover={{ y: -4, boxShadow: "0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)" }}
      transition={{ type: "spring", stiffness: 300, damping: 20 }}
      // Glow on hover
      onMouseEnter={(e) => {
        e.currentTarget.classList.add(phase.glowColor);
      }}
      onMouseLeave={(e) => {
        e.currentTarget.classList.remove(phase.glowColor);
      }}
    >
      {/* Phase number - decorative background */}
      <span className="pointer-events-none absolute top-2 left-1/2 -translate-x-1/2 text-6xl font-bold text-muted-foreground/[0.04] select-none">
        {PHASE_NUMBERS[index]}
      </span>

      {/* Icon circle */}
      <motion.div
        className={cn(
          "relative flex h-16 w-16 items-center justify-center rounded-full ring-1 ring-inset sm:h-20 sm:w-20",
          phase.circleColor,
          phase.textColor,
        )}
        whileHover={{ scale: 1.05 }}
        transition={{ type: "spring", stiffness: 400, damping: 20 }}
      >
        <Icon className="h-7 w-7 sm:h-9 sm:w-9" strokeWidth={1.8} />
      </motion.div>

      {/* Phase label */}
      <p className={cn("mt-4 text-xs font-semibold uppercase tracking-widest sm:text-sm", phase.textColor)}>
        {phase.label}
      </p>

      {/* Phase title */}
      <h3 className="mt-1 text-2xl font-bold tracking-tight text-foreground sm:text-3xl">
        {phase.title}
      </h3>

      {/* Description */}
      <p className="mt-3 max-w-xs text-sm leading-relaxed text-muted-foreground sm:text-base">
        {phase.description}
      </p>
    </motion.article>
  );
}

export function PipelineSection() {
  const sectionRef = useRef<HTMLElement>(null);
  const isInView = useInView(sectionRef, { once: true, margin: "-80px 0px" });

  return (
    <section
      id="pipeline"
      ref={sectionRef}
      className="relative w-full px-4 py-20 sm:py-28"
      aria-label="Fusion Pipeline"
    >
      {/* Subtle warm radial gradient background */}
      <div
        className="pointer-events-none absolute inset-x-0 top-0 h-[400px]"
        style={{
          background:
            'radial-gradient(ellipse at top center, rgba(243,128,32,0.04) 0%, rgba(243,128,32,0.01) 40%, transparent 70%)',
        }}
        aria-hidden="true"
      />
      <div className="mx-auto max-w-6xl">
        {/* Section header */}
        <motion.div
          className="mb-14 text-center md:mb-20"
          variants={headerVariants}
          initial="hidden"
          animate={isInView ? "visible" : "hidden"}
        >
          <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl md:text-5xl">
            The Fusion Pipeline
          </h2>
          <p className="mt-3 text-base text-muted-foreground sm:mt-4 sm:text-lg md:text-xl">
            How experiential understanding meets expert knowledge
          </p>
        </motion.div>

        {/* Pipeline flow */}
        <div className="flex flex-col items-center gap-0 md:flex-row md:items-start md:justify-center md:gap-0">
          {phases.map((phase, index) => (
            <div key={phase.title} className="contents">
              <PhaseCard phase={phase} index={index} isInView={isInView} />
              {index < phases.length - 1 && <ConnectionLine index={index} isInView={isInView} />}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
