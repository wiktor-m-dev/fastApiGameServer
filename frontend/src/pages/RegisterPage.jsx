import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { authAPI } from '../services/api';
import { useAuth } from '../hooks/useAuth';

export default function RegisterPage() {
  const [user, setUser] = useState('');
  const [pwd, setPwd] = useState('');
  const [err, setErr] = useState('');
  const [load, setLoad] = useState(false);
  const { login } = useAuth();
  const nav = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErr('');
    setLoad(true);
    try {
      const res = await authAPI.register(user, pwd);
      login({ user_id: res.user_id, username: res.username });
      nav('/');
    } catch (e) {
      setErr(e.message);
    } finally {
      setLoad(false);
    }
  };

  return (
    <div style={{ maxWidth: '400px', margin: '50px auto', padding: '20px', border: '1px solid #ccc' }}>
      <h2>Register</h2>
      {err && <p style={{ color: 'red' }}>{err}</p>}
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Username"
          value={user}
          onChange={(e) => setUser(e.target.value)}
          style={{ width: '100%', padding: '10px', marginBottom: '10px' }}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={pwd}
          onChange={(e) => setPwd(e.target.value)}
          style={{ width: '100%', padding: '10px', marginBottom: '10px' }}
          required
        />
        <button type="submit" style={{ width: '100%', padding: '10px' }} disabled={load}>
          {load ? 'Registering...' : 'Register'}
        </button>
      </form>
      <p><Link to="/login">Login</Link></p>
    </div>
  );
}
