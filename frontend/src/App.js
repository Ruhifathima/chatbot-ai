import React, { useState } from "react";
import axios from "axios";

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const sendMessage = async () => {
    if (!input.trim()) return;
    
    const userMessage = { role: "user", content: input };
    setMessages([...messages, userMessage]); // Add user message to chat

    try {
      const response = await axios.post("http://127.0.0.1:8000/chat", {
        message: input,
      });

      const aiMessage = { role: "ai", content: response.data.response };
      setMessages([...messages, userMessage, aiMessage]); // Add AI response
      setInput(""); // Clear input field
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <div style={{ maxWidth: "600px", margin: "auto", padding: "20px" }}>
      <h2>Chatbot</h2>
      <div style={{ border: "1px solid #ddd", padding: "10px", height: "400px", overflowY: "scroll" }}>
        {messages.map((msg, index) => (
          <p key={index} style={{ textAlign: msg.role === "user" ? "right" : "left" }}>
            <strong>{msg.role === "user" ? "You: " : "Bot: "}</strong>
            {msg.content}
          </p>
        ))}
      </div>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Type a message..."
        style={{ width: "80%", padding: "10px" }}
      />
      <button onClick={sendMessage} style={{ padding: "10px" }}>Send</button>
    </div>
  );
}

export default App;
