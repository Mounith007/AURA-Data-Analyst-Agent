
import React from 'react';

interface HeaderProps {
  isConnected: boolean;
}

const Header: React.FC<HeaderProps> = ({ isConnected }) => {
  return (
    <header className="header">
      <h1>AURA - Analyst in a Box</h1>
      <p>Connection Status: {isConnected ? 'Connected' : 'Disconnected'}</p>
    </header>
  );
};

export default Header;
