// src/components/triage/TriagePanel.jsx
import { useState } from "react";
import { runTriage } from "../../api/apiClient";
import EmailInput from "./EmailInput";
import SampleEmails from "./SampleEmails";
import ClassificationCard from "./ClassificationCard";
import EntityCard from "./EntityCard";
import DraftResponse from "./DraftResponse";

const TriagePanel = () => {
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);
  const [step, setStep] = useState(0);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleRun = async () => {
    if (!text.trim()) return;
    setLoading(true);
    setResult(null);
    setError(null);
    setStep(1);

    const t1 = setTimeout(() => setStep(2), 900);
    const t2 = setTimeout(() => setStep(3), 1800);

    try {
      const data = await runTriage(text);
      clearTimeout(t1);
      clearTimeout(t2);
      setResult(data);
    } catch (e) {
      setError(e?.response?.data?.detail || "Connection error. Please try again.");
    } finally {
      setLoading(false);
      setStep(0);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8 py-4">
      {/* Header: Cleaner typography */}
      <header>
        <h2 className="text-2xl font-semibold text-white tracking-tight">
          Email Triage Agent
        </h2>
        <p className="text-gray-400 text-sm mt-1">
          Automated classification, entity extraction, and draft generation.
        </p>
      </header>

      {/* Main Input Area: Less "boxy", more integrated */}
      <div className="space-y-4">
        <EmailInput
          value={text}
          onChange={setText}
          onSubmit={handleRun}
          loading={loading}
          step={step}
        />
        <SampleEmails onSelect={setText} />
      </div>

      {/* Error State */}
      {error && (
        <div className="p-4 bg-red-950/20 border border-red-900/50 rounded-lg text-red-400 text-sm">
          {error}
        </div>
      )}

      {/* Results Section */}
      {result && (
        <div className="space-y-6 animate-in fade-in duration-500">
          {/* Simple Step Breadcrumbs */}
          <div className="flex items-center gap-4 text-xs font-medium uppercase tracking-wider text-gray-500 border-b border-white/5 pb-4">
            {["Classified", "Extracted", "Drafted"].map((label, i) => (
              <div key={i} className="flex items-center gap-2">
                <span className="text-teal-500">●</span>
                <span>{label}</span>
              </div>
            ))}
          </div>

          {/* Grid: 1 col on mobile, 2 on desktop */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <ClassificationCard classification={result.classification} />
            <EntityCard entities={result.entities} />
          </div>

          {/* Draft area: Full width for readability */}
          <div className="pt-2">
            <DraftResponse draft={result.draft_response} />
          </div>
        </div>
      )}
    </div>
  );
};

export default TriagePanel;