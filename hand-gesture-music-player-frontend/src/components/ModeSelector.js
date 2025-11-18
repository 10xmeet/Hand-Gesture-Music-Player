import React from 'react';
import './ModeSelector.css';

const ModeSelector = ({ modes, activeMode, onModeChange }) => {
  return (
    <div className="mode-selector">
      <h2>Select Mode</h2>
      <div className="mode-buttons">
        {modes.map((mode) => (
          <button
            key={mode}
            className={`mode-button ${activeMode === mode ? 'active' : ''}`}
            onClick={() => onModeChange(mode)}
          >
            {mode}
          </button>
        ))}
      </div>
    </div>
  );
};

export default ModeSelector;