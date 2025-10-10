import React from 'react';
import MessageList from './MessageList';
import ChatInput from './ChatInput';

export interface Message {
  id: string;
  type: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: Date;
  data?: any;
}

interface ChatAreaProps {
  onQuerySubmit: (prompt: string) => Promise<void>;
  isLoading: boolean;
  messages?: Message[];
  isTyping?: boolean;
  onQuickAction?: (action: string) => void;
}

const ChatArea: React.FC<ChatAreaProps> = ({ 
  onQuerySubmit, 
  isLoading, 
  messages = [],
  isTyping = false,
  onQuickAction
}) => {
  return (
    <div className="chat-area">
      <MessageList 
        messages={messages}
        isTyping={isTyping}
        onQuickAction={onQuickAction}
      />
      <ChatInput onQuerySubmit={onQuerySubmit} isLoading={isLoading} />
    </div>
  );
};

export default ChatArea;