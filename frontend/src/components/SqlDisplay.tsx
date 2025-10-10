import React, { useState, useEffect } from 'react';
import { useTheme } from '../contexts/ThemeContext';

interface SqlDisplayProps {
  sqlQuery: string;
  pendingApproval?: boolean;
  onApproval?: (approved: boolean, editedQuery?: string) => void;
  isEditable?: boolean;
  showVersionHistory?: boolean;
}

interface VersionHistoryItem {
  version: number;
  query: string;
  timestamp: Date;
  approved: boolean;
  editedBy: 'ai' | 'human';
}

const SqlDisplay: React.FC<SqlDisplayProps> = ({ 
  sqlQuery, 
  pendingApproval = false, 
  onApproval,
  isEditable = true,
  showVersionHistory = false
}) => {
  const { theme } = useTheme();
  const [editedQuery, setEditedQuery] = useState(sqlQuery);
  const [isEditing, setIsEditing] = useState(false);
  const [hasChanges, setHasChanges] = useState(false);
  const [versionHistory, setVersionHistory] = useState<VersionHistoryItem[]>([]);
  const [showHistory, setShowHistory] = useState(false);

  // Update edited query when sqlQuery prop changes
  useEffect(() => {
    setEditedQuery(sqlQuery);
    setHasChanges(false);
    
    // Add to version history
    if (sqlQuery) {
      const newVersion: VersionHistoryItem = {
        version: versionHistory.length + 1,
        query: sqlQuery,
        timestamp: new Date(),
        approved: false,
        editedBy: 'ai'
      };
      setVersionHistory(prev => [...prev, newVersion]);
    }
  }, [sqlQuery]);

  const handleQueryChange = (value: string) => {
    setEditedQuery(value);
    setHasChanges(value !== sqlQuery);
  };

  const handleApprove = () => {
    if (onApproval) {
      onApproval(true, hasChanges ? editedQuery : undefined);
    }
    // Add approval to version history
    if (hasChanges) {
      const newVersion: VersionHistoryItem = {
        version: versionHistory.length + 1,
        query: editedQuery,
        timestamp: new Date(),
        approved: true,
        editedBy: 'human'
      };
      setVersionHistory(prev => [...prev, newVersion]);
    }
    setIsEditing(false);
    setHasChanges(false);
  };

  const handleReject = () => {
    if (onApproval) {
      onApproval(false);
    }
    setIsEditing(false);
    setEditedQuery(sqlQuery);
    setHasChanges(false);
  };

  const handleRevert = () => {
    setEditedQuery(sqlQuery);
    setHasChanges(false);
  };

  const loadVersion = (version: VersionHistoryItem) => {
    setEditedQuery(version.query);
    setHasChanges(version.query !== sqlQuery);
    setShowHistory(false);
  };

  return (
    <div className="sql-display glass-box-ide" data-theme={theme}>
      <div className="sql-header">
        <div className="header-left">
          <h3>🔍 Glass Box - SQL Code Review</h3>
          {hasChanges && (
            <span className="changes-indicator">● Modified</span>
          )}
        </div>
        
        <div className="header-actions">
          {showVersionHistory && (
            <button 
              className="version-history-btn"
              onClick={() => setShowHistory(!showHistory)}
              title="Version History"
            >
              📚 History ({versionHistory.length})
            </button>
          )}
          
          {isEditable && !isEditing && (
            <button 
              className="edit-btn"
              onClick={() => setIsEditing(true)}
              title="Edit Query"
            >
              ✏️ Edit
            </button>
          )}
        </div>
      </div>

      {/* Version History Panel */}
      {showHistory && (
        <div className="version-history-panel">
          <h4>Query Evolution</h4>
          <div className="history-list">
            {versionHistory.map((version) => (
              <div 
                key={version.version}
                className={`history-item ${version.editedBy}`}
                onClick={() => loadVersion(version)}
              >
                <div className="version-header">
                  <span className="version-number">v{version.version}</span>
                  <span className="version-author">
                    {version.editedBy === 'ai' ? '🤖 AI Generated' : '👤 Human Edited'}
                  </span>
                  <span className="version-status">
                    {version.approved ? '✅ Approved' : '⏳ Pending'}
                  </span>
                </div>
                <div className="version-time">
                  {version.timestamp.toLocaleString()}
                </div>
                <div className="version-preview">
                  {version.query.substring(0, 100)}...
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
      
      <div className="sql-code-container">
        {isEditing ? (
          <div className="code-editor">
            <div className="editor-toolbar">
              <span className="editor-label">📝 Collaborative SQL Editor</span>
              <div className="editor-actions">
                {hasChanges && (
                  <button 
                    className="revert-btn"
                    onClick={handleRevert}
                    title="Revert Changes"
                  >
                    ↶ Revert
                  </button>
                )}
                <button 
                  className="format-btn"
                  onClick={() => {
                    // Simple SQL formatting
                    const formatted = editedQuery
                      .replace(/\s+(SELECT|FROM|WHERE|JOIN|GROUP BY|ORDER BY|HAVING)\s+/gi, '\n$1 ')
                      .replace(/,\s*/g, ',\n  ');
                    setEditedQuery(formatted);
                    setHasChanges(formatted !== sqlQuery);
                  }}
                  title="Format SQL"
                >
                  🎨 Format
                </button>
              </div>
            </div>
            <textarea
              value={editedQuery}
              onChange={(e) => handleQueryChange(e.target.value)}
              className="sql-textarea"
              rows={12}
              placeholder="Write your SQL query here..."
              spellCheck={false}
            />
            <div className="editor-status">
              {hasChanges ? (
                <span className="status-modified">
                  ⚠️ Query modified - Review changes before approval
                </span>
              ) : (
                <span className="status-original">
                  ✓ Original AI-generated query
                </span>
              )}
            </div>
          </div>
        ) : (
          <div className="code-viewer">
            <pre><code className="sql-code">{editedQuery}</code></pre>
          </div>
        )}
      </div>

      {/* AI Explanation Panel */}
      <div className="ai-explanation">
        <h4>🤖 AI Analysis</h4>
        <div className="explanation-content">
          <p><strong>Query Purpose:</strong> This query retrieves data for analysis and visualization.</p>
          <p><strong>Performance Impact:</strong> Estimated execution time: &lt;1s</p>
          <p><strong>Data Sources:</strong> Primary tables accessed in the query</p>
          {hasChanges && (
            <div className="change-analysis">
              <p><strong>⚠️ Changes Detected:</strong> Human modifications made to AI-generated query. Please review for accuracy.</p>
            </div>
          )}
        </div>
      </div>
      
      {/* Approval Controls */}
      {pendingApproval && (
        <div className="approval-controls">
          <div className="approval-message">
            <div className="message-content">
              {hasChanges ? (
                <>
                  <span className="approval-icon">📝</span>
                  <div className="approval-text">
                    <strong>Modified Query Ready for Review</strong>
                    <p>You've made changes to the AI-generated query. Please review and approve to execute.</p>
                  </div>
                </>
              ) : (
                <>
                  <span className="approval-icon">🔍</span>
                  <div className="approval-text">
                    <strong>AI-Generated Query Ready</strong>
                    <p>Review the generated SQL query and approve to execute against your data.</p>
                  </div>
                </>
              )}
            </div>
          </div>
          
          <div className="approval-buttons">
            <button 
              className="approve-btn"
              onClick={handleApprove}
              disabled={!editedQuery.trim()}
            >
              ✅ Approve & Execute
              {hasChanges && <span className="btn-badge">Modified</span>}
            </button>
            <button 
              className="reject-btn"
              onClick={handleReject}
            >
              ❌ Reject
            </button>
            {isEditing && (
              <button 
                className="cancel-edit-btn"
                onClick={() => {
                  setIsEditing(false);
                  setEditedQuery(sqlQuery);
                  setHasChanges(false);
                }}
              >
                Cancel Edit
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default SqlDisplay;