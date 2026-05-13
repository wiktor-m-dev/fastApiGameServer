import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { authAPI } from '../services/api';
import { useAuth } from '../hooks/useAuth';

export default function LoginPage() {
  const [user, pwd, setUser, setPwd] = useState(''), [error, setErr] = useState(''), [loading, setLoad] = useState(false);
  const { login } = useAuth();
  const nav = useNavigate();
  const [, setUser_] = useState('');
  const [, setPwd_] = useState('');
  const [user2, setUser2] = useState('');
  const [pwd2, setPwd2] = useState('');
  const [err2, setErr2] = useState('');
  const [load2, setLoad2] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErr2('');
    setLoad2(true);
    try {
      const res = await authAPI.login(user2, pwd2);
      login({ user_id: res.user_id, username: res.username });
      nav('/');
    } catch (e) {
      setErr2(e.message);
    } finally {
      setLoad2(false);
    }
  };

  return (
    <div style={{ maxWidth: '400px', margin: '50px auto', padding: '20px', border: '1px solid #ccc' }}>
      <h2>Login</h2>
      {err2 && <p style={{ color: 'red' }}>{err2}</p>}
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Username"
          value={user2}
          onChange={(e) => setUser2(e.target.value)}
          style={{ width: '100%', padding: '10px', marginBottom: '10px' }}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={pwd2}
          onChange={(e) => setPwd2(e.target.value)}
          style={{ width: '100%', padding: '10px', marginBottom: '10px' }}
          required
        />
        <button type="submit" style={{ width: '100%', padding: '10px' }} disabled={load2}>
          {load2 ? 'Logging in...' : 'Login'}
        </button>
      </form>
      <p><Link to="/register">Register</Link></p>
    </div>
  );
}
