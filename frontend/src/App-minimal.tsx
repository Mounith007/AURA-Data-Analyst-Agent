import { useState } from 'react';
import './App.css';

function App() {
  const [message, setMessage] = useState('🔍 AURA Glass Box - Testing!');

  return (
    <div className="app" style={{padding: '2rem', textAlign: 'center'}}>
      <h1 style={{color: '#007bff'}}>{message}</h1>
      <button 
        onClick={() => setMessage('✅ AURA Frontend is Working!')}
        style={{
          padding: '1rem 2rem',
          fontSize: '1.2rem',
          backgroundColor: '#28a745',
          color: 'white',
          border: 'none',
          borderRadius: '8px',
          cursor: 'pointer'
        }}
      >
        Test Glass Box Feature
      </button>
    </div>
  );
}

export default App;