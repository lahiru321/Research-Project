import React, { useEffect, useState } from 'react';
import './LearningPlans.css'; // Import the CSS file

function LearningPlans() {
  const [plans, setPlans] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [openIndex, setOpenIndex] = useState(null); // State for controlling the open items

  useEffect(() => {
    const fetchPlans = async () => {
      setLoading(true);
      setError(null);

      try {
        const response = await fetch('http://localhost:8000/learning-plans');
        if (!response.ok) {
          throw new Error('Failed to fetch learning plans');
        }
        const data = await response.json();
        setPlans(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchPlans();
  }, []);

  const formatLinks = (text) => {
    const linkRegex = /\[([^\]]+)\]\((https?:\/\/[^\s]+)\)/g;
    return text.split('\n').map((line, index) =>
      <div key={index} dangerouslySetInnerHTML={{ __html: line.replace(linkRegex, '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>') }} />
    );
  };

  const formatExercises = (exercises) => {
    if (!exercises) return "No exercises available.";
    return exercises.split('Day').map((day, index) => {
      if (day.trim()) {
        return (
          <div key={index}>
            <strong>Day {index + 1}:</strong> {day.trim()}
          </div>
        );
      }
      return null;
    });
  };

  const toggleAccordion = (index) => {
    setOpenIndex(openIndex === index ? null : index); // Toggle the open index
  };

  if (loading) {
    return <p>Loading...</p>;
  }

  if (error) {
    return <p>Error: {error}</p>;
  }

  return (
    <div className="learning-plans">
      <h1>Your Learning Plans</h1>
      {plans.length === 0 ? (
        <p>No learning plans found.</p>
      ) : (
        plans.map((plan, index) => (
          <div key={plan.id} className="accordion-item">
            <div className="accordion-header" onClick={() => toggleAccordion(index)}>
              <h2>{plan.subject} - {plan.topic}</h2>
            </div>
            {openIndex === index && (
              <div className="accordion-body">
                <div>
                  <strong>Exercises:</strong>
                  {formatExercises(plan.plan.exercises)}
                </div>
                <div>
                  <strong>Quizzes:</strong>
                  {formatLinks(plan.plan.quizzes)}
                </div>
                <div>
                  <strong>Video Links:</strong>
                  {formatLinks(plan.plan.video_links)}
                </div>
              </div>
            )}
          </div>
        ))
      )}
    </div>
  );
}

export default LearningPlans;
