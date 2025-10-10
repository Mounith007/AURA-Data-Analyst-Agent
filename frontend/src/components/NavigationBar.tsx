import React from 'react';
import './NavigationBar.css';
import ThemeToggle from './ThemeToggle';

interface NavigationBarProps {
  currentMode: 'chat' | 'database' | 'visualization' | 'strategic';
  onModeChange: (mode: 'chat' | 'database' | 'visualization' | 'strategic') => void;
}

const NavigationBar: React.FC<NavigationBarProps> = () => {

  return (
    <nav className="navigation-bar">
      <div className="nav-left">
        <div className="nav-brand">
          <div className="brand-logo">
            <div className="logo-icon">🚀</div>
            <div className="logo-glow"></div>
          </div>
          <div className="brand-text">
            <h1>AURA</h1>
            <p>Advanced Unified Research Analytics</p>
            <div className="brand-tagline">Powered by AI Intelligence</div>
          </div>
        </div>
        <div className="connection-status">
          <div className="status-dot online"></div>
          <span className="status-text">All Systems Online</span>
        </div>
      </div>

      <div className="nav-controls">
        <ThemeToggle />
      </div>
    </nav>
  );
};

export default NavigationBar;