// src/components/quiz/SessionScore.jsx
import PropTypes from "prop-types";
import ScoreRing from "../ui/ScoreRing";

const SessionScore = ({ score, difficulty }) => {
  const { total, correct } = score;
  const pct = total > 0 ? Math.round((correct / total) * 100) : 0;

  const diffColor = {
    easy:   "text-emerald-400",
    medium: "text-yellow-400",
    hard:   "text-red-400",
  }[difficulty] ?? "text-[#a5a5c0]";

  return (
    <div
      className="bg-[#1a1a26] border border-[#2a2a3e] rounded-xl p-5
        flex items-center gap-5 animate-[fadeUp_0.35s_ease_forwards]"
    >
      <ScoreRing pct={pct} size={80} />

      <div className="flex-1">
        <p className="font-['Syne'] text-base font-bold text-[#e8e8f0] mb-0.5">
          Session Score
        </p>
        <p className="text-[0.72rem] font-mono text-[#6b6b88]">
          {correct} correct out of {total} question{total !== 1 ? "s" : ""}
        </p>
        <p className={`text-[0.68rem] font-mono mt-1 ${diffColor}`}>
          Adaptive difficulty: <strong>{difficulty.toUpperCase()}</strong>
        </p>
      </div>

      {/* Progress bar */}
      <div className="hidden md:block w-36">
        <div className="flex justify-between text-[0.6rem] font-mono text-[#6b6b88] mb-1.5">
          <span>Progress</span>
          <span>{pct}%</span>
        </div>
        <div className="h-1 bg-[#12121a] rounded-full overflow-hidden">
          <div
            className="h-full rounded-full transition-all duration-700"
            style={{
              width: `${pct}%`,
              background: "linear-gradient(90deg, #7B6EF6, #00D4B4)",
            }}
          />
        </div>
      </div>
    </div>
  );
};

SessionScore.propTypes = {
  score: PropTypes.shape({
    total:   PropTypes.number.isRequired,
    correct: PropTypes.number.isRequired,
  }).isRequired,
  difficulty: PropTypes.oneOf(["easy", "medium", "hard"]).isRequired,
};

export default SessionScore;