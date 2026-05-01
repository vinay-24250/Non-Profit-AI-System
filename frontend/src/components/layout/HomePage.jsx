import PropTypes from "prop-types";
import { useState, useEffect } from "react";

function useCounter(target, duration = 1600, start = false) {
  const [count, setCount] = useState(0);
  useEffect(() => {
    if (!start) return;
    let t0 = null;
    const tick = (ts) => {
      if (!t0) t0 = ts;
      const p = Math.min((ts - t0) / duration, 1);
      setCount(Math.floor((1 - Math.pow(1 - p, 3)) * target));
      if (p < 1) requestAnimationFrame(tick);
      else setCount(target);
    };
    requestAnimationFrame(tick);
  }, [start, target, duration]);
  return count;
}

function Stat({ value, label, suffix = "", started }) {
  const count = useCounter(value, 1400, started);
  return (
    <div className="text-center px-6">
      <div className="text-3xl font-bold text-amber-400 font-mono">
        {count}{suffix}
      </div>
      <div className="text-xs text-slate-500 uppercase tracking-widest mt-1 font-mono">
        {label}
      </div>
    </div>
  );
}
Stat.propTypes = {
  value: PropTypes.number.isRequired,
  label: PropTypes.string.isRequired,
  suffix: PropTypes.string,
  started: PropTypes.bool.isRequired,
};

function Chip({ label, color }) {
  const cls = {
    amber:  "bg-amber-400/10 border-amber-400/20 text-amber-400",
    indigo: "bg-indigo-400/10 border-indigo-400/20 text-indigo-400",
    teal:   "bg-teal-400/10   border-teal-400/20   text-teal-400",
    slate:  "bg-slate-700/40  border-slate-600/30  text-slate-400",
  }[color] || "bg-slate-700/40 border-slate-600/30 text-slate-400";

  return (
    <span className={`inline-block px-3 py-1 rounded-full text-xs font-mono border tracking-wider ${cls}`}>
      {label}
    </span>
  );
}
Chip.propTypes = {
  label: PropTypes.string.isRequired,
  color: PropTypes.string.isRequired,
};

const HomePage = ({ onNavigate }) => {
  // eslint-disable-next-line no-unused-vars
  const [started, setStarted] = useState(false);
  const [hovered, setHovered] = useState(null);

  useEffect(() => {
    const t = setTimeout(() => setStarted(true), 600);
    return () => clearTimeout(t);
  }, []);

  return (
    <div className="min-h-screen bg-[#040B14] text-white font-mono overflow-x-hidden">

      <section className="max-w-4xl mx-auto px-6 pt-20 pb-16 text-center">
        <div className="inline-flex items-center gap-2 mb-8 px-4 py-1.5 rounded-full bg-amber-400/8 border border-amber-400/20">
          <span className="w-1.5 h-1.5 rounded-full bg-amber-400 animate-pulse" />
          <span className="text-xs text-amber-400 uppercase tracking-[0.25em]">
            Agentic AI · Gen AI · DevOps
          </span>
        </div>

        <h1 className="text-4xl md:text-6xl font-bold text-white leading-tight mb-5 tracking-tight">
          AI Platform for
          <br />
          <span className="text-amber-400">Non-Profit</span> Communications
        </h1>

        <p className="text-base text-slate-400 max-w-xl mx-auto leading-relaxed mb-10">
          Automate workflows and train your team using AI-powered tools.
        </p>

        <div className="flex flex-wrap gap-3 justify-center mb-14">
          <button
            onClick={() => onNavigate("triage")}
            className="px-7 py-3 rounded-xl bg-amber-400 text-[#040B14] text-sm font-semibold tracking-wider hover:bg-amber-300 active:scale-95 transition-all duration-200"
          >
            ⚡ Triage Agent
          </button>
          <button
            onClick={() => onNavigate("quiz")}
            className="px-7 py-3 rounded-xl border border-indigo-400/40 text-indigo-400 text-sm tracking-wider hover:bg-indigo-400/10 active:scale-95 transition-all duration-200"
          >
            🎓 Quiz Tutor
          </button>
        </div>

      </section>

      <section className="max-w-5xl mx-auto px-6 py-16">
        <div className="text-center mb-10">
          <p className="text-xs text-amber-400 uppercase tracking-[0.25em] mb-2">
            Features
          </p>
          <h2 className="text-2xl md:text-3xl font-bold text-white">
            Choose your tool
          </h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">

          <div
            className={`relative rounded-2xl p-7 cursor-pointer transition-all duration-300
              ${hovered === "triage"
                ? "bg-amber-400/5 border border-amber-400/30 -translate-y-1"
                : "bg-slate-900/50 border border-slate-800 hover:-translate-y-1"
              }`}
            onMouseEnter={() => setHovered("triage")}
            onMouseLeave={() => setHovered(null)}
            onClick={() => onNavigate("triage")}
          >
            <div className="flex items-start justify-between mb-5">
              <div className="w-12 h-12 rounded-xl bg-amber-400/10 border border-amber-400/20 flex items-center justify-center text-2xl">
                ⚡
              </div>
              <span className="text-xs font-mono uppercase tracking-widest px-3 py-1 rounded-full bg-amber-400/10 border border-amber-400/20 text-amber-400">
                Agentic AI
              </span>
            </div>

            <h3 className="text-xl font-bold text-white mb-2">
              Reactive Triage Agent
            </h3>
            <p className="text-sm text-slate-400 mb-6">
              Automate email classification and generate smart replies using AI.
            </p>

            <div className="flex flex-wrap gap-2 mb-6">
              {["CrewAI", "Groq LLM"].map(t => (
                <Chip key={t} label={t} color="amber" />
              ))}
            </div>

            <button
              onClick={e => { e.stopPropagation(); onNavigate("triage"); }}
              className={`w-full py-2.5 rounded-xl text-sm font-mono tracking-wider transition-all duration-200 border
                ${hovered === "triage"
                  ? "bg-amber-400 text-[#040B14] border-amber-400 font-semibold"
                  : "bg-amber-400/8 text-amber-400 border-amber-400/25"
                }`}
            >
              Launch Triage Agent →
            </button>
          </div>

          <div
            className={`relative rounded-2xl p-7 cursor-pointer transition-all duration-300
              ${hovered === "quiz"
                ? "bg-indigo-400/5 border border-indigo-400/30 -translate-y-1"
                : "bg-slate-900/50 border border-slate-800 hover:-translate-y-1"
              }`}
            onMouseEnter={() => setHovered("quiz")}
            onMouseLeave={() => setHovered(null)}
            onClick={() => onNavigate("quiz")}
          >
            <div className="flex items-start justify-between mb-5">
              <div className="w-12 h-12 rounded-xl bg-indigo-400/10 border border-indigo-400/20 flex items-center justify-center text-2xl">
                🎓
              </div>
              <span className="text-xs font-mono uppercase tracking-widest px-3 py-1 rounded-full bg-indigo-400/10 border border-indigo-400/20 text-indigo-400">
                Gen AI + RAG
              </span>
            </div>

            <h3 className="text-xl font-bold text-white mb-2">
              AI Quiz Tutor
            </h3>
            <p className="text-sm text-slate-400 mb-6">
              Practice with AI-generated quizzes and get instant feedback.
            </p>

            <div className="flex flex-wrap gap-2 mb-6">
              {["RAG", "ChromaDB"].map(t => (
                <Chip key={t} label={t} color="indigo" />
              ))}
            </div>

            <button
              onClick={e => { e.stopPropagation(); onNavigate("quiz"); }}
              className={`w-full py-2.5 rounded-xl text-sm font-mono tracking-wider transition-all duration-200 border
                ${hovered === "quiz"
                  ? "bg-indigo-400 text-[#040B14] border-indigo-400 font-semibold"
                  : "bg-indigo-400/8 text-indigo-400 border-indigo-400/25"
                }`}
            >
              Launch Quiz Tutor →
            </button>
          </div>

        </div>
      </section>

      <footer className="border-t border-slate-800/40 px-6 py-6 text-center">
        <p className="text-xs text-slate-700 font-mono uppercase tracking-widest">
          NonProfit AI Platform · v3.0
        </p>
      </footer>

    </div>
  );
};

HomePage.propTypes = {
  onNavigate: PropTypes.func.isRequired,
};

export default HomePage;