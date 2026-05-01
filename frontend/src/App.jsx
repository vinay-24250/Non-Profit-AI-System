// src/App.jsx
import { useState } from "react";
import Header from "./components/layout/Header";
import HomePage from "./components/layout/HomePage";
import TriagePanel from "./components/triage/TriagePanel";
import QuizPanel from "./components/quiz/QuizPanel";

const App = () => {
  const [activeTab, setActiveTab] = useState("home");

  const renderContent = () => {
    switch (activeTab) {
      case "home":
        return <HomePage onNavigate={setActiveTab} />;
      case "triage":
        return (
          <main className="max-w-5xl mx-auto px-6 py-10">
            <TriagePanel />
          </main>
        );
      case "quiz":
        return (
          <main className="max-w-5xl mx-auto px-6 py-10">
            <QuizPanel />
          </main>
        );
      default:
        return <HomePage onNavigate={setActiveTab} />;
    }
  };

  return (
    <div
      className="min-h-screen"
      style={{ background: "#040B14", color: "#F8FAFC" }}
    >
      {/* Header always visible */}
      <Header activeTab={activeTab} onTabChange={setActiveTab} />

      {/* Page content */}
      {renderContent()}
    </div>
  );
};

export default App;