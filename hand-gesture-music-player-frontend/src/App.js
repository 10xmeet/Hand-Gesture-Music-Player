import React, { useState, useEffect } from 'react';
import ModeSelector from './components/ModeSelector';
import MainDisplay from './components/MainDisplay';
import Training from './components/Training';
import './App.css';

function App() {
  const [activeMode, setActiveMode] = useState('Stem Player');
  const [volume, setVolume] = useState(0.5);
  const [fingerCount, setFingerCount] = useState(0);
  const [gestureName, setGestureName] = useState('None');

  const modes = ['Stem Player', 'Training'];

  useEffect(() => {
    const interval = setInterval(() => {
      fetch('http://localhost:5000/status')
        .then(res => res.json())
        .then(data => {
          setVolume(data.volume);
          setFingerCount(data.finger_count);
          setGestureName(data.gesture_name);
        })
        .catch(err => console.error("Error fetching status:", err));
    }, 100); // Poll every 100ms

    return () => clearInterval(interval);
  }, []);

  const handleModeChange = (mode) => {
    setActiveMode(mode);
  };

  return (
    <div className="App">
      <div className="background-overlay"></div>
      <header className="App-header">
        <h1 className="app-title">Sonic Hands</h1>
        <ModeSelector modes={modes} activeMode={activeMode} onModeChange={handleModeChange} />
        {activeMode === 'Training' ? (
          <Training />
        ) : (
          <MainDisplay volume={volume} fingerCount={fingerCount} gestureName={gestureName} />
        )}
      </header>
    </div>
  );
}

export default App;
