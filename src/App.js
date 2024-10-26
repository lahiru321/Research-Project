// App.js
import React, { useState, useEffect } from 'react';
import { Routes, Route, useNavigate } from 'react-router-dom';
import Home from './components/Home';
import Academic from './components/Academic';
import Relationship from './components/Relationship';
import Social from './components/Social';
import Financial from './components/Financial';
import Login from './components/Login';
import Signup from './components/Signup';
import Navbar from './components/Navbar'; // Import the Navbar component
import { signOut } from 'firebase/auth';  // Import signOut from Firebase
import { auth } from './firebase';          // Import the initialized auth

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const navigate = useNavigate(); // Hook for navigation

  useEffect(() => {
    const unsubscribe = auth.onAuthStateChanged(user => {
      if (user) {
        setIsAuthenticated(true); // User is signed in
      } else {
        setIsAuthenticated(false); // No user is signed in
      }
    });

    // Clean up the observer on unmount
    return () => unsubscribe();
  }, []);

  const handleSignOut = async () => {
    await signOut(auth);
    setIsAuthenticated(false); // Update authenticated state
    navigate('/login'); // Redirect to login page after sign out
  };

  return (
    <div>
      <Navbar isAuthenticated={isAuthenticated} onSignOut={handleSignOut} /> {/* Use Navbar component */}
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/academic" element={<Academic />} />
        <Route path="/relationship" element={<Relationship />} />
        <Route path="/social" element={<Social />} />
        <Route path="/financial" element={<Financial />} />
        <Route path="/login" element={<Login setIsAuthenticated={setIsAuthenticated} />} />
        <Route path="/signup" element={<Signup />} />
      </Routes>
    </div>
  );
}

export default App;
