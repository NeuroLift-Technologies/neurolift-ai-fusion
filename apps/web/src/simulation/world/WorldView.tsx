"use client";

import { useEffect, useRef, useState } from "react";
import type { PointerEvent } from "react";

import type { Furniture, Room, SimSummary, WorldState } from "./types";
import { minimumNeed, simColor, simPosition } from "./useWorldPolling";

interface WorldViewProps {
  state: WorldState | null;
  selectedSimId: string | null;
  onSelectSim: (sim: SimSummary) => void;
  className?: string;
}

interface Layout {
  cellSize: number;
  originX: number;
  originY: number;
  cols: number;
  rows: number;
}

interface SimFrame {
  x: number;
  y: number;
  heading: number;
}

interface LerpState {
  from: Map<string, { x: number; y: number }>;
  to: Map<string, { x: number; y: number }>;
  start: number;
  duration: number;
}

const ROOM_COLORS: Record<string, string> = {
  bedroom: "hsl(210, 40%, 88%)",
  kitchen: "hsl(40, 50%, 88%)",
  living_room: "hsl(150, 30%, 88%)",
  bathroom: "hsl(190, 50%, 88%)",
  office: "hsl(260, 30%, 88%)",
};

function roomColor(name: string): string {
  if (ROOM_COLORS[name]) return ROOM_COLORS[name];
  let hash = 0;
  for (let i = 0; i < name.length; i++) hash = (hash * 29 + name.charCodeAt(i)) | 0;
  const h = Math.abs(hash) % 360;
  return `hsl(${h}, 35%, 88%)`;
}

function furnitureFillColor(type: string): string {
  switch (type) {
    case "bed":
      return "hsl(220, 70%, 68%)";
    case "couch":
      return "hsl(25, 55%, 50%)";
    case "stove":
      return "hsl(0, 0%, 55%)";
    case "toilet":
      return "hsl(0, 0%, 95%)";
    case "computer":
      return "hsl(220, 20%, 18%)";
    case "fridge":
      return "hsl(210, 20%, 92%)";
    case "shower":
      return "hsl(195, 60%, 80%)";
    case "door":
      return "hsl(30, 25%, 55%)";
    case "counter":
      return "hsl(0, 0%, 78%)";
    case "table":
      return "hsl(30, 45%, 52%)";
    default:
      return "hsl(0, 0%, 70%)";
  }
}

function computeLayout(
  cols: number,
  rows: number,
  width: number,
  height: number,
): Layout {
  const margin = 16;
  const availW = width - margin * 2;
  const availH = height - margin * 2;
  const cellSize = Math.floor(
    Math.min(availW / cols, availH / rows),
  );
  const gridW = cellSize * cols;
  const gridH = cellSize * rows;
  const originX = (width - gridW) / 2 + margin;
  const originY = (height - gridH) / 2 + margin;
  return { cellSize, originX, originY, cols, rows };
}

function lerp(a: number, b: number, t: number): number {
  return a + (b - a) * t;
}

function easeInOut(t: number): number {
  return t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
}

function cellCenter(
  gx: number,
  gy: number,
  layout: Layout,
): { cx: number; cy: number } {
  return {
    cx: layout.originX + (gx + 0.5) * layout.cellSize,
    cy: layout.originY + (gy + 0.5) * layout.cellSize,
  };
}

function roomBounds(room: Room): { minX: number; minY: number; maxX: number; maxY: number } | null {
  const cells: { x: number; y: number }[] = [];
  for (const f of room.furniture) {
    cells.push(f.position);
  }
  if (cells.length === 0) return null;
  let minX = Infinity;
  let minY = Infinity;
  let maxX = -Infinity;
  let maxY = -Infinity;
  for (const c of cells) {
    if (c.x < minX) minX = c.x;
    if (c.y < minY) minY = c.y;
    if (c.x > maxX) maxX = c.x;
    if (c.y > maxY) maxY = c.y;
  }
  // Expand by one cell of padding so the room frame reads as a room.
  return {
    minX: Math.max(0, minX - 1),
    minY: Math.max(0, minY - 1),
    maxX: maxX + 1,
    maxY: maxY + 1,
  };
}

function drawRoom(
  ctx: CanvasRenderingContext2D,
  room: Room,
  layout: Layout,
): void {
  const bounds = roomBounds(room);
  if (!bounds) return;

  const x = layout.originX + bounds.minX * layout.cellSize;
  const y = layout.originY + bounds.minY * layout.cellSize;
  const w = (bounds.maxX - bounds.minX + 1) * layout.cellSize;
  const h = (bounds.maxY - bounds.minY + 1) * layout.cellSize;

  const radius = Math.max(4, layout.cellSize * 0.12);
  const color = roomColor(room.name);

  ctx.fillStyle = color;
  roundRect(ctx, x, y, w, h, radius, true, false);
  ctx.fill();
  ctx.strokeStyle = "hsl(224 32% 85%)";
  ctx.lineWidth = Math.max(1, layout.cellSize * 0.05);
  roundRect(ctx, x, y, w, h, radius, false, true);
  ctx.stroke();

  const labelX = x + Math.max(6, layout.cellSize * 0.25);
  const labelY = y + Math.max(6, layout.cellSize * 0.35);
  ctx.fillStyle = "hsl(224 32% 28%)";
  ctx.font = `bold ${Math.max(10, layout.cellSize * 0.35)}px ui-monospace, monospace`;
  ctx.textBaseline = "top";
  ctx.fillText(room.name, labelX, labelY);
}

function drawFurniture(
  ctx: CanvasRenderingContext2D,
  furniture: Furniture,
  layout: Layout,
): void {
  const center = cellCenter(
    furniture.position.x,
    furniture.position.y,
    layout,
  );
  const cs = layout.cellSize;
  const fill = furnitureFillColor(furniture.furniture_type);

  ctx.save();
  ctx.translate(center.cx, center.cy);

  const outer = cs * 0.55;
  const inner = cs * 0.32;

  switch (furniture.furniture_type) {
    case "bed": {
      const w = cs * 0.8;
      const h = cs * 0.42;
      ctx.fillStyle = fill;
      roundRect(ctx, -w / 2, -h / 2, w, h, Math.max(3, cs * 0.08), true, false);
      ctx.fill();
      ctx.strokeStyle = "hsla(0,0%,20%,0.4)";
      ctx.lineWidth = Math.max(1, cs * 0.06);
      roundRect(ctx, -w / 2, -h / 2, w, h, Math.max(3, cs * 0.08), false, true);
      ctx.stroke();
      break;
    }
    case "couch": {
      const w = cs * 0.75;
      const h = cs * 0.32;
      ctx.fillStyle = fill;
      roundRect(ctx, -w / 2, -h / 2, w, h, cs * 0.06, true, false);
      ctx.fill();
      ctx.strokeStyle = "hsla(0,0%,20%,0.4)";
      ctx.lineWidth = Math.max(1, cs * 0.06);
      roundRect(ctx, -w / 2, -h / 2, w, h, cs * 0.06, false, true);
      ctx.stroke();
      // L-shaped arm: a second perpendicular cushion forming the L-shape
      const aw = cs * 0.28;
      const ah = cs * 0.32;
      roundRect(ctx, -w / 2, -h / 2, aw, ah, cs * 0.06, true, false);
      ctx.fillStyle = "hsla(0,0%,100%,0.28)";
      ctx.fill();
      break;
    }
    case "toilet": {
      ctx.fillStyle = fill;
      ctx.beginPath();
      ctx.arc(0, 0, inner * 0.38, 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = "hsla(0,0%,20%,0.4)";
      ctx.lineWidth = Math.max(1, cs * 0.06);
      ctx.stroke();
      break;
    }
    case "stove":
    case "shower": {
      ctx.fillStyle = fill;
      roundRect(ctx, -inner / 2, -inner / 2, inner, inner, cs * 0.08, true, false);
      ctx.fill();
      ctx.strokeStyle = "hsla(0,0%,20%,0.4)";
      ctx.lineWidth = Math.max(1, cs * 0.06);
      roundRect(ctx, -inner / 2, -inner / 2, inner, inner, cs * 0.08, false, true);
      ctx.stroke();
      if (furniture.furniture_type === "shower") {
        ctx.strokeStyle = "hsla(195,60%,80%,0.55)";
        ctx.setLineDash([2, 2]);
        ctx.lineWidth = Math.max(1, cs * 0.06);
        ctx.beginPath();
        ctx.arc(0, 0, inner * 0.5, 0, Math.PI * 2);
        ctx.stroke();
        ctx.setLineDash([]);
      }
      break;
    }
    case "computer": {
      const deskW = cs * 0.7;
      const deskH = cs * 0.36;
      ctx.fillStyle = fill;
      roundRect(ctx, -deskW / 2, -deskH / 2, deskW, deskH, cs * 0.06, true, false);
      ctx.fill();
      ctx.strokeStyle = "hsla(0,0%,20%,0.4)";
      ctx.lineWidth = Math.max(1, cs * 0.06);
      roundRect(ctx, -deskW / 2, -deskH / 2, deskW, deskH, cs * 0.06, false, true);
      ctx.stroke();
      // screen
      const sw = cs * 0.42;
      const sh = cs * 0.2;
      ctx.fillStyle = "hsl(0, 0%, 14%)";
      roundRect(ctx, -sw / 2, -deskH / 2 - sh - cs * 0.04, sw, sh, cs * 0.04, true, false);
      ctx.fill();
      ctx.strokeStyle = "hsla(0,0%,100%,0.2)";
      ctx.lineWidth = Math.max(1, cs * 0.04);
      roundRect(ctx, -sw / 2, -deskH / 2 - sh - cs * 0.04, sw, sh, cs * 0.04, false, true);
      ctx.stroke();
      break;
    }
    case "door": {
      const dw = cs * 0.22;
      const dh = cs * 0.5;
      ctx.fillStyle = fill;
      roundRect(ctx, -dw / 2, -dh / 2, dw, dh, cs * 0.05, true, false);
      ctx.fill();
      break;
    }
    default: {
      ctx.fillStyle = fill;
      roundRect(ctx, -inner / 2, -inner / 2, inner, inner, cs * 0.08, true, false);
      ctx.fill();
      ctx.strokeStyle = "hsla(0,0%,20%,0.4)";
      ctx.lineWidth = Math.max(1, cs * 0.06);
      roundRect(ctx, -inner / 2, -inner / 2, inner, inner, cs * 0.08, false, true);
      ctx.stroke();
    }
  }

  // Affordance hint — show a small dot when a Sim is using it.
  if (furniture.in_use_by) {
    ctx.fillStyle = "hsl(130, 70%, 55%)";
    ctx.beginPath();
    ctx.arc(outer / 2 - cs * 0.1, -outer / 2 + cs * 0.1, cs * 0.1, 0, Math.PI * 2);
    ctx.fill();
  }

  ctx.restore();
}

function drawSim(
  ctx: CanvasRenderingContext2D,
  sim: SimSummary,
  frame: SimFrame,
  selected: boolean,
  layout: Layout,
): void {
  const { cx, cy } = cellCenter(frame.x, frame.y, layout);
  const cs = layout.cellSize;
  const r = Math.max(5, cs * 0.28);

  // Needs meter above the Sim.
  const needLevel = minimumNeed(sim.needs_summary);
  const barW = cs * 0.8;
  const barH = Math.max(3, cs * 0.12);
  const barX = cx - barW / 2;
  const barY = cy - r - cs * 0.22 - barH;

  ctx.fillStyle = "hsla(0,0%,95%,0.7)";
  ctx.fillRect(barX, barY, barW, barH);
  ctx.fillStyle = needColor(needLevel);
  ctx.fillRect(barX, barY, barW * (needLevel / 100), barH);
  ctx.strokeStyle = "hsla(0,0%,25%,0.55)";
  ctx.lineWidth = Math.max(1, cs * 0.05);
  ctx.strokeRect(barX, barY, barW, barH);

  // Direction indicator — a small triangle pointing the heading.
  const indicatorLen = r * 0.8;
  const p1 = polarToCartesian(cx, cy, r + cs * 0.08, frame.heading);
  const p2 = polarToCartesian(cx, cy, r + cs * 0.08, frame.heading + 2.3);
  const p3 = polarToCartesian(cx, cy, r + cs * 0.08, frame.heading - 2.3);

  // Sim body.
  ctx.fillStyle = simColor(sim.sim_id);
  ctx.beginPath();
  ctx.arc(cx, cy, r, 0, Math.PI * 2);
  ctx.fill();
  ctx.strokeStyle = selected ? "hsl(45, 100%, 55%)" : "hsla(0,0%,0%,0.6)";
  ctx.lineWidth = Math.max(2, cs * 0.1);
  ctx.stroke();

  // Direction triangle.
  ctx.fillStyle = "hsla(0,0%,100%,0.9)";
  ctx.beginPath();
  ctx.moveTo(p1.x, p1.y);
  ctx.lineTo(p2.x, p2.y);
  ctx.lineTo(p3.x, p3.y);
  ctx.closePath();
  ctx.fill();

  // Name below.
  ctx.fillStyle = "hsl(224 32% 22%)";
  ctx.font = `bold ${Math.max(9, cs * 0.32)}px ui-sans, system-ui, sans-serif`;
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  ctx.fillText(sim.name, cx, cy + r + cs * 0.28);
}

function needColor(value: number): string {
  if (value < 30) return "hsl(0, 75%, 58%)";
  if (value < 55) return "hsl(40, 85%, 52%)";
  return "hsl(140, 60%, 50%)";
}

function polarToCartesian(
  cx: number,
  cy: number,
  radius: number,
  angle: number,
): { x: number; y: number } {
  return {
    x: cx + radius * Math.cos(angle),
    y: cy + radius * Math.sin(angle),
  };
}

// Draw a rounded rectangle path then optionally fill/stroke it.
function roundRect(
  ctx: CanvasRenderingContext2D,
  x: number,
  y: number,
  w: number,
  h: number,
  radius: number,
  doFill: boolean,
  doStroke: boolean,
): void {
  const r = Math.min(radius, Math.min(w, h) / 2);
  ctx.beginPath();
  ctx.moveTo(x + r, y);
  ctx.lineTo(x + w - r, y);
  ctx.quadraticCurveTo(x + w, y, x + w, y + r);
  ctx.lineTo(x + w, y + h - r);
  ctx.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
  ctx.lineTo(x + r, y + h);
  ctx.quadraticCurveTo(x, y + h, x, y + h - r);
  ctx.lineTo(x, y + r);
  ctx.quadraticCurveTo(x, y, x + r, y);
  ctx.closePath();
  if (doFill) ctx.fill();
  if (doStroke) ctx.stroke();
}

export default function WorldView({
  state,
  selectedSimId,
  onSelectSim,
  className,
}: WorldViewProps) {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const containerRef = useRef<HTMLDivElement | null>(null);
  const frameIdRef = useRef<number>(0);
  const layoutRef = useRef<Layout>({
    cellSize: 0,
    originX: 0,
    originY: 0,
    cols: 20,
    rows: 20,
  });
  const dprRef = useRef(1);

  // Latest state snapshot (rooms/furniture are static between state updates;
  // sims animate via the lerp below).
  const latestStateRef = useRef<WorldState | null>(null);
  // Current animated sim frames.
  const simFramesRef = useRef<Map<string, SimFrame>>(new Map());
  // Previous sim positions (for direction + lerp source).
  const prevPositionsRef = useRef<Map<string, { x: number; y: number }>>(new Map());
  // Lerp bookkeeping.
  const lerpRef = useRef<LerpState>({
    from: new Map(),
    to: new Map(),
    start: 0,
    duration: 0,
  });
  const rafPendingRef = useRef(false);

  const [dimensions, setDimensions] = useState<{ w: number; h: number }>({
    w: 0,
    h: 0,
  });

  // Resize handling
  useEffect(() => {
    const el = containerRef.current;
    if (!el) return;
    const update = () => {
      const rect = el.getBoundingClientRect();
      setDimensions({ w: Math.round(rect.width), h: Math.round(rect.height) });
    };
    update();
    const ro = new ResizeObserver(update);
    ro.observe(el);
    return () => ro.disconnect();
  }, []);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;
    const dpr = typeof window !== "undefined" ? window.devicePixelRatio || 1 : 1;
    dprRef.current = dpr;
    canvas.width = dimensions.w * dpr;
    canvas.height = dimensions.h * dpr;
    ctx.scale(dpr, dpr);
    layoutRef.current = computeLayout(
      state?.config.grid_width ?? 20,
      state?.config.grid_height ?? 20,
      dimensions.w,
      dimensions.h,
    );
  }, [dimensions, state?.config.grid_width, state?.config.grid_height]);

  // Seed lerp whenever a new state arrives.
  useEffect(() => {
    if (!state || !state.sims) return;
    const prev = prevPositionsRef.current;
    const from = new Map<string, { x: number; y: number }>();
    const to = new Map<string, { x: number; y: number }>();
    const newFrames = new Map<string, SimFrame>();

    for (const sim of state.sims) {
      const pos = simPosition(sim);
      to.set(sim.sim_id, { ...pos });
      const p = prev.get(sim.sim_id);
      from.set(sim.sim_id, p ? { ...p } : { ...pos });

      // Heading from movement delta (fall back to "north").
      let heading = -Math.PI / 2;
      if (p) {
        const dx = pos.x - p.x;
        const dy = pos.y - p.y;
        if (Math.abs(dx) + Math.abs(dy) > 1e-6) {
          heading = Math.atan2(dy, dx);
        } else {
          const old = simFramesRef.current.get(sim.sim_id);
          if (old) heading = old.heading;
        }
      }
      newFrames.set(sim.sim_id, { x: pos.x, y: pos.y, heading });
    }

    lerpRef.current = {
      from,
      to,
      start: performance.now(),
      duration: 420,
    };
    simFramesRef.current = newFrames;
    prevPositionsRef.current = new Map(to);
    latestStateRef.current = state;
    rafPendingRef.current = false;
    scheduleFrame();
  }, [state]);

  function scheduleFrame() {
    if (!rafPendingRef.current) {
      rafPendingRef.current = true;
      frameIdRef.current = requestAnimationFrame(renderFrame);
    }
  }

  function renderFrame(now: number) {
    rafPendingRef.current = false;
    const canvas = canvasRef.current;
    const ctx = canvas?.getContext("2d");
    if (!canvas || !ctx) return;

    const layout = layoutRef.current;
    const w = canvas.width / dprRef.current;
    const h = canvas.height / dprRef.current;

    // Clear
    ctx.fillStyle = "hsl(224 32% 97%)";
    ctx.fillRect(0, 0, w, h);

    if (!layout.cellSize || layout.cellSize <= 0) {
      return;
    }

    // Subtle grid
    ctx.strokeStyle = "hsl(224 32% 92%)";
    ctx.lineWidth = 1;
    ctx.setLineDash([1, Math.max(2, layout.cellSize * 0.3)]);
    ctx.beginPath();
    for (let i = 0; i <= layout.cols; i++) {
      const x = layout.originX + i * layout.cellSize;
      ctx.moveTo(x, layout.originY);
      ctx.lineTo(x, layout.originY + layout.rows * layout.cellSize);
    }
    for (let j = 0; j <= layout.rows; j++) {
      const y = layout.originY + j * layout.cellSize;
      ctx.moveTo(layout.originX, y);
      ctx.lineTo(layout.originX + layout.cols * layout.cellSize, y);
    }
    ctx.stroke();
    ctx.setLineDash([]);

    const currentState = latestStateRef.current;
    if (currentState) {
      for (const room of currentState.rooms) {
        drawRoom(ctx, room, layout);
      }
      for (const room of currentState.rooms) {
        for (const furniture of room.furniture) {
          drawFurniture(ctx, furniture, layout);
        }
      }
      // Draw entities (non-room-tagged) furniture too — usually none extra.
    }

    // Interpolated sim frames
    const lerpState = lerpRef.current;
    // Only keep the animation loop alive while a transition is in flight;
    // defaulting to true here caused an idle ~60fps redraw loop.
    let progressed = false;
    if (lerpState.duration > 0 && currentState) {
      const elapsed = now - lerpState.start;
      const t = Math.min(1, elapsed / lerpState.duration);
      const p = easeInOut(t);
      progressed = t < 1;

      for (const sim of currentState.sims) {
        const to = lerpState.to.get(sim.sim_id);
        const from = lerpState.from.get(sim.sim_id);
        if (!to) continue;
        const frame: SimFrame = simFramesRef.current.get(sim.sim_id) ?? {
          x: to.x,
          y: to.y,
          heading: -Math.PI / 2,
        };
        if (from) {
          frame.x = lerp(from.x, to.x, p);
          frame.y = lerp(from.y, to.y, p);
        } else {
          frame.x = to.x;
          frame.y = to.y;
        }
        simFramesRef.current.set(sim.sim_id, frame);
      }
    }

    if (currentState) {
      for (const sim of currentState.sims) {
        const frame = simFramesRef.current.get(sim.sim_id);
        if (!frame) continue;
        drawSim(ctx, sim, frame, sim.sim_id === selectedSimId, layout);
      }
    }

    if (progressed) {
      scheduleFrame();
    }
  }

  // Redraw once whenever dimensions change (first paint / resize) — the
  // state-seeding effect schedules frames when new snapshots arrive.
  useEffect(() => {
    scheduleFrame();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [dimensions]);

  // Cancel any in-flight animation frame on unmount.
  useEffect(() => {
    return () => {
      if (frameIdRef.current) {
        cancelAnimationFrame(frameIdRef.current);
        rafPendingRef.current = false;
      }
    };
  }, []);

  // Click → hit test the nearest Sim (using target positions from latest state).
  function handlePointerDown(e: PointerEvent<HTMLDivElement>) {
    const sims = latestStateRef.current?.sims;
    if (!sims || sims.length === 0) return;
    const canvas = canvasRef.current;
    if (!canvas) return;
    const rect = canvas.getBoundingClientRect();
    const px = e.clientX - rect.left;
    const py = e.clientY - rect.top;
    const layout = layoutRef.current;
    if (!layout.cellSize || layout.cellSize <= 0) return;

    let best: { sim: SimSummary; dist: number } | null = null;
    for (const sim of sims) {
      const center = cellCenter(sim.position.x, sim.position.y, layout);
      const dist = Math.hypot(center.cx - px, center.cy - py);
      if (!best || dist < best.dist) best = { sim, dist };
    }
    if (best && best.dist <= Math.max(24, layout.cellSize * 0.7)) {
      onSelectSim(best.sim);
    }
  }

  return (
    <div
      ref={containerRef}
      className={className}
      onPointerDown={handlePointerDown}
      style={{ width: "100%", height: "100%", touchAction: "none", cursor: "crosshair" }}
    >
      <canvas
        ref={canvasRef}
        width={dimensions.w}
        height={dimensions.h}
        style={{ display: "block", width: "100%", height: "100%" }}
      />
      {state && state.sims && state.sims.length === 0 && (
        <div className="absolute inset-0 flex items-center justify-center text-sm text-muted-foreground">
          No Sims in the world yet.
        </div>
      )}
    </div>
  );
}
