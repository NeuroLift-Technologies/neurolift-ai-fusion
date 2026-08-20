"use client";

import { useState, useCallback, useEffect } from "react";
import dynamic from "next/dynamic";
import { Loader2, Heart, Download, Eye } from "lucide-react";
import { toast } from "sonner";
import { NavHeader } from "@/components/neurolift/nav-header";
import { HeroSection } from "@/components/neurolift/hero-section";
import { PipelineSection } from "@/components/neurolift/pipeline-section";
import { PairsGrid } from "@/components/neurolift/pairs-grid";
import StatsFooter from "@/components/neurolift/stats-footer";
import { BackToTop } from "@/components/neurolift/back-to-top";
import { OnboardingToast } from "@/components/neurolift/onboarding-toast";
import { PAIRS, type AvatarAidePair } from "@/lib/avatar-pairs-data";

// ── Inline skeleton for lazy-loaded component fallbacks ──
function SectionSkeleton() {
  return (
    <div className="min-h-[200px] animate-pulse rounded-2xl bg-muted/30 flex items-center justify-center">
      <Loader2 className="h-6 w-6 animate-spin text-muted-foreground/50" />
    </div>
  );
}

// ── Lazy-loaded heavy components (code-split via next/dynamic) ──
const FusionSimulator = dynamic(
  () => import("@/components/neurolift/fusion-simulator").then((m) => ({ default: m.FusionSimulator })),
  { loading: () => <SectionSkeleton />, ssr: false },
);

const PairDetailSheet = dynamic(
  () => import("@/components/neurolift/pair-detail-sheet").then((m) => ({ default: m.PairDetailSheet })),
  { loading: () => <SectionSkeleton />, ssr: false },
);

const PairComparisonDialog = dynamic(
  () => import("@/components/neurolift/pair-comparison-dialog").then((m) => ({ default: m.PairComparisonDialog })),
  { loading: () => <SectionSkeleton />, ssr: false },
);

const KeyboardShortcutsDialog = dynamic(
  () => import("@/components/neurolift/keyboard-shortcuts-dialog").then((m) => ({ default: m.KeyboardShortcutsDialog })),
  { loading: () => <SectionSkeleton />, ssr: false },
);

export default function HomePage() {
  const [selectedPair, setSelectedPair] = useState<AvatarAidePair | null>(null);
  const [sheetOpen, setSheetOpen] = useState(false);
  const [compareOpen, setCompareOpen] = useState(false);
  const [shortcutsOpen, setShortcutsOpen] = useState(false);

  // ── URL deep linking: read ?pair=ID on mount ──
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const pairId = params.get("pair");
    if (pairId) {
      const id = parseInt(pairId, 10);
      const pair = PAIRS.find((p) => p.id === id);
      if (pair) {
        requestAnimationFrame(() => {
          setSelectedPair(pair);
          setSheetOpen(true);
        });
      }
    }
  }, []);

  // ── Global ? key to toggle keyboard shortcuts dialog ──
  useEffect(() => {
    function handleKeyDown(e: KeyboardEvent) {
      // Ignore when typing in inputs/textareas
      const tag = (e.target as HTMLElement).tagName;
      if (tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT") return;
      if (e.key === "?") {
        e.preventDefault();
        setShortcutsOpen((prev) => !prev);
      }
    }
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, []);

  // ── Escape key to close detail sheet (when no dialog is open) ──
  useEffect(() => {
    if (!sheetOpen) return;
    function handleEscape(e: KeyboardEvent) {
      const tag = (e.target as HTMLElement).tagName;
      if (tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT") return;
      if (e.key === "Escape" && !shortcutsOpen && !compareOpen) {
        setSheetOpen(false);
      }
    }
    window.addEventListener("keydown", handleEscape);
    return () => window.removeEventListener("keydown", handleEscape);
  }, [sheetOpen, shortcutsOpen, compareOpen]);

  // Toast callbacks for PairsGrid actions
  const handleFavoriteToast = useCallback((pairName: string, isFavorited: boolean) => {
    toast(isFavorited ? "Added to favorites" : "Removed from favorites", {
      description: pairName,
      action: { label: <Heart className="h-4 w-4" />, onClick: () => {} },
      duration: 2500,
    });
  }, []);

  const handleExportToast = useCallback(() => {
    toast("Summary exported successfully", {
      description: "neurolift-pairs-summary.md downloaded",
      action: { label: <Download className="h-4 w-4" />, onClick: () => {} },
      duration: 2500,
    });
  }, []);

  const handleSelectPair = useCallback((pair: AvatarAidePair) => {
    setSelectedPair(pair);
    setSheetOpen(true);
    toast(`Viewing: ${pair.avatarName}`, {
      description: `${pair.aideName} · ${pair.advocateName}`,
      action: { label: <Eye className="h-4 w-4" />, onClick: () => {} },
      duration: 2500,
    });
    // Update URL with ?pair=ID (no navigation)
    const url = new URL(window.location.href);
    url.searchParams.set("pair", String(pair.id));
    window.history.replaceState(null, "", url.toString());
  }, []);

  const handleNavigate = useCallback(
    (direction: "prev" | "next") => {
      if (!selectedPair) return;
      const idx = PAIRS.findIndex((p) => p.id === selectedPair.id);
      if (idx === -1) return;
      const nextIdx =
        direction === "prev"
          ? idx - 1 < 0
            ? PAIRS.length - 1
            : idx - 1
          : idx + 1 >= PAIRS.length
            ? 0
            : idx + 1;
      const nextPair = PAIRS[nextIdx];
      setSelectedPair(nextPair);
      // Update URL for navigated pair
      const url = new URL(window.location.href);
      url.searchParams.set("pair", String(nextPair.id));
      window.history.replaceState(null, "", url.toString());
    },
    [selectedPair],
  );

  // ── Arrow key navigation when detail sheet is open ──
  useEffect(() => {
    if (!sheetOpen) return;
    function handleArrowKey(e: KeyboardEvent) {
      const tag = (e.target as HTMLElement).tagName;
      if (tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT") return;
      if (e.key === "ArrowLeft") {
        e.preventDefault();
        handleNavigate("prev");
      } else if (e.key === "ArrowRight") {
        e.preventDefault();
        handleNavigate("next");
      }
    }
    window.addEventListener("keydown", handleArrowKey);
    return () => window.removeEventListener("keydown", handleArrowKey);
  }, [sheetOpen, handleNavigate]);

  const handleSheetChange = useCallback((open: boolean) => {
    setSheetOpen(open);
    if (!open) {
      // Remove ?pair=ID from URL when sheet closes
      const url = new URL(window.location.href);
      url.searchParams.delete("pair");
      window.history.replaceState(null, "", url.toString());
      // Small delay so the close animation finishes before clearing
      setTimeout(() => setSelectedPair(null), 300);
    }
  }, []);

  return (
    <div className="min-h-screen flex flex-col">
      <a href="#main-content" className="skip-link">
        Skip to content
      </a>
      <NavHeader onOpenShortcuts={() => setShortcutsOpen(true)} />

      {/* Hero */}
      <main id="main-content">
        <HeroSection />

        <div className="section-divider section-divider-animated" aria-hidden="true"><div className="section-divider-icon" /><span className="divider-flow-dot" /></div>

        {/* Fusion Pipeline Explanation */}
        <PipelineSection />

        <div className="section-divider section-divider-animated" aria-hidden="true"><div className="section-divider-icon" /><span className="divider-flow-dot" /></div>

        {/* Fusion Simulator */}
        <FusionSimulator />

        <div className="section-divider section-divider-animated" aria-hidden="true"><div className="section-divider-icon" /><span className="divider-flow-dot" /></div>

        {/* Pairs Grid */}
        <PairsGrid onSelectPair={handleSelectPair} onOpenCompare={() => setCompareOpen(true)} onFavoriteToast={handleFavoriteToast} onExportToast={handleExportToast} />

        <div className="section-divider section-divider-animated" aria-hidden="true"><div className="section-divider-icon" /><span className="divider-flow-dot" /></div>

        {/* Stats Overview */}
        <StatsFooter />
      </main>

      {/* Pair Detail Sheet */}
      <PairDetailSheet
        pair={selectedPair}
        open={sheetOpen}
        onOpenChange={handleSheetChange}
        onNavigate={handleNavigate}
      />

      {/* Pair Comparison Dialog */}
      <PairComparisonDialog open={compareOpen} onOpenChange={setCompareOpen} />

      {/* Keyboard Shortcuts Dialog */}
      <KeyboardShortcutsDialog open={shortcutsOpen} onOpenChange={setShortcutsOpen} />

      {/* Back-to-Top floating button */}
      <BackToTop />

      {/* First-visit onboarding toast */}
      <OnboardingToast />
    </div>
  );
}
