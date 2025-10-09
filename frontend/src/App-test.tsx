import { useState } from 'react';
import './App.css';

function App() {
  const [message, setMessage] = useState('Hello AURA!');

  return (
    <div className="app">
      <h1>{message}</h1>
      <button onClick={() => setMessage('AURA is working!')}>
        Test Button
      </button>
    </div>
  );
}

export default App;