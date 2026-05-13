import React from 'react';
import { Container, Button } from 'react-bootstrap';
import { Link } from 'react-router-dom';

const HomePage = () => (
  <Container className="mt-5 text-center">
    <div className="p-5 mb-4 bg-light rounded-3 border">
      <h1 className="display-5 fw-bold">Welcome to the RPG Realm</h1>
      <p className="fs-4">
        Build your character, challenge rivals, and dominate the leaderboard.
      </p>
      <div className="d-flex gap-2 justify-content-center">
        <Link to="/login">
          <Button variant="primary" size="lg">
            Login
          </Button>
        </Link>
        <Link to="/register">
          <Button variant="success" size="lg">
            Create Account
          </Button>
        </Link>
      </div>
    </div>
  </Container>
);

export default HomePage;
