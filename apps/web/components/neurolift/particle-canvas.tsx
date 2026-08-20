"use client";

import { useEffect, useRef, useCallback } from "react";

const WARM_HEX_COLORS = ['#F38020', '#F59E0B', '#EA580C', '#FB923C', '#F97316'];

function hexToRgb(hex: string): [number, number, number] {
  const r = parseInt(hex.slice(1, 3), 16);
  const g = parseInt(hex.slice(3, 5), 16);
  const b = parseInt(hex.slice(5, 7), 16);
  return [r, g, b];
}

const WARM_COLORS_RGB = WARM_HEX_COLORS.map(hexToRgb);

function randomWarmColor(): [number, number, number] {
  return WARM_COLORS_RGB[Math.floor(Math.random() * WARM_COLORS_RGB.length)] as [number, number, number];
}

interface Particle {
  x: number;
  y: number;
  vx: number;
  vy: number;
  radius: number;
  opacity: number;
  color: [number, number, number];
}

const PARTICLE_COUNT = 50;
const CONNECTION_DISTANCE = 150;
const MOUSE_INFLUENCE_RADIUS = 120;
const MOUSE_PUSH_STRENGTH = 0.15;
const MOUSE_GLOW_RADIUS = 120;
const MOUSE_LINE_RADIUS = 100;

function createParticle(width: number, height: number): Particle {
  return {
    x: Math.random() * width,
    y: Math.random() * height,
    vx: (Math.random() - 0.5) * 0.35,
    vy: (Math.random() - 0.5) * 0.35,
    radius: 1.2 + Math.random() * 1.8,
    opacity: 0.05 + Math.random() * 0.2,
    color: randomWarmColor(),
  };
}

export function ParticleCanvas() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const animationRef = useRef<number>(0);
  const particlesRef = useRef<Particle[]>([]);
  const mouseRef = useRef({ x: -1000, y: -1000 });
  const sizeRef = useRef({ width: 0, height: 0 });

  const initParticles = useCallback((width: number, height: number) => {
    particlesRef.current = Array.from({ length: PARTICLE_COUNT }, () =>
      createParticle(width, height)
    );
  }, []);

  useEffect(() => {
    if (typeof window === "undefined") return;

    const canvas = canvasRef.current!;
    if (!canvas) return;

    const ctx = canvas.getContext("2d")!;
    if (!ctx) return;

    const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const dpr = window.devicePixelRatio || 1;

    function resize() {
      if (!canvas) return;
      const rect = canvas.parentElement?.getBoundingClientRect();
      if (!rect) return;

      const width = rect.width;
      const height = rect.height;

      canvas.width = width * dpr;
      canvas.height = height * dpr;
      canvas.style.width = `${width}px`;
      canvas.style.height = `${height}px`;

      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

      sizeRef.current = { width, height };

      if (particlesRef.current.length === 0) {
        initParticles(width, height);
        if (prefersReducedMotion) {
          for (const p of particlesRef.current) {
            p.vx = 0;
            p.vy = 0;
          }
        }
      }
    }

    function handleMouseMove(e: MouseEvent) {
      const rect = canvas.getBoundingClientRect();
      mouseRef.current = {
        x: e.clientX - rect.left,
        y: e.clientY - rect.top,
      };
    }

    function handleMouseLeave() {
      mouseRef.current = { x: -1000, y: -1000 };
    }

    function draw() {
      const { width, height } = sizeRef.current;
      if (width === 0 || height === 0) {
        animationRef.current = requestAnimationFrame(draw);
        return;
      }

      ctx.clearRect(0, 0, width, height);

      // Subtle warm radial gradient overlay for depth
      const gradient = ctx.createRadialGradient(
        width * 0.5,
        height * 0.4,
        0,
        width * 0.5,
        height * 0.4,
        Math.max(width, height) * 0.6
      );
      gradient.addColorStop(0, "rgba(243, 128, 32, 0.04)");
      gradient.addColorStop(0.5, "rgba(245, 158, 11, 0.02)");
      gradient.addColorStop(1, "rgba(0, 0, 0, 0)");
      ctx.fillStyle = gradient;
      ctx.fillRect(0, 0, width, height);

      const particles = particlesRef.current;
      const mouse = mouseRef.current;

      // Update particle positions (skip if reduced motion)
      if (!prefersReducedMotion) {
        for (let i = 0; i < particles.length; i++) {
          const p = particles[i];

          // Mouse interaction: gently push away
          const dx = p.x - mouse.x;
          const dy = p.y - mouse.y;
          const dist = Math.sqrt(dx * dx + dy * dy);

          if (dist < MOUSE_INFLUENCE_RADIUS && dist > 0) {
            const force = ((MOUSE_INFLUENCE_RADIUS - dist) / MOUSE_INFLUENCE_RADIUS) * MOUSE_PUSH_STRENGTH;
            p.vx += (dx / dist) * force;
            p.vy += (dy / dist) * force;
          }

          // Damping to keep movement slow
          p.vx *= 0.995;
          p.vy *= 0.995;

          // Clamp velocity
          const speed = Math.sqrt(p.vx * p.vx + p.vy * p.vy);
          if (speed > 0.6) {
            p.vx = (p.vx / speed) * 0.6;
            p.vy = (p.vy / speed) * 0.6;
          }

          // If nearly stopped, give a tiny nudge to keep drifting
          if (speed < 0.05) {
            p.vx += (Math.random() - 0.5) * 0.02;
            p.vy += (Math.random() - 0.5) * 0.02;
          }

          p.x += p.vx;
          p.y += p.vy;

          // Bounce off edges
          if (p.x < 0) {
            p.x = 0;
            p.vx = Math.abs(p.vx);
          } else if (p.x > width) {
            p.x = width;
            p.vx = -Math.abs(p.vx);
          }

          if (p.y < 0) {
            p.y = 0;
            p.vy = Math.abs(p.vy);
          } else if (p.y > height) {
            p.y = height;
            p.vy = -Math.abs(p.vy);
          }
        }
      }

      // Draw connection lines (skip if reduced motion)
      if (!prefersReducedMotion) {
        for (let i = 0; i < particles.length; i++) {
          for (let j = i + 1; j < particles.length; j++) {
            const a = particles[i];
            const b = particles[j];
            const dx = a.x - b.x;
            const dy = a.y - b.y;
            const dist = Math.sqrt(dx * dx + dy * dy);

            if (dist < CONNECTION_DISTANCE) {
              const opacity =
                0.03 + (0.05 * (1 - dist / CONNECTION_DISTANCE));
              ctx.beginPath();
              ctx.moveTo(a.x, a.y);
              ctx.lineTo(b.x, b.y);
              ctx.strokeStyle = `rgba(243, 128, 32, ${opacity})`;
              ctx.lineWidth = 0.5;
              ctx.stroke();
            }
          }
        }
      }

      // Draw mouse-to-particle connection lines (skip if reduced motion)
      if (!prefersReducedMotion && mouse.x > -500) {
        for (let i = 0; i < particles.length; i++) {
          const p = particles[i];
          const dx = p.x - mouse.x;
          const dy = p.y - mouse.y;
          const dist = Math.sqrt(dx * dx + dy * dy);
          if (dist < MOUSE_LINE_RADIUS) {
            ctx.beginPath();
            ctx.moveTo(mouse.x, mouse.y);
            ctx.lineTo(p.x, p.y);
            ctx.strokeStyle = `rgba(243, 128, 32, 0.08)`;
            ctx.lineWidth = 0.5;
            ctx.stroke();
          }
        }
      }

      // Draw particles with mouse proximity glow
      for (let i = 0; i < particles.length; i++) {
        const p = particles[i];
        const [cr, cg, cb] = p.color;

        // Calculate proximity to mouse for glow effect
        const dx = p.x - mouse.x;
        const dy = p.y - mouse.y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        const proximity = mouse.x > -500 && dist < MOUSE_GLOW_RADIUS
          ? 1 - dist / MOUSE_GLOW_RADIUS
          : 0;
        const glowOpacity = p.opacity + proximity * (1.0 - p.opacity);

        // Draw radial gradient halo when near mouse
        if (proximity > 0) {
          const glowSize = p.radius * (2 + proximity * 3);
          const haloGrad = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, glowSize);
          haloGrad.addColorStop(0, `rgba(${cr}, ${cg}, ${cb}, ${proximity * 0.4})`);
          haloGrad.addColorStop(1, `rgba(${cr}, ${cg}, ${cb}, 0)`);
          ctx.beginPath();
          ctx.arc(p.x, p.y, glowSize, 0, Math.PI * 2);
          ctx.fillStyle = haloGrad;
          ctx.fill();
        }

        // Draw the particle itself
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(${cr}, ${cg}, ${cb}, ${glowOpacity})`;
        ctx.fill();
      }

      animationRef.current = requestAnimationFrame(draw);
    }

    // Initial setup
    resize();
    window.addEventListener("resize", resize);
    window.addEventListener("mousemove", handleMouseMove);
    window.addEventListener("mouseleave", handleMouseLeave);

    animationRef.current = requestAnimationFrame(draw);

    return () => {
      cancelAnimationFrame(animationRef.current);
      window.removeEventListener("resize", resize);
      window.removeEventListener("mousemove", handleMouseMove);
      window.removeEventListener("mouseleave", handleMouseLeave);
    };
  }, [initParticles]);

  if (typeof window === "undefined") return null;

  return (
    <canvas
      ref={canvasRef}
      className="pointer-events-none absolute inset-0 z-0"
      aria-hidden="true"
    />
  );
}
