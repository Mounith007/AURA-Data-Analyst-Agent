import React, { useState } from 'react';
import ChartDisplay from './ChartDisplay';
import DataTable from './DataTable';
import type { DataResult } from '../types';

interface VisualizationPanelProps {
  data: DataResult;
}

type ViewMode = 'chart' | 'table' | 'both';
type ChartType = 'auto' | 'bar' | 'line' | 'pie' | 'scatter' | 'histogram' | 'box' | 'area' | 'heatmap' | 'donut';

const VisualizationPanel: React.FC<VisualizationPanelProps> = ({ data }) => {
  const [viewMode, setViewMode] = useState<ViewMode>('both');
  const [chartType, setChartType] = useState<ChartType>('auto');
  
  return (
    <div className="visualization-panel">
      <div className="visualization-header">
        <h2>📊 Data Analysis Results</h2>
        <div className="visualization-controls">
          <div className="view-mode-controls">
            <label>View:</label>
            <select 
              value={viewMode} 
              onChange={(e) => setViewMode(e.target.value as ViewMode)}
              className="view-mode-select"
            >
              <option value="both">📊📋 Chart & Table</option>
              <option value="chart">📊 Chart Only</option>
              <option value="table">📋 Table Only</option>
            </select>
          </div>
          
          {(viewMode === 'chart' || viewMode === 'both') && (
            <div className="chart-type-controls">
              <label>Chart Type:</label>
              <select 
                value={chartType} 
                onChange={(e) => setChartType(e.target.value as ChartType)}
                className="chart-type-select"
              >
                <option value="auto">🤖 Auto Select</option>
                <option value="bar">📊 Bar Chart</option>
                <option value="line">📈 Line Chart</option>
                <option value="area">🏔️ Area Chart</option>
                <option value="pie">🥧 Pie Chart</option>
                <option value="donut">🍩 Donut Chart</option>
                <option value="scatter">⚫ Scatter Plot</option>
                <option value="histogram">📉 Histogram</option>
                <option value="box">📦 Box Plot</option>
                <option value="heatmap">🔥 Heatmap</option>
              </select>
            </div>
          )}
        </div>
      </div>
      
      <div className={`visualization-content ${viewMode}`}>
        {(viewMode === 'chart' || viewMode === 'both') && (
          <div className="chart-section">
            <ChartDisplay data={data} chartType={chartType} />
          </div>
        )}
        
        {(viewMode === 'table' || viewMode === 'both') && (
          <div className="table-section">
            <DataTable data={data} />
          </div>
        )}
      </div>
      
      <div className="data-summary">
        <div className="summary-stats">
          <div className="stat-item">
            <span className="stat-label">Columns:</span>
            <span className="stat-value">{data.columns.length}</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">Rows:</span>
            <span className="stat-value">{data.rows.length}</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">Data Points:</span>
            <span className="stat-value">{data.columns.length * data.rows.length}</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default VisualizationPanel;