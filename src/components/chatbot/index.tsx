import React, { useState } from 'react';
// import styles from './Chatbot.module.css'; // Import as an object
import './Chatbot.css'; // Import as a string

// Define types for messages
interface Message {
  text: string;
  sender: 'user' | 'bot';
}

const Chatbot: React.FC = () => {
  const [isOpen, setIsOpen] = useState<boolean>(false);
  const [messages, setMessages] = useState<Message[]>([]);

  const toggleChat = () => setIsOpen(!isOpen);

  const sendMessage = (text: string, sender: 'user' | 'bot') => {
    setMessages((prevMessages) => [...prevMessages, { text, sender }]);
  };

  const handleUserInput = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === 'Enter' && event.currentTarget.value) {
      const userInput = event.currentTarget.value;
      sendMessage(userInput, 'user');
      event.currentTarget.value = ''; // Clear input field
      handleBotResponse();
    }
  };

  const handleBotResponse = () => {
    // Simulate a bot response
    setTimeout(() => {
      sendMessage("I'm not able to respond to that right now.", 'bot');
    }, 1000);
  };

  return (
    <div className="chatbot-container">
      <button onClick={toggleChat} className="chat-toggle">
        {isOpen ? 'Close Chat' : 'Chat'}
      </button>
      {isOpen && (
        <div className="chat-window">
          <div className="message-container">
            {messages.map((msg, index) => (
              <div key={index} className={`message ${msg.sender}`}>
                {msg.text}
              </div>
            ))}
          </div>
          <input
            type="text"
            className="message-input"
            placeholder="Type a message..."
            onKeyPress={handleUserInput}
          />
        </div>
      )}
    </div>
  );
};

export default Chatbot;
