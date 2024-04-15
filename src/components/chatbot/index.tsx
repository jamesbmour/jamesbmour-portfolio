import React, { useState } from 'react';
import axios from 'axios';
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
      handleBotResponse(userInput);
    }
  };

  const handleBotResponse = (userInput: string) => {
    // Placeholder for your API key, replace with a secure method to handle keys
    const apiKey = 'your-openai-api-key';
    const apiUrl = 'https://api.openai.com/v1/engines/davinci/completions';

    const headers = {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${apiKey}`,
    };

    const data = {
      prompt: userInput,
      max_tokens: 150,
    };

    axios
      .post(apiUrl, data, { headers })
      .then((response) => {
        const botResponse = response.data.choices[0].text.trim();
        sendMessage(botResponse, 'bot');
      })
      .catch((error) => {
        console.error('Error responding:', error);
        sendMessage("I'm having trouble responding right now.", 'bot');
      });
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
