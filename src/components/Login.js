import React, { useState } from 'react';
import { signInWithEmailAndPassword } from 'firebase/auth';
import { auth } from '../firebase';
import { Navigate, Link } from 'react-router-dom';

const Login = ({ setIsAuthenticated }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [redirectToHome, setRedirectToHome] = useState(false);

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      await signInWithEmailAndPassword(auth, email, password);
      setIsAuthenticated(true);
      setRedirectToHome(true);
    } catch (err) {
      setError(err.message);
    }
  };

  if (redirectToHome) {
    return <Navigate to="/" />;
  }

  return (
    <div style={styles.container}>
      <h1>Login</h1>
      {error && <p style={styles.error}>{error}</p>}
      <form onSubmit={handleLogin} style={styles.form}>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email"
          style={styles.input}
        />
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
          style={styles.input}
        />
        <button type="submit" style={styles.button}>Login</button>
      </form>
      <p style={styles.linkText}>
        Don't have an account? <Link to="/signup" style={styles.link}>Sign Up</Link>
      </p>
    </div>
  );
};

const styles = {
  container: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    height: '100vh',
    backgroundColor: '#f0f0f0',
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
  },
  input: {
    padding: '10px',
    margin: '10px',
    width: '250px',
    borderRadius: '5px',
    border: '1px solid #ccc',
  },
  button: {
    padding: '10px',
    margin: '10px',
    width: '250px',
    borderRadius: '5px',
    border: 'none',
    backgroundColor: '#4CAF50',
    color: 'white',
    fontSize: '16px',
    cursor: 'pointer',
  },
  error: {
    color: 'red',
  },
  linkText: {
    marginTop: '15px',
  },
  link: {
    color: '#4CAF50',
    textDecoration: 'none',
  },
};

export default Login;
