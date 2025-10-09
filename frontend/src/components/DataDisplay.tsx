import React from 'react';
import VisualizationPanel from './VisualizationPanel';
import type { DataResult } from '../types';

interface DataDisplayProps {
  dataResult: DataResult | null;
}

const DataDisplay: React.FC<DataDisplayProps> = ({ dataResult }) => {
  if (!dataResult) {
    return (
      <div className="data-display">
        <div className="no-data-message">
          <h3>💡 Ready for Analysis</h3>
          <p>Submit a query to see your data visualized with interactive charts and tables.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="data-display">
      <VisualizationPanel data={dataResult} />
    </div>
  );
};

export default DataDisplay;