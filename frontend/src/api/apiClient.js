import axios from "axios";

const apiClient = axios.create({
baseURL: "http://3.6.190.26:8080",
  headers: { "Content-Type": "application/json" },
  timeout: 30000,
})

// http://15.207.184.18:3000/

export const runTriage = (text) =>
  apiClient.post("/api/triage", { text }).then((r) => r.data);

export const generateQuestion = (topic, difficulty) =>
  apiClient.post("/api/quiz/generate", { topic, difficulty }).then((r) => r.data);

export const evaluateAnswer = (question, correct_answer, user_answer, topic) =>
  apiClient
    .post("/api/quiz/evaluate", { question, correct_answer, user_answer, topic })
    .then((r) => r.data);

export const healthCheck = () =>
  apiClient.get("/health").then((r) => r.data);

export default apiClient;