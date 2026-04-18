// src/components/quiz/EvalResult.jsx
import PropTypes from "prop-types";
import Spinner from "../ui/Spinner";

const EvalResult = ({ evalResult, loading, onNext, loadingNext }) => {
  if (loading) {
    return (
      <div
        className="bg-[#1a1a26] border border-[#2a2a3e] rounded-xl p-6
          flex items-center gap-3 text-sm font-mono text-[#6b6b88]"
      >
        <Spinner />
        Evaluating your answer with Llama 3.1…
      </div>
    );
  }

  if (!evalResult) return null;

  const { is_correct, score, feedback, explanation, real_world_example } = evalResult;

  return (
    <div
      className={`bg-[#1a1a26] border rounded-xl p-6 space-y-5
        animate-[fadeUp_0.35s_ease_forwards]
        ${is_correct ? "border-emerald-500/40" : "border-red-500/40"}`}
    >
      {/* Result header */}
      <div className="flex items-start gap-4">
        <span className="text-3xl mt-0.5">{is_correct ? "✅" : "❌"}</span>
        <div className="flex-1">
          <div className="flex items-center gap-3 mb-1">
            <h4 className="font-['Syne'] font-bold text-[#e8e8f0] text-base">
              {is_correct ? "Correct!" : "Not quite."}
            </h4>
            <span
              className={`text-xs font-mono px-2.5 py-0.5 rounded-full border
                ${is_correct
                  ? "text-emerald-400 bg-emerald-500/15 border-emerald-500/30"
                  : "text-red-400 bg-red-500/15 border-red-500/30"
                }`}
            >
              {score}/100
            </span>
          </div>
          <p className="text-[0.75rem] font-mono text-[#8888aa] leading-relaxed">
            {feedback}
          </p>
        </div>
      </div>

      <hr className="border-[#2a2a3e]" />

      {/* Deep explanation */}
      <div>
        <p className="text-[0.6rem] font-mono uppercase tracking-widest text-[#6b6b88] mb-2">
          Deep Explanation
        </p>
        <p className="text-[0.78rem] font-mono text-[#c8c8e0] leading-7">
          {explanation}
        </p>
      </div>

      {/* Real-world example */}
      <div className="bg-[#12121a] border border-[#2a2a3e] rounded-xl p-4">
        <p className="text-[0.6rem] font-mono uppercase tracking-widest text-[#6b6b88] mb-2">
          Real-World Example
        </p>
        <p className="text-[0.75rem] font-mono text-[#8888aa] leading-7">
          💡 {real_world_example}
        </p>
      </div>

      {/* Next question */}
      <div className="flex justify-end pt-1">
        <button
          onClick={onNext}
          disabled={loadingNext}
          className="flex items-center gap-2 px-6 py-2.5 bg-violet-600 hover:bg-violet-500
            disabled:opacity-40 disabled:cursor-not-allowed text-white text-xs font-mono
            tracking-wider rounded-lg transition-all duration-200 active:scale-95 cursor-pointer"
        >
          {loadingNext ? <><Spinner /> Loading…</> : <>Next Question →</>}
        </button>
      </div>
    </div>
  );
};

EvalResult.propTypes = {
  evalResult: PropTypes.shape({
    is_correct:        PropTypes.bool.isRequired,
    score:             PropTypes.number.isRequired,
    feedback:          PropTypes.string.isRequired,
    explanation:       PropTypes.string.isRequired,
    real_world_example: PropTypes.string.isRequired,
  }),
  loading:     PropTypes.bool.isRequired,
  onNext:      PropTypes.func.isRequired,
  loadingNext: PropTypes.bool.isRequired,
};

EvalResult.defaultProps = {
  evalResult: null,
};

export default EvalResult;