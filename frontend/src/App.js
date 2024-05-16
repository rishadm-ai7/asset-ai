import React, { useState } from "react";
import Header from "./components/Header";
import ChatForm from "./components/ChatForm";
import ChatHistory from "./components/ChatHistory";
import "./App.css";

function App() {
  const [messages, setMessages] = useState([]);

  const addMessage = (message) => {
    setMessages((prevMessages) => [...prevMessages, message]);
  };

  return (
    <div className="App">
      <Header />
      <ChatHistory messages={messages} />
      <ChatForm addMessage={addMessage} />
    </div>
  );
}

export default App;
