import React, { useState, useMemo } from 'react';
import type { DataResult } from '../types';

interface DataTableProps {
  data: DataResult;
}

type SortDirection = 'asc' | 'desc' | null;

const DataTable: React.FC<DataTableProps> = ({ data }) => {
  const [sortColumn, setSortColumn] = useState<number | null>(null);
  const [sortDirection, setSortDirection] = useState<SortDirection>(null);
  const [filter, setFilter] = useState('');
  
  const filteredAndSortedData = useMemo(() => {
    let processedRows = [...data.rows];
    
    // Apply filter
    if (filter) {
      processedRows = processedRows.filter(row =>
        row.some(cell => 
          cell?.toString().toLowerCase().includes(filter.toLowerCase())
        )
      );
    }
    
    // Apply sorting
    if (sortColumn !== null && sortDirection) {
      processedRows.sort((a, b) => {
        const aVal = a[sortColumn];
        const bVal = b[sortColumn];
        
        // Handle different data types
        let comparison = 0;
        if (typeof aVal === 'number' && typeof bVal === 'number') {
          comparison = aVal - bVal;
        } else {
          comparison = String(aVal || '').localeCompare(String(bVal || ''));
        }
        
        return sortDirection === 'asc' ? comparison : -comparison;
      });
    }
    
    return processedRows;
  }, [data.rows, sortColumn, sortDirection, filter]);
  
  const handleSort = (columnIndex: number) => {
    if (sortColumn === columnIndex) {
      // Cycle through: asc -> desc -> null
      if (sortDirection === 'asc') {
        setSortDirection('desc');
      } else if (sortDirection === 'desc') {
        setSortDirection(null);
        setSortColumn(null);
      }
    } else {
      setSortColumn(columnIndex);
      setSortDirection('asc');
    }
  };
  
  const getSortIcon = (columnIndex: number) => {
    if (sortColumn !== columnIndex) return '↕️';
    if (sortDirection === 'asc') return '⬆️';
    if (sortDirection === 'desc') return '⬇️';
    return '↕️';
  };
  
  return (
    <div className="data-table">
      <div className="table-header">
        <h3>📋 Data Table</h3>
        <div className="table-controls">
          <input
            type="text"
            placeholder="Filter data..."
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            className="table-filter"
          />
          <span className="row-count">
            {filteredAndSortedData.length} of {data.rows.length} rows
          </span>
        </div>
      </div>
      
      <div className="table-container">
        <table className="responsive-table">
          <thead>
            <tr>
              {data.columns.map((column, index) => (
                <th 
                  key={index}
                  onClick={() => handleSort(index)}
                  className={`sortable ${sortColumn === index ? 'sorted' : ''}`}
                >
                  <div className="header-content">
                    <span className="column-name">{column}</span>
                    <span className="sort-icon">{getSortIcon(index)}</span>
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {filteredAndSortedData.map((row, rowIndex) => (
              <tr key={rowIndex} className={rowIndex % 2 === 0 ? 'even-row' : 'odd-row'}>
                {row.map((cell, cellIndex) => (
                  <td key={cellIndex} className={getColumnType(cell)}>
                    {formatCellValue(cell)}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
        
        {filteredAndSortedData.length === 0 && (
          <div className="no-data">
            <p>No data matches your filter criteria.</p>
          </div>
        )}
      </div>
    </div>
  );
};

function getColumnType(value: any): string {
  if (typeof value === 'number') return 'number-cell';
  if (value && typeof value === 'string' && !isNaN(Date.parse(value))) return 'date-cell';
  return 'text-cell';
}

function formatCellValue(value: any): string {
  if (value === null || value === undefined) return '-';
  if (typeof value === 'number') {
    return value.toLocaleString();
  }
  return String(value);
}

export default DataTable;