import React from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import Home from './components/Home';
import Academic from './components/Academic';
import Relationship from './components/Relationship';
import Social from './components/Social';
import Financial from './components/Financial';

function App() {
  return (
    <div>
      <nav style={styles.navbar}>
        <ul style={styles.navList}>
          <li><Link to="/" style={styles.navItem}>Home</Link></li>
          <li><Link to="/academic" style={styles.navItem}>Academic</Link></li>
          <li><Link to="/relationship" style={styles.navItem}>Relationship</Link></li>
          <li><Link to="/social" style={styles.navItem}>Social</Link></li>
          <li><Link to="/financial" style={styles.navItem}>ExpenseWise</Link></li>
        </ul>
      </nav>

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/academic" element={<Academic />} />
        <Route path="/relationship" element={<Relationship />} />
        <Route path="/social" element={<Social />} />
        <Route path="/financial" element={<Financial />} />
      </Routes>
    </div>
  );
}

const styles = {
  navbar: { backgroundColor: '#f8f8f8', padding: '10px' },
  navList: { listStyleType: 'none', display: 'flex', justifyContent: 'space-around' },
  navItem: { textDecoration: 'none', color: 'black', fontWeight: 'bold' },
};

export default App;
