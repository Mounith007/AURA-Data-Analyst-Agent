import React from 'react';
import './NavigationBar.css';

interface NavigationBarProps {
  currentMode: 'chat' | 'database' | 'visualization' | 'strategic';
  onModeChange: (mode: 'chat' | 'database' | 'visualization' | 'strategic') => void;
}

const NavigationBar: React.FC<NavigationBarProps> = ({ currentMode, onModeChange }) => {
  const modes = [
    { key: 'chat', label: '💬 AI Chat', icon: '🤖', description: 'Interactive AI Assistant' },
    { key: 'database', label: '🗄️ Databases', icon: '🔗', description: 'Connect & Manage' },
    { key: 'visualization', label: '📊 Visualize', icon: '📈', description: 'Create Charts' },
    { key: 'strategic', label: '🚀 Strategy', icon: '⭐', description: 'Strategic Vision' }
  ] as const;

  return (
    <nav className="navigation-bar">
      <div className="nav-brand">
        <div className="brand-logo">🌟</div>
        <div className="brand-text">
          <h1>AURA</h1>
          <p>Analyst in a Box</p>
        </div>
      </div>

      <div className="nav-modes">
        {modes.map((mode) => (
          <button
            key={mode.key}
            className={`nav-mode ${currentMode === mode.key ? 'active' : ''}`}
            onClick={() => onModeChange(mode.key as any)}
            title={mode.description}
          >
            <span className="mode-icon">{mode.icon}</span>
            <span className="mode-label">{mode.label}</span>
          </button>
        ))}
      </div>

      <div className="nav-status">
        <div className="connection-status">
          <div className="status-indicator active"></div>
          <span>All Systems Online</span>
        </div>
      </div>
    </nav>
  );
};

export default NavigationBar;