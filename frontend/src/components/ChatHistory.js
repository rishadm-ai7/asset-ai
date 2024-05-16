import React from "react";

function ChatHistory({ messages }) {
  return (
    <div className="chat-history">
      {messages.map((msg, index) => (
        <div key={index} className={`message ${msg.user}`}>
          <strong>{msg.user}:</strong> {msg.text.replace(`${msg.user}: `, "")}
        </div>
      ))}
    </div>
  );
}

export default ChatHistory;
