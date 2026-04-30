import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "NeuroLift AI Fusion",
  description: "Avatar-Aide-Advocate ADHD training platform",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-gray-50 dark:bg-gray-950">
        <nav className="border-b border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 px-6 py-3 flex items-center gap-4">
          <span className="font-bold text-brand-600 text-lg">NeuroLift</span>
          <a href="/" className="text-sm text-gray-600 hover:text-gray-900 dark:text-gray-400 dark:hover:text-gray-100">Home</a>
          <a href="/dashboard" className="text-sm text-gray-600 hover:text-gray-900 dark:text-gray-400 dark:hover:text-gray-100">Dashboard</a>
          <a href="/session/new" className="text-sm text-gray-600 hover:text-gray-900 dark:text-gray-400 dark:hover:text-gray-100">New Session</a>
        </nav>
        <main className="max-w-7xl mx-auto px-6 py-8">{children}</main>
      </body>
    </html>
  );
}
