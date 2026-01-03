import React, { useState, useRef, useEffect } from 'react';
import { BsChatQuoteFill, BsSend, BsX } from 'react-icons/bs';
import axios from 'axios';

// Configure API URL from environment or default to localhost
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

const ChatWidget: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    { role: 'assistant', content: 'Hi! I am James\'s AI assistant. Ask me anything about his skills or experience.' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = input.trim();
    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setIsLoading(true);

    try {
      const response = await axios.post(`${API_BASE_URL}/chat/`, {
        message: userMessage
      });
      
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: response.data.response 
      }]);
    } catch (error) {
      console.error('Chat error:', error);
      let errorMessage = 'Sorry, I encountered an error. Please try again later.';

      if (axios.isAxiosError(error)) {
        if (error.response?.status === 429) {
          errorMessage = 'Too many requests. Please wait a moment and try again.';
        } else if (error.response?.status === 500) {
          errorMessage = 'Server error. The assistant is temporarily unavailable.';
        } else if (!error.response) {
          errorMessage = 'Cannot connect to the assistant. Please check your internet connection.';
        }
      }

      setMessages(prev => [...prev, {
        role: 'assistant',
        content: errorMessage
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="fixed bottom-6 left-6 z-50 font-sans">
      {/* Chat Window */}
      {isOpen && (
        <div className="mb-4 w-[350px] rounded-2xl bg-base-100 shadow-2xl overflow-hidden border border-base-300 flex flex-col h-[500px]">
          {/* Header */}
          <div className="bg-primary p-4 flex justify-between items-center text-primary-content">
            <h3 className="font-bold flex items-center gap-2">
              <BsChatQuoteFill /> Assistant
            </h3>
            <button 
              onClick={() => setIsOpen(false)}
              className="hover:bg-primary-focus p-1 rounded-full transition-colors"
            >
              <BsX size={24} />
            </button>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-base-200/50">
            {messages.map((msg, idx) => (
              <div
                key={idx}
                className={`flex w-full ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[80%] rounded-2xl px-4 py-2 text-sm ${
                    msg.role === 'user' 
                      ? 'bg-primary text-primary-content rounded-br-none' 
                      : 'bg-base-100 border border-base-300 rounded-bl-none'
                  }`}
                >
                  {msg.content}
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-base-100 border border-base-300 rounded-2xl rounded-bl-none px-4 py-2 text-sm">
                  <span className="loading loading-dots loading-xs"></span>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <form onSubmit={handleSubmit} className="p-3 bg-base-100 border-t border-base-300 flex gap-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your question..."
              className="input input-sm input-bordered flex-1 rounded-full"
              disabled={isLoading}
            />
            <button 
              type="button"
              onClick={handleSubmit} 
              className="btn btn-sm btn-circle btn-primary"
              disabled={isLoading || !input.trim()}
            >
              <BsSend />
            </button>
          </form>
        </div>
      )}

      {/* Toggle Button */}
      {!isOpen && (
        <button
          onClick={() => setIsOpen(true)}
          className="btn btn-circle btn-lg btn-primary shadow-lg hover:scale-110 transition-transform"
        >
          <BsChatQuoteFill size={28} />
        </button>
      )}
    </div>
  );
};

export default ChatWidget;
