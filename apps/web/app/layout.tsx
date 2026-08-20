import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import { ThemeProvider } from "next-themes";
import "./globals.css";
import { Toaster } from "@/components/ui/toaster";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "NeuroLift AI Fusion — Avatar-Aide-Advocate Visualization",
  description:
    "Interactive visualization of the 19 Avatar-Aide-Advocate pairs. AI avatars with ADHD traits experience authentic struggles, coached by expert aides, fusing into empathetic advocates.",
  keywords: [
    "NeuroLift",
    "ADHD",
    "AI",
    "experiential learning",
    "Avatar",
    "Aide",
    "Advocate",
    "neurodivergent",
    "executive function",
    "simulation",
  ],
  authors: [{ name: "Joshua W. Dorsey, Sr." }],
  openGraph: {
    title: "NeuroLift AI Fusion — 19 Avatar-Aide-Advocate Pairs",
    description:
      "Explore the 19 AI pairs that train through authentic ADHD experience. Interactive visualization of the fusion pipeline.",
    siteName: "NeuroLift AI Fusion",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased bg-background text-foreground`}
      >
        <ThemeProvider attribute="class" defaultTheme="system" enableSystem disableTransitionOnChange>
          <nav className="border-b border-border bg-card px-6 py-3 flex flex-wrap items-center gap-4">
            <span className="font-bold text-brand-600 text-lg">NeuroLift</span>
            <a href="/" className="text-sm text-muted-foreground hover:text-foreground transition-colors">Home</a>
            <a href="/pairs" className="text-sm text-muted-foreground hover:text-foreground transition-colors">Pair Atlas</a>
            <a href="/dashboard" className="text-sm text-muted-foreground hover:text-foreground transition-colors">Dashboard</a>
            <a href="/session/new" className="text-sm text-muted-foreground hover:text-foreground transition-colors">New Session</a>
            <a href="/simulation-lab" className="text-sm text-muted-foreground hover:text-foreground transition-colors">Simulation Lab</a>
          </nav>
          <main className="max-w-7xl mx-auto px-6 py-8">{children}</main>
          <Toaster />
        </ThemeProvider>
      </body>
    </html>
  );
}
