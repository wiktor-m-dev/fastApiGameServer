import React, { useState, useEffect } from 'react';
import { Container, Card, Button, Row, Col, Spinner, Alert, ProgressBar } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { queueAPI, matchAPI } from '../services/api';

const MatchmakingPage = () => {
  const { user, isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const [status, setStatus] = useState('idle'); // idle, waiting, matched
  const [error, setError] = useState('');
  const [matchData, setMatchData] = useState(null);
  const [timeRemaining, setTimeRemaining] = useState(30);
  const [pollInterval, setPollInterval] = useState(null);

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login');
    }
  }, [isAuthenticated, navigate]);

  // Poll for match status
  useEffect(() => {
    if (status === 'waiting' && user) {
      const checkStatus = async () => {
        try {
          const result = await queueAPI.getStatus(user.user_id);
          
          if (result.status === 'matched') {
            // Match found!
            setStatus('matched');
            setMatchData(result);
            if (pollInterval) clearInterval(pollInterval);
          }
        } catch (err) {
          console.error('Status check error:', err);
        }
      };

      const interval = setInterval(checkStatus, 1000); // Poll every second
      setPollInterval(interval);

      return () => {
        if (interval) clearInterval(interval);
      };
    }
  }, [status, user, pollInterval]);

  // Timer countdown
  useEffect(() => {
    if (status === 'waiting' && timeRemaining > 0) {
      const timer = setTimeout(() => {
        setTimeRemaining(t => t - 1);
      }, 1000);

      return () => clearTimeout(timer);
    } else if (status === 'waiting' && timeRemaining === 0) {
      // Timeout - leave queue
      handleLeaveQueue();
    }
  }, [status, timeRemaining]);

  const handleFindMatch = async () => {
    if (!user) return;

    try {
      setError('');
      setStatus('waiting');
      setTimeRemaining(30);
      
      const result = await queueAPI.join(user.user_id);
      
      if (result.status === 'matched') {
        // Immediately matched
        setStatus('matched');
        setMatchData(result);
      } else if (result.status === 'queued') {
        // Waiting for opponent
        setStatus('waiting');
      }
    } catch (err) {
      setError(err.message || 'Failed to join queue');
      setStatus('idle');
    }
  };

  const handleLeaveQueue = async () => {
    if (!user) return;

    try {
      await queueAPI.leave(user.user_id);
      setStatus('idle');
      setTimeRemaining(30);
      if (pollInterval) clearInterval(pollInterval);
    } catch (err) {
      setError(err.message || 'Failed to leave queue');
    }
  };

  const handleEndMatch = async () => {
    if (!matchData || !user) return;

    try {
      setError('');
      await matchAPI.endMatch(matchData.match_id, user.user_id);
      
      // Reset state
      setStatus('idle');
      setMatchData(null);
      setTimeRemaining(30);
      
      // Navigate to match history
      navigate('/history');
    } catch (err) {
      setError(err.message || 'Failed to end match');
    }
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

      {status === 'idle' && (
        <Card className="shadow-lg mx-auto" style={{ maxWidth: '500px' }}>
          <Card.Body className="text-center py-5">
            <h3 className="mb-4">Ready to Battle?</h3>
            <Button
              variant="primary"
              size="lg"
              onClick={handleFindMatch}
              className="px-5 py-3"
            >
              Find Opponent
            </Button>
          </Card.Body>
        </Card>
      )}

      {status === 'waiting' && (
        <Card className="shadow-lg mx-auto" style={{ maxWidth: '500px' }}>
          <Card.Body className="text-center py-5">
            <h3 className="mb-4">Searching for Opponent...</h3>
            <Spinner animation="border" role="status" className="mb-4">
              <span className="visually-hidden">Loading...</span>
            </Spinner>
            
            <div className="mb-4">
              <p className="mb-2">Time remaining: <strong>{timeRemaining}s</strong></p>
              <ProgressBar 
                now={(timeRemaining / 30) * 100} 
                striped 
                animated 
                className="mb-4"
              />
            </div>

            <Button
              variant="danger"
              size="sm"
              onClick={handleLeaveQueue}
            >
              Cancel Search
            </Button>
          </Card.Body>
        </Card>
      )}

      {status === 'matched' && matchData && (
        <div>
          <Row className="g-3 mb-4">
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

          <div className="text-center">
            <Button
              variant="success"
              size="lg"
              onClick={handleEndMatch}
              className="px-5 py-3"
            >
              End Match
            </Button>
          </div>
        </div>
      )}
    </Container>
  );
};

export default MatchmakingPage;
