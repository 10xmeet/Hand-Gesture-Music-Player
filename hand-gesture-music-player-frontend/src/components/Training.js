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
                        <p>Play professional EDM drum samples from "Something Just Like This" using your fingers. Each finger triggers a different sound - create your own beats!</p>
                    </div>

                    <div className="finger-mapping">
                        <h3>👆 Finger Controls</h3>
                        <div className="mapping-grid">
                            <div className="mapping-item">
                                <div className="finger-icon"><FaDrum /></div>
                                <div className="mapping-info">
                                    <strong>Thumb</strong>
                                    <span>Kick Drum</span>
                                </div>
                            </div>
                            <div className="mapping-item">
                                <div className="finger-icon"><FaGuitar /></div>
                                <div className="mapping-info">
                                    <strong>Index</strong>
                                    <span>Clap</span>
                                </div>
                            </div>
                            <div className="mapping-item">
                                <div className="finger-icon"><FaMusic /></div>
                                <div className="mapping-info">
                                    <strong>Middle</strong>
                                    <span>Snap</span>
                                </div>
                            </div>
                            <div className="mapping-item">
                                <div className="finger-icon"><FaMicrophone /></div>
                                <div className="mapping-info">
                                    <strong>Ring</strong>
                                    <span>Crash</span>
                                </div>
                            </div>
                            <div className="mapping-item">
                                <div className="finger-icon"><FaMusic /></div>
                                <div className="mapping-info">
                                    <strong>Pinky</strong>
                                    <span>Percussion</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div className="instruction-section">
                        <h3>🎮 How to Play</h3>
                        <ol className="instructions-list">
                            <li>Show your hand to the camera</li>
                            <li>Raise a finger to trigger a drum sound</li>
                            <li>Lower and raise again to play it again</li>
                            <li>Use multiple fingers to create rhythms</li>
                            <li>Move your hand up/down to control volume</li>
                        </ol>
                    </div>

                    <div className="tips-section">
                        <h3>💡 Pro Tips</h3>
                        <ul className="tips-list">
                            <li>Start with just the kick drum (thumb)</li>
                            <li>Add claps on beats 2 and 4</li>
                            <li>Layer in snaps and percussion for complexity</li>
                            <li>Create your own beat patterns!</li>
                            <li>Both hands work - double the fun!</li>
                        </ul>
                    </div>
                </div>

                <div className="training-footer">
                    <p>Switch to <strong>Stem Player</strong> mode to start playing!</p>
                </div>
            </div>
        </div>
    );
};

export default Training;
