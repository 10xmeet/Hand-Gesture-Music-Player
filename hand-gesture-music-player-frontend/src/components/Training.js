import React from 'react';
import { FaHandPaper, FaDrum, FaGuitar, FaMicrophone, FaMusic } from 'react-icons/fa';
import './Training.css';

const Training = () => {
    return (
        <div className="training-container">
            <div className="training-card">
                <h2 className="training-title">How to Use Stem Player</h2>

                <div className="training-content">
                    <div className="instruction-section">
                        <h3>🎵 What is Stem Player?</h3>
                        <p>Control individual instruments of "Animals" by Martin Garrix using your fingers. Each finger controls a different part of the song!</p>
                    </div>

                    <div className="finger-mapping">
                        <h3>👆 Finger Controls</h3>
                        <div className="mapping-grid">
                            <div className="mapping-item">
                                <div className="finger-icon"><FaDrum /></div>
                                <div className="mapping-info">
                                    <strong>Thumb</strong>
                                    <span>Drums</span>
                                </div>
                            </div>
                            <div className="mapping-item">
                                <div className="finger-icon"><FaGuitar /></div>
                                <div className="mapping-info">
                                    <strong>Index</strong>
                                    <span>Bass</span>
                                </div>
                            </div>
                            <div className="mapping-item">
                                <div className="finger-icon"><FaMusic /></div>
                                <div className="mapping-info">
                                    <strong>Middle</strong>
                                    <span>Melody</span>
                                </div>
                            </div>
                            <div className="mapping-item">
                                <div className="finger-icon"><FaMicrophone /></div>
                                <div className="mapping-info">
                                    <strong>Ring</strong>
                                    <span>Vocals</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div className="instruction-section">
                        <h3>🎮 How to Play</h3>
                        <ol className="instructions-list">
                            <li>Show your hand to the camera</li>
                            <li>Raise fingers to unmute instruments</li>
                            <li>Lower fingers to mute them</li>
                            <li>Mix multiple instruments by raising multiple fingers</li>
                            <li>Move your hand up/down to control volume</li>
                        </ol>
                    </div>

                    <div className="tips-section">
                        <h3>💡 Pro Tips</h3>
                        <ul className="tips-list">
                            <li>Start with just drums (thumb) to feel the beat</li>
                            <li>Add bass (index) for the foundation</li>
                            <li>Layer in melody and vocals for the full experience</li>
                            <li>Experiment with different combinations!</li>
                        </ul>
                    </div>
                </div>

                <div className="training-footer">
                    <p>Switch to <strong>Stem Player</strong> mode to start mixing!</p>
                </div>
            </div>
        </div>
    );
};

export default Training;
