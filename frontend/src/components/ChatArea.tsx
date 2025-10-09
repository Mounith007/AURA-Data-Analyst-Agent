import React from 'react';
import MessageList from './MessageList';
import ChatInput from './ChatInput';

interface ChatAreaProps {
  onQuerySubmit: (prompt: string) => Promise<void>;
  isLoading: boolean;
}

const ChatArea: React.FC<ChatAreaProps> = ({ onQuerySubmit, isLoading }) => {
  return (
    <div className="chat-area">
      <MessageList />
      <ChatInput onQuerySubmit={onQuerySubmit} isLoading={isLoading} />
    </div>
  );
};

export default ChatArea;