import GameNavbar from './components/Navbar';
import { Container, Button } from 'react-bootstrap';

function App() {
  return (
    <>
      <GameNavbar />
      <Container className="mt-5 text-center">
        <div className="p-5 mb-4 bg-light rounded-3 border">
          <h1 className="display-5 fw-bold">Welcome to the RPG Realm</h1>
          <p className="fs-4">
            Build your character, challenge rivals, and dominate the leaderboard.
          </p>
          <Button variant="primary" size="lg">Create Character</Button>
        </div>
      </Container>
    </>
  );
}

export default App;