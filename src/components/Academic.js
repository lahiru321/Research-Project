import React, { useState } from 'react';
import { db } from '../firebase'; 
import { addDoc, collection } from 'firebase/firestore';
import './Academic.css';
import { useNavigate } from 'react-router-dom';

function Academic() {
  const navigate = useNavigate();
  const [subject, setSubject] = useState('');
  const [topic, setTopic] = useState('');
  const [isRunning, setIsRunning] = useState(false);
  const [learningPlan, setLearningPlan] = useState(null); 

  const handleStart = async () => {
    setIsRunning(true);
    try {
      const response = await fetch('http://localhost:8000/start', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ subject, topic }),
      });
      if (response.ok) {
        console.log('Engagement detection started');
      } else {
        console.error('Failed to start engagement detection:', response.status);
      }
    } catch (error) {
      console.error('Error starting the engagement detection:', error);
    }
  };

  const handleEnd = async (score) => {
    setIsRunning(false);
    try {
      const response = await fetch('http://localhost:8000/end', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ subject, topic, score }),
      });
      if (response.ok) {
        const data = await response.json();
        setLearningPlan(data.learning_plan); 
      } else {
        console.error('Failed to fetch learning plan:', response.status);
      }
    } catch (error) {
      console.error('Error ending the engagement detection:', error);
    }
  };

  const saveLearningPlan = async () => {
    if (!learningPlan) return; 
    try {
      await addDoc(collection(db, 'learning_plans'), {
        subject: subject,
        topic: topic,
        plan: learningPlan 
      });
      console.log('Learning plan saved successfully!');
    } catch (error) {
      console.error('Error adding document:', error);
    }
  };

  const renderLearningPlan = () => {

    if (!learningPlan) return null;

    return (
      <div className="learning-plan">
        <h2>Generated Learning Plan</h2>
        <h4>Video Links:</h4>
        <pre>{learningPlan.video_links}</pre> 
        <h4>Quizzes:</h4>
        <pre>{learningPlan.quizzes}</pre> 
        <h4>Exercises:</h4>
        <pre>{learningPlan.exercises}</pre> 
        
        <button className="academic-button" onClick={saveLearningPlan}>
          Save Learning Plan
        </button>
      </div>
    );
  };

  return (
    <div className="academic-container">
      <h1 className="academic-title">Academic Page</h1>
      <p className="academic-description">
        Enter subject and topic, then start the engagement detection program.
      </p>
      <input
        type="text"
        value={subject}
        onChange={(e) => setSubject(e.target.value)}
        placeholder="Enter subject name"
        className="academic-input"
      />
      <input
        type="text"
        value={topic}
        onChange={(e) => setTopic(e.target.value)}
        placeholder="Enter topic"
        className="academic-input"
      />
      <button className="academic-button" onClick={handleStart} disabled={isRunning || !subject || !topic}>
        Start Program
      </button>
      <button className="academic-button" onClick={() => handleEnd(70)} disabled={!isRunning}>
        End Program
      </button>
      <button className="academic-button learning-plan-button" onClick={() => navigate('/learning-plans')}>
        Learning Plan 
      </button>

      {renderLearningPlan()} 
    </div>
  );
}

export default Academic;
