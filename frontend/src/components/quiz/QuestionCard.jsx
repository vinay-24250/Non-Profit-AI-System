// src/components/quiz/QuestionCard.jsx
import PropTypes from "prop-types";
import Badge from "../ui/Badge";

const QuestionCard = ({ question, selected, onAnswer }) => {
  const { question: q, options, correct_answer, topic, difficulty } = question;

  const getOptionClass = (opt) => {
    const letter = opt.charAt(0);
    const base =
      "w-full text-left bg-[#12121a] border rounded-xl px-4 py-3 text-[0.78rem] font-mono leading-relaxed transition-all duration-200";

    if (!selected) {
      return `${base} border-[#2a2a3e] text-[#e8e8f0] hover:border-violet-500/60 hover:bg-[#1a1a26] cursor-pointer`;
    }
    if (letter === correct_answer) {
      return `${base} border-emerald-500/60 bg-emerald-500/10 text-emerald-300`;
    }
    if (opt === selected) {
      return `${base} border-red-500/60 bg-red-500/10 text-red-300`;
    }
    return `${base} border-[#2a2a3e] text-[#4a4a62] cursor-default`;
  };

  return (
    <div
      className="bg-[#1a1a26] border border-[#2a2a3e] rounded-xl p-6 space-y-5
        animate-[fadeUp_0.35s_ease_forwards]"
    >
      {/* Meta row */}
      <div className="flex items-center justify-between">
        <Badge variant="accent">{topic}</Badge>
        <Badge variant={difficulty}>{difficulty}</Badge>
      </div>

      {/* Question text */}
      <h3 className="font-['Syne'] text-[1rem] font-semibold text-[#e8e8f0] leading-relaxed">
        {q}
      </h3>

      {/* Options */}
      <div className="space-y-2">
        {options.map((opt, i) => (
          <button
            key={i}
            className={getOptionClass(opt)}
            disabled={!!selected}
            onClick={() => !selected && onAnswer(opt)}
          >
            <span className="text-[#6b6b88] mr-2">{opt.charAt(0)}.</span>
            {opt.slice(3)}
          </button>
        ))}
      </div>

      {/* Correct answer hint shown after selection */}
      {selected && (
        <p className="text-[0.68rem] font-mono text-[#6b6b88]">
          Correct answer:{" "}
          <span className="text-emerald-400">
            {options.find((o) => o.charAt(0) === correct_answer)}
          </span>
        </p>
      )}
    </div>
  );
};

QuestionCard.propTypes = {
  question: PropTypes.shape({
    question:       PropTypes.string.isRequired,
    options:        PropTypes.arrayOf(PropTypes.string).isRequired,
    correct_answer: PropTypes.string.isRequired,
    topic:          PropTypes.string.isRequired,
    difficulty:     PropTypes.string.isRequired,
  }).isRequired,
  selected: PropTypes.string,
  onAnswer: PropTypes.func.isRequired,
};

QuestionCard.defaultProps = {
  selected: null,
};

export default QuestionCard;