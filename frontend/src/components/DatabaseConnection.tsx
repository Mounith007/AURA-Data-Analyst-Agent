import React, { useState } from 'react';
import './DatabaseConnection.css';

interface DatabaseConnectionProps {
  onConnect: (connectionDetails: any) => void;
  onClose: () => void;
}

const DatabaseConnection: React.FC<DatabaseConnectionProps> = ({ onConnect, onClose }) => {
  const [connectionDetails, setConnectionDetails] = useState({
    type: 'postgresql',
    host: 'localhost',
    port: 5432,
    user: '',
    password: '',
    dbname: '',
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setConnectionDetails(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onConnect(connectionDetails);
  };

  return (
    <div className="db-connection-modal">
      <div className="db-connection-form">
        <h3>New Database Connection</h3>
        <form onSubmit={handleSubmit}>
          <label>
            Database Type:
            <select name="type" value={connectionDetails.type} onChange={handleChange}>
              <option value="postgresql">PostgreSQL</option>
              <option value="mysql">MySQL</option>
              <option value="mssql">SQL Server</option>
              <option value="sqlite">SQLite</option>
            </select>
          </label>
          <label>
            Host:
            <input type="text" name="host" value={connectionDetails.host} onChange={handleChange} />
          </label>
          <label>
            Port:
            <input type="number" name="port" value={connectionDetails.port} onChange={handleChange} />
          </label>
          <label>
            User:
            <input type="text" name="user" value={connectionDetails.user} onChange={handleChange} />
          </label>
          <label>
            Password:
            <input type="password" name="password" value={connectionDetails.password} onChange={handleChange} />
          </label>
          <label>
            Database Name:
            <input type="text" name="dbname" value={connectionDetails.dbname} onChange={handleChange} />
          </label>
          <div className="form-actions">
            <button type="submit">Connect</button>
            <button type="button" onClick={onClose}>Cancel</button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default DatabaseConnection;
