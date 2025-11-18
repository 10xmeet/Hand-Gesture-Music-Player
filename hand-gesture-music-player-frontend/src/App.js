import React, { useState, useEffect } from 'react';
import ModeSelector from './components/ModeSelector';
import MainDisplay from './components/MainDisplay';
import { fetchGestureData } from './utils/api';
import './App.css';

function App() {
  const [activeMode, setActiveMode] = useState('Basic Mode');
  const [volume, setVolume] = useState(0.5);
  const [fingerCount, setFingerCount] = useState(0);
  const [gestureName, setGestureName] = useState('None');

  const modes = ['Basic Mode', 'Advanced Mode', 'Custom Mode', 'Game Mode'];

  const handleModeChange = (mode) => {
    setActiveMode(mode);
    // Reset values when mode changes
    setVolume(0.5);
    setFingerCount(0);
    setGestureName('None');
  };

  useEffect(() => {
    const interval = setInterval(async () => {
      const data = await fetchGestureData();
      if (data) {
        setVolume(data.volume);
        setFingerCount(data.fingerCount);
        setGestureName(data.gestureName);
      }
    }, 500);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Hand Gesture Music Player</h1>
        <ModeSelector modes={modes} activeMode={activeMode} onModeChange={handleModeChange} />
        <MainDisplay volume={volume} fingerCount={fingerCount} gestureName={gestureName} />
      </header>
    </div>
  );
}

export default App;
