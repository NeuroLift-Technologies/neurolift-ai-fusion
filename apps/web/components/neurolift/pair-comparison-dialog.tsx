"use client";

import { useState, useMemo, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import type { Variants } from "framer-motion";
import {
  RadarChart,
  Radar,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
} from "recharts";
import {
  CheckCircle2,
  CircleDot,
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
  Sparkles,
  Star,
  Circle,
  User,
  Bot,
  ArrowRight,
  Trophy,
  Scale,
} from "lucide-react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from "@/components/ui/dialog";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Separator } from "@/components/ui/separator";
import {
  Card,
  CardHeader,
  CardTitle,
  CardContent,
} from "@/components/ui/card";
import {
  PAIRS,
  STATUS_CONFIG,
  EMPATHY_LABELS,
  CATEGORY_LABELS,
  type AvatarAidePair,
  type EmpathyLevel,
} from "@/lib/avatar-pairs-data";
import { cn } from "@/lib/utils";

// ─── Empathy depth ordering for comparison ────────────────────────
const EMPATHY_ORDER: Record<EmpathyLevel, number> = {
  theoretical: 1,
  observational: 2,
  experiential: 3,
  deep_experiential: 4,
};

// ─── Props ───────────────────────────────────────────────────────
interface PairComparisonDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

// ─── Component ───────────────────────────────────────────────────
export function PairComparisonDialog({
  open,
  onOpenChange,
}: PairComparisonDialogProps) {
  const [pairAId, setPairAId] = useState<string>("1");
  const [pairBId, setPairBId] = useState<string>("2");
  const [swapKey, setSwapKey] = useState(0);

  const handleSwap = useCallback(() => {
    setPairAId(pairBId);
    setPairBId(pairAId);
    setSwapKey((k) => k + 1);
  }, [pairAId, pairBId]);

  const pairA = useMemo(
    () => PAIRS.find((p) => p.id === Number(pairAId)),
    [pairAId],
  );
  const pairB = useMemo(
    () => PAIRS.find((p) => p.id === Number(pairBId)),
    [pairBId],
  );

  // Determine which pair has higher readiness
  const readinessWinner = useMemo(() => {
    if (!pairA || !pairB) return null;
    if (pairA.readinessScore > pairB.readinessScore) return "a";
    if (pairB.readinessScore > pairA.readinessScore) return "b";
    return null; // tie
  }, [pairA, pairB]);

  // Determine which pair has higher empathy
  const empathyWinner = useMemo(() => {
    if (!pairA || !pairB) return null;
    const a = EMPATHY_ORDER[pairA.empathyLevel];
    const b = EMPATHY_ORDER[pairB.empathyLevel];
    if (a > b) return "a";
    if (b > a) return "b";
    return null;
  }, [pairA, pairB]);

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-5xl max-h-[90vh] overflow-y-auto p-0">
        {/* ── Header ──────────────────────────────────── */}
        <DialogHeader className="p-6 pb-4">
          <DialogTitle className="text-xl font-bold tracking-tight">
            Compare Pairs
          </DialogTitle>
          <DialogDescription>
            Select two pairs to see a detailed side-by-side comparison of their
            traits, readiness, and capabilities.
          </DialogDescription>
        </DialogHeader>

        {/* ── Selectors ──────────────────────────────── */}
        <div className="flex flex-col gap-3 px-6 pb-4 sm:flex-row sm:items-end">
          <div className="flex-1">
            <label
              htmlFor="pair-a-select"
              className="mb-1.5 block text-sm font-medium text-foreground"
            >
              Pair A
            </label>
            <Select value={pairAId} onValueChange={setPairAId}>
              <SelectTrigger id="pair-a-select" className="w-full">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {PAIRS.map((p) => (
                  <SelectItem key={p.id} value={String(p.id)}>
                    {p.avatarName} &mdash; {p.trait}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div className="flex items-center justify-center pb-2">
            <Button
              variant="ghost"
              size="icon"
              className="h-8 w-8 rounded-full"
              onClick={handleSwap}
              aria-label="Swap pairs"
            >
              <motion.span
                key={swapKey}
                initial={{ rotate: 0 }}
                animate={{ rotate: 180 }}
                transition={{ duration: 0.3, ease: "easeInOut" }}
                className="flex items-center"
              >
                <ArrowLeftRight className="h-4 w-4 text-muted-foreground" />
              </motion.span>
            </Button>
          </div>

          <div className="flex-1">
            <label
              htmlFor="pair-b-select"
              className="mb-1.5 block text-sm font-medium text-foreground"
            >
              Pair B
            </label>
            <Select value={pairBId} onValueChange={setPairBId}>
              <SelectTrigger id="pair-b-select" className="w-full">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {PAIRS.map((p) => (
                  <SelectItem key={p.id} value={String(p.id)}>
                    {p.avatarName} &mdash; {p.trait}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </div>

        <Separator />

        {/* ── Side-by-side comparison ────────────────── */}
        {pairA && pairB ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-0 p-6">
            <PairColumn
              pair={pairA}
              label="A"
              showReadinessWinner={readinessWinner === "a"}
              showEmpathyWinner={empathyWinner === "a"}
              isLeft
              index={0}
            />
            {/* Divider (desktop only) */}
            <div className="hidden md:block">
              <Separator orientation="vertical" className="mx-0 h-full" />
            </div>
            <PairColumn
              pair={pairB}
              label="B"
              showReadinessWinner={readinessWinner === "b"}
              showEmpathyWinner={empathyWinner === "b"}
              isLeft={false}
              index={1}
            />
          </div>
        ) : (
          <div className="flex items-center justify-center py-16 text-muted-foreground">
            Select two pairs to compare
          </div>
        )}

        {/* ── Radar Chart + Score Summary ────────── */}
        {pairA && pairB && (
          <>
            <Separator />
            <div className="p-6">
              <AnimatePresence mode="wait">
                <motion.div
                  key={`${pairAId}-${pairBId}`}
                  initial={{ opacity: 0, y: 12 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -12 }}
                  transition={{ duration: 0.3, ease: "easeOut" }}
                >
                  <Card className="[background-image:radial-gradient(circle,hsl(var(--border))_1px,transparent_1px)] [background-size:16px_16px] overflow-hidden">
                    <CardHeader className="pb-0">
                      <CardTitle className="text-sm font-semibold">
                        Metrics Comparison
                      </CardTitle>
                    </CardHeader>
                    <CardContent className="pt-2">
                      <ComparisonRadar pairA={pairA} pairB={pairB} />
                    </CardContent>
                  </Card>
                </motion.div>
              </AnimatePresence>
            </div>

            <ScoreSummary pairA={pairA} pairB={pairB} />
          </>
        )}
      </DialogContent>
    </Dialog>
  );
}

// ─── Radar chart axes ───────────────────────────────────────────
const RADAR_AXES = ["Empathy Depth", "Cognitive Load", "Adaptive Response"];

// ─── Comparison Radar ────────────────────────────────────────────
function ComparisonRadar({
  pairA,
  pairB,
}: {
  pairA: AvatarAidePair;
  pairB: AvatarAidePair;
}) {
  const data = useMemo(() => {
    return RADAR_AXES.map((axis, i) => ({
      metric: axis,
      pairA: pairA.keyMetrics[i]?.value ?? 0,
      pairB: pairB.keyMetrics[i]?.value ?? 0,
    }));
  }, [pairA, pairB]);

  return (
    <ResponsiveContainer width="100%" height={280}>
      <RadarChart data={data} cx="50%" cy="50%" outerRadius="70%">
        <PolarGrid stroke="hsl(var(--border))" />
        <PolarAngleAxis
          dataKey="metric"
          tick={{ fontSize: 11, fill: "hsl(var(--muted-foreground))" }}
        />
        <PolarRadiusAxis
          tick={false}
          axisLine={false}
          domain={[0, "auto"]}
        />
        <Radar
          name={pairA.avatarName}
          dataKey="pairA"
          stroke={pairA.color}
          fill={pairA.color}
          fillOpacity={0.3}
        />
        <Radar
          name={pairB.avatarName}
          dataKey="pairB"
          stroke={pairB.color}
          fill={pairB.color}
          fillOpacity={0.3}
        />
      </RadarChart>
    </ResponsiveContainer>
  );
}

// ─── Overall Score Summary ────────────────────────────────────────
function ScoreSummary({
  pairA,
  pairB,
}: {
  pairA: AvatarAidePair;
  pairB: AvatarAidePair;
}) {
  const result = useMemo(() => {
    let winsA = 0;
    let winsB = 0;

    // Readiness score
    if (pairA.readinessScore > pairB.readinessScore) winsA++;
    else if (pairB.readinessScore > pairA.readinessScore) winsB++;

    // Empathy order
    const aEmp = EMPATHY_ORDER[pairA.empathyLevel];
    const bEmp = EMPATHY_ORDER[pairB.empathyLevel];
    if (aEmp > bEmp) winsA++;
    else if (bEmp > aEmp) winsB++;

    // 3 key metrics
    for (let i = 0; i < 3; i++) {
      const aVal = pairA.keyMetrics[i]?.value ?? 0;
      const bVal = pairB.keyMetrics[i]?.value ?? 0;
      if (aVal > bVal) winsA++;
      else if (bVal > aVal) winsB++;
    }

    return { winsA, winsB };
  }, [pairA, pairB]);

  const isTie = result.winsA === result.winsB;
  const winnerIsA = result.winsA > result.winsB;
  const winner = winnerIsA ? pairA : pairB;
  const winnerLabel = winnerIsA ? "A" : "B";
  const winCount = winnerIsA ? result.winsA : result.winsB;

  return (
    <div className="flex items-center justify-center gap-2 px-6 pb-6">
      {isTie ? (
        <>
          <Scale className="h-4 w-4 text-muted-foreground" />
          <span className="text-sm font-medium text-muted-foreground">
            Tied &mdash; both pairs are evenly matched
          </span>
        </>
      ) : (
        <>
          <Trophy className="h-4 w-4" style={{ color: winner.color }} />
          <span
            className="text-sm font-semibold"
            style={{ color: winner.color }}
          >
            Pair {winnerLabel} leads in {winCount} of 5 categories
          </span>
        </>
      )}
    </div>
  );
}

// ─── Single pair column ───────────────────────────────────────────
const columnVariants: Variants = {
  hidden: { opacity: 0, y: 20 },
  visible: (index: number) => ({
    opacity: 1,
    y: 0,
    transition: {
      delay: index * 0.15,
      duration: 0.4,
      ease: "easeOut",
    },
  }),
};

function PairColumn({
  pair,
  label,
  showReadinessWinner,
  showEmpathyWinner,
  isLeft,
  index,
}: {
  pair: AvatarAidePair;
  label: string;
  showReadinessWinner: boolean;
  showEmpathyWinner: boolean;
  isLeft: boolean;
  index: number;
}) {
  const statusConf = STATUS_CONFIG[pair.status];
  const readinessPercent = Math.round(pair.readinessScore * 100);
  const empathyLabel = EMPATHY_LABELS[pair.empathyLevel];

  return (
    <motion.div
      custom={index}
      variants={columnVariants}
      initial="hidden"
      animate="visible"
      className={cn("px-4", isLeft ? "md:pr-8" : "md:pl-8")}
    >
      {/* Column label badge */}
      <div className="mb-4">
        <span
          className="inline-flex items-center gap-1.5 rounded-md px-2.5 py-1 text-xs font-bold uppercase tracking-wider"
          style={{
            backgroundColor: `${pair.color}15`,
            color: pair.color,
          }}
        >
          Pair {label}
        </span>
      </div>

      {/* Name + trait + icon */}
      <div className="flex items-center gap-3 mb-3">
        <div
          className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full"
          style={{ backgroundColor: `${pair.color}15` }}
        >
          <PairIcon name={pair.iconName} color={pair.color} />
        </div>
        <div className="min-w-0">
          <h3 className="text-lg font-bold leading-tight text-foreground truncate">
            {pair.avatarName}
          </h3>
          <p className="text-sm text-muted-foreground truncate">
            {pair.trait}
          </p>
        </div>
      </div>

      {/* Badges */}
      <div className="flex flex-wrap gap-1.5 mb-5">
        <Badge
          variant="secondary"
          className={cn("text-[11px] font-medium", pair.bgClass, pair.colorClass)}
        >
          {CATEGORY_LABELS[pair.category]}
        </Badge>
        <Badge
          variant="secondary"
          className={cn(
            "text-[11px] font-medium",
            statusConf.bgColor,
            statusConf.color,
          )}
        >
          {statusConf.label}
        </Badge>
      </div>

      {/* Readiness Score */}
      <div className="mb-5">
        <div className="flex items-center justify-between mb-1.5">
          <span className="text-sm font-medium text-foreground flex items-center gap-2">
            Readiness
            {showReadinessWinner && (
              <CheckCircle2 className="h-4 w-4 text-emerald-500" />
            )}
          </span>
          <span
            className="text-sm font-bold tabular-nums"
            style={{ color: pair.color }}
          >
            {readinessPercent}%
          </span>
        </div>
        <Progress value={readinessPercent} className="h-2" />
      </div>

      {/* Empathy Level */}
      <div className="mb-5">
        <div className="flex items-center justify-between mb-1.5">
          <span className="text-sm font-medium text-foreground flex items-center gap-2">
            Empathy
            {showEmpathyWinner && (
              <CheckCircle2 className="h-4 w-4 text-emerald-500" />
            )}
          </span>
          <span
            className={cn(
              "inline-flex items-center gap-1 rounded-full px-2.5 py-0.5 text-xs font-semibold",
              getEmpathyBadgeClasses(pair.empathyLevel),
            )}
          >
            <CircleDot className="h-3 w-3" />
            {empathyLabel}
          </span>
        </div>
        {/* Visual empathy indicator — filled dots */}
        <div className="flex items-center gap-1.5">
          {[1, 2, 3, 4].map((level) => (
            <div
              key={level}
              className="h-2.5 w-2.5 rounded-full transition-colors duration-300"
              style={{
                backgroundColor:
                  EMPATHY_ORDER[pair.empathyLevel] >= level
                    ? pair.color
                    : "hsl(var(--muted-foreground) / 0.2)",
              }}
            />
          ))}
          <span className="ml-2 text-[11px] text-muted-foreground">
            {EMPATHY_ORDER[pair.empathyLevel]} / 4
          </span>
        </div>
      </div>

      <Separator className="my-5" />

      {/* Avatar Struggles */}
      <div className="mb-5">
        <h4 className="mb-2.5 flex items-center gap-2 text-sm font-semibold text-foreground">
          <User className="h-4 w-4" style={{ color: pair.color }} />
          Avatar Struggles
        </h4>
        <ul className="space-y-1.5">
          {pair.avatarStruggles.map((s, i) => (
            <li
              key={i}
              className="flex items-start gap-2 text-sm text-muted-foreground"
            >
              <ArrowRight
                className="mt-0.5 h-3 w-3 shrink-0"
                style={{ color: `${pair.color}90` }}
              />
              <span>{s}</span>
            </li>
          ))}
        </ul>
      </div>

      {/* Aide Expertise */}
      <div className="mb-5">
        <h4 className="mb-2.5 flex items-center gap-2 text-sm font-semibold text-foreground">
          <Bot className="h-4 w-4" style={{ color: pair.color }} />
          Aide Expertise
        </h4>
        <ul className="space-y-1.5">
          {pair.aideExpertise.map((e, i) => (
            <li
              key={i}
              className="flex items-start gap-2 text-sm text-muted-foreground"
            >
              <ArrowRight
                className="mt-0.5 h-3 w-3 shrink-0"
                style={{ color: `${pair.color}90` }}
              />
              <span>{e}</span>
            </li>
          ))}
        </ul>
      </div>

      <Separator className="my-5" />

      {/* Key Metrics */}
      <div>
        <h4 className="mb-3 flex items-center gap-2 text-sm font-semibold text-foreground">
          Key Metrics
        </h4>
        <div className="grid grid-cols-3 gap-3">
          {pair.keyMetrics.map((metric, i) => (
            <div
              key={i}
              className="rounded-lg bg-muted/50 p-3 text-center"
            >
              <div
                className="text-xl font-bold tabular-nums"
                style={{ color: pair.color }}
              >
                {metric.value}
              </div>
              <div className="mt-0.5 text-[11px] font-medium text-muted-foreground leading-tight">
                {metric.label}
              </div>
              <div className="mt-0.5 text-[10px] text-muted-foreground/60 leading-tight">
                {metric.description}
              </div>
            </div>
          ))}
        </div>
      </div>
    </motion.div>
  );
}

// ─── Empathy badge color mapping ──────────────────────────────────
function getEmpathyBadgeClasses(level: EmpathyLevel): string {
  switch (level) {
    case "theoretical":
      return "bg-slate-500/15 text-slate-400";
    case "observational":
      return "bg-sky-500/15 text-sky-400";
    case "experiential":
      return "bg-amber-500/15 text-amber-500";
    case "deep_experiential":
      return "bg-emerald-500/15 text-emerald-400";
    default:
      return "bg-slate-500/15 text-slate-400";
  }
}

// ─── Pair icon renderer ───────────────────────────────────────────
function PairIcon({ name, color }: { name: string; color: string }) {
  const props = { className: "h-5 w-5" as const, style: { color } };
  switch (name) {
    case "Eye":
      return <Eye {...props} />;
    case "Shield":
      return <Shield {...props} />;
    case "Target":
      return <Target {...props} />;
    case "Clock":
      return <Clock {...props} />;
    case "Brain":
      return <Brain {...props} />;
    case "Heart":
      return <Heart {...props} />;
    case "Rocket":
      return <Rocket {...props} />;
    case "Flame":
      return <Flame {...props} />;
    case "ListChecks":
      return <ListChecks {...props} />;
    case "ArrowLeftRight":
      return <ArrowLeftRight {...props} />;
    case "ScanEye":
      return <ScanEye {...props} />;
    case "Mountain":
      return <Mountain {...props} />;
    case "Battery":
      return <Battery {...props} />;
    case "Gauge":
      return <Gauge {...props} />;
    case "ShieldAlert":
      return <ShieldAlert {...props} />;
    case "Ear":
      return <Ear {...props} />;
    case "Users":
      return <Users {...props} />;
    case "Sparkles":
      return <Sparkles {...props} />;
    case "Star":
      return <Star {...props} />;
    default:
      return <Circle {...props} />;
  }
}
