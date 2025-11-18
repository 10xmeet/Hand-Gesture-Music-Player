import React, { useEffect, useRef } from 'react';
import './MainDisplay.css';

const MainDisplay = ({ volume, fingerCount, gestureName }) => {
  const videoRef = useRef(null);

  useEffect(() => {
    const videoElement = videoRef.current;
    if (videoElement) {
      videoElement.src = 'http://localhost:5000/video_feed';
    }
  }, []);

  return (
    <div className="main-display">
      <div className="info">
        <p>Volume: {volume}</p>
        <p>Finger Count: {fingerCount}</p>
        <p>Gesture Name: {gestureName}</p>
      </div>
      <div className="video-container">
        <img ref={videoRef} alt="Live Gesture Feed" className="camera-feed" />
      </div>
      <div className="volume-bar">
        <div className="volume-fill" style={{ width: `${volume}%` }}></div>
      </div>
    </div>
  );
};

export default MainDisplay;