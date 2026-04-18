// src/components/triage/SampleEmails.jsx
import PropTypes from "prop-types";
import { SAMPLE_EMAILS } from "../../constants/data";

const SampleEmails = ({ onSelect }) => {
  return (
    <div className="pt-2">
      <p className="text-xs font-medium text-gray-500 mb-3">
        Try a sample email
      </p>
      
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
        {SAMPLE_EMAILS.map((s, i) => (
          <button
            key={i}
            onClick={() => onSelect(s.text)}
            className="text-left bg-white/5 border border-white/10 hover:bg-white/10 
                       hover:border-white/20 rounded-xl p-4 transition-all 
                       duration-200 group cursor-pointer"
          >
            <span className="block text-[10px] font-bold uppercase tracking-wider text-teal-500 mb-1">
              {s.label}
            </span>
            <span className="block text-sm text-gray-400 group-hover:text-gray-200 
                             line-clamp-2 leading-snug transition-colors">
              {s.preview}
            </span>
          </button>
        ))}
      </div>
    </div>
  );
};

SampleEmails.propTypes = {
  onSelect: PropTypes.func.isRequired,
};

export default SampleEmails;