"use client";

import { useState, useEffect, useCallback } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { ArrowUp } from "lucide-react";

// ─── Constants ───────────────────────────────────────────────────────
const SCROLL_THRESHOLD = 400;
const BRAND_COLOR = "#F38020";
const BUTTON_SIZE = 44; // px
const STROKE_WIDTH = 3;
const RING_RADIUS = (BUTTON_SIZE - STROKE_WIDTH) / 2;
const RING_CIRCUMFERENCE = 2 * Math.PI * RING_RADIUS;

// ─── Component ───────────────────────────────────────────────────────
export function BackToTop() {
  const [visible, setVisible] = useState(false);
  const [scrollProgress, setScrollProgress] = useState(0);

  // Track scroll position and compute progress
  useEffect(() => {
    function handleScroll() {
      const scrollTop = window.scrollY;
      const docHeight = document.documentElement.scrollHeight - window.innerHeight;

      setVisible(scrollTop > SCROLL_THRESHOLD);

      if (docHeight > 0) {
        const raw = Math.min(scrollTop / docHeight, 1);
        setScrollProgress(raw);
      }
    }

    window.addEventListener("scroll", handleScroll, { passive: true });
    handleScroll(); // initial check
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const scrollToTop = useCallback(() => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  }, []);

  // SVG dash offset for the circular progress ring
  const dashOffset = RING_CIRCUMFERENCE * (1 - scrollProgress);

  return (
    <AnimatePresence>
      {visible && (
        <motion.button
          initial={{ opacity: 0, scale: 0.6, y: 12 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          exit={{ opacity: 0, scale: 0.6, y: 12 }}
          transition={{ type: "spring", stiffness: 400, damping: 25 }}
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.95 }}
          onClick={scrollToTop}
          aria-label="Back to top"
          className={
            "fixed bottom-6 right-6 z-40 flex items-center justify-center rounded-full shadow-lg transition-shadow duration-200 hover:shadow-xl focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-orange-500/50"
          }
          style={{
            width: BUTTON_SIZE,
            height: BUTTON_SIZE,
            backgroundColor: BRAND_COLOR,
          }}
        >
          {/* Circular progress ring */}
          <svg
            className="pointer-events-none absolute inset-0"
            width={BUTTON_SIZE}
            height={BUTTON_SIZE}
            style={{ transform: "rotate(-90deg)" }}
            aria-hidden="true"
          >
            {/* Background ring */}
            <circle
              cx={BUTTON_SIZE / 2}
              cy={BUTTON_SIZE / 2}
              r={RING_RADIUS}
              fill="none"
              stroke="rgba(255,255,255,0.25)"
              strokeWidth={STROKE_WIDTH}
            />
            {/* Progress ring */}
            <circle
              cx={BUTTON_SIZE / 2}
              cy={BUTTON_SIZE / 2}
              r={RING_RADIUS}
              fill="none"
              stroke="white"
              strokeWidth={STROKE_WIDTH}
              strokeLinecap="round"
              strokeDasharray={RING_CIRCUMFERENCE}
              strokeDashoffset={dashOffset}
              style={{ transition: "stroke-dashoffset 0.15s ease-out" }}
            />
          </svg>
          <ArrowUp className="h-5 w-5 text-white" strokeWidth={2.5} />
        </motion.button>
      )}
    </AnimatePresence>
  );
}
