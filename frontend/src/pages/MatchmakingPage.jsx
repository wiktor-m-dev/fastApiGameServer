import React, { useState } from 'react';
import { Container, Card, Button, Row, Col, Spinner, Alert } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { matchAPI } from '../services/api';

const MatchmakingPage = () => {
  const { user, isAuthenticated } = useAuth();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [matchData, setMatchData] = useState(null);
  const navigate = useNavigate();

  React.useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login');
    }
  }, [isAuthenticated, navigate]);

  const handleFindMatch = async () => {
    if (!user) return;

    try {
      setLoading(true);
      setError('');
      const result = await matchAPI.findMatch(user.user_id);
      setMatchData(result);
    } catch (err) {
      setError(err.message || 'Failed to find match');
    } finally {
      setLoading(false);
    }
  };

  const handleBackToProfile = () => {
    navigate('/profile');
  };

  if (!isAuthenticated) {
    return null;
  }

  return (
    <Container className="py-5">
      <div className="text-center mb-5">
        <h1 className="display-4 mb-4">Matchmaking Arena</h1>
        <p className="fs-5 text-muted">Find an opponent and prove your worth!</p>
      </div>

      {error && <Alert variant="danger">{error}</Alert>}

      {!matchData ? (
        <Card className="shadow-lg mx-auto" style={{ maxWidth: '500px' }}>
          <Card.Body className="text-center py-5">
            <h3 className="mb-4">Ready to Battle?</h3>
            <Button
              variant="primary"
              size="lg"
              onClick={handleFindMatch}
              disabled={loading}
              className="px-5 py-3"
            >
              {loading ? (
                <>
                  <Spinner
                    animation="border"
                    size="sm"
                    className="me-2"
                    role="status"
                  >
                    <span className="visually-hidden">Loading...</span>
                  </Spinner>
                  Finding opponent...
                </>
              ) : (
                'Find Opponent'
              )}
            </Button>
          </Card.Body>
        </Card>
      ) : (
        <Row className="g-3">
          <Col md={5}>
            <Card className="shadow-lg">
              <Card.Header className="bg-primary text-white">
                <h5 className="mb-0">Your Character</h5>
              </Card.Header>
              <Card.Body>
                <p>
                  <strong>Username:</strong> {user.username}
                </p>
                <hr />
                <div className="stats">
                  <p className="mb-1">
                    <strong>Level:</strong> <span className="badge bg-info">1</span>
                  </p>
                  <p className="mb-1">
                    <strong>Health:</strong> <span className="text-success">100</span>
                  </p>
                  <p className="mb-1">
                    <strong>Attack:</strong> <span className="text-danger">10</span>
                  </p>
                  <p>
                    <strong>Defense:</strong> <span className="text-warning">10</span>
                  </p>
                </div>
              </Card.Body>
            </Card>
          </Col>

          <Col md={2} className="d-flex align-items-center justify-content-center">
            <div className="text-center">
              <h2>VS</h2>
            </div>
          </Col>

          <Col md={5}>
            <Card className="shadow-lg">
              <Card.Header className="bg-danger text-white">
                <h5 className="mb-0">Opponent</h5>
              </Card.Header>
              <Card.Body>
                <p>
                  <strong>Username:</strong> {matchData.opponent.username}
                </p>
                <hr />
                <div className="stats">
                  <p className="mb-1">
                    <strong>Level:</strong>{' '}
                    <span className="badge bg-info">{matchData.opponent.level}</span>
                  </p>
                  <p className="mb-1">
                    <strong>Health:</strong>{' '}
                    <span className="text-success">{matchData.opponent.health}</span>
                  </p>
                  <p className="mb-1">
                    <strong>Attack:</strong>{' '}
                    <span className="text-danger">{matchData.opponent.attack}</span>
                  </p>
                  <p>
                    <strong>Defense:</strong>{' '}
                    <span className="text-warning">{matchData.opponent.defense}</span>
                  </p>
                </div>
              </Card.Body>
            </Card>
          </Col>
        </Row>
      )}

      <div className="text-center mt-5">
        <Button
          variant="secondary"
          onClick={handleBackToProfile}
          size="lg"
        >
          Back to Profile
        </Button>
      </div>
    </Container>
  );
};

export default MatchmakingPage;
