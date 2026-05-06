import { Navbar, Container, Nav } from 'react-bootstrap';

const GameNavbar = () => (
  <Navbar bg="dark" variant="dark" expand="lg">
    <Container>
      <Navbar.Brand href="#home">FastAPI RPG</Navbar.Brand>
      <Nav className="me-auto">
        <Nav.Link href="#home">Home</Nav.Link>
        <Nav.Link href="#matchmaking">Matchmaking</Nav.Link>
      </Nav>
    </Container>
  </Navbar>
);

export default GameNavbar;