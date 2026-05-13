import React, { useState, useEffect } from 'react';
import { Container, Card, Button, Table, Spinner, Alert } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { matchAPI } from '../services/api';

const MatchHistoryPage = () => {
  const { user, isAuthenticated } = useAuth();
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }

    const fetchMatchHistory = async () => {
      try {
        setLoading(true);
        const data = await matchAPI.getMatchHistory(user.user_id);
        setMatches(data.matches || []);
      } catch (err) {
        setError(err.message || 'Failed to load match history');
      } finally {
        setLoading(false);
      }
    };

    fetchMatchHistory();
  }, [isAuthenticated, user, navigate]);

  const handleBackToProfile = () => {
    navigate('/profile');
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
      <h1 className="mb-4">Match History</h1>

      {error && <Alert variant="danger">{error}</Alert>}

      {matches.length === 0 ? (
        <Card className="text-center py-5">
          <Card.Body>
            <p className="text-muted fs-5">No matches found yet. Go find some opponents!</p>
          </Card.Body>
        </Card>
      ) : (
        <Card className="shadow-lg">
          <Card.Body>
            <Table striped bordered hover responsive>
              <thead className="table-dark">
                <tr>
                  <th>Match ID</th>
                  <th>Player 1</th>
                  <th>Player 2</th>
                  <th>Status</th>
                  <th>Date</th>
                </tr>
              </thead>
              <tbody>
                {matches.map((match) => (
                  <tr key={match.match_id}>
                    <td>#{match.match_id}</td>
                    <td>Player {match.player1_id}</td>
                    <td>Player {match.player2_id}</td>
                    <td>
                      <span className={`badge bg-${match.status === 'completed' ? 'success' : 'warning'}`}>
                        {match.status}
                      </span>
                    </td>
                    <td>{match.created_at || 'N/A'}</td>
                  </tr>
                ))}
              </tbody>
            </Table>
          </Card.Body>
        </Card>
      )}

      <div className="text-center mt-4">
        <Button
          variant="primary"
          onClick={handleBackToProfile}
          size="lg"
        >
          Back to Profile
        </Button>
      </div>
    </Container>
  );
};

export default MatchHistoryPage;
