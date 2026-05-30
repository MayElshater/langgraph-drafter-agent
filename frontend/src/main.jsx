import React, { useEffect, useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import { FileText, Save, Send, Sparkles } from "lucide-react";
import "./styles.css";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

function createSessionId() {
  const existing = localStorage.getItem("drafter_session_id");
  if (existing) return existing;

  const next = crypto.randomUUID();
  localStorage.setItem("drafter_session_id", next);
  return next;
}

function App() {
  const sessionId = useMemo(createSessionId, []);
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content: "Hi, I am Drafter. Tell me what you want to write or paste a rough draft to improve.",
    },
  ]);
  const [input, setInput] = useState("");
  const [documentContent, setDocumentContent] = useState("");
  const [toolStatus, setToolStatus] = useState("No tool used yet.");
  const [filename, setFilename] = useState("document.txt");
  const [isSending, setIsSending] = useState(false);
  const [isSaving, setIsSaving] = useState(false);

  useEffect(() => {
    fetch(`${API_URL}/document/${sessionId}`)
      .then((response) => response.json())
      .then((data) => setDocumentContent(data.document_content || ""))
      .catch(() => setToolStatus("Backend is not reachable yet."));
  }, [sessionId]);

  async function sendMessage(event) {
    event.preventDefault();
    const trimmed = input.trim();
    if (!trimmed || isSending) return;

    setMessages((current) => [...current, { role: "user", content: trimmed }]);
    setInput("");
    setIsSending(true);
    setToolStatus("Thinking...");

    try {
      const response = await fetch(`${API_URL}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id: sessionId, message: trimmed }),
      });

      if (!response.ok) {
        throw new Error("Chat request failed.");
      }

      const data = await response.json();
      setMessages((current) => [...current, { role: "assistant", content: data.ai_message }]);
      setDocumentContent(data.document_content || "");
      setToolStatus(data.tool_used ? `${data.tool_used}: ${data.tool_result}` : "No tool used for this response.");
    } catch (error) {
      setMessages((current) => [
        ...current,
        { role: "assistant", content: "I could not reach the backend. Check that FastAPI is running." },
      ]);
      setToolStatus(error.message);
    } finally {
      setIsSending(false);
    }
  }

  async function saveDocument() {
    setIsSaving(true);
    setToolStatus("Saving document...");

    try {
      const response = await fetch(`${API_URL}/save`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id: sessionId, filename }),
      });

      if (!response.ok) {
        throw new Error("Save request failed.");
      }

      const data = await response.json();
      setToolStatus(data.message);
    } catch (error) {
      setToolStatus(error.message);
    } finally {
      setIsSaving(false);
    }
  }

  return (
    <main className="app-shell">
      <section className="workspace">
        <div className="topbar">
          <div>
            <p className="eyebrow">LangGraph + Gemini</p>
            <h1>AI Document Drafter</h1>
          </div>
          <div className="status-pill">
            <Sparkles size={16} />
            Portfolio Demo
          </div>
        </div>

        <div className="panels">
          <section className="chat-panel" aria-label="Chat">
            <div className="panel-header">
              <h2>Chat</h2>
              <span>{messages.length} messages</span>
            </div>

            <div className="message-list">
              {messages.map((message, index) => (
                <div className={`message ${message.role}`} key={`${message.role}-${index}`}>
                  {message.content}
                </div>
              ))}
            </div>

            <form className="composer" onSubmit={sendMessage}>
              <textarea
                value={input}
                onChange={(event) => setInput(event.target.value)}
                placeholder="Ask Drafter to write, revise, summarize, or save..."
                rows={3}
              />
              <button type="submit" disabled={isSending || !input.trim()} title="Send message">
                <Send size={18} />
                {isSending ? "Sending" : "Send"}
              </button>
            </form>
          </section>

          <section className="document-panel" aria-label="Document preview">
            <div className="panel-header">
              <h2>
                <FileText size={19} />
                Document
              </h2>
              <span>{documentContent.length} chars</span>
            </div>

            <div className="document-preview">
              {documentContent || "Your draft will appear here after the agent updates the document."}
            </div>

            <div className="save-row">
              <input
                value={filename}
                onChange={(event) => setFilename(event.target.value)}
                aria-label="Filename"
              />
              <button type="button" onClick={saveDocument} disabled={isSaving} title="Save document">
                <Save size={18} />
                {isSaving ? "Saving" : "Save"}
              </button>
            </div>

            <div className="tool-status">
              <span>Tool status</span>
              <p>{toolStatus}</p>
            </div>
          </section>
        </div>
      </section>
    </main>
  );
}

createRoot(document.getElementById("root")).render(<App />);
