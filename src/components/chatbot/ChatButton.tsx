/**
 * Floating chat button component
 * Positioned in the bottom-left corner of the screen
 */
import React from 'react';
import { ChatButtonProps } from './types';

const ChatButton: React.FC<ChatButtonProps> = ({ onClick, isOpen, unreadCount = 0 }) => {
  return (
    <button
      onClick={onClick}
      className={`fixed bottom-5 left-5 z-50 w-14 h-14 rounded-full shadow-lg
        transition-all duration-300 ease-in-out transform hover:scale-110
        ${isOpen ? 'bg-red-500 hover:bg-red-600' : 'bg-blue-600 hover:bg-blue-700'}
        flex items-center justify-center`}
      aria-label={isOpen ? 'Close chat' : 'Open chat'}
    >
      {/* Chat Icon or Close Icon */}
      {isOpen ? (
        <svg
          className="w-6 h-6 text-white"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M6 18L18 6M6 6l12 12"
          />
        </svg>
      ) : (
        <svg
          className="w-6 h-6 text-white"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"
          />
        </svg>
      )}

      {/* Unread Badge */}
      {!isOpen && unreadCount > 0 && (
        <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs font-bold rounded-full h-5 w-5 flex items-center justify-center">
          {unreadCount > 9 ? '9+' : unreadCount}
        </span>
      )}
    </button>
  );
};

export default ChatButton;
