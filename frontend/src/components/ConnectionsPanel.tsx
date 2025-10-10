import React, { useState } from 'react';
import './ConnectionsPanel.css';

interface Connection {
  id: string;
  name: string;
  type: 'postgresql' | 'mysql' | 'mongodb' | 'sqlite' | 'api';
  status: 'connected' | 'disconnected' | 'connecting';
  host?: string;
  database?: string;
  lastConnected?: Date;
}

interface ConnectionsPanelProps {
  connections: Connection[];
  onConnectionSelect: (connection: Connection) => void;
  onNewConnection: () => void;
}

const ConnectionsPanel: React.FC<ConnectionsPanelProps> = ({
  connections,
  onConnectionSelect,
  onNewConnection,
}) => {
  const [selectedConnection, setSelectedConnection] = useState<string | null>(null);

  const getConnectionIcon = (type: Connection['type']) => {
    switch (type) {
      case 'postgresql': return '🐘';
      case 'mysql': return '🐬';
      case 'mongodb': return '🍃';
      case 'sqlite': return '🗃️';
      case 'api': return '🔗';
      default: return '💾';
    }
  };



  const handleConnectionClick = (connection: Connection) => {
    setSelectedConnection(connection.id);
    onConnectionSelect(connection);
  };

  return (
    <div className="connections-panel">
      <div className="connections-header">
        <div className="header-title">
          <span className="header-icon">🔌</span>
          <span>Connections</span>
        </div>
        <button 
          className="new-connection-btn"
          onClick={onNewConnection}
          title="Add New Connection"
        >
          ➕
        </button>
      </div>

      <div className="connections-list">
        {connections.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon">📊</div>
            <p>No connections yet</p>
            <button 
              className="add-first-connection"
              onClick={onNewConnection}
            >
              Add Your First Connection
            </button>
          </div>
        ) : (
          connections.map((connection) => (
            <div
              key={connection.id}
              className={`connection-item ${selectedConnection === connection.id ? 'selected' : ''}`}
              onClick={() => handleConnectionClick(connection)}
            >
              <div className="connection-info">
                <div className="connection-header">
                  <span className="connection-icon">
                    {getConnectionIcon(connection.type)}
                  </span>
                  <span className="connection-name">{connection.name}</span>
                  <div 
                    className={`connection-status ${connection.status}`}
                    title={connection.status}
                  />
                </div>
                <div className="connection-details">
                  <span className="connection-type">{connection.type.toUpperCase()}</span>
                  {connection.host && (
                    <span className="connection-host">📍 {connection.host}</span>
                  )}
                  {connection.database && (
                    <span className="connection-database">🗄️ {connection.database}</span>
                  )}
                </div>
                {connection.lastConnected && (
                  <div className="connection-last-used">
                    Last used: {connection.lastConnected.toLocaleDateString()}
                  </div>
                )}
              </div>
            </div>
          ))
        )}
      </div>

      <div className="connections-footer">
        <div className="connection-stats">
          <span className="stat">
            <span className="stat-value">{connections.filter(c => c.status === 'connected').length}</span>
            <span className="stat-label">Active</span>
          </span>
          <span className="stat">
            <span className="stat-value">{connections.length}</span>
            <span className="stat-label">Total</span>
          </span>
        </div>
      </div>
    </div>
  );
};

export default ConnectionsPanel;