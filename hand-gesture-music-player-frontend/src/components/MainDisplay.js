import React, { useEffect, useRef } from 'react';
import { FaHandPaper, FaMusic, FaVolumeUp } from 'react-icons/fa';
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
      <div className="glass-card">

        {/* Header / Top Bar */}
        <div className="glass-header">
          <div className="status-item">
            <FaMusic className="icon" />
            <span>Now Playing: Something Just Like This</span>
          </div>
        </div>

        <div className="content-grid">
          {/* Left Panel: Stats */}
          <div className="stats-panel">
            <div className="stat-item">
              <div className="icon-wrapper">
                <FaHandPaper />
              </div>
              <div className="stat-info">
                <h3>Fingers</h3>
                <span className="stat-value">{fingerCount}</span>
              </div>
            </div>

            <div className="stat-item">
              <div className="icon-wrapper">
                <FaMusic />
              </div>
              <div className="stat-info">
                <h3>Gesture</h3>
                <span className="stat-value">{gestureName}</span>
              </div>
            </div>

            <div className="volume-control">
              <div className="icon-wrapper">
                <FaVolumeUp />
              </div>
              <div className="volume-slider-container">
                <div className="volume-slider-track">
                  <div
                    className="volume-slider-fill"
                    style={{ width: `${volume * 100}%` }}
                  ></div>
                </div>
              </div>
              <span className="volume-value">{(volume * 100).toFixed(0)}%</span>
            </div>
          </div>

          {/* Right Panel: Video Feed */}
          <div className="video-wrapper">
            <img ref={videoRef} alt="Live Gesture Feed" className="camera-feed" />
            <div className="video-overlay"></div>
          </div>
        </div>

      </div>
    </div>
  );
};

export default MainDisplay;