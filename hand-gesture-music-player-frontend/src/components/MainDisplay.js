import React from 'react';
import './MainDisplay.css';

const MainDisplay = ({ volume, fingerCount, gestureName }) => {
  return (
    <div className="main-display">
      <div className="info">
        <h3>Volume: {volume}</h3>
        <h3>Finger Count: {fingerCount}</h3>
        <h3>Gesture: {gestureName}</h3>
      </div>
      <div className="volume-bar">
        <div
          className="volume-fill"
          style={{ width: `${volume * 100}%` }}
        ></div>
      </div>
    </div>
  );
};

export default MainDisplay;