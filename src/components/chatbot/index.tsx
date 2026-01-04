/**
 * Main Chatbot Component
 * Manages chat state and API communication
 */
import React, { useState, useCallback } from 'react';
import ChatButton from './ChatButton';
import ChatWindow from './ChatWindow';
import { Message, ChatState } from './types';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const Chatbot: React.FC = () => {
  const [chatState, setChatState] = useState<ChatState>({
    isOpen: false,
    messages: [],
    isLoading: false,
    error: null,
  });

  const toggleChat = useCallback(() => {
    setChatState((prev) => ({
      ...prev,
      isOpen: !prev.isOpen,
      error: null,
    }));
  }, []);

  const closeChat = useCallback(() => {
    setChatState((prev) => ({
      ...prev,
      isOpen: false,
      error: null,
    }));
  }, []);

  const sendMessage = useCallback(async (messageText: string) => {
    // Create user message
    const userMessage: Message = {
      id: `user-${Date.now()}`,
      content: messageText,
      sender: 'user',
      timestamp: new Date(),
    };

    // Add user message to chat
    setChatState((prev) => ({
      ...prev,
      messages: [...prev.messages, userMessage],
      isLoading: true,
      error: null,
    }));

    try {
      // Call backend API
      const response = await fetch(`${API_URL}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: messageText,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      if (!data.success) {
        throw new Error(data.error || 'Failed to get response');
      }

      // Create bot message
      const botMessage: Message = {
        id: `bot-${Date.now()}`,
        content: data.response,
        sender: 'bot',
        timestamp: new Date(),
        sources: data.sources || [],
      };

      // Add bot message to chat
      setChatState((prev) => ({
        ...prev,
        messages: [...prev.messages, botMessage],
        isLoading: false,
      }));
    } catch (error) {
      console.error('Error sending message:', error);

      const errorMessage =
        error instanceof Error ? error.message : 'Failed to send message. Please try again.';

      setChatState((prev) => ({
        ...prev,
        isLoading: false,
        error: errorMessage,
      }));

      // Add error as bot message
      const errorBotMessage: Message = {
        id: `bot-error-${Date.now()}`,
        content: `Sorry, I encountered an error: ${errorMessage}. Please make sure the backend server is running.`,
        sender: 'bot',
        timestamp: new Date(),
      };

      setChatState((prev) => ({
        ...prev,
        messages: [...prev.messages, errorBotMessage],
      }));
    }
  }, []);

  return (
    <>
      <ChatButton onClick={toggleChat} isOpen={chatState.isOpen} />
      <ChatWindow
        isOpen={chatState.isOpen}
        onClose={closeChat}
        messages={chatState.messages}
        isLoading={chatState.isLoading}
        error={chatState.error}
        onSendMessage={sendMessage}
      />
    </>
  );
};

export default Chatbot;
