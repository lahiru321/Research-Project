import React, { useState } from 'react';
import './Academic.css'; // Import the CSS file

function Academic() {
  const [isRunning, setIsRunning] = useState(false);

  // Function to start the engagement detection system
  const handleStart = async () => {
    setIsRunning(true);
    try {
      const response = await fetch('http://localhost:8000/start', { method: 'POST' });
      if (response.ok) {
        console.log('Engagement detection started');
      }
    } catch (error) {
      console.error('Error starting the engagement detection:', error);
    }
  };

  // Function to end the engagement detection system
  const handleEnd = async () => {
    setIsRunning(false);
    try {
      const response = await fetch('http://localhost:8000/end', { method: 'POST' });
      if (response.ok) {
        console.log('Engagement detection ended');
      }
    } catch (error) {
      console.error('Error ending the engagement detection:', error);
    }
  };

  return (
    <div className="academic-container">
      <h1 className="academic-title">Academic Page</h1>
      <p className="academic-description">
        Click the buttons below to start and end the engagement detection program.
      </p>
      <button className="academic-button" onClick={handleStart} disabled={isRunning}>
        Start Program
      </button>
      <button className="academic-button" onClick={handleEnd} disabled={!isRunning}>
        End Program
      </button>
    </div>
  );
}

export default Academic;
