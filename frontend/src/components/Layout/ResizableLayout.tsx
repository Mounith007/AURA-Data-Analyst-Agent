import React, { useState, useRef, useCallback } from 'react';
import { useTheme } from '../../contexts/ThemeContext';
import './ResizableLayout.css';

interface Panel {
  id: string;
  title: string;
  content: React.ReactNode;
  minWidth?: number;
  minHeight?: number;
  defaultWidth?: number;
  defaultHeight?: number;
}

interface ResizableLayoutProps {
  leftPanel: Panel;
  middleTopPanel: Panel;
  middleBottomPanel: Panel;
  rightPanel: Panel;
}

const ResizableLayout: React.FC<ResizableLayoutProps> = ({
  leftPanel,
  middleTopPanel,
  middleBottomPanel,
  rightPanel,
}) => {
  const { theme } = useTheme();
  const [leftWidth, setLeftWidth] = useState(leftPanel.defaultWidth || 300);
  const [rightWidth, setRightWidth] = useState(rightPanel.defaultWidth || 350);
  const [middleTopHeight, setMiddleTopHeight] = useState(middleTopPanel.defaultHeight || 400);
  
  const [isResizing, setIsResizing] = useState<string | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  const handleMouseDown = useCallback((resizer: string) => {
    setIsResizing(resizer);
  }, []);

  const handleMouseMove = useCallback((e: MouseEvent) => {
    if (!isResizing || !containerRef.current) return;

    const containerRect = containerRef.current.getBoundingClientRect();
    const containerWidth = containerRect.width;
    const containerHeight = containerRect.height;

    switch (isResizing) {
      case 'left':
        const newLeftWidth = Math.max(
          leftPanel.minWidth || 250,
          Math.min(
            containerWidth * 0.5,
            e.clientX - containerRect.left
          )
        );
        setLeftWidth(newLeftWidth);
        break;
      
      case 'right':
        const newRightWidth = Math.max(
          rightPanel.minWidth || 300,
          Math.min(
            containerWidth * 0.5,
            containerRect.right - e.clientX
          )
        );
        setRightWidth(newRightWidth);
        break;
      
      case 'middle':
        const newMiddleTopHeight = Math.max(
          middleTopPanel.minHeight || 200,
          Math.min(
            containerHeight * 0.8,
            e.clientY - containerRect.top - 60 // Account for header
          )
        );
        setMiddleTopHeight(newMiddleTopHeight);
        break;
    }
  }, [isResizing, leftPanel.minWidth, rightPanel.minWidth, middleTopPanel.minHeight]);

  const handleMouseUp = useCallback(() => {
    setIsResizing(null);
  }, []);

  React.useEffect(() => {
    if (isResizing) {
      document.addEventListener('mousemove', handleMouseMove);
      document.addEventListener('mouseup', handleMouseUp);
      return () => {
        document.removeEventListener('mousemove', handleMouseMove);
        document.removeEventListener('mouseup', handleMouseUp);
      };
    }
  }, [isResizing, handleMouseMove, handleMouseUp]);

  return (
    <div className="resizable-layout" ref={containerRef} data-theme={theme}>
      {/* Left Panel */}
      <div 
        className="layout-panel layout-left" 
        style={{ width: leftWidth }}
      >
        <div className="panel-header">
          <h3>{leftPanel.title}</h3>
        </div>
        <div className="panel-content">
          {leftPanel.content}
        </div>
      </div>

      {/* Left Resizer */}
      <div 
        className="resizer resizer-vertical left-resizer"
        onMouseDown={() => handleMouseDown('left')}
      />

      {/* Middle Section */}
      <div 
        className="layout-middle"
        style={{ 
          left: leftWidth + 4,
          right: rightWidth + 4
        }}
      >
        {/* Middle Top Panel */}
        <div 
          className="layout-panel layout-middle-top"
          style={{ height: middleTopHeight }}
        >
          <div className="panel-header">
            <h3>{middleTopPanel.title}</h3>
          </div>
          <div className="panel-content">
            {middleTopPanel.content}
          </div>
        </div>

        {/* Middle Horizontal Resizer */}
        <div 
          className="resizer resizer-horizontal middle-resizer"
          onMouseDown={() => handleMouseDown('middle')}
        />

        {/* Middle Bottom Panel */}
        <div 
          className="layout-panel layout-middle-bottom"
          style={{ 
            top: middleTopHeight + 4,
            bottom: 0
          }}
        >
          <div className="panel-header">
            <h3>{middleBottomPanel.title}</h3>
          </div>
          <div className="panel-content">
            {middleBottomPanel.content}
          </div>
        </div>
      </div>

      {/* Right Resizer */}
      <div 
        className="resizer resizer-vertical right-resizer"
        style={{ right: rightWidth }}
        onMouseDown={() => handleMouseDown('right')}
      />

      {/* Right Panel */}
      <div 
        className="layout-panel layout-right" 
        style={{ width: rightWidth }}
      >
        <div className="panel-header">
          <h3>{rightPanel.title}</h3>
        </div>
        <div className="panel-content">
          {rightPanel.content}
        </div>
      </div>
    </div>
  );
};

export default ResizableLayout;