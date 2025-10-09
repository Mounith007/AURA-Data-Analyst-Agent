import React, { useState, useEffect } from 'react';
import './DatabaseConnector.css';

interface DatabaseType {
  type: string;
  name: string;
  default_port: number;
  supports_ssl: boolean;
  description: string;
}

interface DatabaseConnection {
  id: string;
  name: string;
  type: string;
  host: string;
  port: number;
  database: string;
  username: string;
  ssl_enabled: boolean;
  is_active: boolean;
  created_at: string;
  updated_at: string;
  metadata: Record<string, any>;
}

interface TableInfo {
  name: string;
  schema: string;
  columns: Array<{
    name: string;
    type: string;
    nullable: boolean;
    primary_key?: boolean;
  }>;
  row_count?: number;
}

interface SchemaInfo {
  connection_id: string;
  schemas: string[];
  tables: TableInfo[];
  views: TableInfo[];
  last_updated: string;
}

const DatabaseConnector: React.FC = () => {
  const [connections, setConnections] = useState<DatabaseConnection[]>([]);
  const [supportedDbs, setSupportedDbs] = useState<DatabaseType[]>([]);
  const [selectedConnection, setSelectedConnection] = useState<string | null>(null);
  const [schemaInfo, setSchemaInfo] = useState<SchemaInfo | null>(null);
  const [showAddForm, setShowAddForm] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Form state
  const [formData, setFormData] = useState({
    name: '',
    type: 'postgresql',
    host: '',
    port: 5432,
    database: '',
    username: '',
    password: '',
    ssl_enabled: false
  });

  useEffect(() => {
    loadConnections();
    loadSupportedDatabases();
  }, []);

  const loadConnections = async () => {
    try {
      const response = await fetch('http://localhost:8002/connections');
      if (response.ok) {
        const data = await response.json();
        setConnections(data);
      }
    } catch (error) {
      console.error('Error loading connections:', error);
    }
  };

  const loadSupportedDatabases = async () => {
    try {
      const response = await fetch('http://localhost:8002/supported-databases');
      if (response.ok) {
        const data = await response.json();
        setSupportedDbs(data.databases);
      }
    } catch (error) {
      console.error('Error loading supported databases:', error);
    }
  };

  const handleAddConnection = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch('http://localhost:8002/connections', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        await loadConnections();
        setShowAddForm(false);
        setFormData({
          name: '',
          type: 'postgresql',
          host: '',
          port: 5432,
          database: '',
          username: '',
          password: '',
          ssl_enabled: false
        });
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Failed to create connection');
      }
    } catch (error) {
      setError('Network error: Unable to create connection');
    } finally {
      setIsLoading(false);
    }
  };

  const handleTestConnection = async (connectionId: string) => {
    setIsLoading(true);
    try {
      const response = await fetch(`http://localhost:8002/connections/${connectionId}/test`, {
        method: 'POST',
      });
      
      if (response.ok) {
        const result = await response.json();
        alert(result.message);
      }
    } catch (error) {
      alert('Failed to test connection');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDeleteConnection = async (connectionId: string) => {
    if (!confirm('Are you sure you want to delete this connection?')) return;

    try {
      const response = await fetch(`http://localhost:8002/connections/${connectionId}`, {
        method: 'DELETE',
      });
      
      if (response.ok) {
        await loadConnections();
        if (selectedConnection === connectionId) {
          setSelectedConnection(null);
          setSchemaInfo(null);
        }
      }
    } catch (error) {
      alert('Failed to delete connection');
    }
  };

  const handleViewSchema = async (connectionId: string) => {
    setIsLoading(true);
    setSelectedConnection(connectionId);
    
    try {
      const response = await fetch(`http://localhost:8002/connections/${connectionId}/schema`);
      if (response.ok) {
        const schema = await response.json();
        setSchemaInfo(schema);
      } else {
        setError('Failed to load schema');
      }
    } catch (error) {
      setError('Network error: Unable to load schema');
    } finally {
      setIsLoading(false);
    }
  };

  const handleTypeChange = (type: string) => {
    const dbType = supportedDbs.find(db => db.type === type);
    setFormData({
      ...formData,
      type,
      port: dbType?.default_port || 5432
    });
  };

  return (
    <div className="database-connector">
      <div className="connector-header">
        <h2>🗄️ Database Connections</h2>
        <p>Connect to any database and explore your data</p>
        <button 
          className="add-connection-btn"
          onClick={() => setShowAddForm(true)}
        >
          ➕ Add Connection
        </button>
      </div>

      {error && (
        <div className="error-message">
          ❌ {error}
          <button onClick={() => setError(null)}>✕</button>
        </div>
      )}

      <div className="connector-content">
        <div className="connections-panel">
          <h3>Active Connections ({connections.length})</h3>
          
          {connections.length === 0 ? (
            <div className="empty-state">
              <p>No database connections configured</p>
              <p>Add your first connection to get started</p>
            </div>
          ) : (
            <div className="connections-list">
              {connections.map((conn) => (
                <div 
                  key={conn.id} 
                  className={`connection-card ${selectedConnection === conn.id ? 'selected' : ''}`}
                >
                  <div className="connection-header">
                    <div className="connection-info">
                      <h4>{conn.name}</h4>
                      <span className="connection-type">{conn.type.toUpperCase()}</span>
                      <span className={`connection-status ${conn.is_active ? 'active' : 'inactive'}`}>
                        {conn.is_active ? '🟢 Active' : '🔴 Inactive'}
                      </span>
                    </div>
                    <div className="connection-actions">
                      <button 
                        onClick={() => handleTestConnection(conn.id)}
                        disabled={isLoading}
                        title="Test Connection"
                      >
                        🔍
                      </button>
                      <button 
                        onClick={() => handleViewSchema(conn.id)}
                        disabled={isLoading}
                        title="View Schema"
                      >
                        📊
                      </button>
                      <button 
                        onClick={() => handleDeleteConnection(conn.id)}
                        className="delete-btn"
                        title="Delete Connection"
                      >
                        🗑️
                      </button>
                    </div>
                  </div>
                  
                  <div className="connection-details">
                    <p><strong>Host:</strong> {conn.host}:{conn.port}</p>
                    <p><strong>Database:</strong> {conn.database}</p>
                    <p><strong>Username:</strong> {conn.username}</p>
                    <p><strong>SSL:</strong> {conn.ssl_enabled ? 'Enabled' : 'Disabled'}</p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {schemaInfo && (
          <div className="schema-panel">
            <h3>📊 Database Schema</h3>
            <div className="schema-info">
              <p><strong>Connection:</strong> {connections.find(c => c.id === selectedConnection)?.name}</p>
              <p><strong>Schemas:</strong> {schemaInfo.schemas.join(', ')}</p>
              <p><strong>Last Updated:</strong> {new Date(schemaInfo.last_updated).toLocaleString()}</p>
            </div>

            <div className="schema-content">
              <div className="tables-section">
                <h4>📋 Tables ({schemaInfo.tables.length})</h4>
                <div className="tables-list">
                  {schemaInfo.tables.map((table, index) => (
                    <div key={index} className="table-card">
                      <div className="table-header">
                        <h5>{table.name}</h5>
                        <span className="table-schema">{table.schema}</span>
                        {table.row_count && (
                          <span className="row-count">{table.row_count.toLocaleString()} rows</span>
                        )}
                      </div>
                      
                      <div className="columns-list">
                        <h6>Columns ({table.columns.length})</h6>
                        <div className="columns-grid">
                          {table.columns.map((column, colIndex) => (
                            <div key={colIndex} className="column-item">
                              <span className="column-name">{column.name}</span>
                              <span className="column-type">{column.type}</span>
                              {column.primary_key && <span className="pk-badge">PK</span>}
                              {!column.nullable && <span className="not-null-badge">NOT NULL</span>}
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {schemaInfo.views.length > 0 && (
                <div className="views-section">
                  <h4>👁️ Views ({schemaInfo.views.length})</h4>
                  <div className="views-list">
                    {schemaInfo.views.map((view, index) => (
                      <div key={index} className="view-card">
                        <h5>{view.name}</h5>
                        <span className="view-schema">{view.schema}</span>
                        <p>{view.columns.length} columns</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        )}
      </div>

      {showAddForm && (
        <div className="modal-overlay">
          <div className="modal-content">
            <div className="modal-header">
              <h3>➕ Add Database Connection</h3>
              <button 
                className="close-btn"
                onClick={() => setShowAddForm(false)}
              >
                ✕
              </button>
            </div>

            <form onSubmit={handleAddConnection}>
              <div className="form-grid">
                <div className="form-group">
                  <label>Connection Name *</label>
                  <input
                    type="text"
                    value={formData.name}
                    onChange={(e) => setFormData({...formData, name: e.target.value})}
                    required
                    placeholder="My Database"
                  />
                </div>

                <div className="form-group">
                  <label>Database Type *</label>
                  <select
                    value={formData.type}
                    onChange={(e) => handleTypeChange(e.target.value)}
                    required
                  >
                    {supportedDbs.map((db) => (
                      <option key={db.type} value={db.type}>
                        {db.name}
                      </option>
                    ))}
                  </select>
                </div>

                <div className="form-group">
                  <label>Host *</label>
                  <input
                    type="text"
                    value={formData.host}
                    onChange={(e) => setFormData({...formData, host: e.target.value})}
                    required
                    placeholder="localhost"
                  />
                </div>

                <div className="form-group">
                  <label>Port *</label>
                  <input
                    type="number"
                    value={formData.port}
                    onChange={(e) => setFormData({...formData, port: parseInt(e.target.value)})}
                    required
                  />
                </div>

                <div className="form-group">
                  <label>Database Name *</label>
                  <input
                    type="text"
                    value={formData.database}
                    onChange={(e) => setFormData({...formData, database: e.target.value})}
                    required
                    placeholder="mydb"
                  />
                </div>

                <div className="form-group">
                  <label>Username *</label>
                  <input
                    type="text"
                    value={formData.username}
                    onChange={(e) => setFormData({...formData, username: e.target.value})}
                    required
                    placeholder="user"
                  />
                </div>

                <div className="form-group">
                  <label>Password *</label>
                  <input
                    type="password"
                    value={formData.password}
                    onChange={(e) => setFormData({...formData, password: e.target.value})}
                    required
                    placeholder="password"
                  />
                </div>

                <div className="form-group checkbox-group">
                  <label>
                    <input
                      type="checkbox"
                      checked={formData.ssl_enabled}
                      onChange={(e) => setFormData({...formData, ssl_enabled: e.target.checked})}
                    />
                    Enable SSL
                  </label>
                </div>
              </div>

              <div className="form-actions">
                <button 
                  type="button" 
                  onClick={() => setShowAddForm(false)}
                  className="cancel-btn"
                >
                  Cancel
                </button>
                <button 
                  type="submit" 
                  disabled={isLoading}
                  className="submit-btn"
                >
                  {isLoading ? 'Connecting...' : 'Add Connection'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default DatabaseConnector;