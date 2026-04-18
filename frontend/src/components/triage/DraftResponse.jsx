// src/components/triage/DraftResponse.jsx
import { useState } from "react";
import PropTypes from "prop-types";
import Toast from "../ui/Toast";

const DraftResponse = ({ draft }) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(draft);
    setCopied(true);
  };

  return (
    <>
      <div className="bg-[#1a1a26] border border-[#2a2a3e] rounded-xl p-5">
        {/* Header row */}
        <div className="flex items-center justify-between mb-4">
          <p className="text-[0.62rem] font-mono uppercase tracking-widest text-[#6b6b88]">
            Generated Draft Response
          </p>
          <button
            onClick={handleCopy}
            className="flex items-center gap-1.5 text-[0.68rem] font-mono text-[#6b6b88]
              hover:text-teal-400 border border-[#2a2a3e] hover:border-teal-500/50
              px-3 py-1.5 rounded-lg transition-all duration-200 cursor-pointer"
          >
            {copied ? "✓ Copied" : "⎘ Copy"}
          </button>
        </div>

        {/* Draft text */}
        <div className="border-l-2 border-violet-500 pl-4 bg-[#12121a] rounded-r-lg py-3 pr-3">
          <pre className="text-[0.78rem] font-mono text-[#e8e8f0] leading-7 whitespace-pre-wrap break-words">
            {draft}
          </pre>
        </div>
      </div>

      {copied && (
        <Toast message="Draft copied to clipboard" onDone={() => setCopied(false)} />
      )}
    </>
  );
};

DraftResponse.propTypes = {
  draft: PropTypes.string.isRequired,
};

export default DraftResponse;