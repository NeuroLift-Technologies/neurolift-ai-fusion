export type PairCategory = 'executive-function' | 'non-executive-function';
export type FusionStatus = 'concept' | 'prototype' | 'training' | 'ready';
export type EmpathyLevel = 'theoretical' | 'observational' | 'experiential' | 'deep_experiential';

export interface AvatarAidePair {
  id: number;
  avatarName: string;
  aideName: string;
  advocateName: string;
  trait: string;
  category: PairCategory;
  iconName: string;
  color: string;
  colorClass: string;
  bgClass: string;
  borderClass: string;
  shortDescription: string;
  avatarStruggles: string[];
  aideExpertise: string[];
  advocateStrength: string;
  exampleScenario: string;
  scenarios: string[];
  status: FusionStatus;
  empathyLevel: EmpathyLevel;
  readinessScore: number;
  keyMetrics: {
    label: string;
    value: number;
    description: string;
  }[];
}

export const PAIRS: AvatarAidePair[] = [
  // ===== EXECUTIVE FUNCTION PAIRS (14) =====
  {
    id: 1,
    avatarName: 'StayAlert',
    aideName: 'FocusKeeper',
    advocateName: 'AttentionAdvocate',
    trait: 'Sustained Attention Deficit',
    category: 'executive-function',
    iconName: 'Eye',
    color: '#F38020',
    colorClass: 'text-orange-500',
    bgClass: 'bg-orange-500/10',
    borderClass: 'border-orange-500/30',
    shortDescription:
      'Struggles to maintain focus over time. Attention drifts during prolonged tasks, and time blindness sets in while focused.',
    avatarStruggles: [
      'Attention drift during long tasks',
      'Mind wanders to unrelated thoughts',
      'Difficulty staying engaged with mundane work',
      'Hyperfocus vulnerability on subtasks',
      'Forgets main objective mid-task',
    ],
    aideExpertise: [
      'Pomodoro technique adaptation',
      'Environmental focus optimization',
      'Task chunking strategies',
      'Attention capacity assessment',
      'Body-doubling protocols',
    ],
    advocateStrength:
      'Deeply understands what it feels like to lose focus repeatedly and knows exactly which strategies actually work to sustain attention.',
    exampleScenario:
      'A 30-minute report writing session: the Avatar loses focus at minute 12, gets hyperfocused on formatting at minute 18, and forgets the conclusion entirely.',
    scenarios: [
      'Report writing session with attention drift',
      'Team standup meeting participation',
      'Online research and information gathering',
    ],
    status: 'prototype',
    empathyLevel: 'experiential',
    readinessScore: 0.42,
    keyMetrics: [
      { label: 'Attention Span', value: 15, description: 'Minutes before drift' },
      { label: 'Drift Probability', value: 30, description: '% chance per check-in' },
      { label: 'Coaching Effectiveness', value: 68, description: '% strategy success rate' },
    ],
  },
  {
    id: 2,
    avatarName: 'ImpulseGuard',
    aideName: 'PauseCoach',
    advocateName: 'ImpulseAdvocate',
    trait: 'Impulsivity Control',
    category: 'executive-function',
    iconName: 'Shield',
    color: '#EF4444',
    colorClass: 'text-red-500',
    bgClass: 'bg-red-500/10',
    borderClass: 'border-red-500/30',
    shortDescription:
      'Acts without thinking, interrupts conversations, and makes hasty decisions that create downstream problems.',
    avatarStruggles: [
      'Blurts out responses before thinking',
      'Makes impulsive purchases',
      'Interrupts others mid-sentence',
      'Sends messages then immediately regrets them',
      'Quits projects abruptly to start new ones',
    ],
    aideExpertise: [
      'Stop-think-act framework',
      'Impulse delay techniques',
      'Decision matrix for quick choices',
      'Emotional regulation bridging',
      'Consequence visualization',
    ],
    advocateStrength:
      'Knows the visceral pull of impulsive urges and has battle-tested methods for creating meaningful pauses.',
    exampleScenario:
      'The Avatar blurts out an answer in a meeting before the question is finished, then sends a frustrated Slack message they instantly regret.',
    scenarios: [
      'Team meeting conversation interruptions',
      'Impulsive online purchase decisions',
      'Regretful message sending',
    ],
    status: 'concept',
    empathyLevel: 'theoretical',
    readinessScore: 0.12,
    keyMetrics: [
      { label: 'Impulse Rate', value: 45, description: 'Impulsive acts per day' },
      { label: 'Pause Success', value: 25, description: '% of impulses paused' },
      { label: 'Regret Incidents', value: 8, description: 'Weekly regret events' },
    ],
  },
  {
    id: 3,
    avatarName: 'FocusFlow',
    aideName: 'FlowDirector',
    advocateName: 'FlowAdvocate',
    trait: 'Hyperfocus Management',
    category: 'executive-function',
    iconName: 'Target',
    color: '#F59E0B',
    colorClass: 'text-amber-500',
    bgClass: 'bg-amber-500/10',
    borderClass: 'border-amber-500/30',
    shortDescription:
      'Gets locked into hyperfocus on interesting tasks, unable to disengage. Misses meals, appointments, and other obligations.',
    avatarStruggles: [
      'Cannot stop working on engaging tasks',
      'Misses appointments while hyperfocused',
      'Neglects basic needs (food, sleep)',
      'Resents being interrupted during flow',
      'Hyperfocus on wrong aspects of projects',
    ],
    aideExpertise: [
      'Flow state entry/exit protocols',
      'Timer-based disengagement cues',
      'Priority alignment techniques',
      'Transition ritual design',
      'Energy management mapping',
    ],
    advocateStrength:
      'Understands both the power and danger of hyperfocus, knowing when to harness it and when to break free.',
    exampleScenario:
      'The Avatar enters deep focus on a design detail at 2 PM, misses a 4 PM doctor appointment, and realizes at 9 PM they haven\'t eaten.',
    scenarios: [
      'Deep design focus trapping',
      'Missed appointments while hyperfocused',
      'Neglecting meals during flow state',
    ],
    status: 'concept',
    empathyLevel: 'theoretical',
    readinessScore: 0.08,
    keyMetrics: [
      { label: 'Avg Hyperfocus', value: 4.5, description: 'Hours per episode' },
      { label: 'Missed Events', value: 6, description: 'Monthly missed obligations' },
      { label: 'Disengagement', value: 15, description: '% successful breaks' },
    ],
  },
  {
    id: 4,
    avatarName: 'Timely',
    aideName: 'TimeSensei',
    advocateName: 'TimeAdvocate',
    trait: 'Time Blindness',
    category: 'executive-function',
    iconName: 'Clock',
    color: '#06B6D4',
    colorClass: 'text-cyan-500',
    bgClass: 'bg-cyan-500/10',
    borderClass: 'border-cyan-500/30',
    shortDescription:
      'Cannot accurately estimate time passage. Chronically late, underestimates task duration, and loses track of time entirely.',
    avatarStruggles: [
      'Consistently underestimates how long tasks take',
      'Loses entire hours without realizing',
      'Always running 15-30 minutes late',
      'Cannot judge if 5 minutes or 30 have passed',
      'Misses deadlines despite working hard',
    ],
    aideExpertise: [
      'Time estimation calibration',
      'External time cueing systems',
      'Buffer time planning',
      'Time-boxing techniques',
      'Visual time tracking methods',
    ],
    advocateStrength:
      'Has lived through the chronic stress of perpetual lateness and developed reliable systems that actually work.',
    exampleScenario:
      'The Avatar estimates a 30-minute task will take 10 minutes, starts 20 minutes late, and is shocked to find 2 hours have vanished.',
    scenarios: [
      'Underestimating morning routine time',
      'Arriving late to meetings',
      'Missing deadlines despite hard work',
    ],
    status: 'concept',
    empathyLevel: 'theoretical',
    readinessScore: 0.05,
    keyMetrics: [
      { label: 'Estimation Error', value: 65, description: '% underestimate on average' },
      { label: 'Lateness Rate', value: 72, description: '% of appointments late' },
      { label: 'Time Awareness', value: 22, description: '% accurate time guesses' },
    ],
  },
  {
    id: 5,
    avatarName: 'MemoryMate',
    aideName: 'RecallGuide',
    advocateName: 'MemoryAdvocate',
    trait: 'Working Memory Deficits',
    category: 'executive-function',
    iconName: 'Brain',
    color: '#A855F7',
    colorClass: 'text-purple-500',
    bgClass: 'bg-purple-500/10',
    borderClass: 'border-purple-500/30',
    shortDescription:
      'Forgets instructions mid-task, loses train of thought, and struggles to hold multiple pieces of information simultaneously.',
    avatarStruggles: [
      'Forgets 3-step instructions by step 2',
      'Loses train of thought mid-sentence',
      'Cannot hold multiple variables while problem-solving',
      'Walks into rooms and forgets why',
      'Rereads the same paragraph repeatedly',
    ],
    aideExpertise: [
      'External memory systems design',
      'Working memory offloading techniques',
      'Chunking and association methods',
      'Checklist and reminder architecture',
      'Verbal rehearsal strategies',
    ],
    advocateStrength:
      'Knows the frustration of information vanishing mid-thought and has built practical systems to externalize memory.',
    exampleScenario:
      'The Avatar is given 4 tasks in a meeting. By the time they return to their desk, they remember only the first one.',
    scenarios: [
      'Multi-step instruction forgetting',
      'Losing train of thought mid-sentence',
      'Walking into rooms and forgetting why',
    ],
    status: 'concept',
    empathyLevel: 'theoretical',
    readinessScore: 0.03,
    keyMetrics: [
      { label: 'Instruction Retention', value: 40, description: '% of steps remembered' },
      { label: 'Thought Interruptions', value: 12, description: 'Daily lost trains of thought' },
      { label: 'External System Use', value: 30, description: '% using memory aids' },
    ],
  },
  {
    id: 6,
    avatarName: 'MoodEase',
    aideName: 'EmotionAnchor',
    advocateName: 'EmotionAdvocate',
    trait: 'Emotional Regulation',
    category: 'executive-function',
    iconName: 'Heart',
    color: '#EC4899',
    colorClass: 'text-pink-500',
    bgClass: 'bg-pink-500/10',
    borderClass: 'border-pink-500/30',
    shortDescription:
      'Experiences emotional overreactions, rapid mood swings, and feelings that are disproportionately intense relative to the trigger.',
    avatarStruggles: [
      'Disproportionate emotional reactions to small triggers',
      'Rapid mood swings throughout the day',
      'Difficulty returning to baseline after emotional spikes',
      'Emotional flooding during conflict',
      'Feeling criticized when receiving feedback',
    ],
    aideExpertise: [
      'Emotion identification and labeling',
      'Grounding techniques (5-4-3-2-1)',
      'Cognitive reframing methods',
      'Emotional regulation toolkit building',
      'Interpersonal effectiveness skills',
    ],
    advocateStrength:
      'Has felt the overwhelming wave of disproportionate emotion and can guide others through it with genuine understanding.',
    exampleScenario:
      'A minor email correction triggers a shame spiral that lasts 2 hours and derails the entire afternoon\'s productivity.',
    scenarios: [
      'Minor email triggering shame spiral',
      'Rapid mood swing during team conflict',
      'Disproportionate reaction to feedback',
    ],
    status: 'concept',
    empathyLevel: 'theoretical',
    readinessScore: 0.02,
    keyMetrics: [
      { label: 'Emotional Recovery', value: 45, description: 'Minutes to baseline' },
      { label: 'Overreaction Rate', value: 60, description: '% of events overreacted to' },
      { label: 'Regulation Success', value: 35, description: '% of episodes managed' },
    ],
  },
  {
    id: 7,
    avatarName: 'TaskKickstart',
    aideName: 'InitiationCoach',
    advocateName: 'ActionAdvocate',
    trait: 'Task Initiation Difficulty',
    category: 'executive-function',
    iconName: 'Rocket',
    color: '#84CC16',
    colorClass: 'text-lime-500',
    bgClass: 'bg-lime-500/10',
    borderClass: 'border-lime-500/30',
    shortDescription:
      'Cannot start tasks even when motivated. Experiences paralyzing procrastination and an invisible wall between intending to act and actually acting.',
    avatarStruggles: [
      'Stares at a blank document unable to begin',
      'Does everything except the important task',
      '"I\'ll start in 5 minutes" loops for hours',
      'Feels physical resistance when trying to start',
      'Can describe the task perfectly but cannot begin',
    ],
    aideExpertise: [
      'Micro-step decomposition',
      'Two-minute rule variations',
      'Momentum-building start rituals',
      'Activation energy reduction',
      'Dopamine priming techniques',
    ],
    advocateStrength:
      'Understands the unique paralysis of task initiation failure and knows that willpower alone never solves it.',
    exampleScenario:
      'The Avatar has a report due Friday. They think about it all week, open the document 6 times, but write nothing until panic sets in Thursday night.',
    scenarios: [
      'Staring at blank document unable to begin',
      'Procrastination loop before deadline',
      'Physical resistance to starting tasks',
    ],
    status: 'prototype',
    empathyLevel: 'observational',
    readinessScore: 0.18,
    keyMetrics: [
      { label: 'Initiation Delay', value: 3.2, description: 'Avg hours before starting' },
      { label: 'Procrastination Loops', value: 8, description: 'False starts per task' },
      { label: 'Panic Starts', value: 55, description: '% started under pressure' },
    ],
  },
  {
    id: 8,
    avatarName: 'CalmCore',
    aideName: 'ResilienceBuilder',
    advocateName: 'ResilienceAdvocate',
    trait: 'Low Frustration Tolerance',
    category: 'executive-function',
    iconName: 'Flame',
    color: '#F97316',
    colorClass: 'text-orange-600',
    bgClass: 'bg-orange-600/10',
    borderClass: 'border-orange-600/30',
    shortDescription:
      'Gives up easily when faced with obstacles. Experiences rapid escalation from minor frustration to overwhelm and shutdown.',
    avatarStruggles: [
      'Abandons tasks at first difficulty',
      'Rapid escalation from annoyed to enraged',
      'Cannot tolerate imperfection in own work',
      'Shuts down when feedback requires revision',
      'Avoids challenging activities preemptively',
    ],
    aideExpertise: [
      'Frustration tolerance building',
      'Growth mindset interventions',
      'Distress tolerance skills',
      'Self-compassion techniques',
      'Graduated difficulty exposure',
    ],
    advocateStrength:
      'Knows the exact moment frustration becomes unbearable and has strategies to extend that threshold.',
    exampleScenario:
      'The Avatar encounters a bug in their code. After 3 failed attempts to fix it, they delete the entire project folder in frustration.',
    scenarios: [
      'Abandoning code after failed fix attempts',
      'Shutting down during revision requests',
      'Avoiding challenging activities preemptively',
    ],
    status: 'concept',
    empathyLevel: 'theoretical',
    readinessScore: 0.01,
    keyMetrics: [
      { label: 'Frustration Threshold', value: 8, description: 'Minutes before giving up' },
      { label: 'Abandonment Rate', value: 70, description: '% of tasks abandoned' },
      { label: 'Recovery Time', value: 30, description: 'Minutes to retry' },
    ],
  },
  {
    id: 9,
    avatarName: 'Planner Pro',
    aideName: 'PriorityMentor',
    advocateName: 'StrategyAdvocate',
    trait: 'Prioritization & Planning',
    category: 'executive-function',
    iconName: 'ListChecks',
    color: '#10B981',
    colorClass: 'text-emerald-500',
    bgClass: 'bg-emerald-500/10',
    borderClass: 'border-emerald-500/30',
    shortDescription:
      'Cannot determine what\'s most important. Everything feels equally urgent, leading to analysis paralysis or working on the wrong things.',
    avatarStruggles: [
      'Everything feels equally urgent',
      'Spends more time planning than doing',
      'Cannot choose between competing priorities',
      'Reorganizes to-do lists instead of doing tasks',
      'Paralyzed by the number of pending items',
    ],
    aideExpertise: [
      'Eisenhower matrix adaptation',
      'Impact/effort scoring',
      'Time-block planning systems',
      'Minimum viable planning',
      'Decision fatigue management',
    ],
    advocateStrength:
      'Has lived through the paralysis of infinite priorities and developed lean planning methods that actually lead to action.',
    exampleScenario:
      'The Avatar has 12 tasks due this week. They spend Monday reorganizing their task list, Tuesday researching planning apps, and Wednesday in a panic.',
    scenarios: [
      'Reorganizing to-do lists instead of doing tasks',
      'Paralysis from 12 competing priorities',
      'Researching productivity apps instead of working',
    ],
    status: 'concept',
    empathyLevel: 'theoretical',
    readinessScore: 0.04,
    keyMetrics: [
      { label: 'Planning vs Doing', value: 65, description: '% time spent planning' },
      { label: 'Priority Accuracy', value: 28, description: '% choosing correct task' },
      { label: 'Task Completion', value: 40, description: '% of planned tasks done' },
    ],
  },
  {
    id: 10,
    avatarName: 'SmoothSwitch',
    aideName: 'TransitionGuide',
    advocateName: 'TransitionAdvocate',
    trait: 'Transition Difficulties',
    category: 'executive-function',
    iconName: 'ArrowLeftRight',
    color: '#14B8A6',
    colorClass: 'text-teal-500',
    bgClass: 'bg-teal-500/10',
    borderClass: 'border-teal-500/30',
    shortDescription:
      'Struggles to switch between tasks or contexts. Gets mentally \'stuck\' and resists transitions even when they\'re necessary.',
    avatarStruggles: [
      'Mentally stuck on previous task',
      'Resists switching even when new task is urgent',
      'Carries old task context into new situations',
      'Needs long warm-up periods for each switch',
      'Difficulty shifting between work and personal life',
    ],
    aideExpertise: [
      'Transition ritual design',
      'Context-switching protocols',
      'Cognitive closure techniques',
      'Buffer zone implementation',
      'Mental state shifting exercises',
    ],
    advocateStrength:
      'Understands the mental \'stickiness\' of task engagement and how to create clean breaks between different modes of work.',
    exampleScenario:
      'After a deep coding session, the Avatar joins a team meeting but spends 15 minutes still thinking about the code they were writing.',
    scenarios: [
      'Mentally stuck after deep coding session',
      'Resisting switch to urgent new task',
      'Difficulty shifting from work to personal life',
    ],
    status: 'concept',
    empathyLevel: 'theoretical',
    readinessScore: 0.02,
    keyMetrics: [
      { label: 'Switch Time', value: 18, description: 'Minutes to fully transition' },
      { label: 'Context Bleed', value: 55, description: '% of transitions with carryover' },
      { label: 'Resistance Events', value: 4, description: 'Daily transition resistance' },
    ],
  },
  {
    id: 11,
    avatarName: 'AwareMate',
    aideName: 'InsightCoach',
    advocateName: 'InsightAdvocate',
    trait: 'Self-Monitoring Challenges',
    category: 'executive-function',
    iconName: 'ScanEye',
    color: '#8B5CF6',
    colorClass: 'text-violet-500',
    bgClass: 'bg-violet-500/10',
    borderClass: 'border-violet-500/30',
    shortDescription:
      'Doesn\'t notice own mistakes, behavior impact, or performance patterns. Lacks the internal observer that catches errors in real-time.',
    avatarStruggles: [
      'Doesn\'t notice when making mistakes',
      'Unaware of how behavior affects others',
      'Cannot self-assess performance accurately',
      'Misses social cues about their own conduct',
      'Surprised by feedback on recurring issues',
    ],
    aideExpertise: [
      'Structured self-reflection prompts',
      'External feedback integration',
      'Pattern recognition training',
      'Journaling and review systems',
      'Mindfulness awareness practices',
    ],
    advocateStrength:
      'Has experienced the shock of discovering blind spots and built reliable external monitoring systems.',
    exampleScenario:
      'The Avatar submits a report they think is perfect. Three different people point out the same formatting error on page one.',
    scenarios: [
      'Submitting work with unnoticed errors',
      'Surprise at recurring feedback themes',
      'Missing social cues about own conduct',
    ],
    status: 'concept',
    empathyLevel: 'theoretical',
    readinessScore: 0.01,
    keyMetrics: [
      { label: 'Error Detection', value: 20, description: '% of errors self-caught' },
      { label: 'Self-Assessment Accuracy', value: 35, description: '% alignment with feedback' },
      { label: 'Blind Spot Awareness', value: 25, description: '% of patterns recognized' },
    ],
  },
  {
    id: 12,
    avatarName: 'SteadyMind',
    aideName: 'ImpulseTherapist',
    advocateName: 'SteadyAdvocate',
    trait: 'Poor Impulse Control',
    category: 'executive-function',
    iconName: 'Mountain',
    color: '#64748B',
    colorClass: 'text-slate-500',
    bgClass: 'bg-slate-500/10',
    borderClass: 'border-slate-500/30',
    shortDescription:
      'Compulsive behaviors, difficulty resisting temptations, and repeated patterns of acting against one\'s own long-term interests.',
    avatarStruggles: [
      'Compulsive phone checking and social media scrolling',
      'Cannot resist snacks when trying to eat healthy',
      'Repeatedly breaks own rules and commitments',
      'Chase-the-dopamine behaviors',
      '"Just one more" loops (one more episode, one more game)',
    ],
    aideExpertise: [
      'Habit loop interruption',
      'Environment design for impulse reduction',
      'Delay gratification training',
      'Dopamine regulation strategies',
      'Commitment device implementation',
    ],
    advocateStrength:
      'Has felt the compulsion loop from the inside and knows which environmental and cognitive levers actually break it.',
    exampleScenario:
      'The Avatar decides to sleep early. At 11 PM they check \"one more thing\" on their phone. It\'s 3 AM. They\'ve watched 4 hours of short-form videos.',
    scenarios: [
      'Late-night phone scrolling trap',
      'Breaking healthy eating commitments',
      '"Just one more" game loop',
    ],
    status: 'concept',
    empathyLevel: 'theoretical',
    readinessScore: 0.01,
    keyMetrics: [
      { label: 'Impulse Yield Rate', value: 78, description: '% giving in to impulses' },
      { label: 'Average Resistance', value: 4, description: 'Seconds before yielding' },
      { label: 'Habit Loop Breaks', value: 15, description: '% successfully interrupted' },
    ],
  },
  {
    id: 13,
    avatarName: 'FocusRecharge',
    aideName: 'EnergyManager',
    advocateName: 'EnergyAdvocate',
    trait: 'Effortful Focus Fatigue',
    category: 'executive-function',
    iconName: 'Battery',
    color: '#EAB308',
    colorClass: 'text-yellow-500',
    bgClass: 'bg-yellow-500/10',
    borderClass: 'border-yellow-500/30',
    shortDescription:
      'Mental energy depletes rapidly during focused work. Experiences brain fog, reduced cognitive function, and inability to continue.',
    avatarStruggles: [
      'Brain fog after 20-30 minutes of effort',
      'Mental exhaustion from tasks others find easy',
      'Inconsistent energy levels throughout the day',
      'Cannot push through fatigue with willpower',
      'Recovery takes longer than expected',
    ],
    aideExpertise: [
      'Energy mapping and tracking',
      'Strategic rest scheduling',
      'Cognitive load management',
      'Nutrition and movement integration',
      'Energy-matched task allocation',
    ],
    advocateStrength:
      'Understands that ADHD focus fatigue is not laziness and has proven methods for working with limited cognitive energy.',
    exampleScenario:
      'The Avatar is sharp for the first hour of work. By hour two, simple decisions feel impossible. By hour three, they\'re staring blankly at the screen.',
    scenarios: [
      'Brain fog after 30 minutes of effort',
      'Mental exhaustion from simple tasks',
      'Inconsistent energy throughout the day',
    ],
    status: 'concept',
    empathyLevel: 'theoretical',
    readinessScore: 0.01,
    keyMetrics: [
      { label: 'Focus Window', value: 35, description: 'Minutes of peak focus' },
      { label: 'Recovery Time', value: 25, description: 'Minutes to recharge' },
      { label: 'Daily Capacity', value: 4, description: 'Hours of productive focus' },
    ],
  },
  {
    id: 14,
    avatarName: 'EffortAlign',
    aideName: 'OutputAnalyst',
    advocateName: 'EfficiencyAdvocate',
    trait: 'Effort vs. Productivity Perception',
    category: 'executive-function',
    iconName: 'Gauge',
    color: '#EC4899',
    colorClass: 'text-pink-400',
    bgClass: 'bg-pink-400/10',
    borderClass: 'border-pink-400/30',
    shortDescription:
      'Misjudges how much effort tasks require. Spends excessive energy on low-priority work and too little on what matters most.',
    avatarStruggles: [
      'Over-invests in minor details',
      'Under-invests in important strategic work',
      'Cannot calibrate effort to task importance',
      'Perfectionism on low-stakes tasks',
      'Rushed work on high-stakes tasks',
    ],
    aideExpertise: [
      'Effort calibration exercises',
      'Done-is-better-than-perfect framing',
      'Priority-weighted effort allocation',
      'Time/effort tracking systems',
      'Good-enough threshold setting',
    ],
    advocateStrength:
      'Knows the trap of polishing the wrong thing and has methods for matching effort to actual importance.',
    exampleScenario:
      'The Avatar spends 3 hours perfecting a slide font while leaving the presentation content unfinished. The audience only sees the content.',
    scenarios: [
      'Perfecting slide fonts over content',
      'Rushing high-stakes strategic work',
      'Over-investing in minor details',
    ],
    status: 'concept',
    empathyLevel: 'theoretical',
    readinessScore: 0.01,
    keyMetrics: [
      { label: 'Effort Mismatch', value: 58, description: '% of tasks with wrong effort level' },
      { label: 'Perfectionism Events', value: 5, description: 'Daily over-investments' },
      { label: 'Priority Alignment', value: 32, description: '% effort matching importance' },
    ],
  },

  // ===== NON-EXECUTIVE FUNCTION PAIRS (5) =====
  {
    id: 15,
    avatarName: 'StressShield',
    aideName: 'CalmArchitect',
    advocateName: 'StressAdvocate',
    trait: 'Stress Sensitivity',
    category: 'non-executive-function',
    iconName: 'ShieldAlert',
    color: '#EF4444',
    colorClass: 'text-red-400',
    bgClass: 'bg-red-400/10',
    borderClass: 'border-red-400/30',
    shortDescription:
      'Overwhelmed by stressors that others handle easily. Experiences physical symptoms (headaches, tension) from relatively minor stress.',
    avatarStruggles: [
      'Physical symptoms from minor stressors',
      'Catastrophizes small problems',
      'Difficulty distinguishing threat levels',
      'Stress accumulates faster than it dissipates',
      'Sleep disruption from worry loops',
    ],
    aideExpertise: [
      'Stress response calibration',
      'Somatic grounding techniques',
      'Worry management protocols',
      'Nervous system regulation',
      'Progressive muscle relaxation',
    ],
    advocateStrength:
      'Has felt the physical weight of disproportionate stress and knows how to recalibrate the stress response system.',
    exampleScenario:
      'A mildly critical email triggers chest tightness, racing thoughts, and 3 hours of worry that prevents all other work.',
    scenarios: [
      'Critical email triggering physical symptoms',
      'Catastrophizing a minor problem',
      'Sleep disruption from worry loops',
    ],
    status: 'concept',
    empathyLevel: 'theoretical',
    readinessScore: 0.01,
    keyMetrics: [
      { label: 'Stress Threshold', value: 3, description: 'Minutes to overwhelm' },
      { label: 'Physical Symptoms', value: 8, description: 'Weekly somatic events' },
      { label: 'Recovery Rate', value: 25, description: '% daily stress resolved' },
    ],
  },
  {
    id: 16,
    avatarName: 'SensoryBalance',
    aideName: 'SensoryGuide',
    advocateName: 'SensoryAdvocate',
    trait: 'Sensory Sensitivity',
    category: 'non-executive-function',
    iconName: 'Ear',
    color: '#0EA5E9',
    colorClass: 'text-sky-500',
    bgClass: 'bg-sky-500/10',
    borderClass: 'border-sky-500/30',
    shortDescription:
      'Overwhelmed by sounds, lights, textures, and smells that others barely notice. Sensory input causes real pain and cognitive overload.',
    avatarStruggles: [
      'Office noise causes inability to concentrate',
      'Fluorescent lights trigger migraines',
      'Clothing textures cause physical discomfort',
      'Multiple simultaneous sounds are unbearable',
      'Sensory overload leads to shutdown',
    ],
    aideExpertise: [
      'Sensory environment audit',
      'Noise management solutions',
      'Sensory diet design',
      'Accommodation self-advocacy',
      'Sensory break scheduling',
    ],
    advocateStrength:
      'Understands that sensory sensitivity is not preference but a neurological reality, and knows how to navigate environments designed for neurotypical perception.',
    exampleScenario:
      'An open-plan office with fluorescent lights, a humming AC, and two conversations happening nearby makes it impossible for the Avatar to think.',
    scenarios: [
      'Open-plan office sensory overload',
      'Fluorescent lights triggering migraines',
      'Multiple simultaneous sounds unbearable',
    ],
    status: 'concept',
    empathyLevel: 'theoretical',
    readinessScore: 0.01,
    keyMetrics: [
      { label: 'Sensory Threshold', value: 15, description: 'Minutes in hostile environment' },
      { label: 'Overload Events', value: 4, description: 'Weekly sensory overloads' },
      { label: 'Accommodation Use', value: 40, description: '% using sensory tools' },
    ],
  },
  {
    id: 17,
    avatarName: 'SocialSync',
    aideName: 'SocialMentor',
    advocateName: 'SocialAdvocate',
    trait: 'Social Challenges',
    category: 'non-executive-function',
    iconName: 'Users',
    color: '#22C55E',
    colorClass: 'text-green-500',
    bgClass: 'bg-green-500/10',
    borderClass: 'border-green-500/30',
    shortDescription:
      'Misreads social cues, experiences intense rejection sensitivity, and struggles with the unwritten rules of social interaction.',
    avatarStruggles: [
      'Misinterprets neutral faces as negative',
      'Rejection sensitivity causes social withdrawal',
      'Misses subtle social cues and norms',
      'Oversharing or under-sharing in conversations',
      'Rumination after social interactions',
    ],
    aideExpertise: [
      'Social cue decoding frameworks',
      'Rejection sensitivity reappraisal',
      'Conversation structure templates',
      'Social energy management',
      'Post-interaction reflection guides',
    ],
    advocateStrength:
      'Has experienced the pain of perceived rejection and social confusion, and can help others navigate social landscapes with confidence.',
    exampleScenario:
      'A colleague doesn\'t reply to a message within 2 hours. The Avatar spirals: \'They\'re mad at me. I said something wrong. Everyone hates me.\'',
    scenarios: [
      'Unreplied message triggering rejection spiral',
      'Oversharing in one-on-one meetings',
      'Post-interaction rumination loop',
    ],
    status: 'concept',
    empathyLevel: 'theoretical',
    readinessScore: 0.01,
    keyMetrics: [
      { label: 'Social Misreads', value: 65, description: '% of cues misinterpreted' },
      { label: 'Rejection Rumination', value: 4, description: 'Hours per rejection event' },
      { label: 'Social Confidence', value: 30, description: '% feeling socially competent' },
    ],
  },
  {
    id: 18,
    avatarName: 'SensorySeeker',
    aideName: 'StimulationCoach',
    advocateName: 'StimulationAdvocate',
    trait: 'Sensory Seeking Behavior',
    category: 'non-executive-function',
    iconName: 'Sparkles',
    color: '#D97706',
    colorClass: 'text-amber-600',
    bgClass: 'bg-amber-600/10',
    borderClass: 'border-amber-600/30',
    shortDescription:
      'Constantly needs stimulation. Fidgeting, restlessness, and seeking novelty create challenges in structured environments.',
    avatarStruggles: [
      'Cannot sit still in meetings or classes',
      'Constant fidgeting that disrupts others',
      'Boredom is physically uncomfortable',
      'Creates unnecessary drama for stimulation',
      'Chase-novelty pattern in work and relationships',
    ],
    aideExpertise: [
      'Channeling stimulation productively',
      'Fidget tool selection and use',
      'Novelty integration into routine tasks',
      'Movement-based learning strategies',
      'Stimulation budgeting techniques',
    ],
    advocateStrength:
      'Understands that the need for stimulation is neurological, not behavioral, and has creative ways to feed it constructively.',
    exampleScenario:
      'During a 2-hour meeting, the Avatar bounces their leg, clicks their pen, checks their phone, doodles, and still can\'t focus.',
    scenarios: [
      'Fidgeting through a 2-hour meeting',
      'Boredom during quiet study period',
      'Creating drama for stimulation',
    ],
    status: 'concept',
    empathyLevel: 'theoretical',
    readinessScore: 0.01,
    keyMetrics: [
      { label: 'Fidget Events', value: 30, description: 'Daily fidgeting episodes' },
      { label: 'Boredom Threshold', value: 8, description: 'Minutes before boredom' },
      { label: 'Productive Channeling', value: 25, description: '% stimulation used well' },
    ],
  },
  {
    id: 19,
    avatarName: 'ConfidenceCoach',
    aideName: 'SelfWorthBuilder',
    advocateName: 'WorthAdvocate',
    trait: 'Self-Esteem & Identity',
    category: 'non-executive-function',
    iconName: 'Star',
    color: '#CA8A04',
    colorClass: 'text-yellow-600',
    bgClass: 'bg-yellow-600/10',
    borderClass: 'border-yellow-600/30',
    shortDescription:
      'Chronic imposter syndrome, negative self-talk, and identity struggles rooted in years of ADHD-related failures and criticisms.',
    avatarStruggles: [
      'Imposter syndrome despite real competence',
      'Internalized \'lazy\' and \'stupid\' labels',
      'Compares own behind-the-scenes to others\' highlights',
      'Difficulty accepting compliments',
      'Identity built on overcoming ADHD vs. living with it',
    ],
    aideExpertise: [
      'Cognitive restructuring of self-narrative',
      'Strengths-based identity building',
      'Evidence journaling (counteracting negativity bias)',
      'ADHD-as-asset reframing',
      'Self-compassion cultivation',
    ],
    advocateStrength:
      'Has emerged from the rubble of shattered self-esteem and can guide others to rebuild their identity on authentic strengths.',
    exampleScenario:
      'Despite receiving a promotion, the Avatar spends weeks convinced it was a mistake and everyone will discover they\'re a fraud.',
    scenarios: [
      'Imposter syndrome after promotion',
      'Dismissing genuine compliments',
      'Comparing behind-the-scenes to others\' highlights',
    ],
    status: 'concept',
    empathyLevel: 'theoretical',
    readinessScore: 0.01,
    keyMetrics: [
      { label: 'Imposter Episodes', value: 12, description: 'Weekly imposter events' },
      { label: 'Self-Talk Positivity', value: 22, description: '% positive self-statements' },
      { label: 'Strengths Recognition', value: 28, description: '% of successes acknowledged' },
    ],
  },
];

export const CATEGORY_LABELS: Record<PairCategory, string> = {
  'executive-function': 'Executive Function',
  'non-executive-function': 'Non-Executive Function',
};

export const STATUS_CONFIG: Record<
  FusionStatus,
  { label: string; color: string; bgColor: string }
> = {
  concept: {
    label: 'Concept',
    color: 'text-slate-400',
    bgColor: 'bg-slate-400/15',
  },
  prototype: {
    label: 'Prototype',
    color: 'text-amber-500',
    bgColor: 'bg-amber-500/15',
  },
  training: {
    label: 'Training',
    color: 'text-cyan-500',
    bgColor: 'bg-cyan-500/15',
  },
  ready: {
    label: 'Ready',
    color: 'text-emerald-500',
    bgColor: 'bg-emerald-500/15',
  },
};

export const EMPATHY_LABELS: Record<EmpathyLevel, string> = {
  theoretical: 'Theoretical',
  observational: 'Observational',
  experiential: 'Experiential',
  deep_experiential: 'Deep Experiential',
};

export function getPairsByCategory(category: PairCategory | 'all') {
  if (category === 'all') return PAIRS;
  return PAIRS.filter((p) => p.category === category);
}

export function getPairById(id: number) {
  return PAIRS.find((p) => p.id === id);
}

export function searchPairs(query: string) {
  const q = query.toLowerCase();
  return PAIRS.filter(
    (p) =>
      p.avatarName.toLowerCase().includes(q) ||
      p.aideName.toLowerCase().includes(q) ||
      p.advocateName.toLowerCase().includes(q) ||
      p.trait.toLowerCase().includes(q) ||
      p.shortDescription.toLowerCase().includes(q),
  );
}

export function getStats() {
  const ef = PAIRS.filter((p) => p.category === 'executive-function').length;
  const nef = PAIRS.filter((p) => p.category === 'non-executive-function').length;
  const prototype = PAIRS.filter((p) => p.status === 'prototype').length;
  const concept = PAIRS.filter((p) => p.status === 'concept').length;
  return { total: PAIRS.length, executiveFunction: ef, nonExecutiveFunction: nef, prototype, concept };
}
