import React from 'react';
import SqlDisplay from './SqlDisplay';
import DataDisplay from './DataDisplay';
import type { DataResult } from '../types';

interface ResultsAreaProps {
  sqlQuery: string;
  dataResult: DataResult | null;
  pendingApproval?: boolean;
  onApproval?: (approved: boolean, editedQuery?: string) => void;
  isLoading?: boolean;
}

const ResultsArea: React.FC<ResultsAreaProps> = ({ 
  sqlQuery, 
  dataResult, 
  pendingApproval = false, 
  onApproval,
  isLoading = false
}) => {
  return (
    <div className="results-area">
      <SqlDisplay 
        sqlQuery={sqlQuery} 
        pendingApproval={pendingApproval}
        onApproval={onApproval}
        isEditable={true}
        showVersionHistory={true}
      />
      {isLoading && (
        <div className="loading-indicator">
          <div className="spinner"></div>
          <p>Executing query...</p>
        </div>
      )}
      {dataResult && !pendingApproval && (
        <DataDisplay dataResult={dataResult} />
      )}
    </div>
  );
};

export default ResultsArea;