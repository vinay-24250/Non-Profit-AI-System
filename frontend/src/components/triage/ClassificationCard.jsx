// src/components/triage/ClassificationCard.jsx
import PropTypes from "prop-types";
import { URGENCY_CONFIG, INTENT_ICON } from "../../constants/data";

const ClassificationCard = ({ classification }) => {
  const { urgency, intent, confidence, reasoning } = classification;
  const cfg = URGENCY_CONFIG[urgency] ?? URGENCY_CONFIG.low;

  const intentLabel = intent?.replace(/_/g, " ").toUpperCase();
  const icon        = INTENT_ICON[intent] ?? "📧";
  const pct         = Math.round((confidence ?? 0) * 100);

  return (
    <div className="bg-[#1a1a26] border border-[#2a2a3e] rounded-xl p-5 space-y-4">
      <p className="text-[0.62rem] font-mono uppercase tracking-widest text-[#6b6b88]">
        Classification
      </p>

      {/* Urgency + intent row */}
      <div className="flex flex-wrap items-center gap-2">
        <span
          className={`${cfg.bg} ${cfg.text} text-[0.65rem] font-mono font-semibold
            tracking-widest px-3 py-1 rounded-md uppercase`}
        >
          {cfg.label}
        </span>
        <span className="text-lg">{icon}</span>
        <span className="text-teal-400 text-[0.72rem] font-mono tracking-wider">
          {intentLabel}
        </span>
      </div>

      {/* Reasoning */}
      <p className="text-[0.72rem] font-mono text-[#8888aa] leading-relaxed">
        {reasoning}
      </p>

      {/* Confidence bar */}
      <div>
        <div className="flex justify-between mb-1.5">
          <span className="text-[0.6rem] font-mono uppercase tracking-widest text-[#6b6b88]">
            Confidence
          </span>
          <span className="text-[0.7rem] font-mono text-[#e8e8f0]">{pct}%</span>
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

ClassificationCard.propTypes = {
  classification: PropTypes.shape({
    urgency:    PropTypes.string.isRequired,
    intent:     PropTypes.string.isRequired,
    confidence: PropTypes.number.isRequired,
    reasoning:  PropTypes.string.isRequired,
  }).isRequired,
};

export default ClassificationCard;