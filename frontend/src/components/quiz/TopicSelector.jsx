// src/components/quiz/TopicSelector.jsx
import PropTypes from "prop-types";
import { QUIZ_TOPICS, DIFFICULTIES } from "../../constants/data";
import Spinner from "../ui/Spinner";

const TopicSelector = ({
  topic,
  onTopicChange,
  difficulty,
  onDifficultyChange,
  onGenerate,
  loading,
}) => {
  return (
    <div className="bg-[#12121a] border border-[#2a2a3e] rounded-2xl p-6 space-y-4">

      {/* Pre-set topic pills */}
      <div>
        <p className="text-[0.62rem] font-mono uppercase tracking-widest text-[#6b6b88] mb-2.5">
          Choose a topic
        </p>
        <div className="flex flex-wrap gap-2">
          {QUIZ_TOPICS.map((t) => (
            <button
              key={t}
              onClick={() => onTopicChange(t)}
              className={`text-[0.68rem] font-mono px-3.5 py-1.5 rounded-full border
                transition-all duration-200 cursor-pointer
                ${topic === t
                  ? "border-violet-500/70 bg-violet-500/15 text-violet-300"
                  : "border-[#2a2a3e] bg-transparent text-[#6b6b88] hover:border-violet-500/40 hover:text-[#a5a5c0]"
                }`}
            >
              {t}
            </button>
          ))}
        </div>
      </div>

      {/* Custom topic + difficulty + button */}
      <div className="flex gap-2 items-stretch">
        <input
          type="text"
          value={topic}
          onChange={(e) => onTopicChange(e.target.value)}
          placeholder="Or type a custom topic…"
          className="flex-1 bg-[#1a1a26] border border-[#2a2a3e] rounded-xl px-4 py-2.5
            text-sm font-mono text-[#e8e8f0] placeholder-[#3a3a52] outline-none
            focus:border-violet-500 transition-colors duration-200"
        />

        <select
          value={difficulty}
          onChange={(e) => onDifficultyChange(e.target.value)}
          className="bg-[#1a1a26] border border-[#2a2a3e] text-[#e8e8f0] text-sm font-mono
            px-3 py-2.5 rounded-xl outline-none focus:border-violet-500
            transition-colors duration-200 cursor-pointer"
        >
          {DIFFICULTIES.map((d) => (
            <option key={d} value={d}>
              {d.charAt(0).toUpperCase() + d.slice(1)}
            </option>
          ))}
        </select>

        <button
          onClick={onGenerate}
          disabled={loading || !topic.trim()}
          className="flex items-center gap-2 px-5 py-2.5 bg-teal-500 hover:bg-teal-400
            disabled:opacity-40 disabled:cursor-not-allowed text-[#0a0a0f] text-xs font-mono
            font-semibold tracking-wider rounded-xl transition-all duration-200
            active:scale-95 cursor-pointer whitespace-nowrap"
        >
          {loading ? (
            <>
              <Spinner light={false} />
              Generating…
            </>
          ) : (
            "Generate Question"
          )}
        </button>
      </div>
    </div>
  );
};

TopicSelector.propTypes = {
  topic:              PropTypes.string.isRequired,
  onTopicChange:      PropTypes.func.isRequired,
  difficulty:         PropTypes.string.isRequired,
  onDifficultyChange: PropTypes.func.isRequired,
  onGenerate:         PropTypes.func.isRequired,
  loading:            PropTypes.bool.isRequired,
};

export default TopicSelector;