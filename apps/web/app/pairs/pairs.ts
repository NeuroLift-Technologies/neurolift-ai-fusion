export type PairStatus = "runtime-pair" | "avatar-implemented" | "design-proposal";

export type PairDomain =
  | "attention-focus"
  | "activation-planning"
  | "regulation-recovery"
  | "awareness-connection";

export type AvatarAidePair = {
  id: string;
  name: string;
  trait: string;
  tag: string;
  hue: number;
  flavor: string;
  blurb: string;
  aide: {
    name: string;
    style: string;
    techniques: string[];
  };
  status: PairStatus;
  domain: PairDomain;
};

export const domainLabels: Record<PairDomain, string> = {
  "attention-focus": "Attention & focus",
  "activation-planning": "Activation & planning",
  "regulation-recovery": "Regulation & recovery",
  "awareness-connection": "Awareness & connection",
};

export const statusLabels: Record<PairStatus, string> = {
  "runtime-pair": "Runtime pair",
  "avatar-implemented": "Avatar implemented",
  "design-proposal": "Design proposal",
};

export const avatarAidePairs: AvatarAidePair[] = [
  {
    id: "stay_alert",
    name: "StayAlert",
    trait: "Sustained Attention",
    tag: "SA",
    hue: 200,
    flavor: "attention",
    blurb: "Drifts off long tasks. Vulnerable to hyperfocus.",
    aide: {
      name: "Dr. Vance",
      style: "supportive skill-building",
      techniques: ["Pomodoro", "attention anchoring", "mental-fatigue management"],
    },
    status: "runtime-pair",
    domain: "attention-focus",
  },
  {
    id: "task_kickstart",
    name: "TaskKickstart",
    trait: "Task Initiation",
    tag: "TK",
    hue: 36,
    flavor: "initiation",
    blurb: "Knows what to do — can’t start.",
    aide: {
      name: "Coach Reyes",
      style: "gentle activation",
      techniques: ["two-minute starts", "ladder steps", "momentum"],
    },
    status: "avatar-implemented",
    domain: "activation-planning",
  },
  {
    id: "focus_flow",
    name: "FocusFlow",
    trait: "Hyperfocus / Switching",
    tag: "FF",
    hue: 168,
    flavor: "focus",
    blurb: "Tunnel vision. Forgets to switch.",
    aide: {
      name: "Coach Mei",
      style: "gentle boundary",
      techniques: ["externally-paced exits", "transition rituals"],
    },
    status: "design-proposal",
    domain: "attention-focus",
  },
  {
    id: "memory_mate",
    name: "MemoryMate",
    trait: "Working Memory",
    tag: "MM",
    hue: 268,
    flavor: "memory",
    blurb: "Loses the thread mid-sentence.",
    aide: {
      name: "Dr. Liang",
      style: "scaffolded",
      techniques: ["external memory", "chunking", "loop-backs"],
    },
    status: "design-proposal",
    domain: "attention-focus",
  },
  {
    id: "time_keeper",
    name: "TimeKeeper",
    trait: "Time Perception",
    tag: "TM",
    hue: 220,
    flavor: "time",
    blurb: "Now and not-now. No in-between.",
    aide: {
      name: "Coach Patel",
      style: "time-anchored",
      techniques: ["visible clocks", "time-blocking", "before / after"],
    },
    status: "design-proposal",
    domain: "attention-focus",
  },
  {
    id: "prioritize_it",
    name: "PrioritizeIt",
    trait: "Prioritization",
    tag: "PR",
    hue: 84,
    flavor: "planning",
    blurb: "All ideas, no rank order.",
    aide: {
      name: "Coach Olsen",
      style: "task scaffolding",
      techniques: ["Eisenhower sort", "MIT method", "one-thing rule"],
    },
    status: "design-proposal",
    domain: "activation-planning",
  },
  {
    id: "emo_steady",
    name: "EmoSteady",
    trait: "Emotional Regulation",
    tag: "ES",
    hue: 14,
    flavor: "emotion",
    blurb: "Feels everything at full volume.",
    aide: {
      name: "Dr. Aronson",
      style: "DBT-informed",
      techniques: ["name-the-wave", "grounding", "co-regulation"],
    },
    status: "design-proposal",
    domain: "regulation-recovery",
  },
  {
    id: "impulse_guard",
    name: "ImpulseGuard",
    trait: "Impulse Control",
    tag: "IG",
    hue: 348,
    flavor: "impulse",
    blurb: "Knows the stop sign, ignores it.",
    aide: {
      name: "Dr. Okafor",
      style: "CBT-flavored",
      techniques: ["pause-name-choose", "response delay", "cues"],
    },
    status: "design-proposal",
    domain: "regulation-recovery",
  },
  {
    id: "social_cue",
    name: "SocialCue",
    trait: "Social Cues",
    tag: "SC",
    hue: 318,
    flavor: "social",
    blurb: "Loses the social thread quickly.",
    aide: {
      name: "Coach Brand",
      style: "social skills",
      techniques: ["thread-tracking", "cue-cards", "graceful exits"],
    },
    status: "design-proposal",
    domain: "awareness-connection",
  },
  {
    id: "transition_ease",
    name: "TransitionEase",
    trait: "Task Switching",
    tag: "TE",
    hue: 290,
    flavor: "transition",
    blurb: "Sticky between contexts.",
    aide: {
      name: "Dr. Holst",
      style: "transition coaching",
      techniques: ["warning windows", "soft cuts", "landing pads"],
    },
    status: "design-proposal",
    domain: "activation-planning",
  },
  {
    id: "organize_well",
    name: "OrganizeWell",
    trait: "Organization",
    tag: "OW",
    hue: 188,
    flavor: "planning",
    blurb: "Visual zones blur fast.",
    aide: {
      name: "Coach Olsen",
      style: "environmental design",
      techniques: ["container method", "visual zones", "single-touch"],
    },
    status: "design-proposal",
    domain: "activation-planning",
  },
  {
    id: "follow_through",
    name: "FollowThrough",
    trait: "Task Completion",
    tag: "FT",
    hue: 138,
    flavor: "initiation",
    blurb: "Starts strong, fades at the finish.",
    aide: {
      name: "Coach Reyes",
      style: "completion ritual",
      techniques: ["finish-before-new", "done lists", "last-mile"],
    },
    status: "design-proposal",
    domain: "activation-planning",
  },
  {
    id: "listen_in",
    name: "ListenIn",
    trait: "Active Listening",
    tag: "LI",
    hue: 48,
    flavor: "monitor",
    blurb: "Mind walks during conversations.",
    aide: {
      name: "Coach Brand",
      style: "metacognitive",
      techniques: ["active recap", "note-anchors", "question prompts"],
    },
    status: "design-proposal",
    domain: "awareness-connection",
  },
  {
    id: "fidget_flow",
    name: "FidgetFlow",
    trait: "Physical Restlessness",
    tag: "FX",
    hue: 322,
    flavor: "sensory",
    blurb: "Needs motion to think.",
    aide: {
      name: "Coach Mei",
      style: "stim channeling",
      techniques: ["movement breaks", "stim objects", "stand-desk"],
    },
    status: "design-proposal",
    domain: "regulation-recovery",
  },
  {
    id: "restore_calm",
    name: "RestoreCalm",
    trait: "Stress Recovery",
    tag: "RC",
    hue: 142,
    flavor: "stress",
    blurb: "Spikes early, recovers slow.",
    aide: {
      name: "Dr. Aronson",
      style: "arousal regulation",
      techniques: ["down-regulation", "sensory reset", "walk breaks"],
    },
    status: "design-proposal",
    domain: "regulation-recovery",
  },
  {
    id: "boundary_set",
    name: "BoundarySet",
    trait: "Boundary Setting",
    tag: "BS",
    hue: 24,
    flavor: "social",
    blurb: "Says yes when meaning no.",
    aide: {
      name: "Dr. Okafor",
      style: "assertion training",
      techniques: ["script rehearsal", "pre-approved no", "time-bound yes"],
    },
    status: "design-proposal",
    domain: "awareness-connection",
  },
  {
    id: "plan_ahead",
    name: "PlanAhead",
    trait: "Forward Planning",
    tag: "PA",
    hue: 186,
    flavor: "planning",
    blurb: "Future-blind under load.",
    aide: {
      name: "Coach Olsen",
      style: "forward planning",
      techniques: ["tomorrow lists", "calendar blocks", "if-then plans"],
    },
    status: "design-proposal",
    domain: "activation-planning",
  },
  {
    id: "self_monitor",
    name: "SelfMonitor",
    trait: "Self-Awareness",
    tag: "SM",
    hue: 280,
    flavor: "monitor",
    blurb: "Can’t tell if it’s working.",
    aide: {
      name: "Coach Brand",
      style: "metacognitive",
      techniques: ["check-in chimes", "mood logs", "five-minute retros"],
    },
    status: "design-proposal",
    domain: "awareness-connection",
  },
  {
    id: "motivate_me",
    name: "MotivateMe",
    trait: "Motivation",
    tag: "MV",
    hue: 52,
    flavor: "effort",
    blurb: "Why-power is low. Reward feels distant.",
    aide: {
      name: "Dr. Vance",
      style: "energy management",
      techniques: ["reward stacking", "why-anchor", "body-double"],
    },
    status: "design-proposal",
    domain: "activation-planning",
  },
];
