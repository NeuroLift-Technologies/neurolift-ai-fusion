import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

/** @type {import("next").NextConfig} */
const nextConfig = {
  outputFileTracingRoot: path.join(__dirname, "../.."),
  webpack: (config) => {
    // Explicit @ alias — ensures @/lib/* resolves to apps/web/lib/* regardless
    // of outputFileTracingRoot or Vercel rootDirectory ("apps").
    // Without this, Vercel's rootDirectory can cause tsconfig paths to resolve
    // from the wrong directory (repo root instead of apps/web).
    config.resolve.alias["@"] = __dirname;
    return config;
  },
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1",
  },
  eslint: {
    ignoreDuringBuilds: true,
  },
};

export default nextConfig;
