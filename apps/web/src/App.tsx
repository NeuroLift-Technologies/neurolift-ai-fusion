import { BrowserRouter, Routes, Route, NavLink } from "react-router-dom";
import Dashboard from "./vite-pages/Dashboard";
import AvatarsPage from "./vite-pages/AvatarsPage";
import AidesPage from "./vite-pages/AidesPage";
import SessionsPage from "./vite-pages/SessionsPage";
import FusionPage from "./vite-pages/FusionPage";
import ScenariosPage from "./vite-pages/ScenariosPage";

const NAV_LINKS = [
  { to: "/", label: "Dashboard" },
  { to: "/avatars", label: "Avatars" },
  { to: "/aides", label: "Aides" },
  { to: "/sessions", label: "Sessions" },
  { to: "/fusion", label: "Fusion" },
  { to: "/scenarios", label: "Scenarios" },
];

export default function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-[#0f0f1a] text-[#e8e8f0] flex flex-col">
        <header className="bg-[#1a1a2e] border-b border-[#2e2e4e] px-6 py-4 flex items-center gap-8">
          <span className="text-[#6c63ff] font-bold text-xl tracking-tight">
            NeuroLift <span className="text-[#48cfad]">AI-Fusion</span>
          </span>
          <nav className="flex gap-4">
            {NAV_LINKS.map(({ to, label }) => (
              <NavLink
                key={to}
                to={to}
                end={to === "/"}
                className={({ isActive }) =>
                  `text-sm px-3 py-1.5 rounded-md transition-colors ${
                    isActive
                      ? "bg-[#6c63ff]/20 text-[#6c63ff] font-semibold"
                      : "text-[#8888aa] hover:text-[#e8e8f0]"
                  }`
                }
              >
                {label}
              </NavLink>
            ))}
          </nav>
        </header>
        <main className="flex-1 p-6">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/avatars" element={<AvatarsPage />} />
            <Route path="/aides" element={<AidesPage />} />
            <Route path="/sessions" element={<SessionsPage />} />
            <Route path="/fusion" element={<FusionPage />} />
            <Route path="/scenarios" element={<ScenariosPage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}


