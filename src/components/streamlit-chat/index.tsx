import React, { useState } from 'react';

interface Message {
  text: string;
  sender: 'user' | 'bot';
}

const StreamlitApp: React.FC = () => {
  const [isOpen, setIsOpen] = useState<boolean>(false);

  const toggleChat = () => setIsOpen(!isOpen);

  return (
    <div className="fixed bottom-5 right-5 z-50">
      <button onClick={toggleChat} className="px-5 py-2.5 bg-blue-800 text-white rounded-lg cursor-pointer focus:outline-none">
        {isOpen ? 'Close Chat' : 'Chat'}
      </button>
      {isOpen && (
        <div className="absolute bottom-12 right-0 w-[800px] h-[600px] bg-gray-900 border border-gray-300 shadow-2xl rounded-lg overflow-hidden">
          <iframe
            src="https://pdfchat-eustkxjfhdghra4qgvs2yr.streamlit.app/?embed=true"
            title="Streamlit Chat"
            className="w-full h-full border-none"
          />
        </div>
      )}
    </div>
  );
};

export default StreamlitApp;
