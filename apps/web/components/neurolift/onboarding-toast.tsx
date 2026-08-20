"use client";

import { useEffect } from "react";
import { toast } from "sonner";

const VISITED_KEY = "neurolift-visited";

export function OnboardingToast() {
  useEffect(() => {
    if (typeof window === "undefined") return;
    if (localStorage.getItem(VISITED_KEY)) return;

    const timer = setTimeout(() => {
      toast("Welcome to NeuroLift AI Fusion! 🧠", {
        description:
          "Explore the 19 Avatar-Aide pairs, try the Fusion Simulator, or press ? for keyboard shortcuts.",
        duration: 8000,
        action: {
          label: "Dismiss",
          onClick: () => {},
        },
      });
      localStorage.setItem(VISITED_KEY, "1");
    }, 2000);

    return () => clearTimeout(timer);
  }, []);

  return null;
}
