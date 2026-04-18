// src/components/layout/Header.jsx
import PropTypes from "prop-types";

const NAV_TABS = [
  { id: "triage", icon: "⚡", label: "Triage Agent" },
  { id: "quiz",   icon: "🎓", label: "Quiz Bot"     },
];

const Header = ({ activeTab, onTabChange }) => {
  return (
    <header
      className="sticky top-0 z-50 flex items-center justify-between px-8 py-4
        border-b border-[#2a2a3e] bg-[#0a0a0f]/75 backdrop-blur-xl"
    >
      {/* Logo */}
      <div className="flex items-center gap-5">
        <span className="font-['Syne'] text-lg font-black tracking-wider text-[#e8e8f0]">
          NONPROFIT <span className="text-teal-400">AI</span>
        </span>
        <span
          className="text-[0.58rem] tracking-widest bg-violet-600 text-white
            px-2 py-0.5 rounded font-mono uppercase"
        >
          Platform
        </span>
      </div>

      {/* Tabs */}
      <nav className="flex gap-1 p-1 bg-[#12121a] border border-[#2a2a3e] rounded-xl">
        {NAV_TABS.map((tab) => (
          <button
            key={tab.id}
            onClick={() => onTabChange(tab.id)}
            className={`flex items-center gap-2 px-5 py-2 rounded-lg text-xs font-mono
              tracking-wider transition-all duration-200 cursor-pointer
              ${activeTab === tab.id
                ? "bg-[#1a1a26] text-[#e8e8f0] border border-[#2a2a3e] shadow-sm"
                : "text-[#6b6b88] hover:text-[#e8e8f0]"
              }`}
          >
            <span>{tab.icon}</span>
            {tab.label}
          </button>
        ))}
      </nav>

      {/* Stack info */}
      <div className="text-[0.65rem] font-mono text-[#6b6b88] hidden md:block">
        Llama&nbsp;3.1 · Groq · FastAPI
      </div>
    </header>
  );
};

Header.propTypes = {
  activeTab:   PropTypes.string.isRequired,
  onTabChange: PropTypes.func.isRequired,
};

export default Header;