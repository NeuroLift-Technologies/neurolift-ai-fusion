"use client";

import { useState, useMemo, useEffect, useCallback, useRef } from "react";
import { toast } from "sonner";
import { motion, AnimatePresence } from "framer-motion";
import type { Variants } from "framer-motion";
import * as TooltipPrimitive from "@radix-ui/react-tooltip";
import {
  Search,
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
  ArrowUpDown,
  User,
  Bot,
  Megaphone,
  GitCompareArrows,
  Shuffle,
  Download,
  LayoutGrid,
  List,
  ChevronsUpDown,
  ChevronUp,
  ChevronDown,
  X,
  Copy,
} from "lucide-react";
import { Input } from "@/components/ui/input";
import { Card, CardContent } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import {
  PAIRS,
  type AvatarAidePair,
  type PairCategory,
  type FusionStatus,
  CATEGORY_LABELS,
  STATUS_CONFIG,
  EMPATHY_LABELS,
} from "@/lib/avatar-pairs-data";

// ─── Confidence Ring (circular progress) ────────────────────────────
const STATUS_READINESS: Record<FusionStatus, number> = {
  concept: 15,
  prototype: 40,
  training: 70,
  ready: 95,
};

function ConfidenceRing({ value, color, size = 36 }: { value: number; color: string; size?: number }) {
  const strokeWidth = 3;
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference * (1 - value / 100);
  return (
    <svg width={size} height={size} className="shrink-0" aria-hidden="true">
      <circle
        cx={size / 2}
        cy={size / 2}
        r={radius}
        fill="none"
        stroke="currentColor"
        strokeWidth={strokeWidth}
        className="text-muted/30"
      />
      <circle
        cx={size / 2}
        cy={size / 2}
        r={radius}
        fill="none"
        stroke={color}
        strokeWidth={strokeWidth}
        strokeLinecap="round"
        strokeDasharray={circumference}
        strokeDashoffset={offset}
        style={{
          transform: 'rotate(-90deg)',
          transformOrigin: '50% 50%',
          transition: 'stroke-dashoffset 0.6s ease',
        }}
      />
      <text
        x={size / 2}
        y={size / 2}
        textAnchor="middle"
        dominantBaseline="central"
        className="fill-foreground text-[9px] font-bold"
        style={{ fontSize: size * 0.25 }}
      >
        {value}%
      </text>
    </svg>
  );
}

// ─── Animated counter ────────────────────────────────────────────────
function AnimatedCounter({ target, suffix = "" }: { target: number; suffix?: string }) {
  const [count, setCount] = useState(0);

  useEffect(() => {
    let start = 0;
    const duration = 800;
    const startTime = performance.now();

    function tick(now: number) {
      const elapsed = now - startTime;
      const progress = Math.min(elapsed / duration, 1);
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

// ─── Filter tab type ─────────────────────────────────────────────────
type FilterKey = "all" | PairCategory | "favorites";

interface FilterOption {
  key: FilterKey;
  label: string;
  icon?: React.ReactNode;
}

const FILTER_OPTIONS: FilterOption[] = [
  { key: "all", label: "All" },
  { key: "executive-function", label: "Executive Function" },
  { key: "non-executive-function", label: "Non-Executive Function" },
  { key: "favorites", label: "Favorites", icon: <Star className="h-3.5 w-3.5" /> },
];

// ─── Status filter options ───────────────────────────────────────────
type StatusFilterKey = FusionStatus | "all";

const STATUS_FILTER_OPTIONS: { key: StatusFilterKey; label: string }[] = [
  { key: "all", label: "All Statuses" },
  { key: "concept", label: STATUS_CONFIG.concept.label },
  { key: "prototype", label: STATUS_CONFIG.prototype.label },
  { key: "training", label: STATUS_CONFIG.training.label },
  { key: "ready", label: STATUS_CONFIG.ready.label },
];

// ─── Sort options ────────────────────────────────────────────────
type SortKey = "default" | "name-asc" | "name-desc" | "readiness-desc" | "readiness-asc";

const SORT_OPTIONS: { value: SortKey; label: string }[] = [
  { value: "default", label: "Default" },
  { value: "name-asc", label: "Name (A-Z)" },
  { value: "name-desc", label: "Name (Z-A)" },
  { value: "readiness-desc", label: "Readiness (High-Low)" },
  { value: "readiness-asc", label: "Readiness (Low-High)" },
];

// ─── Category Overview Cards ──────────────────────────────────────
function CategoryOverviewCards({
  activeFilter,
  onFilterChange,
  favoritesCount,
}: {
  activeFilter: FilterKey;
  onFilterChange: (key: FilterKey) => void;
  favoritesCount: number;
}) {
  const efCount = PAIRS.filter((p) => p.category === "executive-function").length;
  const nefCount = PAIRS.filter((p) => p.category === "non-executive-function").length;

  const cards = [
    {
      key: "executive-function" as FilterKey,
      label: "Executive Function",
      count: efCount,
      icon: <Brain className="h-4 w-4" />,
      borderClass: "border-l-orange-500",
      iconColor: "text-orange-500",
    },
    {
      key: "non-executive-function" as FilterKey,
      label: "Non-Executive Function",
      count: nefCount,
      icon: <Heart className="h-4 w-4" />,
      borderClass: "border-l-amber-500",
      iconColor: "text-amber-500",
    },
    {
      key: "favorites" as FilterKey,
      label: "Favorited",
      count: favoritesCount,
      icon: <Heart className="h-4 w-4" />,
      borderClass: "border-l-rose-500",
      iconColor: "text-rose-500",
    },
  ];

  return (
    <div className="mb-6 flex flex-wrap gap-3 justify-center sm:justify-start">
      {cards.map((card) => {
        const isActive = activeFilter === card.key;
        return (
          <motion.button
            key={card.key}
            type="button"
            onClick={() => onFilterChange(card.key)}
            whileHover={{ scale: 1.02 }}
            transition={{ duration: 0.15 }}
            className={`
              flex items-center gap-3 rounded-lg border bg-muted/40 px-4 py-3
              transition-colors duration-200 hover:bg-muted/60
              border-l-[3px]
              ${isActive ? card.borderClass : "border-l-transparent"}
            `}
            aria-label={`Filter by ${card.label}`}
            aria-pressed={isActive}
          >
            <span className={card.iconColor}>{card.icon}</span>
            <div className="text-left">
              <span className="block text-xl font-bold leading-none tabular-nums">
                {card.count}
              </span>
              <span className="mt-0.5 block text-xs text-muted-foreground">
                {card.label}
              </span>
            </div>
          </motion.button>
        );
      })}
    </div>
  );
}

// ─── Animation variants ──────────────────────────────────────────────
const containerVariants: Variants = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.04, delayChildren: 0.1 },
  },
};

const cardVariants: Variants = {
  hidden: { opacity: 0, y: 16, scale: 0.97 },
  show: {
    opacity: 1,
    y: 0,
    scale: 1,
    transition: { duration: 0.35, ease: "easeOut" },
  },
  exit: {
    opacity: 0,
    y: -8,
    scale: 0.97,
    transition: { duration: 0.2, ease: "easeIn" },
  },
};

// ─── Favorites storage helpers ───────────────────────────────────────
const FAVORITES_KEY = "neurolift-favorites";

function loadFavorites(): number[] {
  if (typeof window === "undefined") return [];
  try {
    const raw = localStorage.getItem(FAVORITES_KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed.map(Number) : [];
  } catch {
    return [];
  }
}

function saveFavorites(ids: number[]) {
  if (typeof window === "undefined") return;
  try {
    localStorage.setItem(FAVORITES_KEY, JSON.stringify(ids));
  } catch {
    // Storage full or unavailable — silently ignore
  }
}

// ─── Search highlight helper ─────────────────────────────────────────
function highlightMatch(text: string, query: string): React.ReactNode {
  if (!query || query.length < 2) return text;
  const lowerText = text.toLowerCase();
  const lowerQuery = query.toLowerCase();
  const idx = lowerText.indexOf(lowerQuery);
  if (idx === -1) return text;
  return (
    <>
      {text.slice(0, idx)}
      <mark className="bg-orange-500/20 text-foreground rounded-sm px-0.5">{text.slice(idx, idx + query.length)}</mark>
      {text.slice(idx + query.length)}
    </>
  );
}

// ─── Props ───────────────────────────────────────────────────────────
interface PairsGridProps {
  onSelectPair: (pair: AvatarAidePair) => void;
  onOpenCompare?: () => void;
  onFavoriteToast?: (pairName: string, isFavorited: boolean) => void;
  onExportToast?: () => void;
}

// ─── Component ───────────────────────────────────────────────────────
export function PairsGrid({ onSelectPair, onOpenCompare, onFavoriteToast, onExportToast }: PairsGridProps) {
  const [activeFilter, setActiveFilter] = useState<FilterKey>("all");
  const [activeStatusFilter, setActiveStatusFilter] = useState<StatusFilterKey>("all");
  const [searchQuery, setSearchQuery] = useState("");
  const [sortKey, setSortKey] = useState<SortKey>("default");
  const [viewMode, setViewMode] = useState<'grid' | 'table'>("grid");
  const [focusedIndex, setFocusedIndex] = useState(-1);
  const [favorites, setFavorites] = useState<number[]>([]);
  const [tableSort, setTableSort] = useState<{ column: string; direction: 'asc' | 'desc' | 'none' }>({ column: '', direction: 'none' });
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [activeSuggestionIndex, setActiveSuggestionIndex] = useState(-1);
  const [selectedRows, setSelectedRows] = useState<Set<number>>(new Set());
  const gridRef = useRef<HTMLDivElement>(null);
  const searchContainerRef = useRef<HTMLDivElement>(null);
  // ── Context menu state (right-click on grid cards) ──
  const [contextMenu, setContextMenu] = useState<{
    x: number;
    y: number;
    pair: AvatarAidePair;
  } | null>(null);

  // Skip persisting favorites on the initial mount to avoid racing with load
  const isFirstRenderRef = useRef(true);

  // Load favorites from localStorage on mount
  useEffect(() => {
    const stored = loadFavorites();
    setFavorites(stored);
    isFirstRenderRef.current = false;
  }, []);

  // Persist favorites to localStorage on change (skip initial mount)
  useEffect(() => {
    if (isFirstRenderRef.current) return;
    saveFavorites(favorites);
  }, [favorites]);

  // Toggle favorite
  const toggleFavorite = useCallback((pairId: number, e: React.MouseEvent) => {
    e.stopPropagation();
    e.preventDefault();
    const pair = PAIRS.find((p) => p.id === pairId);
    const wasFavorited = favorites.includes(pairId);

    // Pure state update — no side effects inside updater
    setFavorites((prev) =>
      wasFavorited
        ? prev.filter((id) => id !== pairId)
        : [...prev, pairId]
    );

    // Fire toast outside the updater to avoid StrictMode double-invocation
    if (pair && onFavoriteToast) {
      onFavoriteToast(pair.avatarName, !wasFavorited);
    }
  }, [onFavoriteToast, favorites]);

  // Random pair discovery
  const handleRandomPair = useCallback(() => {
    const available = PAIRS.filter((p) => {
      if (activeFilter === "favorites") {
        if (!favorites.includes(p.id)) return false;
      } else if (activeFilter !== "all" && p.category !== activeFilter) {
        return false;
      }
      if (activeStatusFilter !== "all" && p.status !== activeStatusFilter) return false;
      if (searchQuery.trim()) {
        const q = searchQuery.toLowerCase().trim();
        return (
          p.avatarName.toLowerCase().includes(q) ||
          p.aideName.toLowerCase().includes(q) ||
          p.advocateName.toLowerCase().includes(q) ||
          p.trait.toLowerCase().includes(q) ||
          p.shortDescription.toLowerCase().includes(q)
        );
      }
      return true;
    });
    if (available.length > 0) {
      const random = available[Math.floor(Math.random() * available.length)];
      onSelectPair(random);
    }
  }, [activeFilter, activeStatusFilter, searchQuery, favorites, onSelectPair]);

  // Empathy level sort order
  const EMPATHY_ORDER: Record<string, number> = {
    theoretical: 1,
    observational: 2,
    experiential: 3,
    deep_experiential: 4,
  };

  // Count pairs per category filter (for badges)
  const filterCounts = useMemo(() => {
    const all = PAIRS.length;
    const ef = PAIRS.filter((p) => p.category === "executive-function").length;
    const nef = PAIRS.filter((p) => p.category === "non-executive-function").length;
    return { all, "executive-function": ef, "non-executive-function": nef, favorites: favorites.length };
  }, [favorites.length]);

  // Count pairs per status filter (for badges)
  const statusCounts = useMemo(() => {
    const counts: Record<StatusFilterKey, number> = {
      all: PAIRS.length,
      concept: 0,
      prototype: 0,
      training: 0,
      ready: 0,
    };
    for (const p of PAIRS) {
      counts[p.status]++;
    }
    return counts;
  }, []);

  // Filtered + searched pairs
  const filteredPairs = useMemo(() => {
    let result = PAIRS;

    // Category / favorites filter
    if (activeFilter === "favorites") {
      result = result.filter((p) => favorites.includes(p.id));
    } else if (activeFilter !== "all") {
      result = result.filter((p) => p.category === activeFilter);
    }

    // Status filter (AND with category)
    if (activeStatusFilter !== "all") {
      result = result.filter((p) => p.status === activeStatusFilter);
    }

    // Search filter
    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase().trim();
      result = result.filter(
        (p) =>
          p.avatarName.toLowerCase().includes(q) ||
          p.aideName.toLowerCase().includes(q) ||
          p.advocateName.toLowerCase().includes(q) ||
          p.trait.toLowerCase().includes(q) ||
          p.shortDescription.toLowerCase().includes(q)
      );
    }

    // Sort
    switch (sortKey) {
      case "name-asc":
        result = [...result].sort((a, b) => a.avatarName.localeCompare(b.avatarName));
        break;
      case "name-desc":
        result = [...result].sort((a, b) => b.avatarName.localeCompare(a.avatarName));
        break;
      case "readiness-desc":
        result = [...result].sort((a, b) => b.readinessScore - a.readinessScore);
        break;
      case "readiness-asc":
        result = [...result].sort((a, b) => a.readinessScore - b.readinessScore);
        break;
      default:
        break;
    }

    return result;
  }, [activeFilter, activeStatusFilter, searchQuery, sortKey, favorites]);

  // Table-sorted pairs (applies column sort on top of filteredPairs)
  const tableSortedPairs = useMemo(() => {
    if (tableSort.direction === 'none') return filteredPairs;
    const sorted = [...filteredPairs];
    const dir = tableSort.direction === 'asc' ? 1 : -1;
    switch (tableSort.column) {
      case 'name':
        sorted.sort((a, b) => a.avatarName.localeCompare(b.avatarName) * dir);
        break;
      case 'readiness':
        sorted.sort((a, b) => (a.readinessScore - b.readinessScore) * dir);
        break;
      case 'empathy':
        sorted.sort((a, b) => ((EMPATHY_ORDER[a.empathyLevel] ?? 0) - (EMPATHY_ORDER[b.empathyLevel] ?? 0)) * dir);
        break;
      case 'id':
        sorted.sort((a, b) => (a.id - b.id) * dir);
        break;
      default:
        break;
    }
    return sorted;
  }, [filteredPairs, tableSort, EMPATHY_ORDER]);

  // Search suggestions (max 5 matches)
  const suggestions = useMemo(() => {
    if (searchQuery.length < 2) return [];
    if (filteredPairs.length === 0) return [];
    if (filteredPairs.length >= PAIRS.length) return [];
    return filteredPairs.slice(0, 5);
  }, [searchQuery, filteredPairs]);

  // Export summary as markdown
  const handleExportSummary = useCallback(() => {
    const timestamp = new Date().toLocaleString('en-US', {
      dateStyle: 'medium',
      timeStyle: 'short',
    });

    const efPairs = filteredPairs.filter((p) => p.category === 'executive-function');
    const nefPairs = filteredPairs.filter((p) => p.category === 'non-executive-function');

    function formatPair(p: AvatarAidePair) {
      return [
        `### ${p.avatarName} & ${p.aideName}`,
        '',
        `- **Trait:** ${p.trait}`,
        `- **Category:** ${CATEGORY_LABELS[p.category]}`,
        `- **Status:** ${STATUS_CONFIG[p.status].label}`,
        `- **Readiness:** ${Math.round(p.readinessScore * 100)}%`,
        `- **Empathy Level:** ${EMPATHY_LABELS[p.empathyLevel]}`,
        `- **Advocate:** ${p.advocateName}`,
        `- **Advocate Strength:** *"${p.advocateStrength}"*`,
        '',
      ].join('\n');
    }

    const sections: string[] = [
      '# NeuroLift AI Fusion — Pairs Summary',
      '',
      `> Generated on ${timestamp} — ${filteredPairs.length} pair${filteredPairs.length === 1 ? '' : 's'} shown (filtered from ${PAIRS.length} total)`,
      '',
    ];

    if (efPairs.length > 0) {
      sections.push('## Executive Function', '');
      for (const pair of efPairs) {
        sections.push(formatPair(pair));
      }
    }

    if (nefPairs.length > 0) {
      sections.push('## Non-Executive Function', '');
      for (const pair of nefPairs) {
        sections.push(formatPair(pair));
      }
    }

    sections.push(
      '---',
      '',
      '*"Every mind deserves an ally that truly understands."* — NeuroLift AI Fusion',
    );

    const blob = new Blob([sections.join('\n')], { type: 'text/markdown;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'neurolift-pairs-summary.md';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    onExportToast?.();
  }, [filteredPairs, onExportToast]);

  // Favorite all selected rows
  const handleFavoriteAllSelected = useCallback(() => {
    const selectedPairs = tableSortedPairs.filter((p) => selectedRows.has(p.id));
    if (selectedPairs.length === 0) return;
    const allFavorited = selectedPairs.every((p) => favorites.includes(p.id));
    setFavorites((prev) => {
      const next = new Set(prev);
      for (const p of selectedPairs) {
        if (allFavorited) {
          next.delete(p.id);
        } else {
          next.add(p.id);
        }
      }
      return Array.from(next);
    });
    if (onFavoriteToast) {
      onFavoriteToast(
        `${selectedPairs.length} pair${selectedPairs.length !== 1 ? 's' : ''}`,
        !allFavorited,
      );
    }
  }, [selectedRows, tableSortedPairs, favorites, onFavoriteToast]);

  // Export selected rows as markdown
  const handleExportSelected = useCallback(() => {
    const selected = tableSortedPairs.filter((p) => selectedRows.has(p.id));
    if (selected.length === 0) return;

    const timestamp = new Date().toLocaleString('en-US', {
      dateStyle: 'medium',
      timeStyle: 'short',
    });

    function formatPair(p: AvatarAidePair) {
      return [
        `### ${p.avatarName} & ${p.aideName}`,
        '',
        `- **Trait:** ${p.trait}`,
        `- **Category:** ${CATEGORY_LABELS[p.category]}`,
        `- **Status:** ${STATUS_CONFIG[p.status].label}`,
        `- **Readiness:** ${Math.round(p.readinessScore * 100)}%`,
        `- **Empathy Level:** ${EMPATHY_LABELS[p.empathyLevel]}`,
        `- **Advocate:** ${p.advocateName}`,
        `- **Advocate Strength:** *"${p.advocateStrength}"*`,
        '',
      ].join('\n');
    }

    const sections: string[] = [
      '# NeuroLift AI Fusion — Selected Pairs',
      '',
      `> Generated on ${timestamp} — ${selected.length} pair${selected.length === 1 ? '' : 's'} selected`,
      '',
    ];

    for (const pair of selected) {
      sections.push(formatPair(pair));
    }

    sections.push(
      '---',
      '',
      '*"Every mind deserves an ally that truly understands."* — NeuroLift AI Fusion',
    );

    const blob = new Blob([sections.join('\n')], { type: 'text/markdown;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'neurolift-selected-pairs.md';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    onExportToast?.();
  }, [selectedRows, tableSortedPairs, onExportToast]);

  // ── Close context menu on click, contextmenu, scroll, or Escape ──
  useEffect(() => {
    if (!contextMenu) return;
    function close() {
      setContextMenu(null);
    }
    document.addEventListener("click", close);
    document.addEventListener("contextmenu", close);
    window.addEventListener("scroll", close, true);
    function handleEsc(e: KeyboardEvent) {
      if (e.key === "Escape") close();
    }
    window.addEventListener("keydown", handleEsc);
    return () => {
      document.removeEventListener("click", close);
      document.removeEventListener("contextmenu", close);
      window.removeEventListener("scroll", close, true);
      window.removeEventListener("keydown", handleEsc);
    };
  }, [contextMenu]);

  // Keyboard navigation
  const getColumns = useCallback(() => {
    if (typeof window === "undefined") return 1;
    if (window.innerWidth >= 1024) return 3;
    if (window.innerWidth >= 640) return 2;
    return 1;
  }, []);

  useEffect(() => {
    function handleKeyDown(e: KeyboardEvent) {
      if (focusedIndex < 0) return;
      if (e.target instanceof HTMLInputElement || e.target instanceof HTMLSelectElement) return;

      const cols = getColumns();
      let nextIdx = focusedIndex;

      switch (e.key) {
        case "ArrowRight":
          nextIdx = Math.min(focusedIndex + 1, filteredPairs.length - 1);
          break;
        case "ArrowLeft":
          nextIdx = Math.max(focusedIndex - 1, 0);
          break;
        case "ArrowDown":
          nextIdx = Math.min(focusedIndex + cols, filteredPairs.length - 1);
          break;
        case "ArrowUp":
          nextIdx = Math.max(focusedIndex - cols, 0);
          break;
        case "Enter":
        case " ":
          if (filteredPairs[focusedIndex]) {
            e.preventDefault();
            onSelectPair(filteredPairs[focusedIndex]);
          }
          return;
        default:
          return;
      }

      e.preventDefault();
      setFocusedIndex(nextIdx);
      const cards = gridRef.current?.querySelectorAll('[role="button"]');
      if (cards) {
        const card = cards[nextIdx];
        if (card instanceof HTMLElement) {
          card.focus();
        }
      }
    }

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [focusedIndex, filteredPairs, getColumns, onSelectPair]);

  // Outside click handler for search suggestions
  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (searchContainerRef.current && !searchContainerRef.current.contains(e.target as Node)) {
        setShowSuggestions(false);
        setActiveSuggestionIndex(-1);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // ── Context menu handler for grid cards (with viewport overflow adjustment) ──
  const handleContextMenu = useCallback((e: React.MouseEvent, pair: AvatarAidePair) => {
    e.preventDefault();
    const menuW = 200;
    const menuH = 160;
    let left = e.clientX;
    let top = e.clientY;
    if (left + menuW > window.innerWidth) left = window.innerWidth - menuW - 8;
    if (top + menuH > window.innerHeight) top = window.innerHeight - menuH - 8;
    if (left < 0) left = 8;
    if (top < 0) top = 8;
    setContextMenu({ x: left, y: top, pair });
  }, []);

  // ── Context menu action handlers ──
  const handleCopyPairInfo = useCallback(() => {
    if (!contextMenu) return;
    const p = contextMenu.pair;
    const text = `${p.avatarName} — ${p.trait} — ${STATUS_CONFIG[p.status].label}`;
    navigator.clipboard.writeText(text).then(() => {
      toast("Copied pair info", { description: text, duration: 2000 });
    });
  }, [contextMenu]);

  // Scroll active suggestion into view
  useEffect(() => {
    if (activeSuggestionIndex >= 0 && showSuggestions) {
      const el = document.getElementById(`search-suggestion-${activeSuggestionIndex}`);
      el?.scrollIntoView({ block: 'nearest' });
    }
  }, [activeSuggestionIndex, showSuggestions]);

  // Handle column sort toggle
  const handleTableSort = useCallback((column: string) => {
    setTableSort((prev) => {
      if (prev.column !== column) return { column, direction: 'asc' };
      if (prev.direction === 'asc') return { column, direction: 'desc' };
      if (prev.direction === 'desc') return { column, direction: 'none' };
      return { column, direction: 'asc' };
    });
  }, []);

  // Select a suggestion
  const handleSelectSuggestion = useCallback((pair: AvatarAidePair) => {
    setSearchQuery(pair.avatarName);
    setShowSuggestions(false);
    setActiveSuggestionIndex(-1);
  }, []);

  return (
    <section
      id="pairs"
      className="py-16 md:py-24 px-4 sm:px-6 lg:px-8 bg-muted/30"
      style={{ background: 'radial-gradient(ellipse at top center, rgba(243,128,32,0.03) 0%, transparent 50%)' }}
      aria-label="The 19 Avatar-Aide-Advocate pairs"
    >
      <div className="mx-auto w-full max-w-7xl">
      {/* ── Section header ──────────────────────────────────── */}
      <div className="mb-10 text-center">
        <h2 className="text-3xl font-bold tracking-tight sm:text-4xl">The 19 Pairs</h2>
        <p className="mt-3 text-base text-muted-foreground sm:text-lg">
          Each pair addresses a unique dimension of the ADHD experience
        </p>
        <p className="mt-2 text-sm text-muted-foreground/70">
          Showing <AnimatePresence mode="wait"><motion.span key={filteredPairs.length} initial={{ opacity: 0, y: -4 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: 4 }} transition={{ duration: 0.2 }} className="font-semibold tabular-nums text-foreground/80">{filteredPairs.length}</motion.span></AnimatePresence> of <span className="font-semibold tabular-nums text-foreground/80">{PAIRS.length}</span> pairs
        </p>
      </div>

      {/* ── Category overview cards ─────────────────────── */}
      <CategoryOverviewCards
        activeFilter={activeFilter}
        onFilterChange={setActiveFilter}
        favoritesCount={favorites.length}
      />

      {/* ── Filter bar ────────────────────────────────────── */}
      <Card className="mb-8 rounded-xl border bg-card/50 backdrop-blur-sm shadow-sm">
        <CardContent className="p-3 sm:p-4">
        {/* Category filter tabs (including Favorites) */}
        <div
          className="flex flex-wrap gap-2"
          role="tablist"
          aria-label="Filter pairs by category"
        >
          {FILTER_OPTIONS.map((opt) => {
            const isActive = activeFilter === opt.key;
            const count = filterCounts[opt.key as keyof typeof filterCounts];
            return (
              <button
                key={opt.key}
                role="tab"
                aria-selected={isActive}
                aria-controls="pairs-grid-panel"
                onClick={() => { setActiveFilter(opt.key); setSelectedRows(new Set()); }}
                className={`
                  inline-flex items-center gap-1.5 rounded-lg px-3.5 py-2 text-sm font-medium
                  transition-all duration-200 focus-visible:outline-none focus-visible:ring-2
                  focus-visible:ring-offset-2 focus-visible:ring-orange-500/50
                  ${
                    isActive
                      ? "bg-orange-500/15 text-orange-600 shadow-sm ring-1 ring-orange-500/30 dark:text-orange-400"
                      : "bg-muted/50 text-muted-foreground hover:bg-muted hover:text-foreground"
                  }
                `}
              >
                {opt.icon}
                <span>{opt.label}</span>
                <span
                  className={`
                    inline-flex h-5 min-w-5 items-center justify-center rounded-full px-1.5 text-xs font-semibold tabular-nums
                    ${
                      isActive
                        ? "bg-orange-500/20 text-orange-700 dark:text-orange-300"
                        : "bg-muted text-muted-foreground/70"
                    }
                  `}
                >
                  <AnimatedCounter target={count} />
                </span>
              </button>
            );
          })}
        </div>

        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between w-full">
          <div className="relative flex-1 sm:w-72" ref={searchContainerRef}>
            <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground/60" />
            <Input
              type="search"
              placeholder="Search pairs…"
              value={searchQuery}
              onChange={(e) => {
                setSearchQuery(e.target.value);
                setActiveSuggestionIndex(-1);
                setShowSuggestions(true);
                setSelectedRows(new Set());
              }}
              onFocus={() => {
                if (searchQuery.length >= 2) setShowSuggestions(true);
              }}
              onKeyDown={(e) => {
                if (e.key === 'Escape') {
                  e.preventDefault();
                  setShowSuggestions(false);
                  setActiveSuggestionIndex(-1);
                  return;
                }
                if (!showSuggestions || suggestions.length === 0) return;

                switch (e.key) {
                  case 'ArrowDown':
                    e.preventDefault();
                    setActiveSuggestionIndex((prev) =>
                      prev >= suggestions.length - 1 ? 0 : prev + 1
                    );
                    break;
                  case 'ArrowUp':
                    e.preventDefault();
                    setActiveSuggestionIndex((prev) =>
                      prev <= 0 ? suggestions.length - 1 : prev - 1
                    );
                    break;
                  case 'Enter':
                    if (activeSuggestionIndex >= 0 && suggestions[activeSuggestionIndex]) {
                      e.preventDefault();
                      handleSelectSuggestion(suggestions[activeSuggestionIndex]);
                    }
                    break;
                }
              }}
              aria-label="Search pairs by name, trait, or description"
              aria-expanded={showSuggestions}
              aria-autocomplete="list"
              aria-activedescendant={activeSuggestionIndex >= 0 ? `search-suggestion-${activeSuggestionIndex}` : undefined}
              aria-controls="search-suggestions-listbox"
              role="combobox"
              className="h-10 pl-9 pr-4"
            />
            {/* Search suggestions dropdown */}
            {showSuggestions && suggestions.length > 0 && (
              <div className="absolute left-0 top-full z-50 mt-1 w-full sm:w-72 max-h-64 overflow-y-auto rounded-lg border bg-card shadow-lg">
                <ul role="listbox" id="search-suggestions-listbox" className="p-1">
                  {suggestions.map((pair, idx) => {
                    const pct = Math.round(pair.readinessScore * 100);
                    const isActive = idx === activeSuggestionIndex;
                    return (
                      <li
                        key={pair.id}
                        id={`search-suggestion-${idx}`}
                        role="option"
                        aria-selected={isActive}
                        className={`flex cursor-pointer items-center gap-2.5 rounded-md px-2.5 py-2 text-sm transition-colors ${isActive ? 'bg-muted' : 'hover:bg-muted/50'}`}
                        onMouseDown={(e) => {
                          e.preventDefault();
                          handleSelectSuggestion(pair);
                        }}
                        onMouseEnter={() => setActiveSuggestionIndex(idx)}
                      >
                        <span
                          className="h-2.5 w-2.5 shrink-0 rounded-full"
                          style={{ backgroundColor: pair.color }}
                          aria-hidden="true"
                        />
                        <span className="min-w-0 flex-1">
                          <span className="font-medium">{highlightMatch(pair.avatarName, searchQuery)}</span>
                          <span className="ml-1.5 text-xs text-muted-foreground">{highlightMatch(pair.trait, searchQuery)}</span>
                        </span>
                        <span
                          className="shrink-0 text-xs font-semibold tabular-nums"
                          style={{ color: pair.color }}
                        >
                          {pct}%
                        </span>
                      </li>
                    );
                  })}
                </ul>
              </div>
            )}
          </div>
          {onOpenCompare && (
            <Button
              variant="secondary"
              size="sm"
              className="shrink-0 gap-1.5"
              onClick={onOpenCompare}
              aria-label="Compare pairs side-by-side"
            >
              <GitCompareArrows className="h-3.5 w-3.5" />
              <span className="hidden sm:inline">Compare</span>
            </Button>
          )}
          <Button
            variant="outline"
            size="sm"
            className="shrink-0 gap-1.5"
            onClick={handleRandomPair}
            aria-label="Discover a random pair"
          >
            <Shuffle className="h-3.5 w-3.5" />
            <span className="hidden sm:inline">Random</span>
          </Button>
          <Button
            variant="outline"
            size="sm"
            className="shrink-0 gap-1.5"
            onClick={handleExportSummary}
            aria-label="Export pairs summary as markdown"
          >
            <Download className="h-3.5 w-3.5" />
            <span className="hidden sm:inline">Export Summary</span>
          </Button>
          <motion.div whileTap={{ scale: 0.93 }} className="inline-block">
          <Button
            variant="outline"
            size="sm"
            className="shrink-0"
            onClick={() => {
              setViewMode((m) => {
                if (m === 'table') setSelectedRows(new Set());
                if (m === 'grid') setTableSort({ column: '', direction: 'none' });
                return m === 'grid' ? 'table' : 'grid';
              });
            }}
            aria-label="Toggle table view"
          >
            {viewMode === 'grid' ? <List className="h-3.5 w-3.5" /> : <LayoutGrid className="h-3.5 w-3.5" />}
          </Button>
          </motion.div>
          <Select value={sortKey} onValueChange={(v) => setSortKey(v as SortKey)}>
            <SelectTrigger
              size="sm"
              className="w-[180px] shrink-0"
              aria-label="Sort pairs"
            >
              <ArrowUpDown className="mr-1.5 h-3.5 w-3.5 text-muted-foreground/60" />
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              {SORT_OPTIONS.map((opt) => (
                <SelectItem key={opt.value} value={opt.value}>
                  {opt.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

      {/* ── Status filter row ────────────────────────────────── */}
      <div className="mt-4 flex flex-wrap gap-2" role="tablist" aria-label="Filter pairs by training status">
        {STATUS_FILTER_OPTIONS.map((opt) => {
          const isActive = activeStatusFilter === opt.key;
          const count = statusCounts[opt.key];
          return (
            <button
              key={opt.key}
              role="tab"
              aria-selected={isActive}
              onClick={() => { setActiveStatusFilter(opt.key); setSelectedRows(new Set()); }}
              className={`
                inline-flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-xs font-medium
                transition-all duration-200 focus-visible:outline-none focus-visible:ring-2
                focus-visible:ring-offset-2 focus-visible:ring-orange-500/50
                ${
                  isActive
                    ? "bg-orange-500/15 text-orange-600 shadow-sm ring-1 ring-orange-500/30 dark:text-orange-400"
                    : "bg-muted/50 text-muted-foreground hover:bg-muted hover:text-foreground"
                }
              `}
            >
              <span>{opt.label}</span>
              <span
                className={`
                  inline-flex h-4 min-w-4 items-center justify-center rounded-full px-1 text-[10px] font-semibold tabular-nums
                  ${
                    isActive
                      ? "bg-orange-500/20 text-orange-700 dark:text-orange-300"
                      : "bg-muted text-muted-foreground/70"
                  }
                `}
              >
                {count}
              </span>
            </button>
          );
        })}
        </div>
        </CardContent>
      </Card>

      {/* ── Grid / Table ────────────────────────────────── */}
      <div id="pairs-grid-panel" role="tabpanel" aria-label="Filtered pairs">
        <TooltipPrimitive.Provider delayDuration={600}>
          <AnimatePresence mode="wait">
            {filteredPairs.length > 0 ? (
              viewMode === 'grid' ? (
                <motion.div
                  key={viewMode}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                  transition={{ duration: 0.25 }}
                >
                  <motion.div
                    ref={gridRef}
                    key={`grid-${activeFilter}-${activeStatusFilter}-${searchQuery}-${sortKey}-${favorites.length}`}
                    className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3"
                    variants={containerVariants}
                    initial="hidden"
                    animate="show"
                >
                  {filteredPairs.map((pair, idx) => (
                    <PairCardWithTooltip
                      key={pair.id}
                      pair={pair}
                      isFavorited={favorites.includes(pair.id)}
                      searchQuery={searchQuery}
                      onClick={() => onSelectPair(pair)}
                      onFocus={() => setFocusedIndex(idx)}
                      onToggleFavorite={(e) => toggleFavorite(pair.id, e)}
                      onContextMenu={(e) => handleContextMenu(e, pair)}
                    />
                  ))}
                </motion.div>
                </motion.div>
              ) : (
                <motion.div
                  key={viewMode}
                  initial={{ opacity: 0, x: 10 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -10 }}
                  transition={{ duration: 0.25 }}
                  className="overflow-x-auto"
                >
                  <AnimatePresence>
                    {selectedRows.size > 0 && (
                      <motion.div
                        initial={{ opacity: 0, y: -8 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -8 }}
                        transition={{ duration: 0.2 }}
                        className="mb-3 flex items-center gap-3 rounded-lg border border-l-[3px] border-l-orange-500 bg-orange-500/5 px-4 py-2.5"
                      >
                        <span className="text-sm font-medium">{selectedRows.size} pair{selectedRows.size !== 1 ? 's' : ''} selected</span>
                        <div className="flex items-center gap-2 ml-auto">
                          <Button variant="outline" size="sm" className="gap-1.5 h-8" onClick={handleFavoriteAllSelected}>
                            <Heart className="h-3.5 w-3.5" />
                            <span className="hidden sm:inline">Favorite All</span>
                          </Button>
                          <Button variant="outline" size="sm" className="gap-1.5 h-8" onClick={handleExportSelected}>
                            <Download className="h-3.5 w-3.5" />
                            <span className="hidden sm:inline">Export Selected</span>
                          </Button>
                          <Button variant="ghost" size="sm" className="gap-1.5 h-8" onClick={() => setSelectedRows(new Set())}>
                            <X className="h-3.5 w-3.5" />
                            <span className="hidden sm:inline">Clear</span>
                          </Button>
                        </div>
                      </motion.div>
                    )}
                  </AnimatePresence>
                  <table className="w-full text-sm">
                    <thead className="sticky top-0 z-10 bg-card">
                      <tr className="border-b border-border bg-muted/50 text-left text-xs font-medium uppercase tracking-wider text-muted-foreground">
                        <th className="px-3 py-3 w-10">
                          <Checkbox
                            checked={
                              tableSortedPairs.length > 0 && tableSortedPairs.every((p) => selectedRows.has(p.id))
                                ? true
                                : tableSortedPairs.some((p) => selectedRows.has(p.id))
                                  ? "indeterminate"
                                  : false
                            }
                            onCheckedChange={(checked) => {
                              if (checked === true) {
                                setSelectedRows(new Set(tableSortedPairs.map((p) => p.id)));
                              } else {
                                setSelectedRows(new Set());
                              }
                            }}
                            aria-label="Select all rows"
                          />
                        </th>
                        <th className="px-3 py-3 pr-2 cursor-pointer select-none" onClick={() => handleTableSort('id')}>
                          <span className="inline-flex items-center gap-1"># {tableSort.column === 'id' ? (tableSort.direction === 'asc' ? <ChevronUp className="h-3 w-3" /> : <ChevronDown className="h-3 w-3" />) : <ChevronsUpDown className="h-3 w-3 opacity-40" />}</span>
                        </th>
                        <th className="px-3 py-3 cursor-pointer select-none" onClick={() => handleTableSort('name')}>
                          <span className="inline-flex items-center gap-1">Name {tableSort.column === 'name' ? (tableSort.direction === 'asc' ? <ChevronUp className="h-3 w-3" /> : <ChevronDown className="h-3 w-3" />) : <ChevronsUpDown className="h-3 w-3 opacity-40" />}</span>
                        </th>
                        <th className="px-3 py-3">Trait</th>
                        <th className="hidden px-3 py-3 md:table-cell">Category</th>
                        <th className="px-3 py-3">Status</th>
                        <th className="px-3 py-3 cursor-pointer select-none" onClick={() => handleTableSort('readiness')}>
                          <span className="inline-flex items-center gap-1">Readiness {tableSort.column === 'readiness' ? (tableSort.direction === 'asc' ? <ChevronUp className="h-3 w-3" /> : <ChevronDown className="h-3 w-3" />) : <ChevronsUpDown className="h-3 w-3 opacity-40" />}</span>
                        </th>
                        <th className="hidden px-3 py-3 sm:table-cell cursor-pointer select-none" onClick={() => handleTableSort('empathy')}>
                          <span className="inline-flex items-center gap-1">Empathy {tableSort.column === 'empathy' ? (tableSort.direction === 'asc' ? <ChevronUp className="h-3 w-3" /> : <ChevronDown className="h-3 w-3" />) : <ChevronsUpDown className="h-3 w-3 opacity-40" />}</span>
                        </th>
                        <th className="px-3 py-3 text-right">Actions</th>
                      </tr>
                    </thead>
                    <tbody>
                      {tableSortedPairs.map((pair) => {
                        const statusConf = STATUS_CONFIG[pair.status];
                        const readinessPercent = Math.round(pair.readinessScore * 100);
                        return (
                          <tr
                            key={pair.id}
                            className="border-b border-border border-l-[3px] transition-colors hover:bg-muted/30 cursor-pointer"
                            style={{ borderLeftColor: pair.color }}
                            onClick={() => onSelectPair(pair)}
                          >
                            <td className="px-3 py-3 w-10" onClick={(e) => e.stopPropagation()}>
                              <Checkbox
                                checked={selectedRows.has(pair.id)}
                                onCheckedChange={(checked) => {
                                  setSelectedRows((prev) => {
                                    const next = new Set(prev);
                                    if (checked === true) {
                                      next.add(pair.id);
                                    } else {
                                      next.delete(pair.id);
                                    }
                                    return next;
                                  });
                                }}
                                aria-label={`Select ${pair.avatarName}`}
                              />
                            </td>
                            <td className="px-3 py-3 pr-2 tabular-nums text-muted-foreground">
                              {pair.id}
                            </td>
                            <td className="px-3 py-3 font-medium">
                              <span className="flex items-center gap-2">
                                <PairIcon name={pair.iconName} color={pair.color} />
                                <span>{highlightMatch(pair.avatarName, searchQuery)}</span>
                              </span>
                            </td>
                            <td className="px-3 py-3 text-muted-foreground">
                              {pair.trait}
                            </td>
                            <td className="hidden px-3 py-3 md:table-cell">
                              <span className={`inline-flex items-center rounded-full px-2 py-0.5 text-[11px] font-medium leading-tight ${pair.bgClass} ${pair.colorClass}`}>
                                {CATEGORY_LABELS[pair.category]}
                              </span>
                            </td>
                            <td className="px-3 py-3">
                              <span className={`inline-flex items-center rounded-full px-2 py-0.5 text-[11px] font-medium leading-tight ${statusConf.bgColor} ${statusConf.color}`}>
                                {statusConf.label}
                              </span>
                            </td>
                            <td className="px-3 py-3">
                              <span className="flex items-center gap-2">
                                <div className="h-1.5 w-16 overflow-hidden rounded-full bg-muted">
                                  <div
                                    className="h-full rounded-full transition-all"
                                    style={{ width: `${readinessPercent}%`, backgroundColor: pair.color }}
                                  />
                                </div>
                                <span className="tabular-nums text-xs font-semibold" style={{ color: pair.color }}>
                                  {readinessPercent}%
                                </span>
                              </span>
                            </td>
                            <td className="hidden px-3 py-3 text-muted-foreground sm:table-cell">
                              {EMPATHY_LABELS[pair.empathyLevel]}
                            </td>
                            <td className="px-3 py-3 text-right">
                              <Button
                                variant="ghost"
                                size="sm"
                                className="h-7 px-2 text-xs"
                                onClick={() => onSelectPair(pair)}
                                aria-label={`View details for ${pair.avatarName}`}
                              >
                                View
                              </Button>
                            </td>
                          </tr>
                        );
                      })}
                    </tbody>
                  </table>
                </motion.div>
              )
            ) : (
              <motion.div
                key="empty"
                initial={{ opacity: 0, y: 12 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -8 }}
                transition={{ duration: 0.3 }}
                className="flex flex-col items-center justify-center py-20 text-center"
              >
                {/* Fun empty state illustration — 3 circles with connecting lines */}
                <svg
                  width="120"
                  height="64"
                  viewBox="0 0 120 64"
                  fill="none"
                  className="mb-5"
                  aria-hidden="true"
                >
                  {/* Connecting lines */}
                  <line x1="36" y1="32" x2="44" y2="32" stroke="currentColor" className="text-muted-foreground/15" strokeWidth="2" strokeDasharray="4 3" />
                  <line x1="76" y1="32" x2="84" y2="32" stroke="currentColor" className="text-muted-foreground/15" strokeWidth="2" strokeDasharray="4 3" />
                  {/* Avatar circle */}
                  <circle cx="20" cy="32" r="16" className="fill-orange-400/10" />
                  <circle cx="20" cy="32" r="16" className="stroke-orange-400/20" strokeWidth="1.5" fill="none" />
                  <User x="12" y="24" width="16" height="16" className="stroke-orange-400/40" strokeWidth="1.5" fill="none" />
                  {/* Aide circle */}
                  <circle cx="60" cy="32" r="16" className="fill-teal-400/10" />
                  <circle cx="60" cy="32" r="16" className="stroke-teal-400/20" strokeWidth="1.5" fill="none" />
                  <Bot x="52" y="24" width="16" height="16" className="stroke-teal-400/40" strokeWidth="1.5" fill="none" />
                  {/* Advocate circle */}
                  <circle cx="100" cy="32" r="16" className="fill-amber-400/10" />
                  <circle cx="100" cy="32" r="16" className="stroke-amber-400/20" strokeWidth="1.5" fill="none" />
                  <Megaphone x="92" y="24" width="16" height="16" className="stroke-amber-400/40" strokeWidth="1.5" fill="none" />
                </svg>
                <p className="text-lg font-medium text-muted-foreground">
                  No pairs found
                </p>
                <p className="mt-1 max-w-sm text-sm text-muted-foreground/70">
                  Try adjusting your search or filter to find what you&apos;re looking for.
                </p>
                {searchQuery && (
                  <button
                    onClick={() => setSearchQuery("")}
                    className="mt-4 text-sm font-medium text-orange-600 transition-colors hover:text-orange-500 dark:text-orange-400"
                  >
                    Clear search
                  </button>
                )}
              </motion.div>
            )}
          </AnimatePresence>
        </TooltipPrimitive.Provider>
      </div>
      </div>

      {/* ═══ Right-Click Context Menu (grid cards only) ═══ */}
      <AnimatePresence>
        {contextMenu && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            transition={{ duration: 0.12 }}
            className="fixed z-[100] min-w-[180px] rounded-lg border bg-popover p-1 shadow-xl"
            style={{ left: contextMenu.x, top: contextMenu.y }}
            role="menu"
            aria-label={`Actions for ${contextMenu.pair.avatarName}`}
          >
            {/* Header: color dot + avatarName (non-clickable) */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0 * 0.05 }}
              className="flex items-center gap-2 px-3 py-2"
            >
              <span className="h-2 w-2 rounded-full" style={{ backgroundColor: contextMenu.pair.color }} />
              <span className="text-sm font-bold truncate">{contextMenu.pair.avatarName}</span>
            </motion.div>
            <div className="border-t my-1" />
            <motion.div
              initial={{ opacity: 0, x: -4 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 1 * 0.05 }}
              role="menuitem" tabIndex={0} className="flex items-center gap-2 px-3 py-2 text-sm rounded-md cursor-pointer hover:bg-muted"
              onClick={() => { onSelectPair(contextMenu.pair); setContextMenu(null); }}
            >
              <Eye className="h-4 w-4" /><span>View Details</span>
            </motion.div>
            <motion.div
              initial={{ opacity: 0, x: -4 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 2 * 0.05 }}
              role="menuitem" tabIndex={0} className="flex items-center gap-2 px-3 py-2 text-sm rounded-md cursor-pointer hover:bg-muted"
              onClick={() => { toggleFavorite(contextMenu.pair.id, { stopPropagation: () => {}, preventDefault: () => {} } as React.MouseEvent); setContextMenu(null); }}
            >
              <Heart className="h-4 w-4" /><span>Toggle Favorite</span>
            </motion.div>
            <motion.div
              initial={{ opacity: 0, x: -4 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 3 * 0.05 }}
              role="menuitem" tabIndex={0} className="flex items-center gap-2 px-3 py-2 text-sm rounded-md cursor-pointer hover:bg-muted"
              onClick={() => { handleCopyPairInfo(); setContextMenu(null); }}
            >
              <Copy className="h-4 w-4" /><span>Copy Info</span>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </section>
  );
}

// ─── Pair card with tooltip wrapper ──────────────────────────────────
function PairCardWithTooltip({
  pair,
  isFavorited,
  searchQuery,
  onClick,
  onFocus,
  onToggleFavorite,
  onContextMenu,
}: {
  pair: AvatarAidePair;
  isFavorited: boolean;
  searchQuery: string;
  onClick: () => void;
  onFocus?: () => void;
  onToggleFavorite: (e: React.MouseEvent) => void;
  onContextMenu?: (e: React.MouseEvent) => void;
}) {
  const statusConf = STATUS_CONFIG[pair.status];
  const readinessPercent = Math.round(pair.readinessScore * 100);
  const empathyLabel = EMPATHY_LABELS[pair.empathyLevel];

  return (
    <TooltipPrimitive.Root>
      <TooltipPrimitive.Trigger asChild>
        <div className="inline-block w-full">
          <PairCard
            pair={pair}
            isFavorited={isFavorited}
            searchQuery={searchQuery}
            onClick={onClick}
            onFocus={onFocus}
            onToggleFavorite={onToggleFavorite}
            onContextMenu={onContextMenu}
          />
        </div>
      </TooltipPrimitive.Trigger>
      <TooltipPrimitive.Portal>
        <TooltipPrimitive.Content
          side="bottom"
          sideOffset={8}
          className="z-50 w-64 rounded-lg border border-border border-l-2 bg-popover p-3 text-sm text-popover-foreground shadow-lg animate-in fade-in-0 zoom-in-95 data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=closed]:zoom-out-95"
          style={{ borderLeftColor: pair.color }}
        >
          {/* Pair color dot + avatarName + trait */}
          <div className="flex items-center gap-2">
            <span className="h-2.5 w-2.5 shrink-0 rounded-full" style={{ backgroundColor: pair.color }} />
            <p className="font-semibold leading-tight">
              {pair.avatarName}
              <span className="mx-1 text-muted-foreground/40">·</span>
              <span className="font-bold">{pair.trait}</span>
            </p>
          </div>

          {/* Status badge + Empathy label */}
          <div className="mt-2 flex flex-wrap items-center gap-2 text-xs">
            <span className={`rounded-full px-1.5 py-0.5 text-[10px] font-medium ${statusConf.bgColor} ${statusConf.color}`}>
              {statusConf.label}
            </span>
            <span className="text-muted-foreground">
              Empathy: <span className="font-semibold text-foreground">{empathyLabel}</span>
            </span>
          </div>

          {/* Readiness with inline progress bar */}
          <div className="mt-2 flex items-center gap-2 text-xs text-muted-foreground">
            <span className="shrink-0">Readiness:</span>
            <div className="h-1.5 flex-1 overflow-hidden rounded-full bg-muted">
              <div
                className="h-full rounded-full transition-all"
                style={{ width: `${readinessPercent}%`, backgroundColor: pair.color }}
              />
            </div>
            <span className="shrink-0 font-semibold tabular-nums text-foreground">{readinessPercent}%</span>
          </div>

          {/* 3 key metrics */}
          {pair.keyMetrics.length > 0 && (
            <div className="mt-2 space-y-0.5 border-t border-border/60 pt-2">
              {pair.keyMetrics.slice(0, 3).map((m) => (
                <div key={m.label} className="flex items-center justify-between text-[11px]">
                  <span className="text-muted-foreground">{m.label}:</span>
                  <span className="font-semibold tabular-nums text-foreground">{m.value}</span>
                </div>
              ))}
            </div>
          )}
        </TooltipPrimitive.Content>
      </TooltipPrimitive.Portal>
    </TooltipPrimitive.Root>
  );
}

// ─── Pair icon renderer (returns static JSX to satisfy lint rules) ─────
function PairIcon({ name, color }: { name: string; color: string }) {
  const props = { className: "h-5 w-5" as const, style: { color } };
  switch (name) {
    case "Eye": return <Eye {...props} />;
    case "Shield": return <Shield {...props} />;
    case "Target": return <Target {...props} />;
    case "Clock": return <Clock {...props} />;
    case "Brain": return <Brain {...props} />;
    case "Heart": return <Heart {...props} />;
    case "Rocket": return <Rocket {...props} />;
    case "Flame": return <Flame {...props} />;
    case "ListChecks": return <ListChecks {...props} />;
    case "ArrowLeftRight": return <ArrowLeftRight {...props} />;
    case "ScanEye": return <ScanEye {...props} />;
    case "Mountain": return <Mountain {...props} />;
    case "Battery": return <Battery {...props} />;
    case "Gauge": return <Gauge {...props} />;
    case "ShieldAlert": return <ShieldAlert {...props} />;
    case "Ear": return <Ear {...props} />;
    case "Users": return <Users {...props} />;
    case "Sparkles": return <Sparkles {...props} />;
    case "Star": return <Star {...props} />;
    default: return <Circle {...props} />;
  }
}

// ─── Individual pair card ────────────────────────────────────────────
function PairCard({
  pair,
  isFavorited,
  searchQuery,
  onClick,
  onFocus,
  onToggleFavorite,
  onContextMenu,
}: {
  pair: AvatarAidePair;
  isFavorited: boolean;
  searchQuery: string;
  onClick: () => void;
  onFocus?: () => void;
  onToggleFavorite: (e: React.MouseEvent) => void;
  onContextMenu?: (e: React.MouseEvent) => void;
}) {
  const statusConf = STATUS_CONFIG[pair.status];
  const readinessPercent = Math.round(pair.readinessScore * 100);

  // Truncate short description to ~80 chars
  const truncatedDesc =
    pair.shortDescription.length > 80
      ? pair.shortDescription.slice(0, 80) + "…"
      : pair.shortDescription;

  return (
    <motion.article
      variants={cardVariants}
      layout
      layoutId={`pair-${pair.id}`}
      onClick={onClick}
      onContextMenu={onContextMenu}
      onFocus={onFocus}
      onKeyDown={(e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          onClick();
        }
      }}
      tabIndex={0}
      role="button"
      aria-label={`View details for ${pair.avatarName} — ${pair.trait}`}
      className={`
        group relative cursor-pointer overflow-hidden rounded-xl border border-border/60
        border-l-[3px] bg-card p-5 shadow-sm transition-all duration-300
        hover:shadow-lg
        focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-orange-500/50
        dark:shadow-none dark:hover:shadow-orange-900/20 dark:hover:shadow-lg
      `}
      style={{
        borderLeftColor: pair.color,
      }}
      whileHover={{
        y: -3,
        transition: { duration: 0.2 },
        boxShadow: `0 10px 30px -8px ${pair.color}26, 0 4px 12px -4px ${pair.color}15`,
      }}
    >
      {/* ── Corner accent ribbon (top-right) ── */}
      {/* ── Hover gradient overlay (top glow) ── */}
      <div
        className="card-hover-gradient"
        style={{
          background: `linear-gradient(180deg, ${pair.color}08 0%, transparent 100%)`,
          borderRadius: 'inherit',
        }}
        aria-hidden="true"
      />

      {/* ── Shimmer sweep on hover ── */}
      <div
        className="card-shimmer-sweep"
        aria-hidden="true"
      />

      <div
        className="absolute top-0 right-0 flex h-8 w-8 items-end justify-start overflow-hidden rounded-bl-md"
        style={{ backgroundColor: `${pair.color}26` }}
        aria-hidden="true"
      >
        <span
          className="pb-0.5 pl-1 text-[10px] font-bold leading-none"
          style={{ color: pair.color }}
        >
          {pair.id}
        </span>
      </div>

      {/* ── Bookmark / Favorite heart icon (top-right, below ribbon) ── */}
      <button
        type="button"
        onClick={onToggleFavorite}
        aria-label={isFavorited ? "Bookmarked" : "Bookmark"}
        className={
          "absolute top-2.5 right-9 z-10 flex h-7 w-7 items-center justify-center rounded-full " +
          "transition-colors duration-200 " +
          (isFavorited
            ? "text-red-500 hover:text-red-600 dark:hover:text-red-400"
            : "text-muted-foreground/30 hover:text-muted-foreground/60 hover:bg-muted/80")
        }
      >
        <motion.div
          initial={false}
          animate={isFavorited ? { scale: [1, 1.35, 1] } : { scale: 1 }}
          transition={{ duration: 0.3, ease: "easeInOut" }}
        >
          <Heart
            className="h-4 w-4"
            fill={isFavorited ? "currentColor" : "none"}
          />
        </motion.div>
      </button>

      {/* Top row: icon + name + badges */}
      <div className="flex items-start gap-3">
        {/* Icon circle with hover pulse */}
        <div className="relative">
          <motion.div
            className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full"
            style={{ backgroundColor: `${pair.color}15` }}
            aria-hidden="true"
            whileHover={{
              scale: [1, 1.15, 1],
              transition: { duration: 0.4, ease: "easeInOut" },
            }}
          >
            <PairIcon name={pair.iconName} color={pair.color} />
          </motion.div>
        </div>

        <div className="min-w-0 flex-1">
          {/* Name */}
          <h3 className="truncate text-base font-bold leading-tight text-foreground">
            {highlightMatch(pair.avatarName, searchQuery)}
          </h3>
          {/* Trait */}
          <p className="mt-0.5 truncate text-sm text-muted-foreground">
            {pair.trait}
          </p>
        </div>
      </div>

      {/* Badges row + Confidence Ring */}
      <div className="mt-3 flex items-center justify-between gap-2">
        <div className="flex flex-wrap items-center gap-1.5 min-w-0">
          {/* Category badge */}
          <span
            className={
              "inline-flex items-center rounded-full px-2 py-0.5 text-[11px] font-medium leading-tight " +
              pair.bgClass + " " + pair.colorClass
            }
          >
            {CATEGORY_LABELS[pair.category]}
          </span>

          {/* Status badge */}
          <span
            className={
              "inline-flex items-center rounded-full px-2 py-0.5 text-[11px] font-medium leading-tight " +
              statusConf.bgColor + " " + statusConf.color
            }
          >
            {statusConf.label}
          </span>
        </div>

        {/* Confidence Ring */}
        <ConfidenceRing
          value={readinessPercent}
          color={pair.color}
        />
      </div>

      {/* Short description */}
      <p className="mt-2 text-xs text-muted-foreground/80 leading-relaxed">
        {truncatedDesc}
      </p>

      {/* Readiness progress bar */}
      <div className="mt-3.5">
        <div className="mb-1 flex items-center justify-between">
          <span className="text-[11px] font-medium text-muted-foreground/70">
            Readiness
          </span>
          <span
            className="text-[11px] font-semibold tabular-nums"
            style={{ color: pair.color }}
          >
            {readinessPercent}%
          </span>
        </div>
        <Progress
          value={readinessPercent}
          className="h-1.5"
          aria-label={`${pair.avatarName} readiness: ${readinessPercent}%`}
        />
      </div>

      {/* Hover border highlight overlay */}
      <div
        className="pointer-events-none absolute inset-0 rounded-xl opacity-0 transition-opacity duration-300 group-hover:opacity-100"
        style={{
          boxShadow: `inset 0 0 0 1px ${pair.color}25`,
        }}
        aria-hidden="true"
      />
    </motion.article>
  );
}
