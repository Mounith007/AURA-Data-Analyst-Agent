import React, { useState, useEffect } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  RadialLinearScale,
} from 'chart.js';
import { Bar, Line, Pie, Doughnut, Radar, PolarArea } from 'react-chartjs-2';
import './DataVisualization.css';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  RadialLinearScale,
  Title,
  Tooltip,
  Legend
);

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
}

interface QueryResult {
  columns: string[];
  data: any[][];
  query_time: number;
  row_count: number;
}

interface ChartConfig {
  type: 'bar' | 'line' | 'pie' | 'doughnut' | 'radar' | 'polarArea';
  title: string;
  xAxis?: string;
  yAxis?: string;
  groupBy?: string;
  aggregation?: 'sum' | 'count' | 'avg' | 'max' | 'min';
}

const DataVisualization: React.FC = () => {
  const [connections, setConnections] = useState<DatabaseConnection[]>([]);
  const [selectedConnection, setSelectedConnection] = useState<string>('');
  const [sqlQuery, setSqlQuery] = useState<string>('');
  const [queryResult, setQueryResult] = useState<QueryResult | null>(null);
  const [chartConfig, setChartConfig] = useState<ChartConfig>({
    type: 'bar',
    title: 'Data Visualization',
    aggregation: 'count'
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showQueryBuilder, setShowQueryBuilder] = useState(false);

  // Predefined query templates
  const queryTemplates = {
    sales_by_month: "SELECT DATE_TRUNC('month', created_at) as month, SUM(amount) as total_sales FROM orders GROUP BY month ORDER BY month",
    top_products: "SELECT product_name, COUNT(*) as orders FROM order_items GROUP BY product_name ORDER BY orders DESC LIMIT 10",
    user_activity: "SELECT DATE(login_date) as date, COUNT(DISTINCT user_id) as active_users FROM user_sessions GROUP BY date ORDER BY date",
    revenue_trend: "SELECT DATE_TRUNC('week', created_at) as week, SUM(revenue) as weekly_revenue FROM transactions GROUP BY week ORDER BY week",
    category_breakdown: "SELECT category, COUNT(*) as product_count FROM products GROUP BY category ORDER BY product_count DESC"
  };

  useEffect(() => {
    loadConnections();
  }, []);

  const loadConnections = async () => {
    try {
      const response = await fetch('http://localhost:8002/connections');
      if (response.ok) {
        const data = await response.json();
        setConnections(data.filter((conn: DatabaseConnection) => conn.is_active));
      }
    } catch (error) {
      console.error('Error loading connections:', error);
    }
  };

  const executeQuery = async () => {
    if (!selectedConnection || !sqlQuery.trim()) {
      setError('Please select a connection and enter a SQL query');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch(`http://localhost:8002/connections/${selectedConnection}/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: sqlQuery }),
      });

      if (response.ok) {
        const result = await response.json();
        setQueryResult(result);
        
        // Auto-configure chart based on data
        if (result.columns.length >= 2) {
          setChartConfig({
            ...chartConfig,
            xAxis: result.columns[0],
            yAxis: result.columns[1]
          });
        }
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Query execution failed');
      }
    } catch (error) {
      setError('Network error: Unable to execute query');
    } finally {
      setIsLoading(false);
    }
  };

  const generateChartData = () => {
    if (!queryResult || !queryResult.data.length) return null;

    const { columns, data } = queryResult;
    const xIndex = columns.indexOf(chartConfig.xAxis || columns[0]);
    const yIndex = columns.indexOf(chartConfig.yAxis || columns[1]);

    if (xIndex === -1 || yIndex === -1) return null;

    const labels = data.map(row => row[xIndex]);
    const values = data.map(row => {
      const value = row[yIndex];
      return typeof value === 'number' ? value : parseFloat(value) || 0;
    });

    const colors = [
      'rgba(102, 126, 234, 0.8)',
      'rgba(237, 137, 54, 0.8)',
      'rgba(75, 192, 192, 0.8)',
      'rgba(255, 99, 132, 0.8)',
      'rgba(54, 162, 235, 0.8)',
      'rgba(255, 206, 86, 0.8)',
      'rgba(153, 102, 255, 0.8)',
      'rgba(255, 159, 64, 0.8)',
      'rgba(199, 199, 199, 0.8)',
      'rgba(83, 102, 255, 0.8)'
    ];

    const borderColors = colors.map(color => color.replace('0.8', '1'));

    return {
      labels,
      datasets: [{
        label: chartConfig.yAxis || 'Value',
        data: values,
        backgroundColor: chartConfig.type === 'pie' || chartConfig.type === 'doughnut' || chartConfig.type === 'polarArea' 
          ? colors.slice(0, values.length)
          : colors[0],
        borderColor: chartConfig.type === 'pie' || chartConfig.type === 'doughnut' || chartConfig.type === 'polarArea'
          ? borderColors.slice(0, values.length)
          : borderColors[0],
        borderWidth: 2,
        tension: chartConfig.type === 'line' ? 0.4 : undefined,
      }]
    };
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: chartConfig.title,
        font: {
          size: 16,
          weight: 'bold' as const
        }
      },
      tooltip: {
        mode: 'index' as const,
        intersect: false,
      }
    },
    scales: chartConfig.type === 'pie' || chartConfig.type === 'doughnut' || chartConfig.type === 'radar' || chartConfig.type === 'polarArea' 
      ? undefined 
      : {
        x: {
          display: true,
          title: {
            display: true,
            text: chartConfig.xAxis || 'X Axis'
          }
        },
        y: {
          display: true,
          title: {
            display: true,
            text: chartConfig.yAxis || 'Y Axis'
          }
        }
      }
  };

  const renderChart = () => {
    const chartData = generateChartData();
    if (!chartData) return null;

    switch (chartConfig.type) {
      case 'bar':
        return <Bar data={chartData} options={chartOptions} />;
      case 'line':
        return <Line data={chartData} options={chartOptions} />;
      case 'pie':
        return <Pie data={chartData} options={chartOptions} />;
      case 'doughnut':
        return <Doughnut data={chartData} options={chartOptions} />;
      case 'radar':
        return <Radar data={chartData} options={chartOptions} />;
      case 'polarArea':
        return <PolarArea data={chartData} options={chartOptions} />;
      default:
        return <Bar data={chartData} options={chartOptions} />;
    }
  };

  return (
    <div className="data-visualization">
      <div className="viz-header">
        <h2>📊 Data Visualization Studio</h2>
        <p>Transform your database queries into beautiful, interactive charts</p>
      </div>

      {error && (
        <div className="error-message">
          ❌ {error}
          <button onClick={() => setError(null)}>✕</button>
        </div>
      )}

      <div className="viz-content">
        <div className="query-panel">
          <div className="connection-selector">
            <label>Database Connection:</label>
            <select
              value={selectedConnection}
              onChange={(e) => setSelectedConnection(e.target.value)}
            >
              <option value="">Select a database...</option>
              {connections.map((conn) => (
                <option key={conn.id} value={conn.id}>
                  {conn.name} ({conn.type})
                </option>
              ))}
            </select>
          </div>

          <div className="query-section">
            <div className="query-header">
              <h3>📝 SQL Query</h3>
              <button 
                className="template-btn"
                onClick={() => setShowQueryBuilder(!showQueryBuilder)}
              >
                {showQueryBuilder ? '📝 Custom Query' : '🎯 Quick Templates'}
              </button>
            </div>

            {showQueryBuilder ? (
              <div className="query-templates">
                <h4>Quick Query Templates:</h4>
                <div className="template-grid">
                  {Object.entries(queryTemplates).map(([key, query]) => (
                    <button
                      key={key}
                      className="template-card"
                      onClick={() => {
                        setSqlQuery(query);
                        setShowQueryBuilder(false);
                      }}
                    >
                      <strong>{key.replace(/_/g, ' ').toUpperCase()}</strong>
                      <p>{query.substring(0, 60)}...</p>
                    </button>
                  ))}
                </div>
              </div>
            ) : (
              <div className="query-editor">
                <textarea
                  value={sqlQuery}
                  onChange={(e) => setSqlQuery(e.target.value)}
                  placeholder="Enter your SQL query here...
Example:
SELECT category, COUNT(*) as count 
FROM products 
GROUP BY category 
ORDER BY count DESC"
                  rows={8}
                />
                <button 
                  className="execute-btn"
                  onClick={executeQuery}
                  disabled={isLoading || !selectedConnection || !sqlQuery.trim()}
                >
                  {isLoading ? '⏳ Executing...' : '▶️ Execute Query'}
                </button>
              </div>
            )}
          </div>

          {queryResult && (
            <div className="query-results">
              <div className="results-header">
                <h3>📋 Query Results</h3>
                <div className="results-stats">
                  <span>⏱️ {queryResult.query_time.toFixed(2)}ms</span>
                  <span>📊 {queryResult.row_count} rows</span>
                  <span>📂 {queryResult.columns.length} columns</span>
                </div>
              </div>

              <div className="results-table">
                <table>
                  <thead>
                    <tr>
                      {queryResult.columns.map((col, index) => (
                        <th key={index}>{col}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {queryResult.data.slice(0, 10).map((row, rowIndex) => (
                      <tr key={rowIndex}>
                        {row.map((cell, cellIndex) => (
                          <td key={cellIndex}>
                            {cell !== null ? cell.toString() : 'NULL'}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
                {queryResult.data.length > 10 && (
                  <p className="table-truncate">
                    Showing first 10 rows of {queryResult.row_count} total rows
                  </p>
                )}
              </div>
            </div>
          )}
        </div>

        {queryResult && (
          <div className="chart-panel">
            <div className="chart-config">
              <h3>🎨 Chart Configuration</h3>
              
              <div className="config-grid">
                <div className="config-group">
                  <label>Chart Type:</label>
                  <select
                    value={chartConfig.type}
                    onChange={(e) => setChartConfig({
                      ...chartConfig,
                      type: e.target.value as ChartConfig['type']
                    })}
                  >
                    <option value="bar">📊 Bar Chart</option>
                    <option value="line">📈 Line Chart</option>
                    <option value="pie">🥧 Pie Chart</option>
                    <option value="doughnut">🍩 Doughnut Chart</option>
                    <option value="radar">🕸️ Radar Chart</option>
                    <option value="polarArea">🎯 Polar Area</option>
                  </select>
                </div>

                <div className="config-group">
                  <label>Chart Title:</label>
                  <input
                    type="text"
                    value={chartConfig.title}
                    onChange={(e) => setChartConfig({
                      ...chartConfig,
                      title: e.target.value
                    })}
                  />
                </div>

                <div className="config-group">
                  <label>X-Axis (Labels):</label>
                  <select
                    value={chartConfig.xAxis || ''}
                    onChange={(e) => setChartConfig({
                      ...chartConfig,
                      xAxis: e.target.value
                    })}
                  >
                    {queryResult.columns.map((col) => (
                      <option key={col} value={col}>{col}</option>
                    ))}
                  </select>
                </div>

                <div className="config-group">
                  <label>Y-Axis (Values):</label>
                  <select
                    value={chartConfig.yAxis || ''}
                    onChange={(e) => setChartConfig({
                      ...chartConfig,
                      yAxis: e.target.value
                    })}
                  >
                    {queryResult.columns.map((col) => (
                      <option key={col} value={col}>{col}</option>
                    ))}
                  </select>
                </div>
              </div>
            </div>

            <div className="chart-container">
              <div className="chart-wrapper">
                {renderChart()}
              </div>
            </div>

            <div className="chart-actions">
              <button className="export-btn">
                📥 Export PNG
              </button>
              <button className="export-btn">
                📊 Export Data
              </button>
              <button className="share-btn">
                🔗 Share Chart
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default DataVisualization;