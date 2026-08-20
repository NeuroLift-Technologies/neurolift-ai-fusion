"use client";

import { useEffect, useRef, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import type { Variants } from "framer-motion";
import { ChevronDown, User, HeartHandshake, Sparkles, ChevronRight, ArrowRight } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { getStats } from "@/lib/avatar-pairs-data";
import { ParticleCanvas } from "./particle-canvas";

const container: Variants = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.18, delayChildren: 0.3 },
  },
};

const fadeUp: Variants = {
  hidden: { opacity: 0, y: 28 },
  show: { opacity: 1, y: 0, transition: { duration: 0.65, ease: "easeOut" } },
};

function AnimatedCounter({ target, suffix = "" }: { target: number; suffix?: string }) {
  const [count, setCount] = useState(0);

  useEffect(() => {
    let start = 0;
    const duration = 1200;
    const startTime = performance.now();

    function tick(now: number) {
      const elapsed = now - startTime;
      const progress = Math.min(elapsed / duration, 1);
      // Ease-out cubic
      const eased = 1 - Math.pow(1 - progress, 3);
      start = Math.round(eased * target);
      setCount(start);
      if (progress < 1) requestAnimationFrame(tick);
    }

    requestAnimationFrame(tick);
  }, [target]);

  return (
    <span className="tabular-nums">
      {count}
      {suffix}
    </span>
  );
}

const ROTATING_WORDS = ["AI Simulation", "Deep Empathy", "Real Understanding", "Fused Intelligence"];

function RotatingTagline() {
  const [index, setIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setIndex((prev) => (prev + 1) % ROTATING_WORDS.length);
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <motion.p
      className="mt-4 text-lg font-medium text-foreground/80 sm:text-xl md:text-2xl"
      variants={fadeUp}
    >
      {"Experiential Learning Through "}
      <span className="rotating-underline relative inline-block min-w-[140px] sm:min-w-[180px] md:min-w-[240px]">
        <AnimatePresence mode="wait">
          <motion.span
            key={ROTATING_WORDS[index]}
            className="gradient-text inline-block"
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -12 }}
            transition={{ duration: 0.4, ease: "easeInOut" }}
          >
            {ROTATING_WORDS[index]}
          </motion.span>
        </AnimatePresence>
      </span>
    </motion.p>
  );
}

function GradientOrbs() {
  return (
    <div className="pointer-events-none absolute inset-0 z-[1] overflow-hidden" aria-hidden="true">
      {/* Primary large orb */}
      <div
        className="absolute -top-32 -left-32 h-[500px] w-[500px] rounded-full opacity-25 blur-[120px]"
        style={{
          background: "radial-gradient(circle, #F38020 0%, transparent 70%)",
          animation: "float-1 14s ease-in-out infinite",
        }}
      />
      {/* Secondary warm orb */}
      <div
        className="absolute top-1/3 -right-24 h-[400px] w-[400px] rounded-full opacity-20 blur-[100px]"
        style={{
          background: "radial-gradient(circle, #F59E0B 0%, transparent 70%)",
          animation: "float-2 18s ease-in-out infinite",
        }}
      />
      {/* Bottom-right amber orb */}
      <div
        className="absolute -bottom-20 left-1/3 h-[350px] w-[350px] rounded-full opacity-15 blur-[90px]"
        style={{
          background: "radial-gradient(circle, #EA580C 0%, transparent 70%)",
          animation: "float-3 16s ease-in-out infinite",
        }}
      />
      {/* Top-right subtle warm glow */}
      <div
        className="absolute top-10 right-1/4 h-[250px] w-[250px] rounded-full opacity-10 blur-[80px]"
        style={{
          background: "radial-gradient(circle, #FB923C 0%, transparent 70%)",
          animation: "float-2 20s ease-in-out infinite reverse",
        }}
      />
    </div>
  );
}

export function HeroSection() {
  const stats = getStats();
  const titleRef = useRef<HTMLHeadingElement>(null);

  // Scroll-driven glow intensification
  useEffect(() => {
    function handleScroll() {
      if (!titleRef.current) return;
      const progress = Math.min(window.scrollY / 400, 1);
      titleRef.current.style.textShadow = `0 0 ${20 + progress * 20}px rgba(243,128,32,${0.15 + progress * 0.2})`;
    }
    handleScroll();
    window.addEventListener("scroll", handleScroll, { passive: true });
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <section
      id="overview"
      className="relative flex min-h-screen flex-col items-center justify-center overflow-hidden px-4 py-20"
      aria-label="Hero"
    >
      {/* Animated particle mesh background */}
      <ParticleCanvas />

      {/* Animated gradient orbs background */}
      <GradientOrbs />

      {/* Subtle noise overlay for texture */}
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_at_center,_transparent_0%,_rgba(255,255,255,0.03)_100%)]" />

      {/* Content */}
      <motion.div
        className="relative z-10 mx-auto flex max-w-4xl flex-col items-center text-center"
        variants={container}
        initial="hidden"
        animate="show"
      >
        {/* Title */}
        <motion.h1
          ref={titleRef}
          className="hero-title text-4xl font-extrabold tracking-tight sm:text-5xl md:text-6xl lg:text-7xl"
          variants={fadeUp}
        >
          <span
            className="bg-clip-text text-transparent"
            style={{
              backgroundImage: "linear-gradient(135deg, #F38020 0%, #F59E0B 40%, #EA580C 80%, #F97316 100%)",
            }}
          >
            NeuroLift AI Fusion
          </span>
        </motion.h1>

        {/* Tagline with rotating words */}
        <RotatingTagline />

        {/* Subtitle paragraph */}
        <motion.p
          className="mt-6 max-w-2xl text-base leading-relaxed text-muted-foreground sm:text-lg"
          variants={fadeUp}
        >
          Each AI entity begins as an <span className="font-semibold text-foreground/90">Avatar</span> that
          lives through authentic ADHD struggles, then fuses with an expert{" "}
          <span className="font-semibold text-foreground/90">Aide</span> who provides proven
          strategies — creating an <span className="font-semibold text-foreground/90">Advocate</span>{" "}
          that truly understands from both experience and expertise.
        </motion.p>

        {/* How It Works — mini pipeline preview */}
        <motion.div
          className="mt-10 hidden sm:flex items-center justify-center gap-1"
          variants={fadeUp}
        >
          {[
            { icon: User, label: "Experience", color: "text-orange-500", bg: "bg-orange-500/10", border: "border-orange-500/20" },
            { icon: HeartHandshake, label: "Coach", color: "text-teal-500", bg: "bg-teal-500/10", border: "border-teal-500/20" },
            { icon: Sparkles, label: "Fuse", color: "text-violet-500", bg: "bg-violet-500/10", border: "border-violet-500/20" },
          ].map((step, i) => (
            <div key={step.label} className="flex items-center gap-1">
              <div className={`mini-pipeline-pulse flex items-center gap-2 rounded-full border px-3 py-1.5 ${step.bg} ${step.border}`}>
                <step.icon className={`h-3.5 w-3.5 ${step.color}`} />
                <span className={`text-xs font-medium ${step.color}`}>{step.label}</span>
              </div>
              {i < 2 && (
                <ChevronRight className="mx-0.5 h-3 w-3 text-muted-foreground/40" />
              )}
            </div>
          ))}
        </motion.div>

        {/* Stat counters */}
        <motion.div
          className="mt-12 flex flex-wrap items-center justify-center gap-3 sm:gap-4 md:gap-6"
          variants={fadeUp}
        >
          <Badge
            variant="outline"
            className="border-orange-500/30 bg-orange-500/5 px-4 py-2 text-sm font-semibold sm:px-5 sm:py-2.5 sm:text-base"
          >
            <AnimatedCounter target={stats.total} /> Pairs
          </Badge>

          <span className="hidden text-muted-foreground/50 sm:inline">|</span>

          <Badge
            variant="outline"
            className="border-amber-500/30 bg-amber-500/5 px-4 py-2 text-sm font-semibold sm:px-5 sm:py-2.5 sm:text-base"
          >
            <AnimatedCounter target={stats.executiveFunction} /> Executive Function
          </Badge>

          <span className="hidden text-muted-foreground/50 sm:inline">|</span>

          <Badge
            variant="outline"
            className="border-orange-600/30 bg-orange-600/5 px-4 py-2 text-sm font-semibold sm:px-5 sm:py-2.5 sm:text-base"
          >
            <AnimatedCounter target={stats.nonExecutiveFunction} /> Non-Executive Function
          </Badge>
        </motion.div>

        {/* CTA Button */}
        <motion.button
          type="button"
          className="cta-gradient-border mt-8 rounded-full bg-[#F38020] px-6 py-3 text-sm font-semibold text-white shadow-[0_0_20px_rgba(243,128,32,0.3)] transition-shadow duration-300 hover:scale-[1.03] hover:shadow-[0_0_32px_rgba(243,128,32,0.5)] sm:px-8 sm:py-3.5 sm:text-base"
          variants={fadeUp}
          onClick={() => {
            document.getElementById("pairs")?.scrollIntoView({ behavior: "smooth" });
          }}
        >
          <span className="flex items-center gap-2">
            Explore All 19 Pairs
            <ArrowRight className="h-4 w-4" />
          </span>
        </motion.button>
      </motion.div>
      <motion.div
        className="absolute bottom-8 left-1/2 z-10 -translate-x-1/2"
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 2, duration: 0.6 }}
      >
    <motion.div
      animate={{ y: [0, 8, 0] }}
      transition={{ duration: 1.8, repeat: Infinity, ease: "easeInOut" }}
    >
      <ChevronDown className="h-6 w-6 text-muted-foreground/60" />
    </motion.div>
  </motion.div>

    </section>
  );
}
