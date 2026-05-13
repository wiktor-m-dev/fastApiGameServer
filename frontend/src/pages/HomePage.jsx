import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { userAPI, matchAPI } from '../services/api';

export default function HomePage() {
  const { user, logout } = useAuth();
  const [profile, setProfile] = useState(null);
  const [matches, setMatches] = useState([]);
  const nav = useNavigate();

  useEffect(() => {
    if (!user) return;
    
    userAPI.getUser(user.user_id)
      .then(p => setProfile(p))
      .catch(e => console.error(e));
    
    matchAPI.getHistory(user.user_id)
      .then(h => setMatches(h.matches || []))
      .catch(e => console.error(e));
  }, [user]);

  const handleFindMatch = () => {
    nav('/matchmaking');
  };

  const handleLogout = () => {
    logout();
    nav('/login');
  };

  if (!user) return <Link to="/login">Login</Link>;

  return (
    <div style={{ padding: '20px' }}>
      <button onClick={handleLogout} style={{ float: 'right' }}>Logout</button>
      <h1>Welcome, {user.username}!</h1>
      
      {profile && (
        <div>
          <h2>Profile</h2>
          <p>Level: {profile.level}</p>
          <p>Attack: {profile.attack}</p>
          <p>Defense: {profile.defense}</p>
          <p>Health: {profile.health}</p>
        </div>
      )}

      <div style={{ marginTop: '20px' }}>
        <h2>Matchmaking</h2>
        <button onClick={handleFindMatch}>Find Match</button>
      </div>

      <div style={{ marginTop: '20px' }}>
        <h2>Match History ({matches.length})</h2>
        {matches.map(m => (
          <div key={m.match_id} style={{ border: '1px solid #ddd', padding: '10px', margin: '5px 0' }}>
            Match {m.match_id}: {m.winner_id ? 'Completed' : 'In Progress'}
          </div>
        ))}
      </div>
    </div>
  );
}
