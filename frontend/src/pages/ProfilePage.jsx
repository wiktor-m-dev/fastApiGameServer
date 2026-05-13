import React, { useState, useEffect } from 'react';
import { Container, Card, Button, Row, Col, Spinner, Alert } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { userAPI } from '../services/api';

const ProfilePage = () => {
  const { user, isAuthenticated, logout } = useAuth();
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }

    const fetchProfile = async () => {
      try {
        setLoading(true);
        const data = await userAPI.getUser(user.user_id);
        setProfile(data);
      } catch (err) {
        setError(err.message || 'Failed to load profile');
      } finally {
        setLoading(false);
      }
    };

    fetchProfile();
  }, [isAuthenticated, user, navigate]);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const handleFindMatch = () => {
    navigate('/matchmaking');
  };

  const handleViewHistory = () => {
    navigate('/match-history');
  };

  if (!isAuthenticated) {
    return null;
  }

  if (loading) {
    return (
      <Container className="d-flex justify-content-center align-items-center min-vh-100">
        <Spinner animation="border" role="status">
          <span className="visually-hidden">Loading...</span>
        </Spinner>
      </Container>
    );
  }

  return (
    <Container className="py-5">
      {error && <Alert variant="danger">{error}</Alert>}

      <Card className="shadow mb-4">
        <Card.Body>
          <Row>
            <Col md={6}>
              <h2 className="mb-4">Player Profile</h2>
              {profile && (
                <div>
                  <p>
                    <strong>Username:</strong> {profile.username}
                  </p>
                  <p>
                    <strong>Character Name:</strong>{' '}
                    {profile.character_name || 'Not set'}
                  </p>
                  <p>
                    <strong>Level:</strong> {profile.level}
                  </p>
                </div>
              )}
            </Col>
            <Col md={6}>
              <h3 className="mb-3">Character Stats</h3>
              {profile && (
                <div>
                  <div className="mb-2">
                    <strong>Health:</strong> {profile.health}
                  </div>
                  <div className="mb-2">
                    <strong>Attack:</strong> {profile.attack}
                  </div>
                  <div className="mb-2">
                    <strong>Defense:</strong> {profile.defense}
                  </div>
                </div>
              )}
            </Col>
          </Row>
        </Card.Body>
      </Card>

      <Row className="g-3 mb-4">
        <Col md={4}>
          <Button
            variant="primary"
            className="w-100"
            onClick={handleFindMatch}
            size="lg"
          >
            Find Match
          </Button>
        </Col>
        <Col md={4}>
          <Button
            variant="info"
            className="w-100"
            onClick={handleViewHistory}
            size="lg"
          >
            Match History
          </Button>
        </Col>
        <Col md={4}>
          <Button
            variant="danger"
            className="w-100"
            onClick={handleLogout}
            size="lg"
          >
            Logout
          </Button>
        </Col>
      </Row>
    </Container>
  );
};

export default ProfilePage;
