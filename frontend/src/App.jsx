import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './hooks/useAuth';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import HomePage from './pages/HomePage';
import MatchmakingPage from './pages/MatchmakingPage';
import MatchHistoryPage from './pages/MatchHistoryPage';
import './App.css';

const ProtectedRoute = ({ children }) => {
  const { user } = useAuth();
  return user ? children : <Navigate to="/login" />;
};

function AppContent() {
  const { user } = useAuth();

  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route path="/" element={user ? <HomePage /> : <Navigate to="/login" />} />
      <Route path="/matchmaking" element={user ? <MatchmakingPage /> : <Navigate to="/login" />} />
      <Route path="/history" element={user ? <MatchHistoryPage /> : <Navigate to="/login" />} />
    </Routes>
  );
}

function App() {
  return (
    <Router>
      <AuthProvider>
        <AppContent />
      </AuthProvider>
    </Router>
  );
}

export default App;