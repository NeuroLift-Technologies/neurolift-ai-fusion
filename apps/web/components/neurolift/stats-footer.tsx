'use client';

import { useRef, useState, useEffect, useMemo, useCallback } from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  RadarChart,
  Radar,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  PieChart,
  Pie,
  Cell,
} from 'recharts';
import {
  getStats,
  PAIRS,
  STATUS_CONFIG,
  EMPATHY_LABELS,
  type FusionStatus,
  type EmpathyLevel,
} from '@/lib/avatar-pairs-data';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Collapsible, CollapsibleTrigger, CollapsibleContent } from '@/components/ui/collapsible';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { motion, useInView } from 'framer-motion';
import type { Variants } from 'framer-motion';
import { Brain, Zap, Shield, Heart, Github, Globe, Mail, BarChart as BarChartIcon, ChevronDown } from 'lucide-react';

// ─── Empathy level rank for comparison ───────────────────────────
const EMPATHY_RANK: Record<EmpathyLevel, number> = {
  theoretical: 0,
  observational: 1,
  experiential: 2,
  deep_experiential: 3,
};

// ─── Solid colors for the development progress bar ───────────────
const STATUS_BAR_COLORS: Record<FusionStatus, string> = {
  concept: 'bg-slate-400',
  prototype: 'bg-amber-500',
  training: 'bg-cyan-500',
  ready: 'bg-emerald-500',
};

// ─── Animated counter hook ───────────────────────────────────────
function useAnimatedCounter(
  target: number,
  inView: boolean,
  duration = 1200,
  decimals = 0,
): number {
  const [value, setValue] = useState(0);

  useEffect(() => {
    if (!inView) return;
    let startTime: number | null = null;
    let rafId: number;

    const step = (timestamp: number) => {
      if (startTime === null) startTime = timestamp;
      const elapsed = timestamp - startTime;
      const progress = Math.min(elapsed / duration, 1);
      // ease-out cubic
      const eased = 1 - Math.pow(1 - progress, 3);
      setValue(eased * target);
      if (progress < 1) {
        rafId = requestAnimationFrame(step);
      }
    };

    rafId = requestAnimationFrame(step);
    return () => cancelAnimationFrame(rafId);
  }, [target, inView, duration]);

  return decimals > 0 ? Number(value.toFixed(decimals)) : Math.round(value);
}

// ─── Color map for status donut chart (hex values for recharts Cell) ──
const STATUS_HEX_COLORS: Record<FusionStatus, string> = {
  concept: '#94a3b8',
  prototype: '#f59e0b',
  training: '#06b6d4',
  ready: '#10b981',
};

function computeDerivedStats() {
  const stats = getStats();
  const inDevelopment = stats.concept + stats.prototype;
  const avgReadiness =
    PAIRS.reduce((sum, p) => sum + p.readinessScore, 0) / PAIRS.length;
  const avgReadinessPct = Math.round(avgReadiness * 100);

  let topEmpathy: EmpathyLevel = 'theoretical';
  for (const pair of PAIRS) {
    if (EMPATHY_RANK[pair.empathyLevel] > EMPATHY_RANK[topEmpathy]) {
      topEmpathy = pair.empathyLevel;
    }
  }

  const statusCounts: Record<FusionStatus, number> = {
    concept: 0,
    prototype: 0,
    training: 0,
    ready: 0,
  };
  PAIRS.forEach((p) => {
    statusCounts[p.status]++;
  });

  const executivePairs = PAIRS.filter(
    (p) => p.category === 'executive-function',
  );
  const nonExecutivePairs = PAIRS.filter(
    (p) => p.category === 'non-executive-function',
  );

  return {
    ...stats,
    inDevelopment,
    avgReadinessPct,
    topEmpathy,
    statusCounts,
    executivePairs,
    nonExecutivePairs,
  };
}

// ─── Custom tooltip for charts ─────────────────────────────────
function ChartTooltip({ active, payload, label }: { active?: boolean; payload?: Array<{ value: number; name?: string }>; label?: string }) {
  if (!active || !payload?.length) return null;
  return (
    <div className="rounded-lg border border-border/60 bg-popover px-3 py-2 text-sm shadow-lg">
      <p className="font-medium text-foreground">{label}</p>
      <p className="text-muted-foreground">{Math.round(payload[0].value)}%</p>
    </div>
  );
}

// ─── Charts sub-section component ────────────────────────────────
function ChartsSection({
  isInView,
  d,
}: {
  isInView: boolean;
  d: ReturnType<typeof computeDerivedStats>;
}) {
  const chartsRef = useRef<HTMLDivElement>(null);
  const chartsInView = useInView(chartsRef, { once: true, margin: '-60px' });

  // Readiness data: sorted highest to lowest, percentage values
  const readinessData = useMemo(
    () =>
      [...PAIRS]
        .sort((a, b) => b.readinessScore - a.readinessScore)
        .map((p) => ({
          name: p.avatarName,
          readiness: Math.round(p.readinessScore * 100),
          color: p.color,
        })),
    [],
  );

  // Empathy radar data: count per empathy level
  const empathyData = useMemo(() => {
    const levels: EmpathyLevel[] = [
      'theoretical',
      'observational',
      'experiential',
      'deep_experiential',
    ];
    return levels.map((level) => ({
      level: EMPATHY_LABELS[level],
      count: PAIRS.filter((p) => p.empathyLevel === level).length,
    }));
  }, []);

  // Status donut data: count per status with hex color
  const statusDonutData = useMemo(
    () =>
      (Object.keys(d.statusCounts) as FusionStatus[]).map((status) => ({
        name: STATUS_CONFIG[status].label,
        value: d.statusCounts[status],
        color: STATUS_HEX_COLORS[status],
      })),
    [d.statusCounts],
  );

  const totalPairs = d.total;

  return (
    <motion.div
      ref={chartsRef}
      className="grid gap-4 md:grid-cols-3 md:gap-6 mt-12"
      initial={{ opacity: 0, y: 30 }}
      animate={chartsInView ? { opacity: 1, y: 0 } : {}}
      transition={{ duration: 0.6, delay: 0.2 }}
    >
      {/* ── 1. Readiness Score Bar Chart ─────────────────────────── */}
      <Card className="col-span-1 md:col-span-2 rounded-xl border border-border/60 bg-card shadow-sm dark:shadow-none">
        <CardHeader className="pb-2">
          <CardTitle className="text-base font-semibold">Readiness Scores</CardTitle>
        </CardHeader>
        <CardContent className="p-4 sm:p-6">
          <div className="max-h-96 overflow-y-auto scrollbar-thin">
            <ResponsiveContainer width="100%" height={Math.max(readinessData.length * 26, 200)}>
              <BarChart
                data={readinessData}
                layout="vertical"
                margin={{ top: 0, right: 40, left: 10, bottom: 0 }}
              >
                <XAxis
                  type="number"
                  domain={[0, 100]}
                  tick={{ fill: 'hsl(var(--muted-foreground))', fontSize: 12 }}
                  tickFormatter={(v: number) => `${v}%`}
                  axisLine={{ stroke: 'hsl(var(--border))' }}
                  tickLine={false}
                />
                <YAxis
                  type="category"
                  dataKey="name"
                  width={100}
                  tick={{ fill: 'hsl(var(--muted-foreground))', fontSize: 11 }}
                  axisLine={false}
                  tickLine={false}
                />
                <Tooltip
                  content={<ChartTooltip />}
                  cursor={{ fill: 'hsl(var(--muted) / 0.4)' }}
                />
                <Bar
                  dataKey="readiness"
                  radius={[0, 4, 4, 0]}
                  maxBarSize={20}
                >
                  {readinessData.map((entry, index) => (
                    <Cell key={index} fill={entry.color} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>

      {/* ── 2. Empathy Depth Radar Chart ─────────────────────────── */}
      <Card className="rounded-xl border border-border/60 bg-card shadow-sm dark:shadow-none">
        <CardHeader className="pb-2">
          <CardTitle className="text-base font-semibold">Empathy Depth Distribution</CardTitle>
        </CardHeader>
        <CardContent className="p-4 sm:p-6">
          <ResponsiveContainer width="100%" height={280}>
            <RadarChart cx="50%" cy="50%" outerRadius="70%" data={empathyData}>
              <PolarGrid stroke="hsl(var(--border))" />
              <PolarAngleAxis
                dataKey="level"
                tick={{ fill: 'hsl(var(--muted-foreground))', fontSize: 11 }}
              />
              <PolarRadiusAxis
                angle={90}
                domain={[0, 'auto']}
                tick={{ fill: 'hsl(var(--muted-foreground))', fontSize: 10 }}
                tickCount={4}
              />
              <Radar
                name="Pairs"
                dataKey="count"
                stroke="#F38020"
                fill="#F38020"
                fillOpacity={0.2}
                strokeWidth={2}
              />
              <Tooltip
                  contentStyle={{
                    backgroundColor: 'hsl(var(--popover))',
                    border: '1px solid hsl(var(--border))',
                    borderRadius: '8px',
                    fontSize: '13px',
                  }}
                  itemStyle={{ color: 'hsl(var(--foreground))' }}
                  labelStyle={{ color: 'hsl(var(--foreground))', fontWeight: 600 }}
                />
            </RadarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      {/* ── 3. Status Donut Chart ────────────────────────────────── */}
      <Card className="rounded-xl border border-border/60 bg-card shadow-sm dark:shadow-none">
        <CardHeader className="pb-2">
          <CardTitle className="text-base font-semibold">Training Status Breakdown</CardTitle>
        </CardHeader>
        <CardContent className="p-4 sm:p-6">
          <div className="relative">
            <ResponsiveContainer width="100%" height={260}>
              <PieChart>
                <Pie
                  data={statusDonutData}
                  cx="50%"
                  cy="50%"
                  innerRadius={65}
                  outerRadius={100}
                  paddingAngle={3}
                  dataKey="value"
                  stroke="none"
                >
                  {statusDonutData.map((entry, index) => (
                    <Cell key={index} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{
                    backgroundColor: 'hsl(var(--popover))',
                    border: '1px solid hsl(var(--border))',
                    borderRadius: '8px',
                    fontSize: '13px',
                  }}
                  itemStyle={{ color: 'hsl(var(--foreground))' }}
                  labelStyle={{ color: 'hsl(var(--foreground))', fontWeight: 600 }}
                />
              </PieChart>
            </ResponsiveContainer>
            {/* Center label */}
            <div className="pointer-events-none absolute inset-0 flex flex-col items-center justify-center">
              <span className="text-3xl font-bold text-foreground">{totalPairs}</span>
              <span className="text-xs text-muted-foreground">pairs</span>
            </div>
          </div>
          {/* Legend */}
          <div className="mt-2 flex flex-wrap justify-center gap-x-4 gap-y-1">
            {statusDonutData.map((entry) => (
              <div key={entry.name} className="flex items-center gap-1.5 text-xs">
                <span
                  className="inline-block h-2.5 w-2.5 rounded-full"
                  style={{ backgroundColor: entry.color }}
                />
                <span className="text-muted-foreground">{entry.name}</span>
                <span className="font-medium text-foreground">{entry.value}</span>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
}

// ─── Stat card data ──────────────────────────────────────────────
type StatItem = {
  label: string;
  value: number;
  decimals: number;
  suffix?: string;
  description: string;
  icon: React.ReactNode;
  iconBg: string;
  gaugePct: number;
};

// ─── Mini Radial Gauge ────────────────────────────────────────
function MiniRadialGauge({ pct, inView }: { pct: number; inView: boolean }) {
  const RADIUS = 13;
  const STROKE_WIDTH = 3;
  const SIZE = 32;
  const CENTER = SIZE / 2;
  const circumference = 2 * Math.PI * RADIUS;
  const clampedPct = Math.max(0, Math.min(100, pct));
  const offset = circumference * (1 - clampedPct / 100);

  return (
    <svg
      width={SIZE}
      height={SIZE}
      viewBox={`0 0 ${SIZE} ${SIZE}`}
      className="shrink-0"
      aria-hidden="true"
    >
      {/* Background track */}
      <circle
        cx={CENTER}
        cy={CENTER}
        r={RADIUS}
        fill="none"
        stroke="hsl(var(--muted) / 0.4)"
        strokeWidth={STROKE_WIDTH}
      />
      {/* Progress arc */}
      <circle
        cx={CENTER}
        cy={CENTER}
        r={RADIUS}
        fill="none"
        stroke="#F38020"
        strokeWidth={STROKE_WIDTH}
        strokeLinecap="round"
        strokeDasharray={circumference}
        strokeDashoffset={inView ? offset : circumference}
        transform={`rotate(-90 ${CENTER} ${CENTER})`}
        style={{ transition: 'stroke-dashoffset 1s ease-out' }}
      />
    </svg>
  );
}

// ─── Main component ──────────────────────────────────────────────
export default function StatsFooter() {
  const sectionRef = useRef<HTMLDivElement>(null);
  const isInView = useInView(sectionRef, { once: true, margin: '-80px' });
  const treemapRef = useRef<HTMLDivElement>(null);
  const treemapInView = useInView(treemapRef, { once: true, margin: '-60px' });

  // ── Collapsible sections state ──
  const [openSections, setOpenSections] = useState<Record<string, boolean>>({
    overview: true,
    progress: true,
    charts: true,
    detailed: true,
  });

  const toggleSection = useCallback((key: string) => {
    setOpenSections((prev) => ({ ...prev, [key]: !prev[key] }));
  }, []);

  const anySectionOpen = Object.values(openSections).some(Boolean);
  const allSectionsClosed = Object.values(openSections).every((v) => !v);

  const toggleAllSections = useCallback(() => {
    setOpenSections((prev) => {
      const nextVal = allSectionsClosed;
      const updated: Record<string, boolean> = {};
      for (const k of Object.keys(prev)) {
        updated[k] = nextVal;
      }
      return updated;
    });
  }, [allSectionsClosed]);

  const d = useMemo(() => computeDerivedStats(), []);

  // Treemap data: all 19 pairs sorted by readiness descending
  const treemapData = useMemo(
    () =>
      [...PAIRS]
        .map((p) => ({
          name: p.avatarName,
          value: Math.round(p.readinessScore * 100),
          color: p.color,
          trait: p.trait,
        }))
        .sort((a, b) => b.value - a.value),
    [],
  );

  const statItems: StatItem[] = useMemo(
    () => [
      {
        label: 'Total Pairs',
        value: d.total,
        decimals: 0,
        description: 'Avatar-Aide-Advocate combinations',
        icon: <Brain className="h-5 w-5" />,
        iconBg: 'bg-orange-500/15 text-orange-500',
        gaugePct: 100,
      },
      {
        label: 'In Development',
        value: d.inDevelopment,
        decimals: 0,
        description: 'Active development phases',
        icon: <Zap className="h-5 w-5" />,
        iconBg: 'bg-amber-500/15 text-amber-500',
        gaugePct: Math.round((d.inDevelopment / d.total) * 100),
      },
      {
        label: 'Avg Readiness',
        value: d.avgReadinessPct,
        decimals: 0,
        suffix: '%',
        description: 'Across all fusion pairs',
        icon: <Shield className="h-5 w-5" />,
        iconBg: 'bg-emerald-500/15 text-emerald-500',
        gaugePct: d.avgReadinessPct,
      },
      {
        label: 'Top Empathy Level',
        value: EMPATHY_RANK[d.topEmpathy],
        decimals: 0,
        description: EMPATHY_LABELS[d.topEmpathy],
        icon: <Heart className="h-5 w-5" />,
        iconBg: 'bg-rose-500/15 text-rose-500',
        gaugePct: Math.round((EMPATHY_RANK[d.topEmpathy] / 3) * 100),
      },
    ],
    [d],
  );

  const counterTotal = useAnimatedCounter(statItems[0].value, isInView, 1400);
  const counterDev = useAnimatedCounter(statItems[1].value, isInView, 1400);
  const counterReadiness = useAnimatedCounter(statItems[2].value, isInView, 1400);
  const counters = [counterTotal, counterDev, counterReadiness, 0];

  const containerVariants: Variants = {
    hidden: {},
    visible: {
      transition: { staggerChildren: 0.1 },
    },
  };

  const itemVariants: Variants = {
    hidden: { opacity: 0, y: 24 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.5, ease: 'easeOut' },
    },
  };

  // For the 4th stat (Top Empathy Level), show the label instead of a number
  const displayValues = statItems.map((item, i) => {
    if (item.label === 'Top Empathy Level') {
      return item.description;
    }
    const num = counters[i];
    return item.suffix ? `${num}${item.suffix}` : String(num);
  });

  return (
    <>
      {/* ═══════════════════ Section 1: System Overview Stats ═══════════════════ */}
      <section id="stats" ref={sectionRef} className="relative py-16 sm:py-20">
        {/* Dot grid background pattern */}
        <div className="dot-grid-bg pointer-events-none absolute inset-0" aria-hidden="true" />
        <div className="relative z-10 mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
          {/* Section header */}
          <div className="mb-10 flex items-center justify-between">
            <div className="text-center sm:text-left">
              <h2 className="text-2xl font-bold tracking-tight sm:text-3xl">
                System Overview
              </h2>
              <p className="mt-2 text-sm text-muted-foreground sm:text-base">
                Current status of the NeuroLift AI Fusion training platform
              </p>
            </div>
            <Button
              variant="ghost"
              size="sm"
              className="shrink-0 text-xs text-muted-foreground hover:text-foreground"
              onClick={toggleAllSections}
            >
              {anySectionOpen ? 'Collapse All' : 'Expand All'}
            </Button>
          </div>

          {/* ═══════════════════ Section 1: Overview Cards ═══════════════════ */}
          <Card className="rounded-xl border border-border/60 bg-card shadow-sm dark:shadow-none">
            <Collapsible open={openSections.overview} onOpenChange={() => toggleSection('overview')}>
              <CollapsibleTrigger className="-m-6 mb-0 w-full p-6 cursor-pointer select-none hover:bg-muted/50 rounded-t-lg transition-colors">
                <div className="flex items-center justify-between">
                  <h3 className="text-lg font-semibold">Overview Cards</h3>
                  <motion.span animate={{ rotate: openSections.overview ? 0 : -90 }} transition={{ duration: 0.2 }}>
                    <ChevronDown className="h-4 w-4 text-muted-foreground" />
                  </motion.span>
                </div>
              </CollapsibleTrigger>
              <CollapsibleContent>
                <CardContent className="p-5 sm:p-6 pt-0">
                  {/* Stat cards grid */}
                  <motion.div
                    className="grid grid-cols-2 gap-4 md:grid-cols-4 md:gap-6"
                    variants={containerVariants}
                    initial="hidden"
                    animate={isInView ? 'visible' : 'hidden'}
                  >
                    {statItems.map((item, i) => (
                      <motion.div key={item.label} variants={itemVariants}>
                        <Card className="rounded-xl border border-border/60 bg-card shadow-sm transition-shadow hover:shadow-md dark:shadow-none dark:hover:shadow-lg">
                          <CardContent className="flex flex-col items-center gap-3 p-5 text-center sm:p-6">
                            <div
                              className={`flex h-11 w-11 items-center justify-center rounded-full ${item.iconBg}`}
                            >
                              {item.icon}
                            </div>
                            <div className="flex items-center gap-2">
                              <MiniRadialGauge pct={item.gaugePct} inView={isInView} />
                              <p className="text-3xl font-bold tracking-tight sm:text-4xl">
                                {displayValues[i]}
                              </p>
                            </div>
                            <p className="text-sm font-medium text-foreground/80">
                              {item.label}
                            </p>
                            <p className="text-xs text-muted-foreground">
                              {item.description === EMPATHY_LABELS[d.topEmpathy]
                                ? 'Highest empathy depth'
                                : item.description}
                            </p>
                          </CardContent>
                        </Card>
                      </motion.div>
                    ))}
                  </motion.div>
                </CardContent>
              </CollapsibleContent>
            </Collapsible>
          </Card>

          {/* ═══════════════════ Section 2: Development Progress ═══════════════════ */}
          <Card className="mt-6 rounded-xl border border-border/60 bg-card shadow-sm dark:shadow-none">
            <Collapsible open={openSections.progress} onOpenChange={() => toggleSection('progress')}>
              <CollapsibleTrigger className="-m-6 mb-0 w-full p-6 cursor-pointer select-none hover:bg-muted/50 rounded-t-lg transition-colors">
                <div className="flex items-center justify-between">
                  <h3 className="text-lg font-semibold">Development Progress</h3>
                  <motion.span animate={{ rotate: openSections.progress ? 0 : -90 }} transition={{ duration: 0.2 }}>
                    <ChevronDown className="h-4 w-4 text-muted-foreground" />
                  </motion.span>
                </div>
              </CollapsibleTrigger>
              <CollapsibleContent>
                <CardContent className="p-5 sm:p-6 pt-0">
                {/* Stacked horizontal bar */}
                <div className="flex h-9 w-full overflow-hidden rounded-lg">
                  {(Object.keys(STATUS_BAR_COLORS) as FusionStatus[]).map(
                    (status) => {
                      const count = d.statusCounts[status];
                      if (count === 0) return null;
                      const pct = (count / d.total) * 100;
                      return (
                        <div
                          key={status}
                          className={`${STATUS_BAR_COLORS[status]} transition-all duration-700 first:rounded-l-lg last:rounded-r-lg hover:brightness-110`}
                          style={{ width: `${pct}%` }}
                          title={`${STATUS_CONFIG[status].label}: ${count}`}
                        />
                      );
                    },
                  )}
                </div>
                {/* Legend with counts */}
                <div className="mt-3 flex flex-wrap gap-x-5 gap-y-2">
                  {(Object.keys(STATUS_BAR_COLORS) as FusionStatus[]).map(
                    (status) => {
                      const count = d.statusCounts[status];
                      return (
                        <div
                          key={status}
                          className="flex items-center gap-2 text-sm"
                        >
                          <span
                            className={`inline-block h-3 w-3 rounded-full ${STATUS_BAR_COLORS[status]}`}
                          />
                          <span className="text-muted-foreground">
                            {STATUS_CONFIG[status].label}
                          </span>
                          <span className="font-semibold">{count}</span>
                        </div>
                      );
                    },
                  )}
                </div>
                </CardContent>
              </CollapsibleContent>
            </Collapsible>
          </Card>

          {/* ═══════════════════ Section 3: Category Distribution ═══════════════════ */}
          <Card className="mt-6 rounded-xl border border-border/60 bg-card shadow-sm dark:shadow-none">
            <Collapsible open={openSections.charts} onOpenChange={() => toggleSection('charts')}>
              <CollapsibleTrigger className="-m-6 mb-0 w-full p-6 cursor-pointer select-none hover:bg-muted/50 rounded-t-lg transition-colors">
                <div className="flex items-center justify-between">
                  <h3 className="text-lg font-semibold">Charts</h3>
                  <motion.span animate={{ rotate: openSections.charts ? 0 : -90 }} transition={{ duration: 0.2 }}>
                    <ChevronDown className="h-4 w-4 text-muted-foreground" />
                  </motion.span>
                </div>
              </CollapsibleTrigger>
              <CollapsibleContent>
                <CardContent className="p-5 sm:p-6 pt-0">
                  <div className="grid gap-4 md:grid-cols-2 md:gap-6">
                    {/* Executive Function */}
                    <Card className="overflow-hidden rounded-xl border border-border/60 bg-card shadow-sm dark:shadow-none">
                      <CardHeader className="border-b border-orange-500/20 bg-orange-500/5 pb-3">
                        <CardTitle className="flex items-center justify-between text-base font-semibold">
                          <span className="flex items-center gap-2">
                            <span className="inline-block h-2.5 w-2.5 rounded-full bg-orange-500" />
                            Executive Function
                          </span>
                          <Badge
                            variant="secondary"
                            className="bg-orange-500/15 text-orange-600 hover:bg-orange-500/20"
                          >
                            {d.executiveFunction} pairs
                          </Badge>
                        </CardTitle>
                      </CardHeader>
                      <CardContent className="p-4">
                        <div className="flex max-h-40 flex-wrap gap-1.5 overflow-y-auto">
                          {d.executivePairs.map((p) => (
                            <Badge
                              key={p.id}
                              variant="outline"
                              className="border-border/60 text-xs font-normal text-muted-foreground"
                            >
                              {p.avatarName}
                            </Badge>
                          ))}
                        </div>
                      </CardContent>
                    </Card>

                    {/* Non-Executive Function */}
                    <Card className="overflow-hidden rounded-xl border border-border/60 bg-card shadow-sm dark:shadow-none">
                      <CardHeader className="border-b border-emerald-500/20 bg-emerald-500/5 pb-3">
                        <CardTitle className="flex items-center justify-between text-base font-semibold">
                          <span className="flex items-center gap-2">
                            <span className="inline-block h-2.5 w-2.5 rounded-full bg-emerald-500" />
                            Non-Executive Function
                          </span>
                          <Badge
                            variant="secondary"
                            className="bg-emerald-500/15 text-emerald-600 hover:bg-emerald-500/20"
                          >
                            {d.nonExecutiveFunction} pairs
                          </Badge>
                        </CardTitle>
                      </CardHeader>
                      <CardContent className="p-4">
                        <div className="flex max-h-40 flex-wrap gap-1.5 overflow-y-auto">
                          {d.nonExecutivePairs.map((p) => (
                            <Badge
                              key={p.id}
                              variant="outline"
                              className="border-border/60 text-xs font-normal text-muted-foreground"
                            >
                              {p.avatarName}
                            </Badge>
                          ))}
                        </div>
                      </CardContent>
                    </Card>
                  </div>
                </CardContent>
              </CollapsibleContent>
            </Collapsible>
          </Card>
          {/* ═══════════════════ Section 4: Interactive Charts ═══════════════════ */}
          <Card className="mt-6 rounded-xl border border-border/60 bg-card shadow-sm dark:shadow-none">
            <Collapsible open={openSections.detailed} onOpenChange={() => toggleSection('detailed')}>
              <CollapsibleTrigger className="-m-6 mb-0 w-full p-6 cursor-pointer select-none hover:bg-muted/50 rounded-t-lg transition-colors">
                <div className="flex items-center justify-between">
                  <h3 className="text-lg font-semibold">Detailed Analytics</h3>
                  <motion.span animate={{ rotate: openSections.detailed ? 0 : -90 }} transition={{ duration: 0.2 }}>
                    <ChevronDown className="h-4 w-4 text-muted-foreground" />
                  </motion.span>
                </div>
              </CollapsibleTrigger>
              <CollapsibleContent>
                <CardContent className="p-5 sm:p-6 pt-0">
            <ChartsSection isInView={isInView} d={d} />

            {/* ── Readiness Distribution Treemap ────────────────────── */}
            <div ref={treemapRef} className="mt-6">
              <Card className="rounded-xl border border-border/60 bg-card shadow-sm dark:shadow-none">
                <CardHeader className="pb-3">
                  <CardTitle className="flex items-center gap-2 text-base font-semibold">
                    <BarChartIcon className="h-4 w-4 text-muted-foreground" />
                    Readiness Distribution
                  </CardTitle>
                </CardHeader>
                <CardContent className="p-4 sm:p-6">
                  <div className="grid grid-cols-3 gap-2 sm:grid-cols-4 md:grid-cols-5">
                    {treemapData.map((item, index) => (
                      <motion.div
                        key={item.name}
                        initial={{ opacity: 0, scale: 0.9 }}
                        animate={
                          treemapInView
                            ? { opacity: 1, scale: 1 }
                            : { opacity: 0, scale: 0.9 }
                        }
                        transition={{ duration: 0.35, delay: index * 0.03 }}
                        className="group relative overflow-hidden rounded-lg transition-transform hover:scale-[1.03]"
                        style={{
                          height: `${Math.max(48, item.value * 0.8)}px`,
                          borderLeft: `3px solid ${item.color}`,
                        }}
                        title={`${item.name} — ${item.trait} — ${item.value}% readiness`}
                      >
                        {/* Base background 15% */}
                        <div
                          className="absolute inset-0 transition-opacity group-hover:opacity-0"
                          style={{ backgroundColor: `${item.color}15` }}
                          aria-hidden="true"
                        />
                        {/* Hover background 25% */}
                        <div
                          className="absolute inset-0 opacity-0 transition-opacity group-hover:opacity-100"
                          style={{ backgroundColor: `${item.color}40` }}
                          aria-hidden="true"
                        />
                        <div className="flex h-full flex-col justify-between px-2.5 py-2">
                          <span className="truncate text-xs font-medium text-foreground/80">
                            {item.name.length > 12
                              ? `${item.name.slice(0, 12)}…`
                              : item.name}
                          </span>
                          <span className="text-sm font-bold tabular-nums text-foreground">
                            {item.value}%
                          </span>
                        </div>
                        {/* Bottom color band */}
                        <div
                          className="absolute bottom-0 left-0 h-[2px]"
                          style={{
                            width: `${item.value}%`,
                            backgroundColor: item.color,
                          }}
                        />
                      </motion.div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>
                </CardContent>
              </CollapsibleContent>
            </Collapsible>
          </Card>
        </div>
      </section>

      {/* ═══════════════════ Section 5: Footer ═══════════════════ */}
      <footer className="mt-auto border-t border-border bg-foreground/[0.03] dark:bg-foreground/[0.02]">
        <div className="mx-auto max-w-6xl px-4 py-10 sm:px-6 sm:py-14 lg:px-8">
          <div className="flex flex-col gap-8 md:flex-row md:items-start md:justify-between">
            {/* Branding */}
            <div className="max-w-sm">
              <h3 className="text-xl font-bold tracking-tight">
                <span style={{ color: '#F38020' }}>NeuroLift</span>{' '}
                <span className="text-foreground">AI Fusion</span>
              </h3>
              <p className="mt-2 text-sm italic text-muted-foreground">
                &ldquo;Nothing About Us Without Us&rdquo;
              </p>
              <p className="mt-3 text-xs leading-relaxed text-muted-foreground/70">
                Learning through experience, not just data.
              </p>
            </div>

            {/* Links */}
            <div className="flex gap-6">
              <a
                href="https://github.com"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-2 text-sm text-muted-foreground transition-colors hover:text-foreground"
                aria-label="GitHub"
              >
                <Github className="h-4 w-4" />
                <span>GitHub</span>
              </a>
              <a
                href="https://neuroliftsolutions.com"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-2 text-sm text-muted-foreground transition-colors hover:text-foreground"
                aria-label="Website"
              >
                <Globe className="h-4 w-4" />
                <span>Website</span>
              </a>
              <a
                href="mailto:neuro.edge24@gmail.com"
                className="flex items-center gap-2 text-sm text-muted-foreground transition-colors hover:text-foreground"
                aria-label="Email"
              >
                <Mail className="h-4 w-4" />
                <span>Email</span>
              </a>
            </div>
          </div>

          {/* Divider */}
          <div className="mt-8 border-t border-border/60" />

          {/* About paragraph */}
          <p className="mt-6 text-center text-xs leading-relaxed text-muted-foreground/60">
            An interactive visualization of 19 Avatar-Aide-Advocate fusion pairs for ADHD experiential learning AI training.
          </p>

          {/* Built With tech stack badges */}
          <div className="mt-4 flex flex-wrap items-center justify-center gap-2">
            <span className="text-[11px] font-medium text-muted-foreground/50">Built with</span>
            {['Next.js', 'React', 'Tailwind CSS', 'Framer Motion', 'Recharts'].map((tech) => (
              <span
                key={tech}
                className="inline-flex items-center rounded-full bg-muted/60 px-2.5 py-0.5 text-[11px] font-medium text-muted-foreground/70"
              >
                {tech}
              </span>
            ))}
          </div>

          {/* Copyright */}
          <div className="mt-6 border-t border-border pt-6 text-center">
            <p className="text-xs text-muted-foreground/60">
              &copy; 2025 NeuroLift Technologies. Joshua W. Dorsey, Sr.
            </p>
          </div>
        </div>
      </footer>
    </>
  );
}
