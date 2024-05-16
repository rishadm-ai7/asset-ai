import React, { useState } from "react";
import axios from "axios";

function ChatForm({ addMessage }) {
  const [chat, setChat] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    const response = await axios.post("http://localhost:8000/api/chat", {
      chat,
    });
    if (response.data) {
      addMessage({ user: "User", text: chat });
      addMessage({ user: "Chatbot", text: response.data.assistant_message });
    }
    setChat("");
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={chat}
        onChange={(e) => setChat(e.target.value)}
        placeholder="Type your message..."
      />
      <button type="submit">Send</button>
    </form>
  );
}

export default ChatForm;
