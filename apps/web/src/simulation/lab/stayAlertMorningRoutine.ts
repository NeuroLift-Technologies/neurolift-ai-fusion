export type DetailLevel = "Simple" | "Coach" | "Technical";

export type LabTaskStatus = "complete" | "active" | "watch" | "pending";

export type GateStatus = "ready" | "watch" | "blocked";

export interface LabMetric {
  label: string;
  value: number;
  max: number;
  tone: "calm" | "focus" | "warm" | "alert";
  summary: string;
}

export interface LabTask {
  id: string;
  label: string;
  location: string;
  status: LabTaskStatus;
  risk: string;
  minutesRemaining: number;
  position: {
    left: number;
    top: number;
  };
}

export interface Stressor {
  id: string;
  label: string;
  active: boolean;
  pressure: "low" | "medium" | "high";
  position: {
    left: number;
    top: number;
  };
}

export interface TimelineEvent {
  minute: string;
  title: string;
  eventType: "task" | "stressor" | "intervention" | "recovery";
  summary: string;
  coachNote: string;
  technicalNote: string;
}

export interface Intervention {
  minute: string;
  strategy: string;
  reason: string;
  result: string;
  supportLevel: "direct" | "guided" | "observing";
}

export interface AttemptTrend {
  attempt: number;
  independence: number;
  supportNeed: number;
  completedTasks: number;
}

export interface FusionGate {
  label: string;
  status: GateStatus;
  progress: number;
  summary: string;
}

export const detailLevels: DetailLevel[] = ["Simple", "Coach", "Technical"];

export const simulationLabFixture = {
  scenario: {
    name: "StayAlert: Apartment Morning Routine",
    route: "/simulation-lab",
    track: "Sustained attention and focus",
    environment: "Apartment morning routine",
    attemptNumber: 4,
    simulatedClock: "8:12 AM",
    status: "Aide observing while Avatar self-recovers",
    objective: "Leave for a 9:00 AM work meeting with notes, breakfast, bag, and one reply sent.",
  },
  avatar: {
    name: "StayAlert Avatar",
    challenge: "Attention drift under mild time pressure",
    currentTask: "Pack work items",
    learnedStrategy: "Two-item scan, then confirm the bag before moving on",
    struggleSignals: ["phone pull", "misplaced notes", "task drift after noise"],
  },
  aide: {
    name: "Focus Aide",
    expertise: "Attention support, task chunking, recovery prompts",
    currentMode: "Observing before intervening",
    fadePlan: "Wait 20 seconds for self-recovery before offering a smaller next step.",
  },
  metrics: [
    {
      label: "Attention energy",
      value: 64,
      max: 100,
      tone: "focus",
      summary: "Enough energy to continue, but distraction risk is rising.",
    },
    {
      label: "Stress",
      value: 38,
      max: 100,
      tone: "warm",
      summary: "Stress is present and still within the target tolerance band.",
    },
    {
      label: "Cognitive load",
      value: 55,
      max: 100,
      tone: "warm",
      summary: "The task stack is getting crowded after the noise event.",
    },
    {
      label: "Confidence",
      value: 71,
      max: 100,
      tone: "calm",
      summary: "Confidence improved after independent recovery on the notes task.",
    },
  ] satisfies LabMetric[],
  tasks: [
    {
      id: "meeting-notes",
      label: "Review meeting notes",
      location: "Desk",
      status: "complete",
      risk: "Done after one self-reset",
      minutesRemaining: 0,
      position: { left: 24, top: 31 },
    },
    {
      id: "breakfast",
      label: "Prepare breakfast",
      location: "Kitchen",
      status: "complete",
      risk: "Kept simple",
      minutesRemaining: 0,
      position: { left: 77, top: 31 },
    },
    {
      id: "pack-bag",
      label: "Pack work items",
      location: "Entry table",
      status: "active",
      risk: "Two items left",
      minutesRemaining: 6,
      position: { left: 55, top: 73 },
    },
    {
      id: "reply-message",
      label: "Reply to important message",
      location: "Phone",
      status: "watch",
      risk: "Could pull attention off routine",
      minutesRemaining: 4,
      position: { left: 35, top: 70 },
    },
    {
      id: "leave",
      label: "Leave on time",
      location: "Door",
      status: "pending",
      risk: "Deadline in 18 minutes",
      minutesRemaining: 18,
      position: { left: 85, top: 75 },
    },
  ] satisfies LabTask[],
  stressors: [
    {
      id: "notification",
      label: "Phone notification",
      active: true,
      pressure: "high",
      position: { left: 35, top: 61 },
    },
    {
      id: "background-noise",
      label: "Hallway noise",
      active: true,
      pressure: "medium",
      position: { left: 12, top: 72 },
    },
    {
      id: "misplaced-item",
      label: "Misplaced badge",
      active: false,
      pressure: "medium",
      position: { left: 58, top: 64 },
    },
  ] satisfies Stressor[],
  timeline: [
    {
      minute: "00:00",
      title: "Routine starts",
      eventType: "task",
      summary: "The Avatar starts with meeting notes visible on the desk.",
      coachNote: "Aide holds back to preserve independence.",
      technicalNote: "Initial support need 0.42, cognitive load 0.31.",
    },
    {
      minute: "03:20",
      title: "Phone pulls attention",
      eventType: "stressor",
      summary: "A notification interrupts the notes review.",
      coachNote: "Aide watches for self-recovery before prompting.",
      technicalNote: "Attention energy drops 9 points; task drift signal emitted.",
    },
    {
      minute: "04:05",
      title: "Self-reset works",
      eventType: "recovery",
      summary: "The Avatar uses a learned two-item scan and returns to notes.",
      coachNote: "This counts as an independence gain because no direct prompt was needed.",
      technicalNote: "Recovery latency 45 seconds; support need reduced by 0.04.",
    },
    {
      minute: "09:45",
      title: "Focus Aide gives a small cue",
      eventType: "intervention",
      summary: "The Aide suggests packing only laptop and badge first.",
      coachNote: "The cue is intentionally narrow to avoid over-supporting.",
      technicalNote: "Intervention strategy chunk_next_action, dependency risk low.",
    },
    {
      minute: "12:00",
      title: "Bag task resumes",
      eventType: "task",
      summary: "The Avatar checks the bag and continues without switching tasks.",
      coachNote: "Aide returns to observation mode.",
      technicalNote: "Current completion probability 0.76 for this attempt.",
    },
  ] satisfies TimelineEvent[],
  interventions: [
    {
      minute: "09:45",
      strategy: "Chunk next action",
      reason: "Packing task stalled after hallway noise increased cognitive load.",
      result: "Avatar resumed movement and packed laptop without escalation.",
      supportLevel: "guided",
    },
    {
      minute: "11:15",
      strategy: "Silence with observation",
      reason: "Avatar looked back to the checklist without an external prompt.",
      result: "Independent recovery preserved; Aide did not interrupt.",
      supportLevel: "observing",
    },
    {
      minute: "13:30",
      strategy: "Delay phone reply",
      reason: "The reply matters, but doing it now risks derailing departure.",
      result: "Queued after bag confirmation; dependency risk remains low.",
      supportLevel: "guided",
    },
  ] satisfies Intervention[],
  attemptTrend: [
    { attempt: 1, independence: 32, supportNeed: 68, completedTasks: 2 },
    { attempt: 2, independence: 47, supportNeed: 57, completedTasks: 3 },
    { attempt: 3, independence: 59, supportNeed: 44, completedTasks: 4 },
    { attempt: 4, independence: 68, supportNeed: 36, completedTasks: 4 },
  ] satisfies AttemptTrend[],
  fusionGates: [
    {
      label: "Self-recovery after attention drift",
      status: "ready",
      progress: 76,
      summary: "Recent attempts show recovery before direct prompting.",
    },
    {
      label: "Support fades over repeated attempts",
      status: "watch",
      progress: 62,
      summary: "Aide interventions are decreasing, but not stable yet.",
    },
    {
      label: "Stress remains tolerable",
      status: "ready",
      progress: 72,
      summary: "Stress is elevated without crossing the burnout band.",
    },
    {
      label: "Generalizes across variations",
      status: "blocked",
      progress: 34,
      summary: "Only one morning routine variation is represented in this fixture.",
    },
  ] satisfies FusionGate[],
};
