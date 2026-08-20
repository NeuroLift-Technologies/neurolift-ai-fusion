"use client";

import { motion } from "framer-motion";
import { Lightbulb } from "lucide-react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from "@/components/ui/dialog";

interface KeyboardShortcutsDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

interface ShortcutEntry {
  keys: string[];
  description: string;
}

interface ShortcutGroup {
  title: string;
  shortcuts: ShortcutEntry[];
}

const SHORTCUT_GROUPS: ShortcutGroup[] = [
  {
    title: "Navigation",
    shortcuts: [
      { keys: ["?", "/"], description: "Toggle this dialog" },
      { keys: ["Home"], description: "Scroll to Overview" },
      { keys: ["1", "-", "5"], description: "Jump to section (1=Overview, 2=Pipeline, 3=Simulator, 4=Pairs, 5=Stats)" },
      { keys: ["Esc"], description: "Close dialog / Close detail sheet" },
    ],
  },
  {
    title: "Pairs Grid",
    shortcuts: [
      { keys: ["←", "→", "↑", "↓"], description: "Navigate between pair cards" },
      { keys: ["Enter", "/", "Space"], description: "Open selected pair details" },
      { keys: ["/"], description: "Focus search input" },
      { keys: ["R"], description: "Open random pair" },
      { keys: ["C"], description: "Open compare dialog" },
      { keys: ["E"], description: "Export summary" },
      { keys: ["F"], description: "Toggle favorites filter" },
    ],
  },
  {
    title: "Detail Sheet",
    shortcuts: [
      { keys: ["←", "→"], description: "Previous / Next pair" },
      { keys: ["Esc"], description: "Close detail sheet" },
      { keys: ["S"], description: "Share pair URL" },
    ],
  },
];

function Kbd({ children }: { children: React.ReactNode }) {
  return (
    <kbd className="bg-muted text-foreground font-mono text-xs px-2 py-1 rounded-md border border-border">
      {children}
    </kbd>
  );
}

export function KeyboardShortcutsDialog({
  open,
  onOpenChange,
}: KeyboardShortcutsDialogProps) {
  // Close on Escape is handled by Radix Dialog natively

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>Keyboard Shortcuts</DialogTitle>
          <DialogDescription>
            Press{" "}
            <kbd className="bg-muted text-foreground font-mono text-xs px-2 py-1 rounded-md border border-border">
              ?
            </kbd>{" "}
            to toggle this dialog
          </DialogDescription>
        </DialogHeader>

        <motion.div
          className="space-y-5 mt-1"
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.25, ease: "easeOut" }}
        >
          {SHORTCUT_GROUPS.map((group) => (
            <div key={group.title}>
              <h3 className="text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-2">
                {group.title}
              </h3>
              <div className="space-y-2">
                {group.shortcuts.map((shortcut) => (
                  <div
                    key={`${group.title}-${shortcut.description}`}
                    className="flex items-center justify-between gap-4"
                  >
                    <div className="flex items-center gap-1 shrink-0">
                      {shortcut.keys.map((key, i) => (
                        <span key={i} className="contents">
                          <Kbd>{key}</Kbd>
                          {i < shortcut.keys.length - 1 && (
                            <span className="text-muted-foreground text-xs mx-0.5">
                              ,
                            </span>
                          )}
                        </span>
                      ))}
                    </div>
                    <span className="text-sm text-foreground/80">
                      {shortcut.description}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          ))}

          {/* Pro Tip */}
          <div className="mt-4 pt-4 border-t border-border flex items-start gap-2">
            <Lightbulb className="h-4 w-4 shrink-0 text-amber-500 mt-0.5" />
            <p className="text-xs text-muted-foreground">
              Tip: Use arrow keys to navigate between pairs when viewing details. Swipe left/right on mobile.
            </p>
          </div>
        </motion.div>
      </DialogContent>
    </Dialog>
  );
}
