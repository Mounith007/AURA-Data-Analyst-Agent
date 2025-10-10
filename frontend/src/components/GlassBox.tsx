import React, { useState } from 'react';
import { useTheme } from '../contexts/ThemeContext';
import './GlassBox.css';

interface GlassBoxProps {
  title?: string;
  children?: React.ReactNode;
}

const GlassBox: React.FC<GlassBoxProps> = ({ 
  title = "Glass Box Panel", 
  children 
}) => {
  const { theme } = useTheme();
  const [activeView, setActiveView] = useState<'overview' | 'insights' | 'settings'>('overview');

  const renderContent = () => {
    switch (activeView) {
      case 'overview':
        return (
          <div className="glass-overview">
            <div className="overview-cards">
              <div className="overview-card">
                <div className="card-icon">📊</div>
                <div className="card-content">
                  <h4>Data Analytics</h4>
                  <p>Ready for real-time data processing and visualization</p>
                  <div className="card-stats">
                    <span className="stat">
                      <span className="stat-value">-</span>
                      <span className="stat-label">Waiting for Data</span>
                    </span>
                  </div>
                </div>
              </div>
              
              <div className="overview-card">
                <div className="card-icon">🎯</div>
                <div className="card-content">
                  <h4>Insights Engine</h4>
                  <p>AI-powered analysis ready to discover patterns</p>
                  <div className="card-stats">
                    <span className="stat">
                      <span className="stat-value">-</span>
                      <span className="stat-label">No Data Yet</span>
                    </span>
                  </div>
                </div>
              </div>
              
              <div className="overview-card">
                <div className="card-icon">⚡</div>
                <div className="card-content">
                  <h4>System Status</h4>
                  <p>All systems operational and ready</p>
                  <div className="card-stats">
                    <span className="stat">
                      <span className="stat-value">✓</span>
                      <span className="stat-label">Online</span>
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        );
      
      case 'insights':
        return (
          <div className="glass-insights">
            <div className="insights-empty">
              <div className="empty-insights-icon">�</div>
              <h4>Insights Awaiting Data</h4>
              <p>Upload data files or connect to databases to generate AI-powered insights and trend analysis.</p>
              <div className="insight-features">
                <div className="feature-item">
                  <span className="feature-icon">�</span>
                  <span>Trend Detection</span>
                </div>
                <div className="feature-item">
                  <span className="feature-icon">🎯</span>
                  <span>Pattern Analysis</span>
                </div>
                <div className="feature-item">
                  <span className="feature-icon">💡</span>
                  <span>Smart Recommendations</span>
                </div>
              </div>
            </div>
          </div>
        );
      
      case 'settings':
        return (
          <div className="glass-settings">
            <div className="settings-group">
              <h4>Display Options</h4>
              <div className="setting-item">
                <label>
                  <input type="checkbox" defaultChecked />
                  Show real-time updates
                </label>
              </div>
              <div className="setting-item">
                <label>
                  <input type="checkbox" defaultChecked />
                  Enable animations
                </label>
              </div>
              <div className="setting-item">
                <label>
                  <input type="checkbox" />
                  Show debug information
                </label>
              </div>
            </div>
            
            <div className="settings-group">
              <h4>Data Preferences</h4>
              <div className="setting-item">
                <label>
                  Auto-refresh interval:
                  <select defaultValue="30">
                    <option value="10">10 seconds</option>
                    <option value="30">30 seconds</option>
                    <option value="60">1 minute</option>
                    <option value="300">5 minutes</option>
                  </select>
                </label>
              </div>
            </div>
          </div>
        );
      
      default:
        return children ? (
          <div className="glass-custom">
            {children}
          </div>
        ) : (
          <div className="glass-default">
            <div className="glass-placeholder">
              <div className="placeholder-icon">✨</div>
              <h3>Glass Box Panel</h3>
              <p>This is a dynamic glass effect panel with blur and transparency</p>
            </div>
          </div>
        );
    }
  };

  return (
    <div className="glass-box" data-theme={theme}>
      <div className="glass-header">
        <h3>{title}</h3>
        <div className="glass-tabs">
          <button
            className={`glass-tab ${activeView === 'overview' ? 'active' : ''}`}
            onClick={() => setActiveView('overview')}
          >
            📊 Overview
          </button>
          <button
            className={`glass-tab ${activeView === 'insights' ? 'active' : ''}`}
            onClick={() => setActiveView('insights')}
          >
            🎯 Insights
          </button>
          <button
            className={`glass-tab ${activeView === 'settings' ? 'active' : ''}`}
            onClick={() => setActiveView('settings')}
          >
            ⚙️ Settings
          </button>
        </div>
      </div>
      
      <div className="glass-content">
        {renderContent()}
      </div>
    </div>
  );
};

export default GlassBox;