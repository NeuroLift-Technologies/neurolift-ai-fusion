"use client";

import { useState, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  X,
  User,
  HeartHandshake,
  Sparkles,
  ArrowRight,
  CheckCircle2,
  AlertTriangle,
  ChevronDown,
  ChevronLeft,
  ChevronRight,
  Eye,
  Shield,
  Target,
  Clock,
  Brain,
  Heart,
  Rocket,
  Flame,
  ListChecks,
  ArrowLeftRight,
  ScanEye,
  Mountain,
  Battery,
  Gauge,
  ShieldAlert,
  Ear,
  Users,
  Star,
  Circle,
  Share2,
  MessageSquare,
  Check,
} from "lucide-react";
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetDescription,
} from "@/components/ui/sheet";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Separator } from "@/components/ui/separator";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Button } from "@/components/ui/button";
import {
  Collapsible,
  CollapsibleTrigger,
  CollapsibleContent,
} from "@/components/ui/collapsible";
import {
  PAIRS,
  type AvatarAidePair,
  STATUS_CONFIG,
  EMPATHY_LABELS,
  CATEGORY_LABELS,
} from "@/lib/avatar-pairs-data";

// ─── Props ───────────────────────────────────────────────────────────
interface PairDetailSheetProps {
  pair: AvatarAidePair | null;
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onNavigate: (direction: "prev" | "next") => void;
}

// ─── Helpers ─────────────────────────────────────────────────────────
function getPairIndex(pair: AvatarAidePair): number {
  return PAIRS.findIndex((p) => p.id === pair.id);
}

function getStatusPhaseIndex(status: AvatarAidePair["status"]): number {
  switch (status) {
    case "concept":
      return 0;
    case "prototype":
      return 1;
    case "training":
      return 2;
    case "ready":
      return 3;
  }
}

function getReadinessMessage(
  status: AvatarAidePair["status"],
  score: number
): string {
  const pct = Math.round(score * 100);
  switch (status) {
    case "concept":
      return `Early concept stage — ${pct}% readiness. Foundation research and design exploration underway.`;
    case "prototype":
      return `Prototype in development — ${pct}% readiness. Core behaviors being built and tested.`;
    case "training":
      return `Training in progress — ${pct}% readiness. Learning from real ADHD experiences.`;
    case "ready":
      return `Fusion complete — ${pct}% readiness. Ready to support real users.`;
  }
}

function getEmpathyColor(level: AvatarAidePair["empathyLevel"]): string {
  switch (level) {
    case "theoretical":
      return "text-slate-400";
    case "observational":
      return "text-amber-500";
    case "experiential":
      return "text-emerald-500";
    case "deep_experiential":
      return "text-orange-500";
  }
}

function getEmpathyBg(level: AvatarAidePair["empathyLevel"]): string {
  switch (level) {
    case "theoretical":
      return "bg-slate-400/10";
    case "observational":
      return "bg-amber-500/10";
    case "experiential":
      return "bg-emerald-500/10";
    case "deep_experiential":
      return "bg-orange-500/10";
  }
}

// ─── Collapsible section component ───────────────────────────────────
function ExpandableSection({
  title,
  icon,
  accentColor,
  accentBg,
  children,
  defaultOpen = false,
}: {
  title: string;
  icon: React.ReactNode;
  accentColor: string;
  accentBg: string;
  children: React.ReactNode;
  defaultOpen?: boolean;
}) {
  const [isOpen, setIsOpen] = useState(defaultOpen);

  return (
    <Collapsible open={isOpen} onOpenChange={setIsOpen}>
      <CollapsibleTrigger asChild>
        <button
          className={`
            flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-left
            transition-colors duration-200 hover:bg-muted/50
            focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2
          `}
          style={{
            // @ts-expect-error CSS custom property
            "--ring-color": accentColor,
          }}
          aria-expanded={isOpen}
        >
          <div
            className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-lg ${accentBg}`}
            aria-hidden="true"
          >
            <span className={accentColor}>{icon}</span>
          </div>
          <span className="flex-1 text-sm font-semibold text-foreground">
            {title}
          </span>
          <motion.span
            animate={{ rotate: isOpen ? 180 : 0 }}
            transition={{ duration: 0.2 }}
            className="text-muted-foreground"
            aria-hidden="true"
          >
            <ChevronDown className="h-4 w-4" />
          </motion.span>
        </button>
      </CollapsibleTrigger>
      <CollapsibleContent>
        <motion.div
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: "auto" }}
          exit={{ opacity: 0, height: 0 }}
          transition={{ duration: 0.25, ease: "easeOut" }}
          className="overflow-hidden"
        >
          <div className="px-3 pb-4 pt-2">{children}</div>
        </motion.div>
      </CollapsibleContent>
    </Collapsible>
  );
}

// ─── Collapsible Section (major content sections with centralized state) ────
function CollapsibleSection({
  sectionKey,
  title,
  isOpen,
  onToggle,
  children,
}: {
  sectionKey: string;
  title: string;
  isOpen: boolean;
  onToggle: (key: string) => void;
  children: React.ReactNode;
}) {
  return (
    <Collapsible
      open={isOpen}
      onOpenChange={() => onToggle(sectionKey)}
      className="mb-6"
    >
      <CollapsibleTrigger asChild>
        <button
          type="button"
          className="flex w-full items-center justify-between hover:bg-muted/50 rounded-lg px-3 py-2 -mx-3 transition-colors"
          aria-expanded={isOpen}
        >
          <h3 className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
            {title}
          </h3>
          <motion.span
            animate={{ rotate: isOpen ? 180 : 0 }}
            transition={{ duration: 0.2 }}
            className="text-muted-foreground"
            aria-hidden="true"
          >
            <ChevronDown className="h-4 w-4" />
          </motion.span>
        </button>
      </CollapsibleTrigger>
      <CollapsibleContent>
        <motion.div
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: "auto" }}
          transition={{ duration: 0.25, ease: "easeOut" }}
          className="overflow-hidden"
        >
          <div className="pt-1">{children}</div>
        </motion.div>
      </CollapsibleContent>
    </Collapsible>
  );
}

// ─── Pipeline step component ─────────────────────────────────────────
function PipelineStep({
  label,
  icon,
  isActive,
  isCompleted,
  accentColor,
}: {
  label: string;
  icon: React.ReactNode;
  isActive: boolean;
  isCompleted: boolean;
  accentColor: string;
}) {
  return (
    <motion.div
      className={`flex flex-col items-center gap-1.5 ${isCompleted ? "opacity-100" : isActive ? "opacity-100" : "opacity-50"}`}
      animate={{ scale: isActive ? 1.05 : 1 }}
      transition={{ duration: 0.3, ease: "easeOut" }}
    >
      <div
        className={`
          flex h-10 w-10 items-center justify-center rounded-xl border-2 transition-all duration-300
          ${isActive ? "shadow-md" : ""}
        `}
        style={{
          borderColor: isActive || isCompleted ? accentColor : undefined,
          backgroundColor: isActive
            ? `${accentColor}15`
            : isCompleted
              ? `${accentColor}08`
              : undefined,
        }}
      >
        <span style={{ color: isActive || isCompleted ? accentColor : undefined }}>
          {icon}
        </span>
      </div>
      <span
        className={`max-w-[72px] text-center text-[11px] font-medium leading-tight ${isActive ? "text-foreground" : "text-muted-foreground"}`}
      >
        {label}
      </span>
    </motion.div>
  );
}

// ─── Animated connector arrow ────────────────────────────────────────
function ConnectorArrow({
  active,
  color,
}: {
  active: boolean;
  color: string;
}) {
  return (
    <div className="flex flex-col items-center gap-0.5">
      <motion.div
        className="h-0.5 w-8 rounded-full"
        style={{ backgroundColor: active ? color : "hsl(var(--muted-foreground) / 0.2)" }}
        initial={{ scaleX: 0 }}
        animate={{ scaleX: 1 }}
        transition={{ duration: 0.5, ease: "easeOut" }}
      />
      <motion.div
        animate={{ x: active ? [0, 3, 0] : 0 }}
        transition={
          active
            ? { duration: 1.2, repeat: Infinity, ease: "easeInOut" }
            : { duration: 0.3 }
        }
      >
        <ArrowRight
          className={`h-3 w-3 ${active ? "" : "text-muted-foreground/20"}`}
          style={{ color: active ? color : undefined }}
        />
      </motion.div>
    </div>
  );
}

// ─── Fusion Journey Visualization ──────────────────────────────────────
type JourneyStep = 0 | 1 | 2;

function FusionJourney({ pair, hideHeading }: { pair: AvatarAidePair; hideHeading?: boolean }) {
  const [activeStep, setActiveStep] = useState<JourneyStep | null>(null);

  const steps: {
    icon: React.ReactNode;
    name: string;
    label: string;
  }[] = [
    { icon: <User className="h-5 w-5" />, name: pair.avatarName, label: "Avatar" },
    { icon: <HeartHandshake className="h-5 w-5" />, name: pair.aideName, label: "Aide" },
    { icon: <Sparkles className="h-5 w-5" />, name: pair.advocateName, label: "Advocate" },
  ];

  const journeyContent = (
    <div className="rounded-xl border border-border/60 bg-muted/30 p-4">
      {/* Steps: vertical on mobile, horizontal on sm+ */}
      <div className="flex flex-col items-center gap-0 sm:flex-row sm:gap-0">
        {steps.map((step, i) => {
            const isActive = activeStep === (i as JourneyStep);
            return (
              <div
                key={i}
                className="flex flex-col items-center sm:flex-row sm:flex-1"
              >
                {/* Vertical connector for mobile (before circle, not first) */}
                {i > 0 && (
                  <motion.div
                    className="my-1 h-6 w-px rounded-full sm:hidden"
                    style={{
                      backgroundColor:
                        activeStep !== null && activeStep >= (i as JourneyStep)
                          ? pair.color
                          : "hsl(var(--muted-foreground) / 0.15)",
                    }}
                    initial={{ scaleY: 0 }}
                    animate={{ scaleY: 1 }}
                    transition={{ duration: 0.4, delay: i * 0.1 }}
                  />
                )}
                {/* Circle button */}
                <button
                  type="button"
                  onClick={() =>
                    setActiveStep(isActive ? null : (i as JourneyStep))
                  }
                  className="group relative flex flex-col items-center gap-2 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 rounded-lg"
                  style={{ "--ring-color": pair.color } as React.CSSProperties}
                  aria-label={`${step.label}: ${step.name}${isActive ? " (selected)" : ""}`}
                  aria-pressed={isActive}
                >
                  <div className="relative">
                    {/* Pulse ring for active step */}
                    {isActive && (
                      <motion.div
                        className="absolute inset-[-6px] rounded-full"
                        style={{ backgroundColor: `${pair.color}25` }}
                        animate={{
                          scale: [1, 1.35, 1],
                          opacity: [0.5, 0, 0.5],
                        }}
                        transition={{
                          duration: 2,
                          repeat: Infinity,
                          ease: "easeInOut",
                        }}
                      />
                    )}
                    <motion.div
                      className="relative flex h-14 w-14 items-center justify-center rounded-full border-2 transition-colors duration-200"
                      style={{
                        borderColor: isActive ? pair.color : "hsl(var(--border))",
                        backgroundColor: isActive ? `${pair.color}15` : "transparent",
                      }}
                      whileHover={{ scale: 1.08 }}
                      whileTap={{ scale: 0.95 }}
                    >
                      <span
                        style={{
                          color: isActive
                            ? pair.color
                            : "hsl(var(--muted-foreground))",
                        }}
                      >
                        {step.icon}
                      </span>
                    </motion.div>
                  </div>
                  <div className="text-center">
                    <p
                      className={`text-xs font-semibold leading-tight ${
                        isActive ? "text-foreground" : "text-muted-foreground"
                      }`}
                    >
                      {step.label}
                    </p>
                    <p className="text-[11px] text-muted-foreground/70">
                      {step.name}
                    </p>
                  </div>
                </button>
                {/* Horizontal connector for desktop (after circle, not last) */}
                {i < steps.length - 1 && (
                  <div className="hidden sm:flex flex-1 items-center mx-3">
                    <motion.div
                      className="h-0.5 w-full rounded-full"
                      style={{
                        backgroundColor:
                          activeStep !== null && activeStep >= (i as JourneyStep)
                            ? pair.color
                            : "hsl(var(--muted-foreground) / 0.15)",
                      }}
                      initial={{ scaleX: 0 }}
                      animate={{ scaleX: 1 }}
                      transition={{
                        duration: 0.5,
                        delay: i * 0.15,
                        ease: "easeOut",
                      }}
                    />
                  </div>
                )}
              </div>
            );
          })}
        </div>

        {/* Collapsible description panel */}
        <AnimatePresence>
          {activeStep !== null && (
            <motion.div
              key={`journey-desc-${activeStep}`}
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: "auto" }}
              exit={{ opacity: 0, height: 0 }}
              transition={{ duration: 0.3, ease: "easeOut" }}
              className="overflow-hidden"
            >
              <div
                className="mt-4 rounded-lg border p-3.5"
                style={{
                  borderColor: `${pair.color}20`,
                  backgroundColor: `${pair.color}05`,
                }}
              >
                {activeStep === 0 && (
                  <div>
                    <p
                      className="mb-2 text-xs font-semibold uppercase tracking-wider"
                      style={{ color: pair.color }}
                    >
                      What {pair.avatarName} Struggles With
                    </p>
                    <ul className="space-y-1.5">
                      {pair.avatarStruggles.slice(0, 3).map((s, j) => (
                        <motion.li
                          key={j}
                          initial={{ opacity: 0, x: -8 }}
                          animate={{ opacity: 1, x: 0 }}
                          transition={{ duration: 0.2, delay: j * 0.05 }}
                          className="flex items-start gap-2 text-sm text-muted-foreground"
                        >
                          <span
                            className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full"
                            style={{ backgroundColor: pair.color }}
                          />
                          {s}
                        </motion.li>
                      ))}
                    </ul>
                  </div>
                )}
                {activeStep === 1 && (
                  <div>
                    <p
                      className="mb-2 text-xs font-semibold uppercase tracking-wider"
                      style={{ color: pair.color }}
                    >
                      How {pair.aideName} Helps
                    </p>
                    <ul className="space-y-1.5">
                      {pair.aideExpertise.slice(0, 3).map((s, j) => (
                        <motion.li
                          key={j}
                          initial={{ opacity: 0, x: -8 }}
                          animate={{ opacity: 1, x: 0 }}
                          transition={{ duration: 0.2, delay: j * 0.05 }}
                          className="flex items-start gap-2 text-sm text-muted-foreground"
                        >
                          <CheckCircle2
                            className="mt-0.5 h-4 w-4 shrink-0"
                            style={{ color: pair.color }}
                          />
                          {s}
                        </motion.li>
                      ))}
                    </ul>
                  </div>
                )}
                {activeStep === 2 && (
                  <div>
                    <p
                      className="mb-2 text-xs font-semibold uppercase tracking-wider"
                      style={{ color: pair.color }}
                    >
                      When They Fuse: {pair.advocateName}
                    </p>
                    <p className="text-sm font-medium leading-relaxed text-foreground italic">
                      &ldquo;{pair.advocateStrength}&rdquo;
                    </p>
                  </div>
                )}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
  );

  if (hideHeading) {
    return journeyContent;
  }

  return (
    <section aria-label="Fusion Journey" className="mb-6">
      <h3 className="mb-3 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
        Fusion Journey
      </h3>
      {journeyContent}
    </section>
  );
}

// ─── Readiness Gauge (Radial/Donut) ────────────────────────────────────
function ReadinessGauge({
  value,
  color,
  size = 80,
}: {
  value: number;
  color: string;
  size?: number;
}) {
  const pct = Math.round(value * 100);
  const strokeWidth = 6;
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const center = size / 2;

  return (
    <div className="relative shrink-0" style={{ width: size, height: size }}>
      <svg
        className="-rotate-90"
        width={size}
        height={size}
        viewBox={`0 0 ${size} ${size}`}
        aria-hidden="true"
      >
        {/* Background track */}
        <circle
          cx={center}
          cy={center}
          r={radius}
          fill="none"
          stroke="hsl(var(--muted))"
          strokeWidth={strokeWidth}
          opacity={0.25}
        />
        {/* Progress ring */}
        <motion.circle
          cx={center}
          cy={center}
          r={radius}
          fill="none"
          stroke={color}
          strokeWidth={strokeWidth}
          strokeLinecap="round"
          strokeDasharray={circumference}
          initial={{ strokeDashoffset: circumference }}
          animate={{
            strokeDashoffset: circumference - circumference * value,
          }}
          transition={{ duration: 1, ease: "easeOut", delay: 0.2 }}
        />
      </svg>
      {/* Center percentage */}
      <div className="absolute inset-0 flex items-center justify-center">
        <motion.span
          className="text-lg font-bold tabular-nums"
          style={{ color }}
          initial={{ opacity: 0, scale: 0.7 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.4, delay: 0.5 }}
        >
          {pct}
          <span className="text-xs font-semibold">%</span>
        </motion.span>
      </div>
    </div>
  );
}

// ─── Empathy Wave ──────────────────────────────────────────────────────
const EMPATHY_LEVELS: AvatarAidePair["empathyLevel"][] = [
  "theoretical",
  "observational",
  "experiential",
  "deep_experiential",
];

const EMPATHY_WAVE_LABELS: Record<AvatarAidePair["empathyLevel"], string> = {
  theoretical: "Theoretical",
  observational: "Observational",
  experiential: "Experiential",
  deep_experiential: "Deep Experiential",
};

function EmpathyWave({
  level,
  color,
}: {
  level: AvatarAidePair["empathyLevel"];
  color: string;
}) {
  const currentIdx = EMPATHY_LEVELS.indexOf(level);

  return (
    <div className="flex flex-col gap-2.5">
      {EMPATHY_LEVELS.map((lvl, i) => {
        const isFilled = i <= currentIdx;
        const opacity = isFilled
          ? 0.4 + (i / (EMPATHY_LEVELS.length - 1)) * 0.6
          : 0.1;
        return (
          <div key={lvl} className="flex items-center gap-2.5">
            <div
              className="h-3.5 w-full max-w-[160px] overflow-hidden rounded-full"
              style={{
                backgroundColor: isFilled
                  ? "transparent"
                  : "hsl(var(--muted) / 0.15)",
              }}
            >
              <motion.div
                className="h-full rounded-full"
                style={{ backgroundColor: color, opacity }}
                initial={{ width: 0 }}
                animate={{ width: isFilled ? "100%" : "0%" }}
                transition={{
                  duration: 0.6,
                  delay: 0.2 + i * 0.12,
                  ease: "easeOut",
                }}
              />
            </div>
            <span
              className={`text-[11px] font-medium whitespace-nowrap ${
                isFilled ? "text-foreground" : "text-muted-foreground/40"
              }`}
            >
              {EMPATHY_WAVE_LABELS[lvl]}
            </span>
          </div>
        );
      })}
    </div>
  );
}

// ─── Module-level insight cache (persists across mount/unmount) ──────
const insightCache = new Map<number, string>();

// ─── Share button component ──────────────────────────────────────
function ShareButton({ pairId }: { pairId: number }) {
  const [copied, setCopied] = useState(false);

  const handleShare = async () => {
    const url = `${window.location.origin}${window.location.pathname}?pair=${pairId}`;
    try {
      await navigator.clipboard.writeText(url);
    } catch {
      // Fallback for environments without clipboard API
      const textarea = document.createElement("textarea");
      textarea.value = url;
      document.body.appendChild(textarea);
      textarea.select();
      document.execCommand("copy");
      document.body.removeChild(textarea);
    }
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  };

  return (
    <Button
      variant="ghost"
      size="sm"
      onClick={handleShare}
      aria-label={copied ? "Link copied" : "Share this pair"}
      className="h-8 gap-1.5 px-2.5 text-xs"
    >
      {copied ? (
        <>
          <Check className="h-3.5 w-3.5 text-emerald-500" />
          <span className="text-emerald-500">Copied!</span>
        </>
      ) : (
        <>
          <Share2 className="h-3.5 w-3.5" />
          <span className="hidden sm:inline">Share</span>
        </>
      )}
    </Button>
  );
}

// ─── AI Insight collapsible section ──────────────────────────────────
function AIInsightSection({ pairId }: { pairId: number }) {
  const [insight, setInsight] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const mountedRef = useRef(true);

  useEffect(() => {
    mountedRef.current = true;

    // Check cache first
    const cached = insightCache.get(pairId);
    if (cached) {
      requestAnimationFrame(() => {
        setInsight(cached);
        setLoading(false);
        setError(false);
      });
      return;
    }

    let cancelled = false;
    requestAnimationFrame(() => {
      setLoading(true);
      setError(false);
      setInsight(null);
    });

    fetch(`/api/insights?pairId=${pairId}`)
      .then((res) => {
        if (!res.ok) throw new Error(res.statusText);
        return res.json();
      })
      .then((data) => {
        if (cancelled) return;
        if (data.insight) {
          insightCache.set(pairId, data.insight);
          setInsight(data.insight);
        } else {
          setError(true);
        }
      })
      .catch(() => {
        if (!cancelled) setError(true);
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => {
      cancelled = true;
      mountedRef.current = false;
    };
  }, [pairId]);

  return (
    <ExpandableSection
      title="AI Insight"
      icon={<Sparkles className="h-4 w-4" />}
      accentColor="text-amber-500"
      accentBg="bg-amber-500/10"
      defaultOpen={true}
    >
      {loading && (
        <div className="space-y-3">
          <Skeleton className="h-4 w-full" />
          <Skeleton className="h-4 w-[85%]" />
          <Skeleton className="h-4 w-[60%]" />
        </div>
      )}
      {!loading && error && (
        <p className="text-sm italic text-muted-foreground/70">
          AI insight unavailable — this pair&apos;s training insights are based on
          the research data above.
        </p>
      )}
      {!loading && insight && (
        <p className="text-sm leading-relaxed text-foreground/80">{insight}</p>
      )}
    </ExpandableSection>
  );
}

// ─── Main component ──────────────────────────────────────────────────
export function PairDetailSheet({
  pair,
  open,
  onOpenChange,
  onNavigate,
}: PairDetailSheetProps) {
  // Touch swipe navigation refs & state
  const touchStartXRef = useRef<number>(0);
  const touchStartYRef = useRef<number>(0);
  const touchStartTimeRef = useRef<number>(0);
  const [swipeOffset, setSwipeOffset] = useState(0);

  // Collapsible sections state (all expanded by default)
  const [openSections, setOpenSections] = useState<Record<string, boolean>>({
    "key-metrics": true,
    "fusion-journey": true,
    "development-roadmap": true,
  });
  const toggleSection = (key: string) => {
    setOpenSections((prev) => ({ ...prev, [key]: !prev[key] }));
  };

  if (!pair) return null;

  const statusConf = STATUS_CONFIG[pair.status];
  const empathyLabel = EMPATHY_LABELS[pair.empathyLevel];
  const categoryLabel = CATEGORY_LABELS[pair.category];
  const readinessPct = Math.round(pair.readinessScore * 100);
  const pairIndex = getPairIndex(pair);
  const isFirst = pairIndex <= 0;
  const isLast = pairIndex >= PAIRS.length - 1;
  const phaseIdx = getStatusPhaseIndex(pair.status);

  // Phase map for pipeline: concept→avatar, prototype→aide, training/ready→advocate
  const avatarPhase = 0;
  const aidePhase = 1;
  const advocatePhase = 2;

  // Touch swipe navigation handlers
  const SWIPE_THRESHOLD = 60;
  const SWIPE_MAX_TIME = 500;
  const SWIPE_MAX_OFFSET = 30;

  const handleTouchStart = (e: React.TouchEvent<HTMLDivElement>) => {
    touchStartXRef.current = e.touches[0].clientX;
    touchStartYRef.current = e.touches[0].clientY;
    touchStartTimeRef.current = Date.now();
  };

  const handleTouchMove = (e: React.TouchEvent<HTMLDivElement>) => {
    const deltaX = e.touches[0].clientX - touchStartXRef.current;
    const deltaY = Math.abs(e.touches[0].clientY - touchStartYRef.current);

    // Only handle horizontal swipes (ignore vertical scrolls)
    if (deltaY >= Math.abs(deltaX)) {
      setSwipeOffset(0);
      return;
    }

    // Clamp offset to max ±30px
    const clamped = Math.max(-SWIPE_MAX_OFFSET, Math.min(SWIPE_MAX_OFFSET, deltaX));
    setSwipeOffset(clamped);
  };

  const handleTouchEnd = (e: React.TouchEvent<HTMLDivElement>) => {
    const endX = e.changedTouches[0].clientX;
    const endY = e.changedTouches[0].clientY;
    const deltaX = endX - touchStartXRef.current;
    const deltaY = Math.abs(endY - touchStartYRef.current);
    const elapsed = Date.now() - touchStartTimeRef.current;

    setSwipeOffset(0);

    // Only handle horizontal swipes
    if (deltaY >= Math.abs(deltaX)) return;
    if (Math.abs(deltaX) < SWIPE_THRESHOLD) return;
    if (elapsed > SWIPE_MAX_TIME) return;

    if (deltaX > 0 && !isFirst) {
      onNavigate("prev");
    } else if (deltaX < 0 && !isLast) {
      onNavigate("next");
    }
  };

  return (
    <Sheet open={open} onOpenChange={onOpenChange}>
      <SheetContent
        side="right"
        className="w-full p-0 sm:max-w-[600px] lg:max-w-[640px]"
        aria-label={`${pair.avatarName} pair details`}
      >
        {/* ── Sticky Header ──────────────────────────────────── */}
        <div
          className={`
            sticky top-0 z-10 border-b bg-background/95 backdrop-blur-sm
          `}
          style={{ borderBottomColor: `${pair.color}20` }}
        >
          {/* Navigation row */}
          <div className="flex items-center justify-between px-4 pt-4 pb-0 sm:px-6">
            <div className="flex items-center gap-1">
              <Button
                variant="ghost"
                size="sm"
                onClick={() => onNavigate("prev")}
                disabled={isFirst}
                aria-label="Previous pair"
                className="h-8 w-8 p-0"
              >
                <ArrowRight className="h-4 w-4 rotate-180" />
              </Button>
              <span className="text-xs tabular-nums text-muted-foreground">
                {pairIndex + 1}/{PAIRS.length}
              </span>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => onNavigate("next")}
                disabled={isLast}
                aria-label="Next pair"
                className="h-8 w-8 p-0"
              >
                <ArrowRight className="h-4 w-4" />
              </Button>
            </div>
            {/* Share + Close */}
            <div className="flex items-center gap-1">
              <ShareButton pairId={pair.id} />
              <button
                onClick={() => onOpenChange(false)}
                className={`
                  rounded-md p-1.5 transition-colors duration-200
                  text-muted-foreground hover:bg-muted hover:text-foreground
                  focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2
                `}
                aria-label="Close details"
              >
                <X className="h-4 w-4" />
              </button>
            </div>
          </div>

          <SheetHeader className="gap-2 px-4 pb-4 pt-3 sm:px-6">
            <div className="flex items-start gap-3.5">
              {/* Large icon circle */}
              <motion.div
                key={`icon-${pair.id}`}
                initial={{ scale: 0.8, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                transition={{ duration: 0.35, ease: "easeOut" }}
                className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl"
                style={{ backgroundColor: `${pair.color}15` }}
                aria-hidden="true"
              >
                <PairIcon name={pair.iconName} color={pair.color} size={24} />
              </motion.div>

              <div className="flex items-center gap-1 min-w-0 flex-1">
                <Button
                  variant="ghost"
                  size="icon"
                  className="h-8 w-8 shrink-0"
                  onClick={() => onNavigate("prev")}
                  aria-label="Previous pair"
                >
                  <ChevronLeft className="h-4 w-4" />
                </Button>
                <div className="min-w-0 flex-1">
                <AnimatePresence mode="wait">
                  <motion.div
                    key={`header-${pair.id}`}
                    initial={{ opacity: 0, y: 8 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -8 }}
                    transition={{ duration: 0.25 }}
                  >
                    <SheetTitle className="text-xl font-bold tracking-tight sm:text-2xl">
                      {pair.avatarName}
                    </SheetTitle>
                    <SheetDescription className="mt-0.5 text-sm">
                      {pair.trait}
                    </SheetDescription>
                  </motion.div>
                </AnimatePresence>
                </div>
                <Button
                  variant="ghost"
                  size="icon"
                  className="h-8 w-8 shrink-0"
                  onClick={() => onNavigate("next")}
                  aria-label="Next pair"
                >
                  <ChevronRight className="h-4 w-4" />
                </Button>
              </div>
            </div>

            {/* Badges row */}
            <AnimatePresence mode="wait">
              <motion.div
                key={`badges-${pair.id}`}
                initial={{ opacity: 0, y: 6 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -6 }}
                transition={{ duration: 0.25, delay: 0.05 }}
                className="flex flex-wrap items-center gap-1.5"
              >
                <Badge
                  variant="secondary"
                  className={`${statusConf.bgColor} ${statusConf.color} border-0 text-[11px] font-medium`}
                >
                  {statusConf.label}
                </Badge>
                <Badge
                  variant="secondary"
                  className={`${pair.bgClass} ${pair.colorClass} border-0 text-[11px] font-medium`}
                >
                  {categoryLabel}
                </Badge>
                <Badge
                  variant="secondary"
                  className={`${getEmpathyBg(pair.empathyLevel)} ${getEmpathyColor(pair.empathyLevel)} border-0 text-[11px] font-medium`}
                >
                  {empathyLabel} Empathy
                </Badge>
              </motion.div>
            </AnimatePresence>
          </SheetHeader>
        </div>

        {/* ── Scrollable Content ──────────────────────────────── */}
        <ScrollArea className="flex-1" aria-label="Pair details content">
          <div
            onTouchStart={handleTouchStart}
            onTouchMove={handleTouchMove}
            onTouchEnd={handleTouchEnd}
            style={{ transform: swipeOffset !== 0 ? `translateX(${swipeOffset}px)` : undefined }}
          >
          <AnimatePresence mode="wait">
            <motion.div
              key={`content-${pair.id}`}
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -12 }}
              transition={{ duration: 0.3, ease: "easeOut" }}
              className="px-4 pb-8 pt-5 sm:px-6"
            >
              {/* ── Fusion Pipeline Mini-Visualization ──────── */}
              <section aria-label="Fusion pipeline" className="mb-6">
                <h3 className="mb-3 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                  Fusion Pipeline
                </h3>
                <div className="flex items-center justify-center gap-2 rounded-xl border border-border/60 bg-muted/30 p-4">
                  <PipelineStep
                    label={pair.avatarName}
                    icon={<User className="h-4 w-4" />}
                    isActive={phaseIdx >= avatarPhase}
                    isCompleted={phaseIdx > avatarPhase}
                    accentColor={pair.color}
                  />
                  <ConnectorArrow
                    active={phaseIdx >= aidePhase}
                    color={pair.color}
                  />
                  <PipelineStep
                    label={pair.aideName}
                    icon={<HeartHandshake className="h-4 w-4" />}
                    isActive={phaseIdx >= aidePhase}
                    isCompleted={phaseIdx > aidePhase}
                    accentColor={pair.color}
                  />
                  <ConnectorArrow
                    active={phaseIdx >= advocatePhase}
                    color={pair.color}
                  />
                  <PipelineStep
                    label={pair.advocateName}
                    icon={<Sparkles className="h-4 w-4" />}
                    isActive={phaseIdx >= advocatePhase}
                    isCompleted={false}
                    accentColor={pair.color}
                  />
                </div>
              </section>

              {/* ── Fusion Journey ────────────────────────────── */}
              <CollapsibleSection
                sectionKey="fusion-journey"
                title="Fusion Journey"
                isOpen={openSections["fusion-journey"]}
                onToggle={toggleSection}
              >
                <FusionJourney pair={pair} hideHeading />
              </CollapsibleSection>

              <Separator className="mb-6" />

              {/* ── Expandable Sections ───────────────────────── */}
              <div className="space-y-1 mb-6">
                {/* Avatar Experience — orange themed */}
                <ExpandableSection
                  title={`What ${pair.avatarName} Struggles With`}
                  icon={<User className="h-4 w-4" />}
                  accentColor="text-orange-500"
                  accentBg="bg-orange-500/10"
                  defaultOpen={true}
                >
                  <ul className="space-y-2">
                    {pair.avatarStruggles.map((struggle, i) => (
                      <motion.li
                        key={i}
                        initial={{ opacity: 0, x: -8 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{
                          duration: 0.25,
                          delay: i * 0.06,
                        }}
                        className="flex items-start gap-2.5 text-sm text-muted-foreground"
                      >
                        <span
                          className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-orange-500"
                          aria-hidden="true"
                        />
                        {struggle}
                      </motion.li>
                    ))}
                  </ul>

                  {/* Example scenario callout */}
                  <div
                    className="mt-4 rounded-lg border border-orange-500/20 bg-orange-500/5 p-3.5"
                  >
                    <div className="mb-2 flex items-center gap-2">
                      <AlertTriangle className="h-4 w-4 shrink-0 text-orange-500" />
                      <span className="text-xs font-semibold uppercase tracking-wider text-orange-600 dark:text-orange-400">
                        Example Scenario
                      </span>
                    </div>
                    <p className="text-sm leading-relaxed text-muted-foreground italic">
                      &ldquo;{pair.exampleScenario}&rdquo;
                    </p>
                  </div>
                </ExpandableSection>

                {/* Aide Expertise — teal/emerald themed */}
                <ExpandableSection
                  title={`How ${pair.aideName} Helps`}
                  icon={<HeartHandshake className="h-4 w-4" />}
                  accentColor="text-emerald-500"
                  accentBg="bg-emerald-500/10"
                  defaultOpen={true}
                >
                  <ul className="space-y-2">
                    {pair.aideExpertise.map((skill, i) => (
                      <motion.li
                        key={i}
                        initial={{ opacity: 0, x: -8 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{
                          duration: 0.25,
                          delay: i * 0.06,
                        }}
                        className="flex items-start gap-2.5 text-sm text-muted-foreground"
                      >
                        <CheckCircle2
                          className="mt-0.5 h-4 w-4 shrink-0 text-emerald-500"
                          aria-hidden="true"
                        />
                        {skill}
                      </motion.li>
                    ))}
                  </ul>
                </ExpandableSection>

                {/* Training Scenarios — pair color themed */}
                <ExpandableSection
                  title="Training Scenarios"
                  icon={<MessageSquare className="h-4 w-4" />}
                  accentColor={pair.colorClass}
                  accentBg={pair.bgClass}
                  defaultOpen={true}
                >
                  <div className="flex flex-wrap gap-2">
                    {pair.scenarios.map((scenario, i) => (
                      <motion.div
                        key={i}
                        initial={{ opacity: 0, x: -12 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{
                          duration: 0.25,
                          delay: i * 0.08,
                        }}
                        className="flex items-center gap-2 rounded-lg border border-border/60 bg-background px-3 py-2"
                        style={{ borderLeftWidth: "3px", borderLeftColor: pair.color }}
                      >
                        <MessageSquare
                          className="h-3.5 w-3.5 shrink-0"
                          style={{ color: pair.color }}
                        />
                        <span className="text-sm text-muted-foreground">
                          {scenario}
                        </span>
                      </motion.div>
                    ))}
                  </div>
                </ExpandableSection>

                {/* Advocate Fusion — violet/purple themed */}
                <ExpandableSection
                  title={`When They Fuse: ${pair.advocateName}`}
                  icon={<Sparkles className="h-4 w-4" />}
                  accentColor="text-violet-500"
                  accentBg="bg-violet-500/10"
                >
                  <p
                    className="text-sm font-medium leading-relaxed text-foreground"
                  >
                    {pair.advocateStrength}
                  </p>

                  <Separator className="my-3" />

                  {/* Empathy level indicator */}
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-medium text-muted-foreground">
                      Empathy Level
                    </span>
                  </div>
                  <div className="mt-3 flex items-start justify-center gap-4">
                    {(
                      [
                        "theoretical",
                        "observational",
                        "experiential",
                        "deep_experiential",
                      ] as const
                    ).map((level, i) => {
                      const levels = [
                        "theoretical",
                        "observational",
                        "experiential",
                        "deep_experiential",
                      ];
                      const currentIdx = levels.indexOf(pair.empathyLevel);
                      const isFilled = i <= currentIdx;
                      const shortLabels = [
                        "Theoretical",
                        "Observational",
                        "Experiential",
                        "Deep",
                      ];
                      return (
                        <div
                          key={level}
                          className="flex flex-col items-center gap-1.5"
                        >
                          <motion.div
                            className="flex h-7 w-7 items-center justify-center rounded-full border-2"
                            style={{
                              borderColor: isFilled
                                ? pair.color
                                : "hsl(var(--muted) / 0.3)",
                              backgroundColor: isFilled
                                ? `${pair.color}20`
                                : "transparent",
                            }}
                            initial={{ scale: 0, opacity: 0 }}
                            animate={{ scale: 1, opacity: 1 }}
                            transition={{
                              duration: 0.3,
                              delay: 0.1 + i * 0.1,
                              ease: "easeOut",
                            }}
                          >
                            {isFilled && (
                              <motion.div
                                initial={{ scale: 0 }}
                                animate={{ scale: 1 }}
                                transition={{
                                  duration: 0.2,
                                  delay: 0.2 + i * 0.1,
                                }}
                              >
                                <Check
                                  className="h-3.5 w-3.5"
                                  style={{ color: pair.color }}
                                />
                              </motion.div>
                            )}
                          </motion.div>
                          <span
                            className={`text-[10px] font-medium leading-tight text-center max-w-[56px] ${
                              isFilled
                                ? "text-foreground"
                                : "text-muted-foreground/50"
                            }`}
                          >
                            {shortLabels[i]}
                          </span>
                        </div>
                      );
                    })}
                  </div>
                </ExpandableSection>
              </div>

              <Separator className="mb-6" />

              {/* ── Key Metrics ────────────────────────────────── */}
              <CollapsibleSection
                sectionKey="key-metrics"
                title="Key Metrics"
                isOpen={openSections["key-metrics"]}
                onToggle={toggleSection}
              >
                <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">
                  {pair.keyMetrics.map((metric, i) => (
                    <motion.div
                      key={metric.label}
                      initial={{ opacity: 0, y: 8 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.3, delay: i * 0.08 }}
                      className="rounded-xl border border-border/60 bg-muted/30 p-3.5"
                    >
                      <p className="text-[11px] font-medium uppercase tracking-wider text-muted-foreground">
                        {metric.label}
                      </p>
                      <p
                        className="mt-1 text-2xl font-bold tabular-nums"
                        style={{ color: pair.color }}
                      >
                        {metric.value}
                      </p>
                      <p className="mt-0.5 text-[11px] text-muted-foreground/70">
                        {metric.description}
                      </p>
                      {/* Mini bar chart */}
                      <div className="mt-2.5 h-1.5 w-full overflow-hidden rounded-full bg-muted">
                        <motion.div
                          className="h-full rounded-full"
                          style={{ backgroundColor: pair.color }}
                          initial={{ width: 0 }}
                          animate={{ width: `${Math.min(metric.value, 100)}%` }}
                          transition={{
                            duration: 0.6,
                            delay: 0.3 + i * 0.1,
                            ease: "easeOut",
                          }}
                        />
                      </div>
                    </motion.div>
                  ))}
                </div>
              </CollapsibleSection>

              <Separator className="mb-6" />

              {/* ── Development Roadmap Timeline ────────────── */}
              <CollapsibleSection
                sectionKey="development-roadmap"
                title="Development Roadmap"
                isOpen={openSections["development-roadmap"]}
                onToggle={toggleSection}
              >
                <Card className="border-border/60">
                  <CardContent className="px-4 pb-4 pt-2">
                    <motion.div
                      className="flex items-center justify-between"
                      initial="hidden"
                      animate="show"
                      variants={{
                        hidden: { opacity: 0 },
                        show: { opacity: 1, transition: { staggerChildren: 0.12 } },
                      }}
                    >
                    {(["concept", "prototype", "training", "ready"] as const).map(
                      (phase, i) => {
                        const phaseIdx = getStatusPhaseIndex(pair.status);
                        const isCompleted = i < phaseIdx;
                        const isCurrent = i === phaseIdx;
                        const isFuture = i > phaseIdx;
                        const labels = ["Concept", "Prototype", "Training", "Ready"];
                        return (
                          <motion.div
                            key={phase}
                            className="flex flex-1 flex-col items-center"
                            variants={{
                              hidden: { opacity: 0, y: 8 },
                              show: { opacity: 1, y: 0, transition: { duration: 0.3, ease: "easeOut" } },
                            }}
                          >
                            {/* Circle + connector line */}
                            <div className="flex w-full items-center">
                              {/* Left connector line */}
                              {i > 0 && (
                                <div className="relative mr-[-10px] z-0 flex-1">
                                  <div
                                    className="h-0.5 w-full rounded-full"
                                    style={{
                                      backgroundColor: isCompleted || isCurrent
                                        ? pair.color
                                        : "hsl(var(--muted-foreground) / 0.15)",
                                    }}
                                  />
                                </div>
                              )}
                              {/* Circle node */}
                              <motion.div
                                className={`relative z-10 flex items-center justify-center rounded-full border-2 transition-all duration-300 ${
                                  isFuture ? "border-muted-foreground/20" : ""
                                }`}
                                style={{
                                  width: isCurrent ? 32 : 24,
                                  height: isCurrent ? 32 : 24,
                                  borderColor: isFuture ? undefined : pair.color,
                                  backgroundColor: isCompleted
                                    ? pair.color
                                    : isCurrent
                                      ? `${pair.color}20`
                                      : "transparent",
                                }}
                                animate={
                                  isCurrent
                                    ? {
                                        boxShadow: [
                                          `0 0 0 0 ${pair.color}40`,
                                          `0 0 0 6px ${pair.color}00`,
                                          `0 0 0 0 ${pair.color}40`,
                                        ],
                                      }
                                    : {}
                                }
                                transition={
                                  isCurrent
                                    ? { duration: 2, repeat: Infinity, ease: "easeInOut" }
                                    : {}
                                }
                              >
                                {isCompleted && (
                                  <Check className="h-3 w-3 text-white" aria-hidden="true" />
                                )}
                                {isCurrent && (
                                  <div
                                    className="h-2.5 w-2.5 rounded-full"
                                    style={{ backgroundColor: pair.color }}
                                  />
                                )}
                              </motion.div>
                              {/* Right connector line */}
                              {i < 3 && (
                                <div className="relative ml-[-10px] z-0 flex-1">
                                  <div
                                    className="h-0.5 w-full rounded-full"
                                    style={{
                                      backgroundColor: isCompleted
                                        ? pair.color
                                        : "hsl(var(--muted-foreground) / 0.15)",
                                    }}
                                  />
                                </div>
                              )}
                            </div>
                            {/* Label */}
                            <span
                              className={`mt-2 text-[11px] font-medium transition-colors duration-300 ${
                                isFuture
                                  ? "text-muted-foreground/40"
                                  : isCurrent
                                    ? "text-foreground"
                                    : "text-muted-foreground/70"
                              }`}
                            >
                              {labels[i]}
                            </span>
                          </motion.div>
                        );
                      },
                    )}
                  </motion.div>
                </CardContent>
              </Card>
              </CollapsibleSection>

              <Separator className="mb-6" />

              {/* ── Readiness & Empathy ──────────────────────────── */}
              <section aria-label="Readiness and empathy">
                <h3 className="mb-3 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                  Readiness & Empathy
                </h3>
                <div className="rounded-xl border border-border/60 bg-muted/30 p-5">
                  <div className="flex flex-col gap-5 sm:flex-row sm:items-center">
                    {/* Radial readiness gauge */}
                    <ReadinessGauge
                      value={pair.readinessScore}
                      color={pair.color}
                      size={96}
                    />
                    <div className="flex-1 min-w-0">
                      <motion.p
                        key={`pct-${pair.id}`}
                        initial={{ opacity: 0, y: 6 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{
                          duration: 0.4,
                          ease: "easeOut",
                          delay: 0.1,
                        }}
                        className="text-sm text-muted-foreground"
                      >
                        {getReadinessMessage(pair.status, pair.readinessScore)}
                      </motion.p>
                      {/* Progress bar (kept for visual continuity) */}
                      <div className="mt-3">
                        <Progress
                          value={readinessPct}
                          className="h-1.5"
                          aria-label={`Readiness: ${readinessPct}%`}
                        />
                      </div>
                    </div>
                    {/* Divider on desktop */}
                    <div className="hidden sm:block h-16 w-px bg-border" />
                    {/* Empathy Wave */}
                    <div className="flex-1 min-w-0">
                      <p className="mb-2.5 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                        Empathy Level
                      </p>
                      <EmpathyWave level={pair.empathyLevel} color={pair.color} />
                    </div>
                  </div>
                </div>
              </section>

              <Separator className="mb-6" />

              {/* ── AI Insight ──────────────────────────────────── */}
              <AIInsightSection pairId={pair.id} />
            </motion.div>
          </AnimatePresence>
          </div>
        </ScrollArea>
      </SheetContent>
    </Sheet>
  );
}

// ─── Pair icon renderer (consistent with pairs-grid) ─────────────────
function PairIcon({
  name,
  color,
  size = 20,
}: {
  name: string;
  color: string;
  size?: number;
}) {
  const iconProps = { style: { color }, width: size, height: size };
  switch (name) {
    case "Eye":
      return <Eye {...iconProps} />;
    case "Shield":
      return <Shield {...iconProps} />;
    case "Target":
      return <Target {...iconProps} />;
    case "Clock":
      return <Clock {...iconProps} />;
    case "Brain":
      return <Brain {...iconProps} />;
    case "Heart":
      return <Heart {...iconProps} />;
    case "Rocket":
      return <Rocket {...iconProps} />;
    case "Flame":
      return <Flame {...iconProps} />;
    case "ListChecks":
      return <ListChecks {...iconProps} />;
    case "ArrowLeftRight":
      return <ArrowLeftRight {...iconProps} />;
    case "ScanEye":
      return <ScanEye {...iconProps} />;
    case "Mountain":
      return <Mountain {...iconProps} />;
    case "Battery":
      return <Battery {...iconProps} />;
    case "Gauge":
      return <Gauge {...iconProps} />;
    case "ShieldAlert":
      return <ShieldAlert {...iconProps} />;
    case "Ear":
      return <Ear {...iconProps} />;
    case "Users":
      return <Users {...iconProps} />;
    case "Sparkles":
      return <Sparkles {...iconProps} />;
    case "Star":
      return <Star {...iconProps} />;
    default:
      return <Circle {...iconProps} />;
  }
}
