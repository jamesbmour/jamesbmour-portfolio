import React, { useState } from 'react';
import './Chatbot.css'; // Ensure you have corresponding CSS for styling

interface Message {
  text: string;
  sender: 'user' | 'bot';
}

const Chatbot: React.FC = () => {
  const [isOpen, setIsOpen] = useState<boolean>(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputText, setInputText] = useState<string>('');

  const toggleChat = () => setIsOpen(!isOpen);

  const sendMessage = (text: string, sender: 'user' | 'bot') => {
    if (text.trim().length > 0) {
      setMessages((prevMessages) => [...prevMessages, { text, sender }]);
    }
  };

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setInputText(event.target.value);
  };

  const handleUserInput = async (
    event: React.KeyboardEvent<HTMLInputElement>,
  ) => {
    if (event.key === 'Enter' && inputText.trim()) {
      sendMessage(inputText, 'user');
      await handleBotResponse(inputText);
      setInputText(''); // Clear input field after sending
    }
  };

  const handleBotResponse = async (userInput: string) => {
    const apiUrl = 'http://localhost:8000/chat/';
    const data = {
      message: userInput,
    };

    try {
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });
      const result = await response.json();
      sendMessage(result.response, 'bot');
    } catch (error) {
      console.error('Error responding:', error);
      sendMessage("I'm having trouble responding right now.", 'bot');
    }
  };

  const clearChat = () => {
    setMessages([]); // Clear the chat history
  };

  return (
    <div className="chatbot-container">
      <button onClick={toggleChat} className="chat-toggle">
        {isOpen ? 'Close Chat' : 'Chat'}
      </button>
      {isOpen && (
        <div className="chat-window">
          <div className="message-container">
            <button
              onClick={clearChat}
              className="btn btn-outline btn-sm text-xs opacity-50 "
            >
              Clear Chat
            </button>
            {messages.map((msg, index) => (
              <div key={index} className={`message ${msg.sender}`}>
                {msg.text}
              </div>
            ))}
          </div>
          <div>
            <input
              type="text"
              className="message-input"
              placeholder="Type a message..."
              value={inputText}
              onChange={handleInputChange}
              onKeyPress={handleUserInput}
            />
          </div>
        </div>
      )}
    </div>
  );
};

export default Chatbot;
