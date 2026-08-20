"use client";

import { useState, useEffect, useCallback, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  User,
  HeartHandshake,
  Sparkles,
  Play,
  RotateCcw,
  ArrowRight,
} from "lucide-react";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { Card, CardContent } from "@/components/ui/card";
import { PAIRS, type AvatarAidePair } from "@/lib/avatar-pairs-data";
import { cn } from "@/lib/utils";

const STEP_LABELS = ["Avatar Struggles", "Aide Coaching", "Advocate Fusion"] as const;
const STEP_DESCRIPTIONS = [
  "The Avatar experiences authentic ADHD challenges in real-time simulation",
  "Expert Aide provides targeted strategies and real-time guidance",
  "Experience and expertise merge into a powerful Advocate entity",
] as const;
const STEP_PROGRESS = [33, 66, 100] as const;
const AUTO_ADVANCE_MS = 2500;

export function FusionSimulator() {
  const [selectedPairId, setSelectedPairId] = useState<string>("1");
  const [step, setStep] = useState(0);
  const [running, setRunning] = useState(false);
  const [completed, setCompleted] = useState(false);
  const [fusionFlash, setFusionFlash] = useState(false);
  const [transitionFlash, setTransitionFlash] = useState(false);
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const stepRef = useRef(0);
  const flashTimersRef = useRef<ReturnType<typeof setTimeout>[]>([]);

  const pair = PAIRS.find((p) => p.id === Number(selectedPairId)) ?? PAIRS[0];

  const clearTimer = useCallback(() => {
    if (timerRef.current) {
      clearTimeout(timerRef.current);
      timerRef.current = null;
    }
  }, []);

  const clearFlashTimers = useCallback(() => {
    flashTimersRef.current.forEach(clearTimeout);
    flashTimersRef.current = [];
  }, []);

  const reset = useCallback(() => {
    clearTimer();
    clearFlashTimers();
    setStep(0);
    setRunning(false);
    setCompleted(false);
    setFusionFlash(false);
    setTransitionFlash(false);
  }, [clearTimer, clearFlashTimers]);

  // Keep stepRef in sync so advanceStep can read current step outside updater
  useEffect(() => {
    stepRef.current = step;
  }, [step]);

  const advanceStep = useCallback(() => {
    clearTimer();
    clearFlashTimers();
    const prev = stepRef.current;
    const next = prev >= 2 ? 2 : prev + 1;
    // Pure state update — no side effects in updater
    setStep(next);

    // Side effects moved outside the updater
    if (next === 2) {
      setTransitionFlash(true);
      flashTimersRef.current.push(
        setTimeout(() => setTransitionFlash(false), 150)
      );
    }
    if (prev === 1) {
      setFusionFlash(true);
      flashTimersRef.current.push(
        setTimeout(() => setFusionFlash(false), 600)
      );
    }
    if (prev >= 2) {
      setRunning(false);
      setCompleted(true);
    }
  }, [clearTimer, clearFlashTimers]);

  useEffect(() => {
    if (running && step < 2) {
      timerRef.current = setTimeout(advanceStep, AUTO_ADVANCE_MS);
    }
    return clearTimer;
  }, [running, step, advanceStep, clearTimer]);

  useEffect(() => {
    requestAnimationFrame(() => reset());
  }, [selectedPairId, reset]);

  // Cleanup flash timers on unmount
  useEffect(() => {
    return clearFlashTimers;
  }, [clearFlashTimers]);

  const handleStart = () => {
    if (completed) {
      reset();
      return;
    }
    if (!running) {
      setRunning(true);
      setStep(0);
      setCompleted(false);
    } else {
      advanceStep();
    }
  };

  const progressValue = step === 0 && !running ? 0 : STEP_PROGRESS[step];

  return (
    <section
      id="simulator"
      className="py-16 md:py-24 px-4 sm:px-6 lg:px-8"
      style={{
        background:
          "radial-gradient(ellipse at top center, rgba(243,128,32,0.06) 0%, transparent 60%)",
      }}
      aria-label="Fusion Simulator"
    >
      <div className="mx-auto max-w-6xl space-y-6">
      {/* Section header */}
      <div className="text-center space-y-2">
        <h2 className="text-3xl font-bold tracking-tight">Fusion Simulator</h2>
        <p className="text-muted-foreground max-w-xl mx-auto">
          Watch an Avatar transform into an Advocate through experiential learning
        </p>
      </div>

      {/* Controls row */}
      <div className="flex flex-col sm:flex-row items-center justify-center gap-3">
        <Select value={selectedPairId} onValueChange={setSelectedPairId}>
          <SelectTrigger className="w-full sm:w-64">
            <SelectValue placeholder="Select a pair" />
          </SelectTrigger>
          <SelectContent>
            {PAIRS.map((p) => (
              <SelectItem key={p.id} value={String(p.id)}>
                {p.avatarName} → {p.advocateName}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>

        <Button
          onClick={handleStart}
          disabled={running && step >= 2}
          className={cn(
            "w-full sm:w-auto min-w-[160px]",
            completed
              ? ""
              : "text-white"
          )}
          style={
            completed
              ? undefined
              : { backgroundColor: pair.color }
          }
          variant={completed ? "outline" : "default"}
        >
          {completed ? (
            <>
              <RotateCcw className="mr-2 h-4 w-4" />
              Reset
            </>
          ) : (
            <>
              <Play className="mr-2 h-4 w-4" />
              {running ? "Next Step" : "Start Simulation"}
            </>
          )}
        </Button>
      </div>

      {/* Step indicators */}
      <div className="flex items-center justify-center gap-2">
        {[0, 1, 2].map((s) => (
          <div key={s} className="flex items-center gap-2">
            <div
              className={cn(
                "flex h-8 w-8 items-center justify-center rounded-full text-xs font-bold transition-all duration-300",
                step > s
                  ? "text-white"
                  : step === s && running
                    ? "text-white ring-2 ring-offset-2 ring-offset-background"
                    : "bg-muted text-muted-foreground"
              )}
              style={
                step > s
                  ? { backgroundColor: pair.color }
                  : step === s && running
                    ? ({ backgroundColor: pair.color, ringColor: pair.color } as React.CSSProperties)
                    : undefined
              }
            >
              {step > s ? "✓" : s + 1}
            </div>
            {s < 2 && (
              <div
                className={cn(
                  "h-0.5 w-8 sm:w-12 rounded-full transition-colors duration-300",
                  step > s ? "" : "bg-muted"
                )}
                style={step > s ? { backgroundColor: pair.color } : undefined}
              />
            )}
          </div>
        ))}
      </div>

      {/* Current step label + description */}
      <AnimatePresence mode="wait">
        <div key={running || completed ? `step-${step}` : "idle"} className="text-center space-y-1">
          <motion.p
            initial={{ opacity: 0, y: -8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 8 }}
            transition={{ duration: 0.2 }}
            className="text-sm font-medium text-muted-foreground"
          >
            {running || completed
              ? `Step ${step + 1}: ${STEP_LABELS[step]}`
              : "Select a pair and press Start"}
          </motion.p>
          {(running || completed) && (
            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.3, delay: 0.1 }}
              className="text-xs text-muted-foreground/60"
            >
              {STEP_DESCRIPTIONS[step]}
            </motion.p>
          )}
        </div>
      </AnimatePresence>

      {/* Visualization area */}
      <Card className={cn("relative overflow-hidden", !running && !completed && "simulator-idle-border")}>
        <CardContent className="p-4 sm:p-6">
          <div className="dot-grid-bg absolute inset-0 pointer-events-none" aria-hidden="true" />
          {/* Transition flash overlay (brief white/brand flash on step change) */}
          <AnimatePresence>
            {transitionFlash && (
              <motion.div
                key="transition-flash"
                initial={{ opacity: 0 }}
                animate={{ opacity: [0, 0.35, 0] }}
                exit={{ opacity: 0 }}
                transition={{ duration: 0.15 }}
                className="absolute inset-0 z-20 rounded-lg pointer-events-none"
                style={{ backgroundColor: "white" }}
              />
            )}
          </AnimatePresence>
          <div className="relative min-h-[320px] sm:min-h-[360px]">
            <AnimatePresence mode="wait">
              {/* Idle state */}
              {!running && !completed && (
                <motion.div
                  key="idle"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="absolute inset-0 flex flex-col items-center justify-center gap-4 text-muted-foreground"
                >
                  <div className="flex items-center gap-6">
                    <motion.div
                      animate={{ y: [0, -6, 0] }}
                      transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
                    >
                      <User className="h-12 w-12 opacity-30" />
                    </motion.div>
                    <ArrowRight className="h-6 w-6 opacity-20" />
                    <motion.div
                      animate={{ y: [0, -6, 0] }}
                      transition={{ duration: 2, repeat: Infinity, ease: "easeInOut", delay: 0.3 }}
                    >
                      <HeartHandshake className="h-12 w-12 opacity-30" />
                    </motion.div>
                    <ArrowRight className="h-6 w-6 opacity-20" />
                    <motion.div
                      animate={{ y: [0, -6, 0] }}
                      transition={{ duration: 2, repeat: Infinity, ease: "easeInOut", delay: 0.6 }}
                    >
                      <Sparkles className="h-12 w-12 opacity-30" />
                    </motion.div>
                  </div>
                  <p className="text-sm">Choose a pair above and start the simulation</p>
                </motion.div>
              )}

              {/* Step 1: Avatar Struggles */}
              {running && step === 0 && (
                <motion.div
                  key="step1"
                  initial={{ opacity: 0, x: 40, scale: 0.95 }}
                  animate={{ opacity: 1, x: 0, scale: 1 }}
                  exit={{ opacity: 0, x: -40, scale: 0.95 }}
                  transition={{ duration: 0.4 }}
                  className="absolute inset-0 flex flex-col items-center justify-center gap-4"
                >
                  <div
                    className="rounded-xl p-6 sm:p-8 w-full max-w-md text-center"
                    style={{ backgroundColor: `${pair.color}08` }}
                  >
                    <motion.div
                      initial={{ scale: 0.5, opacity: 0 }}
                      animate={{ scale: 1, opacity: 1 }}
                      transition={{ type: "spring", stiffness: 200, damping: 15 }}
                      className="mx-auto mb-3 flex h-16 w-16 items-center justify-center rounded-full"
                      style={{ backgroundColor: `${pair.color}20` }}
                    >
                      <User className="h-8 w-8" style={{ color: pair.color }} />
                    </motion.div>
                    <motion.h3
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: 0.15 }}
                      className="text-lg font-bold"
                    >
                      {pair.avatarName}
                    </motion.h3>
                    <motion.p
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{ delay: 0.25 }}
                      className="text-xs text-muted-foreground mb-4"
                    >
                      {pair.trait}
                    </motion.p>
                    <div className="space-y-2 text-left">
                      {pair.avatarStruggles.slice(0, 4).map((struggle, i) => (
                        <motion.div
                          key={i}
                          initial={{ opacity: 0, x: -20 }}
                          animate={{ opacity: 1, x: 0 }}
                          transition={{ delay: 0.35 + i * 0.15, duration: 0.35 }}
                          className="flex items-start gap-2 text-sm"
                        >
                          <span
                            className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full"
                            style={{ backgroundColor: pair.color }}
                          />
                          <span className="text-foreground/80">{struggle}</span>
                        </motion.div>
                      ))}
                    </div>
                  </div>
                </motion.div>
              )}

              {/* Step 2: Aide Coaching */}
              {running && step === 1 && (
                <motion.div
                  key="step2"
                  initial={{ opacity: 0, x: 40, scale: 0.95 }}
                  animate={{ opacity: 1, x: 0, scale: 1 }}
                  exit={{ opacity: 0, x: -40, scale: 0.95 }}
                  transition={{ duration: 0.4 }}
                  className="absolute inset-0 flex flex-col items-center justify-center gap-4"
                >
                  {/* Connection pulse from Avatar to Aide */}
                  <div className="w-full max-w-lg px-4">
                    <div className="flex items-center justify-between mb-4">
                      <motion.div
                        initial={{ scale: 0.8, opacity: 0.5 }}
                        animate={{ scale: 1, opacity: 1 }}
                        className="flex items-center gap-2 text-xs text-muted-foreground"
                      >
                        <User className="h-4 w-4" style={{ color: pair.color }} />
                        <span>{pair.avatarName}</span>
                      </motion.div>

                      <div className="flex-1 mx-3 relative h-0.5 bg-muted rounded-full">
                        <motion.div
                          initial={{ width: "0%" }}
                          animate={{ width: "100%" }}
                          transition={{ duration: 1.2, ease: "easeInOut" }}
                          className="absolute inset-y-0 left-0 rounded-full"
                          style={{ backgroundColor: pair.color }}
                        />
                        <motion.div
                          initial={{ left: "0%" }}
                          animate={{ left: "100%" }}
                          transition={{ duration: 1.2, ease: "easeInOut" }}
                          className="absolute top-1/2 -translate-y-1/2 -translate-x-1/2 h-3 w-3 rounded-full"
                          style={{ backgroundColor: pair.color, boxShadow: `0 0 8px ${pair.color}60` }}
                        />
                      </div>

                      <motion.div
                        initial={{ scale: 0.8, opacity: 0.5 }}
                        animate={{ scale: 1, opacity: 1 }}
                        transition={{ delay: 1.2 }}
                        className="flex items-center gap-2 text-xs font-medium"
                        style={{ color: pair.color }}
                      >
                        <span>{pair.aideName}</span>
                        <HeartHandshake className="h-4 w-4" />
                      </motion.div>
                    </div>
                  </div>

                  <div
                    className="rounded-xl p-6 sm:p-8 w-full max-w-md text-center"
                    style={{ backgroundColor: `${pair.color}08` }}
                  >
                    <motion.div
                      initial={{ scale: 0.5, opacity: 0 }}
                      animate={{ scale: 1, opacity: 1 }}
                      transition={{ type: "spring", stiffness: 200, damping: 15, delay: 1.3 }}
                      className="mx-auto mb-3 flex h-16 w-16 items-center justify-center rounded-full"
                      style={{ backgroundColor: `${pair.color}20` }}
                    >
                      <HeartHandshake className="h-8 w-8" style={{ color: pair.color }} />
                    </motion.div>
                    <motion.h3
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: 1.45 }}
                      className="text-lg font-bold"
                    >
                      {pair.aideName}
                    </motion.h3>
                    <motion.p
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{ delay: 1.55 }}
                      className="text-xs text-muted-foreground mb-4"
                    >
                      Expertise &amp; Coaching
                    </motion.p>
                    <div className="space-y-2 text-left">
                      {pair.aideExpertise.slice(0, 4).map((exp, i) => (
                        <motion.div
                          key={i}
                          initial={{ opacity: 0, x: -20 }}
                          animate={{ opacity: 1, x: 0 }}
                          transition={{ delay: 1.65 + i * 0.15, duration: 0.35 }}
                          className="flex items-start gap-2 text-sm"
                        >
                          <span
                            className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full"
                            style={{ backgroundColor: pair.color }}
                          />
                          <span className="text-foreground/80">{exp}</span>
                        </motion.div>
                      ))}
                    </div>
                  </div>
                </motion.div>
              )}

              {/* Step 3: Advocate Fusion */}
              {step === 2 && (running || completed) && (
                <motion.div
                  key="step3"
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.95 }}
                  transition={{ duration: 0.4 }}
                  className="absolute inset-0 flex flex-col items-center justify-center gap-4"
                >
                  {/* Fusion flash overlay */}
                  <AnimatePresence>
                    {fusionFlash && (
                      <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: [0, 0.6, 0] }}
                        exit={{ opacity: 0 }}
                        transition={{ duration: 0.6 }}
                        className="absolute inset-0 z-10 rounded-lg"
                        style={{
                          backgroundColor: pair.color,
                          mixBlendMode: "overlay",
                        }}
                      />
                    )}
                  </AnimatePresence>

                  {/* Two sides merging to center */}
                  <div className="w-full max-w-lg px-4 mb-2">
                    <div className="flex items-center justify-center gap-4">
                      <motion.div
                        initial={{ x: -80, opacity: 0 }}
                        animate={{ x: 0, opacity: 0.4 }}
                        transition={{ duration: 0.8, ease: "easeOut" }}
                        className="flex items-center gap-1.5 text-xs text-muted-foreground"
                      >
                        <User className="h-4 w-4" />
                        <span>{pair.avatarName}</span>
                      </motion.div>

                      <motion.div
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        transition={{
                          type: "spring",
                          stiffness: 150,
                          damping: 12,
                          delay: 0.5,
                        }}
                        className="flex items-center gap-1.5 text-xs font-semibold"
                        style={{ color: pair.color }}
                      >
                        <span>Fusion</span>
                        <ArrowRight className="h-3 w-3" />
                      </motion.div>

                      <motion.div
                        initial={{ x: 80, opacity: 0 }}
                        animate={{ x: 0, opacity: 0.4 }}
                        transition={{ duration: 0.8, ease: "easeOut" }}
                        className="flex items-center gap-1.5 text-xs text-muted-foreground"
                      >
                        <span>{pair.aideName}</span>
                        <HeartHandshake className="h-4 w-4" />
                      </motion.div>
                    </div>
                  </div>

                  {/* Advocate result */}
                  <motion.div
                    initial={{ scale: 0, rotate: -10 }}
                    animate={{ scale: 1, rotate: 0 }}
                    transition={{
                      type: "spring",
                      stiffness: 120,
                      damping: 10,
                      delay: 0.6,
                    }}
                    className="rounded-xl p-6 sm:p-8 w-full max-w-md text-center relative"
                    style={{ backgroundColor: `${pair.color}08` }}
                  >
                    {/* Glow ring behind icon */}
                    <motion.div
                      initial={{ scale: 0.5, opacity: 0 }}
                      animate={{ scale: [1, 1.15, 1], opacity: [0.3, 0.6, 0.3] }}
                      transition={{
                        duration: 2,
                        repeat: Infinity,
                        ease: "easeInOut",
                        delay: 1.2,
                      }}
                      className="absolute top-6 left-1/2 -translate-x-1/2 h-20 w-20 rounded-full"
                      style={{
                        backgroundColor: pair.color,
                        filter: "blur(20px)",
                      }}
                    />

                    <motion.div
                      initial={{ scale: 0, opacity: 0 }}
                      animate={{ scale: 1, opacity: 1 }}
                      transition={{
                        type: "spring",
                        stiffness: 200,
                        damping: 12,
                        delay: 0.8,
                      }}
                      className="relative mx-auto mb-3 flex h-16 w-16 items-center justify-center rounded-full"
                      style={{ backgroundColor: `${pair.color}25` }}
                    >
                      <Sparkles className="h-8 w-8" style={{ color: pair.color }} />
                    </motion.div>

                    <motion.h3
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: 1.0 }}
                      className="relative text-xl font-bold"
                    >
                      {pair.advocateName}
                    </motion.h3>

                    <motion.p
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{ delay: 1.2 }}
                      className="relative text-xs text-muted-foreground mb-4"
                    >
                      {pair.trait} — Fused Advocate
                    </motion.p>

                    <motion.div
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: 1.4 }}
                      className="relative rounded-lg p-3"
                      style={{ backgroundColor: `${pair.color}10` }}
                    >
                      <p className="text-sm font-medium leading-relaxed" style={{ color: pair.color }}>
                        &ldquo;{pair.advocateStrength}&rdquo;
                      </p>
                    </motion.div>
                  </motion.div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          {/* Progress bar */}
          <div className="mt-6 space-y-1.5">
            <div className="flex justify-between text-xs text-muted-foreground">
              <span>Simulation Progress</span>
              <span>{progressValue}%</span>
            </div>
            <Progress value={progressValue} className="h-2" />
          </div>
        </CardContent>
      </Card>
    </div>
    </section>
  );
}
