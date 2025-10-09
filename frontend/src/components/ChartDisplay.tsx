import React, { useMemo } from 'react';
import Plot from 'react-plotly.js';
import type { DataResult } from '../types';

interface ChartDisplayProps {
  data: DataResult;
  chartType?: 'auto' | 'bar' | 'line' | 'pie' | 'scatter' | 'histogram' | 'box' | 'area' | 'heatmap' | 'donut' | 'waterfall';
}

const ChartDisplay: React.FC<ChartDisplayProps> = ({ data, chartType = 'auto' }) => {
  const chartData = useMemo(() => {
    if (!data.rows || data.rows.length === 0) return null;

    const columns = data.columns;
    const rows = data.rows;

    // Determine best chart type if auto is selected
    let selectedChartType = chartType;
    if (chartType === 'auto') {
      selectedChartType = suggestChartType(columns, rows);
    }

    // Prepare data based on chart type
    switch (selectedChartType) {
      case 'bar':
        return createBarChart(columns, rows);
      case 'line':
        return createLineChart(columns, rows);
      case 'pie':
        return createPieChart(columns, rows);
      case 'scatter':
        return createScatterChart(columns, rows);
      case 'histogram':
        return createHistogramChart(columns, rows);
      case 'box':
        return createBoxChart(columns, rows);
      case 'area':
        return createAreaChart(columns, rows);
      case 'heatmap':
        return createHeatmapChart(columns, rows);
      case 'donut':
        return createDonutChart(columns, rows);
      default:
        return createBarChart(columns, rows);
    }
  }, [data, chartType]);

  if (!chartData) {
    return (
      <div className="chart-display">
        <p>No data available for visualization</p>
      </div>
    );
  }

  return (
    <div className="chart-display">
      <div className="chart-header">
        <h3>📊 Data Visualization</h3>
        <div className="chart-info">
          <span className="chart-type">{chartData.type.toUpperCase()} Chart</span>
          <span className="data-points">{data.rows.length} data points</span>
        </div>
      </div>
      <div className="chart-container">
        <Plot
          data={chartData.data as any}
          layout={{
            ...chartData.layout,
            autosize: true,
            margin: { l: 50, r: 50, t: 50, b: 50 }
          } as any}
          config={{
            responsive: true,
            displayModeBar: true,
            modeBarButtonsToRemove: ['pan2d', 'lasso2d'],
            displaylogo: false
          }}
          style={{ width: '100%', height: '400px' }}
        />
      </div>
    </div>
  );
};

// Chart type suggestion logic
function suggestChartType(columns: string[], rows: any[][]): 'bar' | 'line' | 'pie' | 'scatter' | 'histogram' | 'box' | 'area' | 'heatmap' | 'donut' {
  if (columns.length < 2) return 'bar';
  
  const firstCol = rows.map(row => row[0]);
  const secondCol = rows.map(row => row[1]);
  
  // Check for date/time columns
  const isDateColumn = firstCol.some(val => 
    val && (val.toString().includes('-') || val.toString().includes('/') || val.toString().includes('2024'))
  );
  
  // Check for numeric data distribution
  const isNumericData = secondCol.every(val => typeof val === 'number' || !isNaN(Number(val)));
  const numericValues = secondCol.filter(val => typeof val === 'number' || !isNaN(Number(val))).map(Number);
  const hasWideRange = numericValues.length > 0 && (Math.max(...numericValues) - Math.min(...numericValues)) > 1000;
  
  // Smart chart selection based on data characteristics
  if (isDateColumn && isNumericData) {
    return hasWideRange ? 'area' : 'line';
  }
  
  if (columns.length === 2 && rows.length <= 8 && isNumericData) {
    const total = numericValues.reduce((sum, val) => sum + val, 0);
    return total > 0 ? 'donut' : 'pie';
  }
  
  if (columns.length === 2 && isNumericData && rows.length > 20) {
    return 'histogram';
  }
  
  if (columns.length >= 3 && isNumericData) {
    return 'scatter';
  }
  
  if (columns.length === 2 && isNumericData && hasWideRange) {
    return 'area';
  }
  
  return 'bar';
}

// Chart creation functions
function createBarChart(columns: string[], rows: any[][]) {
  const xData = rows.map(row => row[0]);
  const yData = rows.map(row => row[1] || 0);
  
  return {
    type: 'bar',
    data: [{
      x: xData,
      y: yData,
      type: 'bar',
      marker: {
        color: 'rgba(55, 128, 191, 0.7)',
        line: {
          color: 'rgba(55, 128, 191, 1.0)',
          width: 1
        }
      },
      hovertemplate: '<b>%{x}</b><br>%{y}<extra></extra>'
    }],
    layout: {
      title: `${columns[1] || 'Value'} by ${columns[0] || 'Category'}`,
      xaxis: { title: columns[0] || 'Category' },
      yaxis: { title: columns[1] || 'Value' },
      showlegend: false
    }
  };
}

function createLineChart(columns: string[], rows: any[][]) {
  const xData = rows.map(row => row[0]);
  const yData = rows.map(row => row[1] || 0);
  
  return {
    type: 'line',
    data: [{
      x: xData,
      y: yData,
      type: 'scatter',
      mode: 'lines+markers',
      line: { color: 'rgb(219, 64, 82)', width: 3 },
      marker: { color: 'rgb(219, 64, 82)', size: 6 },
      hovertemplate: '<b>%{x}</b><br>%{y}<extra></extra>'
    }],
    layout: {
      title: `${columns[1] || 'Value'} Trend Over ${columns[0] || 'Time'}`,
      xaxis: { title: columns[0] || 'Time' },
      yaxis: { title: columns[1] || 'Value' },
      showlegend: false
    }
  };
}

function createPieChart(columns: string[], rows: any[][]) {
  const labels = rows.map(row => row[0]);
  const values = rows.map(row => row[1] || 0);
  
  return {
    type: 'pie',
    data: [{
      labels: labels,
      values: values,
      type: 'pie',
      textinfo: 'label+percent',
      textposition: 'outside',
      hovertemplate: '<b>%{label}</b><br>%{value}<br>%{percent}<extra></extra>'
    }],
    layout: {
      title: `Distribution of ${columns[1] || 'Values'} by ${columns[0] || 'Category'}`,
      showlegend: true,
      legend: { orientation: 'v', x: 1, y: 1 }
    }
  };
}

function createScatterChart(columns: string[], rows: any[][]) {
  const xData = rows.map(row => row[0]);
  const yData = rows.map(row => row[1] || 0);
  
  return {
    type: 'scatter',
    data: [{
      x: xData,
      y: yData,
      type: 'scatter',
      mode: 'markers',
      marker: {
        size: 10,
        color: 'rgba(152, 0, 67, 0.8)',
        line: {
          color: 'rgb(152, 0, 67)',
          width: 2
        }
      },
      hovertemplate: '<b>%{x}</b><br>%{y}<extra></extra>'
    }],
    layout: {
      title: `${columns[1] || 'Y-Axis'} vs ${columns[0] || 'X-Axis'}`,
      xaxis: { title: columns[0] || 'X-Axis' },
      yaxis: { title: columns[1] || 'Y-Axis' },
      showlegend: false
    }
  };
}

function createHistogramChart(columns: string[], rows: any[][]) {
  const data = rows.map(row => row[1] || 0);
  
  return {
    type: 'histogram',
    data: [{
      x: data,
      type: 'histogram',
      marker: {
        color: 'rgba(100, 200, 102, 0.7)',
        line: {
          color: 'rgba(100, 200, 102, 1)',
          width: 1
        }
      },
      hovertemplate: 'Range: %{x}<br>Count: %{y}<extra></extra>'
    }],
    layout: {
      title: `Distribution of ${columns[1] || 'Values'}`,
      xaxis: { title: columns[1] || 'Value' },
      yaxis: { title: 'Frequency' },
      showlegend: false
    }
  };
}

function createBoxChart(columns: string[], rows: any[][]) {
  const data = rows.map(row => row[1] || 0);
  
  return {
    type: 'box',
    data: [{
      y: data,
      type: 'box',
      name: columns[1] || 'Values',
      marker: { color: 'rgba(255, 144, 14, 0.8)' },
      boxpoints: 'outliers',
      hovertemplate: '%{y}<extra></extra>'
    }],
    layout: {
      title: `${columns[1] || 'Values'} Distribution Analysis`,
      yaxis: { title: columns[1] || 'Value' },
      showlegend: false
    }
  };
}

function createAreaChart(columns: string[], rows: any[][]) {
  const xData = rows.map(row => row[0]);
  const yData = rows.map(row => row[1] || 0);
  
  return {
    type: 'area',
    data: [{
      x: xData,
      y: yData,
      type: 'scatter',
      mode: 'lines',
      fill: 'tonexty',
      fillcolor: 'rgba(74, 144, 226, 0.3)',
      line: { color: 'rgb(74, 144, 226)', width: 3 },
      hovertemplate: '<b>%{x}</b><br>%{y}<extra></extra>'
    }],
    layout: {
      title: `${columns[1] || 'Value'} Area Trend`,
      xaxis: { title: columns[0] || 'Category' },
      yaxis: { title: columns[1] || 'Value' },
      showlegend: false
    }
  };
}

function createDonutChart(columns: string[], rows: any[][]) {
  const labels = rows.map(row => row[0]);
  const values = rows.map(row => row[1] || 0);
  
  return {
    type: 'donut',
    data: [{
      labels: labels,
      values: values,
      type: 'pie',
      hole: 0.4,
      textinfo: 'label+percent',
      textposition: 'outside',
      marker: {
        colors: ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F']
      },
      hovertemplate: '<b>%{label}</b><br>%{value}<br>%{percent}<extra></extra>'
    }],
    layout: {
      title: `${columns[1] || 'Values'} Distribution (Donut)`,
      showlegend: true,
      legend: { orientation: 'v', x: 1, y: 1 }
    }
  };
}

function createHeatmapChart(columns: string[], rows: any[][]) {
  if (columns.length < 3) {
    return createBarChart(columns, rows);
  }
  
  const xData = [...new Set(rows.map(row => row[0]))];
  const yData = [...new Set(rows.map(row => row[1]))];
  const zData = [];
  
  for (let i = 0; i < yData.length; i++) {
    const row = [];
    for (let j = 0; j < xData.length; j++) {
      const matchingRow = rows.find(r => r[0] === xData[j] && r[1] === yData[i]);
      row.push(matchingRow ? (matchingRow[2] || 0) : 0);
    }
    zData.push(row);
  }
  
  return {
    type: 'heatmap',
    data: [{
      x: xData,
      y: yData,
      z: zData,
      type: 'heatmap',
      colorscale: 'Viridis',
      hovertemplate: '<b>%{x}</b><br><b>%{y}</b><br>Value: %{z}<extra></extra>'
    }],
    layout: {
      title: `${columns[2] || 'Values'} Heatmap`,
      xaxis: { title: columns[0] || 'X-Axis' },
      yaxis: { title: columns[1] || 'Y-Axis' },
      showlegend: false
    }
  };
}

export default ChartDisplay;