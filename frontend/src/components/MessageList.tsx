
import React, { useEffect, useRef } from 'react';
import { useTheme } from '../contexts/ThemeContext';

export interface Message {
  id: string;
  type: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: Date;
  isLoading?: boolean;
  data?: any;
}

interface MessageListProps {
  messages: Message[];
  isTyping?: boolean;
  onQuickAction?: (action: string) => void;
}

const MessageList: React.FC<MessageListProps> = ({ messages, isTyping, onQuickAction }) => {
  const { theme } = useTheme();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  const welcomeCards = [
    {
      icon: '🚀',
      title: 'Get Started',
      description: 'Ask me to analyze your data or create visualizations',
      example: 'Show me sales trends for the last quarter',
      action: 'analyze_trends'
    },
    {
      icon: '📊',
      title: 'Data Analysis',
      description: 'I can help you understand patterns in your data',
      example: 'What are the top performing products?',
      action: 'create_chart'
    },
    {
      icon: '🔍',
      title: 'Smart Insights',
      description: 'Get AI-powered insights and recommendations',
      example: 'Find anomalies in customer behavior',
      action: 'find_insights'
    }
  ];

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const renderMessage = (message: Message) => {
    return (
      <div key={message.id} className={`message ${message.type}`}>
        <div className="message-avatar">
          {message.type === 'user' ? '👤' : message.type === 'assistant' ? '🤖' : '💡'}
        </div>
        <div className="message-content">
          <div className="message-header">
            <span className="message-sender">
              {message.type === 'user' ? 'You' : message.type === 'assistant' ? 'AURA' : 'System'}
            </span>
            <span className="message-time">{formatTime(message.timestamp)}</span>
          </div>
          <div className="message-text">
            {message.isLoading ? (
              <div className="message-loading">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
                <span>AURA is thinking...</span>
              </div>
            ) : (
              <>
                {message.content}
                {message.data && (
                  <div className="message-data">
                    <pre>{JSON.stringify(message.data, null, 2)}</pre>
                  </div>
                )}
              </>
            )}
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="message-list" data-theme={theme}>
      {messages.length === 0 ? (
        <div className="welcome-section">
          <div className="welcome-header">
            <h2>👋 Welcome to AURA</h2>
            <p>Your AI-powered data analysis assistant</p>
          </div>
          
          <div className="welcome-cards">
            {welcomeCards.map((card, index) => (
              <div 
                key={index} 
                className="welcome-card"
                onClick={() => onQuickAction?.(card.action)}
              >
                <div className="card-icon">{card.icon}</div>
                <div className="card-content">
                  <h3>{card.title}</h3>
                  <p>{card.description}</p>
                  <div className="card-example">
                    <span className="example-label">Try: </span>
                    <span className="example-text">"{card.example}"</span>
                  </div>
                </div>
              </div>
            ))}
          </div>

          <div className="quick-actions">
            <h4>🎯 Quick Actions</h4>
            <div className="action-buttons">
              <button className="action-btn" onClick={() => onQuickAction?.('create_chart')}>
                📈 Create Chart
              </button>
              <button className="action-btn" onClick={() => onQuickAction?.('connect_database')}>
                🗄️ Connect Database
              </button>
              <button className="action-btn" onClick={() => onQuickAction?.('analyze_data')}>
                🔍 Analyze Data
              </button>
            </div>
          </div>
        </div>
      ) : (
        <div className="conversation">
          {messages.map(renderMessage)}
          {isTyping && (
            <div className="message assistant typing">
              <div className="message-avatar">🤖</div>
              <div className="message-content">
                <div className="message-header">
                  <span className="message-sender">AURA</span>
                  <span className="message-time">{formatTime(new Date())}</span>
                </div>
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      )}
    </div>
  );
};

export default MessageList;
