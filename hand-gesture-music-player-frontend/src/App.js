import React, { useState } from 'react';
import ModeSelector from './components/ModeSelector';
import './App.css';

function App() {
  const [activeMode, setActiveMode] = useState('Basic Mode');

  const modes = ['Basic Mode', 'Advanced Mode', 'Custom Mode', 'Game Mode'];

  const handleModeChange = (mode) => {
    setActiveMode(mode);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Hand Gesture Music Player</h1>
        <ModeSelector modes={modes} activeMode={activeMode} onModeChange={handleModeChange} />
        <p>Active Mode: {activeMode}</p>
      </header>
    </div>
  );
}

export default App;
