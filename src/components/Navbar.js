// Navbar.js
import React from 'react';
import { Link } from 'react-router-dom';
import { signOut } from 'firebase/auth';  
import { auth } from '../firebase';          // Adjust path if necessary
import './Navbar.css'; // Import the CSS file

const Navbar = ({ isAuthenticated, onSignOut }) => {
  return (
    isAuthenticated && (
      <nav className="navbar">
        <ul className="nav-list">
          <li className="nav-item"><Link to="/" className="nav-link">Home</Link></li>
          <li className="nav-item"><Link to="/academic" className="nav-link">Academic</Link></li>
          <li className="nav-item"><Link to="/relationship" className="nav-link">Relationship</Link></li>
          <li className="nav-item"><Link to="/social" className="nav-link">Social</Link></li>
          <li className="nav-item"><Link to="/financial" className="nav-link">Financial</Link></li>
          <li className="nav-item"><button onClick={onSignOut} className="sign-out-button">Sign Out</button></li>
        </ul>
      </nav>
    )
  );
};

export default Navbar;
