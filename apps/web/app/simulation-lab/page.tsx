"use client";

import { useMemo, useState, type ReactNode } from "react";
import {
  detailLevels,
  simulationLabFixture,
  type DetailLevel,
  type FusionGate,
  type GateStatus,
  type LabMetric,
  type LabTask,
  type LabTaskStatus,
  type Stressor,
  type TimelineEvent,
} from "../../src/simulation/lab/stayAlertMorningRoutine";

const metricToneClasses: Record<LabMetric["tone"], string> = {
  calm: "text-[var(--lab-green)]",
  focus: "text-[var(--lab-blue)]",
  warm: "text-[var(--lab-amber)]",
  alert: "text-[var(--lab-rose)]",
};

const taskStatusClasses: Record<LabTaskStatus, string> = {
  complete: "border-[var(--lab-green)] bg-[var(--lab-green-soft)] text-[var(--lab-green)]",
  active: "border-[var(--lab-blue)] bg-[var(--lab-blue-soft)] text-[var(--lab-blue)]",
  watch: "border-[var(--lab-amber)] bg-[var(--lab-amber-soft)] text-[var(--lab-amber)]",
  pending: "border-[var(--lab-line)] bg-[var(--lab-surface-soft)] text-[var(--lab-muted)]",
};

const eventTypeClasses: Record<TimelineEvent["eventType"], string> = {
  task: "bg-[var(--lab-blue)]",
  stressor: "bg-[var(--lab-rose)]",
  intervention: "bg-[var(--lab-teal)]",
  recovery: "bg-[var(--lab-green)]",
};

const gateStatusClasses: Record<GateStatus, string> = {
  ready: "text-[var(--lab-green)] bg-[var(--lab-green-soft)]",
  watch: "text-[var(--lab-amber)] bg-[var(--lab-amber-soft)]",
  blocked: "text-[var(--lab-rose)] bg-[var(--lab-rose-soft)]",
};

const speedOptions = [0.5, 1, 1.5];

function ProgressBar({ value, tone }: { value: number; tone: LabMetric["tone"] | GateStatus }) {
  const colorClass =
    tone === "ready" || tone === "calm"
      ? "bg-[var(--lab-green)]"
      : tone === "blocked" || tone === "alert"
        ? "bg-[var(--lab-rose)]"
        : tone === "watch" || tone === "warm"
          ? "bg-[var(--lab-amber)]"
          : "bg-[var(--lab-blue)]";

  return (
    <div className="h-2 rounded-full bg-[var(--lab-surface-soft)] overflow-hidden">
      <div
        className={`h-full rounded-full transition-all motion-reduce:transition-none ${colorClass}`}
        style={{ width: `${Math.min(value, 100)}%` }}
      />
    </div>
  );
}

function Panel({
  title,
  eyebrow,
  children,
}: {
  title: string;
  eyebrow?: string;
  children: ReactNode;
}) {
  return (
    <section className="rounded-lg border border-[var(--lab-line)] bg-[var(--lab-panel)] p-5 shadow-sm shadow-black/20">
      <div className="mb-4">
        {eyebrow && (
          <div className="mb-1 text-xs font-semibold uppercase tracking-wide text-[var(--lab-muted)]">
            {eyebrow}
          </div>
        )}
        <h2 className="text-lg font-semibold text-[var(--lab-text)]">{title}</h2>
      </div>
      {children}
    </section>
  );
}

function StatusPill({ label, className }: { label: string; className: string }) {
  return (
    <span className={`inline-flex rounded-full px-2.5 py-1 text-xs font-semibold ${className}`}>
      {label}
    </span>
  );
}

function WorldMarker({ task }: { task: LabTask }) {
  return (
    <div
      className="absolute -translate-x-1/2 -translate-y-1/2"
      style={{ left: `${task.position.left}%`, top: `${task.position.top}%` }}
    >
      <div
        className={`min-w-28 rounded-lg border px-3 py-2 text-xs font-semibold shadow-lg shadow-black/30 ${taskStatusClasses[task.status]}`}
      >
        <div>{task.label}</div>
        <div className="mt-1 text-[10px] font-normal opacity-80">{task.location}</div>
      </div>
    </div>
  );
}

function StressorMarker({ stressor }: { stressor: Stressor }) {
  if (!stressor.active) return null;

  const pressureClass =
    stressor.pressure === "high"
      ? "border-[var(--lab-rose)] bg-[var(--lab-rose-soft)] text-[var(--lab-rose)]"
      : "border-[var(--lab-amber)] bg-[var(--lab-amber-soft)] text-[var(--lab-amber)]";

  return (
    <div
      className="absolute -translate-x-1/2 -translate-y-1/2"
      style={{ left: `${stressor.position.left}%`, top: `${stressor.position.top}%` }}
    >
      <div className={`rounded-full border px-3 py-1 text-[11px] font-semibold ${pressureClass}`}>
        {stressor.label}
      </div>
    </div>
  );
}

function WorldView() {
  const { scenario, tasks, stressors } = simulationLabFixture;

  return (
    <Panel title="World View" eyebrow={scenario.environment}>
      <div className="relative min-h-[390px] overflow-hidden rounded-lg border border-[var(--lab-line)] bg-[#101722]">
        <div className="absolute left-[5%] top-[12%] h-[38%] w-[38%] rounded-lg border border-[var(--lab-line)] bg-[#182335] p-3 text-xs text-[var(--lab-muted)]">
          Desk and living area
        </div>
        <div className="absolute right-[6%] top-[12%] h-[38%] w-[34%] rounded-lg border border-[var(--lab-line)] bg-[#1d2732] p-3 text-xs text-[var(--lab-muted)]">
          Kitchen
        </div>
        <div className="absolute bottom-[10%] left-[10%] h-[32%] w-[78%] rounded-lg border border-[var(--lab-line)] bg-[#172235] p-3 text-xs text-[var(--lab-muted)]">
          Entry path
        </div>
        <div className="absolute left-[49%] top-[50%] h-9 w-9 -translate-x-1/2 -translate-y-1/2 rounded-full border-2 border-white/80 bg-[var(--lab-teal)] shadow-lg shadow-black/30" />
        <div className="absolute left-[49%] top-[58%] -translate-x-1/2 rounded-full bg-black/35 px-3 py-1 text-xs font-semibold text-white">
          StayAlert Avatar
        </div>
        {tasks.map((task) => (
          <WorldMarker key={task.id} task={task} />
        ))}
        {stressors.map((stressor) => (
          <StressorMarker key={stressor.id} stressor={stressor} />
        ))}
      </div>
      <div className="mt-4 grid gap-3 text-sm text-[var(--lab-muted)] md:grid-cols-3">
        <div>
          <span className="text-[var(--lab-text)]">Clock:</span> {scenario.simulatedClock}
        </div>
        <div>
          <span className="text-[var(--lab-text)]">Attempt:</span> {scenario.attemptNumber}
        </div>
        <div>
          <span className="text-[var(--lab-text)]">Status:</span> {scenario.status}
        </div>
      </div>
    </Panel>
  );
}

function AvatarStatePanel() {
  const { avatar, aide, metrics } = simulationLabFixture;

  return (
    <Panel title="Avatar State" eyebrow={`${avatar.name} + ${aide.name}`}>
      <div className="space-y-5">
        <div className="rounded-lg border border-[var(--lab-line)] bg-[var(--lab-surface)] p-4">
          <div className="text-sm text-[var(--lab-muted)]">Current task</div>
          <div className="mt-1 text-xl font-semibold text-[var(--lab-text)]">{avatar.currentTask}</div>
          <p className="mt-2 text-sm leading-6 text-[var(--lab-muted)]">{avatar.learnedStrategy}</p>
        </div>
        <div className="space-y-4">
          {metrics.map((metric) => (
            <div key={metric.label}>
              <div className="mb-1.5 flex items-center justify-between gap-3">
                <span className="text-sm text-[var(--lab-muted)]">{metric.label}</span>
                <span className={`text-sm font-semibold ${metricToneClasses[metric.tone]}`}>
                  {metric.value}/{metric.max}
                </span>
              </div>
              <ProgressBar value={(metric.value / metric.max) * 100} tone={metric.tone} />
              <p className="mt-1.5 text-xs leading-5 text-[var(--lab-muted)]">{metric.summary}</p>
            </div>
          ))}
        </div>
        <div>
          <div className="mb-2 text-sm font-semibold text-[var(--lab-text)]">Struggle signals</div>
          <div className="flex flex-wrap gap-2">
            {avatar.struggleSignals.map((signal) => (
              <StatusPill
                key={signal}
                label={signal}
                className="bg-[var(--lab-surface-soft)] text-[var(--lab-muted)]"
              />
            ))}
          </div>
        </div>
        <div className="border-t border-[var(--lab-line)] pt-4">
          <div className="text-sm font-semibold text-[var(--lab-text)]">{aide.currentMode}</div>
          <p className="mt-1 text-sm leading-6 text-[var(--lab-muted)]">{aide.fadePlan}</p>
        </div>
      </div>
    </Panel>
  );
}

function TimelinePanel({
  selectedIndex,
  onSelect,
  detailLevel,
}: {
  selectedIndex: number;
  onSelect: (index: number) => void;
  detailLevel: DetailLevel;
}) {
  const events = simulationLabFixture.timeline;
  const selected = events[selectedIndex];

  const detailText =
    detailLevel === "Simple"
      ? selected.summary
      : detailLevel === "Coach"
        ? selected.coachNote
        : selected.technicalNote;

  return (
    <Panel title="Learning Timeline" eyebrow="Attempt progression">
      <div className="grid gap-4 lg:grid-cols-[220px_minmax(0,1fr)]">
        <div className="space-y-2">
          {events.map((event, index) => (
            <button
              key={`${event.minute}-${event.title}`}
              type="button"
              onClick={() => onSelect(index)}
              className={`w-full rounded-lg border px-3 py-2 text-left text-sm transition-colors motion-reduce:transition-none ${
                index === selectedIndex
                  ? "border-[var(--lab-blue)] bg-[var(--lab-blue-soft)] text-[var(--lab-text)]"
                  : "border-[var(--lab-line)] bg-transparent text-[var(--lab-muted)] hover:border-[var(--lab-blue)]"
              }`}
            >
              <span className={`mr-2 inline-block h-2.5 w-2.5 rounded-full ${eventTypeClasses[event.eventType]}`} />
              <span className="font-mono text-xs">{event.minute}</span>
              <div className="mt-1 font-semibold">{event.title}</div>
            </button>
          ))}
        </div>
        <div className="rounded-lg border border-[var(--lab-line)] bg-[var(--lab-surface)] p-4">
          <div className="mb-2 flex flex-wrap items-center gap-2">
            <StatusPill
              label={selected.eventType}
              className="bg-[var(--lab-surface-soft)] text-[var(--lab-muted)] capitalize"
            />
            <span className="font-mono text-xs text-[var(--lab-muted)]">{selected.minute}</span>
          </div>
          <h3 className="text-xl font-semibold text-[var(--lab-text)]">{selected.title}</h3>
          <p className="mt-3 text-sm leading-6 text-[var(--lab-muted)]">{detailText}</p>
        </div>
      </div>
    </Panel>
  );
}

function AideLogPanel() {
  const { interventions } = simulationLabFixture;

  return (
    <Panel title="Aide Intervention Log" eyebrow="Support fading">
      <div className="divide-y divide-[var(--lab-line)]">
        {interventions.map((entry) => (
          <div key={`${entry.minute}-${entry.strategy}`} className="py-4 first:pt-0 last:pb-0">
            <div className="mb-2 flex flex-wrap items-center gap-2">
              <span className="font-mono text-xs text-[var(--lab-muted)]">{entry.minute}</span>
              <StatusPill
                label={entry.supportLevel}
                className="bg-[var(--lab-teal-soft)] text-[var(--lab-teal)]"
              />
            </div>
            <div className="font-semibold text-[var(--lab-text)]">{entry.strategy}</div>
            <p className="mt-2 text-sm leading-6 text-[var(--lab-muted)]">{entry.reason}</p>
            <p className="mt-2 text-sm leading-6 text-[var(--lab-text)]">{entry.result}</p>
          </div>
        ))}
      </div>
    </Panel>
  );
}

function IndependencePanel() {
  const { attemptTrend } = simulationLabFixture;

  return (
    <Panel title="Independence Meter" eyebrow="Repeated attempts">
      <div className="space-y-4">
        {attemptTrend.map((attempt) => (
          <div key={attempt.attempt} className="grid gap-2 md:grid-cols-[90px_minmax(0,1fr)_80px] md:items-center">
            <div className="text-sm font-semibold text-[var(--lab-text)]">Attempt {attempt.attempt}</div>
            <div>
              <div className="mb-1 flex justify-between text-xs text-[var(--lab-muted)]">
                <span>Independence {attempt.independence}%</span>
                <span>Support need {attempt.supportNeed}%</span>
              </div>
              <ProgressBar value={attempt.independence} tone="calm" />
            </div>
            <div className="text-sm text-[var(--lab-muted)]">{attempt.completedTasks}/5 tasks</div>
          </div>
        ))}
      </div>
    </Panel>
  );
}

function FusionGatePanel() {
  const gates = simulationLabFixture.fusionGates;

  const gateTone = (gate: FusionGate) => gate.status;

  return (
    <Panel title="Fusion Gate" eyebrow="Prototype criteria">
      <div className="space-y-4">
        {gates.map((gate) => (
          <div key={gate.label}>
            <div className="mb-2 flex flex-wrap items-center justify-between gap-2">
              <div className="font-semibold text-[var(--lab-text)]">{gate.label}</div>
              <StatusPill label={gate.status} className={gateStatusClasses[gate.status]} />
            </div>
            <ProgressBar value={gate.progress} tone={gateTone(gate)} />
            <p className="mt-2 text-sm leading-6 text-[var(--lab-muted)]">{gate.summary}</p>
          </div>
        ))}
      </div>
    </Panel>
  );
}

export default function SimulationLab() {
  const [isPaused, setIsPaused] = useState(true);
  const [speed, setSpeed] = useState(1);
  const [detailLevel, setDetailLevel] = useState<DetailLevel>("Simple");
  const [selectedEventIndex, setSelectedEventIndex] = useState(0);

  const activeTasks = useMemo(
    () => simulationLabFixture.tasks.filter((task) => task.status === "active" || task.status === "watch"),
    [],
  );

  return (
    <div className="-mx-6 -my-8 min-h-[calc(100vh-4rem)] bg-[var(--lab-bg)] px-4 py-6 text-left sm:px-6 lg:px-8">
      <div className="mx-auto max-w-6xl space-y-6">
      <div className="flex flex-col gap-4 rounded-lg border border-[var(--lab-line)] bg-[var(--lab-panel)] p-5 lg:flex-row lg:items-start lg:justify-between">
        <div className="max-w-3xl">
          <div className="text-xs font-semibold uppercase tracking-wide text-[var(--lab-muted)]">
            Simulation Lab
          </div>
          <h1 className="mt-2 text-3xl font-bold text-[var(--lab-text)]">
            {simulationLabFixture.scenario.name}
          </h1>
          <p className="mt-3 max-w-2xl text-sm leading-6 text-[var(--lab-muted)]">
            {simulationLabFixture.scenario.objective}
          </p>
          <div className="mt-4 flex flex-wrap gap-2">
            <StatusPill
              label={simulationLabFixture.scenario.track}
              className="bg-[var(--lab-blue-soft)] text-[var(--lab-blue)]"
            />
            <StatusPill
              label={`${activeTasks.length} watched tasks`}
              className="bg-[var(--lab-amber-soft)] text-[var(--lab-amber)]"
            />
          </div>
        </div>
        <div className="grid gap-3 sm:grid-cols-3 lg:min-w-[360px]">
          <button
            type="button"
            onClick={() => setIsPaused((current) => !current)}
            className="rounded-lg bg-[var(--lab-blue)] px-4 py-2 text-sm font-semibold text-[#06111f] transition-colors hover:bg-[var(--lab-blue-hover)] motion-reduce:transition-none"
          >
            {isPaused ? "Resume" : "Pause"}
          </button>
          <select
            aria-label="Simulation speed"
            value={speed}
            onChange={(event) => setSpeed(Number(event.target.value))}
            className="rounded-lg border border-[var(--lab-line)] bg-[var(--lab-surface)] px-3 py-2 text-sm text-[var(--lab-text)]"
          >
            {speedOptions.map((option) => (
              <option key={option} value={option}>
                {option}x
              </option>
            ))}
          </select>
          <select
            aria-label="Detail level"
            value={detailLevel}
            onChange={(event) => setDetailLevel(event.target.value as DetailLevel)}
            className="rounded-lg border border-[var(--lab-line)] bg-[var(--lab-surface)] px-3 py-2 text-sm text-[var(--lab-text)]"
          >
            {detailLevels.map((level) => (
              <option key={level} value={level}>
                {level}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="grid gap-6 xl:grid-cols-[minmax(0,1.35fr)_minmax(340px,0.65fr)]">
        <WorldView />
        <AvatarStatePanel />
      </div>

      <div className="grid gap-6 xl:grid-cols-[minmax(0,1fr)_minmax(340px,0.72fr)]">
        <TimelinePanel
          selectedIndex={selectedEventIndex}
          onSelect={setSelectedEventIndex}
          detailLevel={detailLevel}
        />
        <AideLogPanel />
      </div>

      <div className="grid gap-6 xl:grid-cols-2">
        <IndependencePanel />
        <FusionGatePanel />
      </div>
      </div>
    </div>
  );
}


