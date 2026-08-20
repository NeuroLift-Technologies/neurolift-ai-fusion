"use client";

import { useState, useEffect, useCallback, useRef } from "react";
import { useTheme } from "next-themes";
import { Sun, Moon, Menu } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Sheet,
  SheetTrigger,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetClose,
} from "@/components/ui/sheet";
import { cn } from "@/lib/utils";

const NAV_LINKS = [
  { label: "Overview", href: "overview" },
  { label: "Pipeline", href: "pipeline" },
  { label: "Simulator", href: "simulator" },
  { label: "Pairs", href: "pairs" },
  { label: "Stats", href: "stats" },
] as const;

interface NavHeaderProps {
  onOpenShortcuts?: () => void;
}

export function NavHeader({ onOpenShortcuts }: NavHeaderProps) {
  const { theme, setTheme } = useTheme();
  const [scrolled, setScrolled] = useState(false);
  const [activeSection, setActiveSection] = useState("overview");
  const [mobileOpen, setMobileOpen] = useState(false);
  const [mounted, setMounted] = useState(false);
  const navRef = useRef<HTMLElement>(null);

  // Hydration guard for theme
  useEffect(() => {
    requestAnimationFrame(() => setMounted(true));
  }, []);

  // Scroll listener — transparent → solid after 50px + border opacity intensification
  useEffect(() => {
    function handleScroll() {
      setScrolled(window.scrollY > 50);
      const borderOpacity = Math.min(window.scrollY / 100, 1) * 0.7 + 0.3;
      navRef.current?.style.setProperty("--nav-border-opacity", String(borderOpacity));
    }
    handleScroll();
    window.addEventListener("scroll", handleScroll, { passive: true });
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  // IntersectionObserver for active section detection
  useEffect(() => {
    const sectionIds = NAV_LINKS.map((l) => l.href);
    const observers: IntersectionObserver[] = [];

    for (const id of sectionIds) {
      const el = document.getElementById(id);
      if (!el) continue;

      const observer = new IntersectionObserver(
        (entries) => {
          for (const entry of entries) {
            if (entry.isIntersecting) {
              setActiveSection(id);
            }
          }
        },
        { rootMargin: "-40% 0px -55% 0px", threshold: 0 }
      );

      observer.observe(el);
      observers.push(observer);
    }

    return () => observers.forEach((o) => o.disconnect());
  }, []);

  const scrollToSection = useCallback((href: string) => {
    const el = document.getElementById(href);
    if (el) {
      el.scrollIntoView({ behavior: "smooth" });
    }
    setMobileOpen(false);
  }, []);

  const toggleTheme = useCallback(() => {
    setTheme(theme === "dark" ? "light" : "dark");
  }, [theme, setTheme]);

  return (
    <header
      ref={navRef}
      className={cn(
        "fixed top-0 left-0 right-0 z-50 transition-all duration-300",
        scrolled
          ? "nav-scrolled border-b border-border shadow-sm"
          : "bg-transparent border-b border-transparent"
      )}
    >
      {/* Gradient accent line on scroll */}
      <div
        className="absolute bottom-0 left-0 right-0 h-[2px]"
        style={{
          background: `linear-gradient(90deg, transparent 0%, rgba(243,128,32,var(--nav-border-opacity, 0.3)) 50%, transparent 100%)`,
          width: scrolled ? '100%' : '0%',
          opacity: scrolled ? 1 : 0,
          transition: 'width 0.5s ease, opacity 0.3s ease',
        }}
        aria-hidden="true"
      />
      <nav
        className="mx-auto flex h-14 max-w-6xl items-center justify-between px-4 sm:px-6 lg:px-8"
        aria-label="Main navigation"
      >
        {/* Left: Logo */}
        <button
          onClick={() => scrollToSection("overview")}
          className="flex items-center gap-2 group"
          aria-label="Scroll to top"
        >
          <span
            className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full text-[11px] font-bold text-white"
            style={{ backgroundColor: "#F38020" }}
          >
            NL
          </span>
          <span className="text-sm font-semibold tracking-tight text-foreground/90 group-hover:text-foreground transition-colors">
            NeuroLift
          </span>
        </button>

        {/* Center: Desktop nav links */}
        <ul className="hidden md:flex items-center gap-1">
          {NAV_LINKS.map((link) => (
            <li key={link.href}>
              <button
                onClick={() => scrollToSection(link.href)}
                className={cn(
                  "relative px-3 py-1.5 text-sm font-medium transition-colors rounded-md",
                  activeSection === link.href
                    ? "text-foreground bg-orange-500/10"
                    : "text-muted-foreground hover:text-foreground/80 hover:bg-muted/50"
                )}
                aria-current={activeSection === link.href ? "page" : undefined}
              >
                {link.label}
                <span
                  className={cn(
                    "nav-active-indicator",
                    activeSection === link.href && "active"
                  )}
                  aria-hidden="true"
                />
              </button>
            </li>
          ))}
        </ul>

        {/* Right: Theme toggle + Mobile hamburger */}
        <div className="flex items-center gap-1">
          {/* Keyboard shortcuts button — desktop only */}
          {onOpenShortcuts && (
            <Button
              variant="ghost"
              size="icon"
              onClick={onOpenShortcuts}
              className="h-9 w-9 hidden md:flex"
              aria-label="Keyboard shortcuts"
            >
              <span className="text-xs font-bold">?</span>
            </Button>
          )}

          {/* Theme toggle — only render after mount to avoid hydration mismatch */}
          {mounted && (
            <Button
              variant="ghost"
              size="icon"
              onClick={toggleTheme}
              className="h-9 w-9"
              aria-label={theme === "dark" ? "Switch to light mode" : "Switch to dark mode"}
            >
              {theme === "dark" ? (
                <Sun className="h-4 w-4" />
              ) : (
                <Moon className="h-4 w-4" />
              )}
            </Button>
          )}

          {/* Mobile hamburger */}
          <Sheet open={mobileOpen} onOpenChange={setMobileOpen}>
            <SheetTrigger asChild>
              <Button
                variant="ghost"
                size="icon"
                className="h-9 w-9 md:hidden"
                aria-label="Open navigation menu"
              >
                <Menu className="h-4 w-4" />
              </Button>
            </SheetTrigger>
            <SheetContent side="right" className="w-64">
              <SheetHeader>
                <SheetTitle className="flex items-center gap-2">
                  <span
                    className="flex h-6 w-6 items-center justify-center rounded-full text-[10px] font-bold text-white"
                    style={{ backgroundColor: "#F38020" }}
                  >
                    NL
                  </span>
                  NeuroLift
                </SheetTitle>
              </SheetHeader>
              <nav className="flex flex-col gap-1 px-4 pt-2">
                {NAV_LINKS.map((link) => (
                  <SheetClose asChild key={link.href}>
                    <button
                      onClick={() => scrollToSection(link.href)}
                      className={cn(
                        "flex items-center rounded-md px-3 py-2.5 text-sm font-medium transition-colors text-left w-full",
                        activeSection === link.href
                          ? "bg-orange-500/10 text-foreground"
                          : "text-muted-foreground hover:bg-muted hover:text-foreground"
                      )}
                    >
                      {link.label}
                      {activeSection === link.href && (
                        <span
                          className="ml-auto h-1.5 w-1.5 rounded-full"
                          style={{ backgroundColor: "#F38020" }}
                        />
                      )}
                    </button>
                  </SheetClose>
                ))}
              </nav>
              <div className="mx-4 mt-2 border-t border-border" />
              {onOpenShortcuts && (
                <div className="px-4 pt-2">
                  <SheetClose asChild>
                    <button
                      onClick={onOpenShortcuts}
                      className="flex items-center gap-2 rounded-md px-3 py-2.5 text-sm font-medium transition-colors text-left w-full text-muted-foreground hover:bg-muted hover:text-foreground"
                    >
                      <span className="flex h-5 w-5 items-center justify-center rounded-md border border-border text-xs font-bold">?</span>
                      Keyboard Shortcuts
                    </button>
                  </SheetClose>
                </div>
              )}
            </SheetContent>
          </Sheet>
        </div>
      </nav>
    </header>
  );
}
