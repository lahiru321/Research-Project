import React, { useState } from 'react';

function Academic() {
  const [isRunning, setIsRunning] = useState(false);

  // Function to start the engagement detection system
  const handleStart = async () => {
    setIsRunning(true);
    try {
      const response = await fetch('http://localhost:5000/start', { method: 'POST' });
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
      const response = await fetch('http://localhost:5000/end', { method: 'POST' });
      if (response.ok) {
        console.log('Engagement detection ended');
      }
    } catch (error) {
      console.error('Error ending the engagement detection:', error);
    }
  };

  return (
    <div>
      <h1>Academic Page</h1>
      <p>Click the buttons below to start and end the engagement detection program.</p>
      <button onClick={handleStart} disabled={isRunning}>
        Start Program
      </button>
      <button onClick={handleEnd} disabled={!isRunning}>
        End Program
      </button>
    </div>
  );
}

export default Academic;
