// src/components/triage/EmailInput.jsx
import PropTypes from "prop-types";
import Spinner from "../ui/Spinner";
import { TRIAGE_STEPS } from "../../constants/data";

const EmailInput = ({ value, onChange, onSubmit, loading, step }) => {
  return (
    <div className="space-y-3">
      <label className="block text-[0.62rem] font-mono uppercase tracking-widest text-[#6b6b88]">
        Paste Incoming Message
      </label>

      <textarea
        rows={6}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Dear team, I'm following up on my donation of $500 made on March 15th…"
        className="w-full bg-[#1a1a26] border border-[#2a2a3e] rounded-xl px-4 py-3.5
          text-sm font-mono text-[#e8e8f0] placeholder-[#05052a] resize-y outline-none
          focus:border-violet-500 transition-colors duration-200 leading-relaxed"
      />

      <div className="flex items-center justify-between">
        <p className="text-[0.65rem] font-mono text-[#6b6b88]">
          {loading && step > 0
            ? `Step ${step}/3 — ${TRIAGE_STEPS[step - 1]}`
            : "Paste any donor or volunteer email above"}
        </p>

        <button
          onClick={onSubmit}
          disabled={loading || !value.trim()}
          className="flex items-center gap-2 px-6 py-2.5 bg-violet-600 hover:bg-violet-500
            disabled:opacity-40 disabled:cursor-not-allowed text-white text-xs font-mono
            tracking-wider rounded-lg transition-all duration-200 active:scale-95 cursor-pointer"
        >
          {loading ? (
            <>
              <Spinner />
              {TRIAGE_STEPS[step - 1] ?? "Processing…"}
            </>
          ) : (
            <>⚡ Run Triage Agent</>
          )}
        </button>
      </div>
    </div>
  );
};

EmailInput.propTypes = {
  value:    PropTypes.string.isRequired,
  onChange: PropTypes.func.isRequired,
  onSubmit: PropTypes.func.isRequired,
  loading:  PropTypes.bool.isRequired,
  step:     PropTypes.number.isRequired,
};

export default EmailInput;