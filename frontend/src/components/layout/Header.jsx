// src/components/layout/Header.jsx
import PropTypes from "prop-types";

const NAV_TABS = [
  { id: "home",   icon: "⬡", label: "Home"          },
  { id: "triage", icon: "⚡", label: "Triage Agent"  },
  { id: "quiz",   icon: "🎓", label: "Quiz Tutor"    },
];

const Header = ({ activeTab, onTabChange }) => {
  return (
    <header
      className="sticky top-0 z-50 flex items-center justify-between px-6 md:px-8 py-4"
      style={{
        borderBottom: "1px solid rgba(255,255,255,0.06)",
        background: "rgba(4,11,20,0.85)",
        backdropFilter: "blur(20px)",
      }}
    >
      {/* ── Logo ──────────────────────────────────────────────────────── */}
      <button
        onClick={() => onTabChange("home")}
        className="flex items-center gap-3 group"
      >
        <div
          className="w-8 h-8 rounded-lg flex items-center justify-center text-sm font-bold transition-all duration-300 group-hover:scale-110"
          style={{
            background: "linear-gradient(135deg, #F59E0B, #D97706)",
            color: "#040B14",
            fontFamily: "'Playfair Display', serif",
          }}
        >
          N
        </div>
        <div>
          <span
            className="font-black tracking-wider text-sm"
            style={{
              fontFamily: "'Playfair Display', serif",
              color: "#F8FAFC",
            }}
          >
            NONPROFIT
          </span>
          <span
            className="text-xs font-['DM_Mono'] ml-2 tracking-widest"
            style={{ color: "#F59E0B" }}
          >
            AI
          </span>
        </div>
        <span
          className="hidden md:inline text-xs px-2 py-0.5 rounded font-['DM_Mono'] uppercase tracking-widest"
          style={{
            background: "rgba(245,158,11,0.1)",
            border: "1px solid rgba(245,158,11,0.2)",
            color: "#F59E0B",
          }}
        >
          Platform
        </span>
      </button>

      {/* ── Navigation tabs ───────────────────────────────────────────── */}
      <nav
        className="flex gap-1 p-1 rounded-xl"
        style={{
          background: "rgba(255,255,255,0.03)",
          border: "1px solid rgba(255,255,255,0.07)",
        }}
      >
        {NAV_TABS.map((tab) => (
          <button
            key={tab.id}
            onClick={() => onTabChange(tab.id)}
            className="flex items-end gap-2 px-4 py-2 rounded-lg text-xs font-['DM_Mono'] tracking-wider transition-all duration-200 cursor-pointer"
            style={
              activeTab === tab.id
                ? {
                    background: tab.id === "home"
                      ? "rgba(245,158,11,0.12)"
                      : tab.id === "triage"
                      ? "rgba(245,158,11,0.12)"
                      : "rgba(99,102,241,0.12)",
                    color: tab.id === "quiz" ? "#818CF8" : "#F59E0B",
                    border: tab.id === "quiz"
                      ? "1px solid rgba(99,102,241,0.25)"
                      : "1px solid rgba(245,158,11,0.25)",
                  }
                : {
                    background: "transparent",
                    color: "#475569",
                    border: "1px solid transparent",
                  }
            }
            onMouseEnter={e => {
              if (activeTab !== tab.id) {
                e.currentTarget.style.color = "#94A3B8";
              }
            }}
            onMouseLeave={e => {
              if (activeTab !== tab.id) {
                e.currentTarget.style.color = "#475569";
              }
            }}
          >
            <span>{tab.icon}</span>
            <span className="hidden sm:inline">{tab.label}</span>
          </button>
        ))}
      </nav>
    </header>
  );
};

Header.propTypes = {
  activeTab:   PropTypes.string.isRequired,
  onTabChange: PropTypes.func.isRequired,
};

export default Header;