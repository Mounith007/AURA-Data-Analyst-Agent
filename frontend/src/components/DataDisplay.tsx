import React from 'react';
import VisualizationPanel from './VisualizationPanel';
import { useTheme } from '../contexts/ThemeContext';
import type { DataResult } from '../types';

interface DataDisplayProps {
  dataResult: DataResult | null;
}

const DataDisplay: React.FC<DataDisplayProps> = ({ dataResult }) => {
  const { theme } = useTheme();
  
  if (!dataResult) {
    return (
      <div className="data-display" data-theme={theme}>
        <div className="no-data-message">
          <h3>💡 Ready for Analysis</h3>
          <p>Submit a query to see your data visualized with interactive charts and tables.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="data-display" data-theme={theme}>
      <VisualizationPanel data={dataResult} />
    </div>
  );
};

export default DataDisplay;