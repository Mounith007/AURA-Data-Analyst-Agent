import React from 'react';

interface SqlDisplayProps {
  sqlQuery: string;
  pendingApproval?: boolean;
  onApproval?: (approved: boolean) => void;
}

const SqlDisplay: React.FC<SqlDisplayProps> = ({ 
  sqlQuery, 
  pendingApproval = false, 
  onApproval 
}) => {
  return (
    <div className="sql-display">
      <div className="sql-header">
        <h3>🔍 Glass Box - Generated SQL</h3>
        {pendingApproval && (
          <div className="approval-badge">
            ⚙️ Auto-executing...
          </div>
        )}
      </div>
      
      <div className="sql-code-container">
        <pre><code>{sqlQuery}</code></pre>
      </div>
      
      {pendingApproval && (
        <div className="auto-execution-message">
          <div className="execution-status">
            ⚙️ Auto-executing query...
          </div>
          <div className="execution-note">
            🔍 Glass Box: Query approved automatically in demo mode
          </div>
        </div>
      )}
    </div>
  );
};

export default SqlDisplay;