import React, { useState } from 'react';

interface ChatInputProps {
  onQuerySubmit: (prompt: string) => Promise<void>;
  isLoading: boolean;
}

const ChatInput: React.FC<ChatInputProps> = ({ onQuerySubmit, isLoading }) => {
  const [message, setMessage] = useState('');

  const handleSend = async () => {
    if (message.trim() && !isLoading) {
      await onQuerySubmit(message);
      setMessage('');
    }
  };

  return (
    <div className="chat-input">
      <input
        type="text"
        placeholder="Ask about your data (e.g., 'Show me total revenue by product')..."
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        onKeyPress={(e) => e.key === 'Enter' && handleSend()}
        disabled={isLoading}
      />
      <button onClick={handleSend} disabled={isLoading}>
        {isLoading ? 'Processing...' : 'Send'}
      </button>
    </div>
  );
};

export default ChatInput;