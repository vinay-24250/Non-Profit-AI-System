import { useState } from "react";
import Header from "./components/layout/Header";
import TriagePanel from "./components/triage/TriagePanel";
import QuizPanel from "./components/quiz/QuizPanel";

const App = () => {
  const [activeTab, setActiveTab] = useState("triage");

  return (
    <div className="min-h-screen font-mono"
      style={{
        background: `
          radial-gradient(ellipse 80% 50% at 20% -10%, rgba(123,110,246,.15) 0%, transparent 60%),
          radial-gradient(ellipse 60% 40% at 80% 110%, rgba(0,212,180,.10) 0%, transparent 60%),
          #0a0a0f
        `,
      }}
    >
      <Header activeTab={activeTab} onTabChange={setActiveTab} />

      <main className="max-w-6xl mx-auto px-6 py-10">
        {activeTab === "triage" ? <TriagePanel /> : <QuizPanel />}
      </main>
    </div>
  );
};

export default App;