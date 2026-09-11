import { useState } from "react";

const API = "http://localhost:5000/api";

export default function App() {
  const [messages, setMessages] = useState([
    { role: "assistant", content: "Hi! I'm the ConneX AI Operator. Ask me about a lead or ask me to create a task." }
  ]);
  const [input, setInput] = useState("");
  const [pending, setPending] = useState(null);
  const [loading, setLoading] = useState(false);

  async function sendMessage(text = input) {
    const message = text.trim();
    if (!message || loading) return;
    setMessages(m => [...m, { role: "user", content: message }]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch(`${API}/chat`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({message, pending})
      });
      const data = await res.json();
      setMessages(m => [...m, {role: "assistant", content: data.reply}]);
      setPending(data.pending);
    } catch {
      setMessages(m => [...m, {
        role: "assistant",
        content: "I couldn't connect to the backend. Make sure Flask is running on port 5000."
      }]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="app">
      <section className="panel">
        <header>
          <div>
            <h1>ConneX AI Operator</h1>
            <p>Ask questions or ask the operator to perform a task.</p>
          </div>
          <span className="status">● Online</span>
        </header>

        <div className="chat">
          {messages.map((m, i) => (
            <div key={i} className={`message ${m.role}`}>
              <div className="label">{m.role === "user" ? "You" : "AI Operator"}</div>
              <div className="bubble">{m.content}</div>
            </div>
          ))}
          {loading && (
            <div className="message assistant">
              <div className="label">AI Operator</div>
              <div className="bubble">Thinking...</div>
            </div>
          )}
        </div>

        <div className="composer">
          <input
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={e => e.key === "Enter" && sendMessage()}
            placeholder="Try: Tell me about Sarah Johnson"
          />
          <button onClick={() => sendMessage()} disabled={loading}>Send</button>
        </div>

        <div className="hint">
          Try:
          <button onClick={() => sendMessage("Tell me about Sarah Johnson")}>Ask about Sarah</button>
          <button onClick={() => sendMessage("Create a task to call Sarah Johnson tomorrow")}>Create a task</button>
        </div>
      </section>
    </main>
  );
}