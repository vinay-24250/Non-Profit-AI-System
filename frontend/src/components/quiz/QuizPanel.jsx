// src/components/quiz/QuizPanel.jsx
import { useState } from "react";
import { generateQuestion, evaluateAnswer } from "../../api/apiClient";
import TopicSelector from "./TopicSelector";
import QuestionCard from "./QuestionCard";
import EvalResult from "./EvalResult";
import SessionScore from "./SessionScore";

const QuizPanel = () => {
  const [topic,      setTopic]      = useState("");
  const [difficulty, setDifficulty] = useState("medium");
  const [question,   setQuestion]   = useState(null);
  const [selected,   setSelected]   = useState(null);
  const [evalResult, setEvalResult] = useState(null);

  const [loadingQ,   setLoadingQ]   = useState(false); // generating question
  const [loadingE,   setLoadingE]   = useState(false); // evaluating answer
  const [error,      setError]      = useState(null);

  const [score, setScore] = useState({ total: 0, correct: 0 });

  // ── Generate a new question ────────────────────────────────────────────────
  const handleGenerate = async () => {
    if (!topic.trim()) return;
    setLoadingQ(true);
    setQuestion(null);
    setSelected(null);
    setEvalResult(null);
    setError(null);

    try {
      const q = await generateQuestion(topic, difficulty);
      setQuestion(q);
    } catch (e) {
      setError(
        e?.response?.data?.detail ||
        "Backend unreachable — start FastAPI on port 8000."
      );
    } finally {
      setLoadingQ(false);
    }
  };

  // ── Evaluate chosen answer ─────────────────────────────────────────────────
  const handleAnswer = async (opt) => {
    if (!question || selected) return;
    setSelected(opt);
    setLoadingE(true);

    try {
      const letter = opt.charAt(0);
      const ev = await evaluateAnswer(
        question.question,
        question.correct_answer,
        letter,
        question.topic
      );
      setEvalResult(ev);

      // Update score + adaptive difficulty
      setScore((s) => ({
        total:   s.total + 1,
        correct: s.correct + (ev.is_correct ? 1 : 0),
      }));
      if (ev.next_difficulty) setDifficulty(ev.next_difficulty);
    } catch (e) {
      setError("Evaluation failed — check your backend.");
    } finally {
      setLoadingE(false);
    }
  };

  return (
    <div className="space-y-6 animate-[fadeUp_0.35s_ease_forwards]">
      {/* Section header */}
      <div>
        <h2 className="font-['Syne'] text-2xl font-bold text-[#e8e8f0] mb-1">
          🎓 Educational Quiz Bot
        </h2>
        <p className="text-[0.77rem] font-mono text-[#6b6b88] leading-relaxed max-w-2xl">
          Select a donor communications topic, generate an AI-crafted MCQ, and receive
          deep contextual feedback on your answer — powered by Llama 3.1 via Groq.
        </p>
      </div>

      {/* Session score (only after first answer) */}
      {score.total > 0 && (
        <SessionScore score={score} difficulty={difficulty} />
      )}

      {/* Topic + difficulty + generate */}
      <TopicSelector
        topic={topic}
        onTopicChange={setTopic}
        difficulty={difficulty}
        onDifficultyChange={setDifficulty}
        onGenerate={handleGenerate}
        loading={loadingQ}
      />

      {/* Error state */}
      {error && (
        <div className="bg-red-500/10 border border-red-500/30 rounded-xl px-5 py-3">
          <p className="text-red-400 text-sm font-mono">⚠ {error}</p>
        </div>
      )}

      {/* Question */}
      {question && (
        <QuestionCard
          question={question}
          selected={selected}
          onAnswer={handleAnswer}
        />
      )}

      {/* Evaluation result */}
      <EvalResult
        evalResult={evalResult}
        loading={loadingE}
        onNext={handleGenerate}
        loadingNext={loadingQ}
      />
    </div>
  );
};

export default QuizPanel;