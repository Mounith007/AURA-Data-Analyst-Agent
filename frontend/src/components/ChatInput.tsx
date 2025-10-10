import React, { useState } from 'react';
import { useTheme } from '../contexts/ThemeContext';

interface ChatInputProps {
  onQuerySubmit: (prompt: string) => Promise<void>;
  isLoading: boolean;
}

const ChatInput: React.FC<ChatInputProps> = ({ onQuerySubmit, isLoading }) => {
  const { theme } = useTheme();
  const [message, setMessage] = useState('');

  const handleSend = async () => {
    if (message.trim() && !isLoading) {
      await onQuerySubmit(message);
      setMessage('');
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const quickSuggestions = [
    '📊 Show me sales data',
    '📈 Create a revenue chart',
    '🔍 Find data patterns',
    '📋 Generate summary report'
  ];

  return (
    <div className="chat-input-container" data-theme={theme}>
      <div className="quick-suggestions">
        {quickSuggestions.map((suggestion, index) => (
          <button 
            key={index}
            className="suggestion-chip"
            onClick={() => setMessage(suggestion.substring(2))}
            disabled={isLoading}
          >
            {suggestion}
          </button>
        ))}
      </div>
      
      <div className="chat-input">
        <div className="input-wrapper">
          <input
            type="text"
            placeholder="Ask about your data... (Press Enter to send, Shift+Enter for new line)"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            disabled={isLoading}
            className="chat-message-input"
          />
          {isLoading && (
            <div className="input-loader">
              <div className="loader-spinner"></div>
            </div>
          )}
        </div>
        
        <button 
          onClick={handleSend} 
          disabled={isLoading || !message.trim()}
          className="send-button"
        >
          {isLoading ? (
            <>
              <div className="button-spinner"></div>
              Processing...
            </>
          ) : (
            <>
              <span className="send-icon">🚀</span>
              Send
            </>
          )}
        </button>
      </div>
    </div>
  );
};

export default ChatInput;