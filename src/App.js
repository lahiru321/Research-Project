import React, { useState } from 'react';
import { Routes, Route, Link, useNavigate } from 'react-router-dom';
import Home from './components/Home';
import Academic from './components/Academic';
import Relationship from './components/Relationship';
import Social from './components/Social';
import Financial from './components/Financial';
import Login from './components/Login';
import Signup from './components/Signup';
import { signOut } from 'firebase/auth';  // Import signOut from Firebase
import { auth } from './firebase';          // Import the initialized auth

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const navigate = useNavigate(); // Hook for navigation

  const handleSignOut = async () => {
    await signOut(auth);
    setIsAuthenticated(false); // Update authenticated state
    navigate('/login'); // Redirect to login page after sign out
  };

  return (
    <div>

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

const styles = {
  navbar: { backgroundColor: '#f8f8f8', padding: '10px' },
  navList: { listStyleType: 'none', display: 'flex', justifyContent: 'space-around' },
  navItem: { textDecoration: 'none', color: 'black', fontWeight: 'bold' },
  signOutButton: { background: 'none', border: 'none', color: 'black', fontWeight: 'bold', cursor: 'pointer' }, // Styles for Sign Out button
};

export default App;
