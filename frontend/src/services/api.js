/**
 * API Service for FastAPI Backend Communication
 * Handles all HTTP requests to the game server
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Helper function for API calls
const apiCall = async (endpoint, options = {}) => {
  const url = `${API_BASE_URL}${endpoint}`;
  const defaultHeaders = {
    'Content-Type': 'application/json',
  };

  const response = await fetch(url, {
    ...options,
    headers: {
      ...defaultHeaders,
      ...options.headers,
    },
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'API request failed');
  }

  return response.json();
};

// Authentication API calls
export const authAPI = {
  register: (username, password) =>
    apiCall('/register', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    }),

  login: (username, password) =>
    apiCall('/login', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    }),
};

// User API calls
export const userAPI = {
  getUser: (userId) =>
    apiCall(`/user/${userId}`, {
      method: 'GET',
    }),

  updateProfile: (userId, data) =>
    apiCall(`/user/${userId}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    }),
};

// Match API calls
export const matchAPI = {
  findMatch: (userId) =>
    apiCall('/match', {
      method: 'POST',
      body: JSON.stringify({ user_id: userId }),
    }),

  getMatchHistory: (userId) =>
    apiCall(`/match/history/${userId}`, {
      method: 'GET',
    }),

  getMatch: (matchId) =>
    apiCall(`/match/${matchId}`, {
      method: 'GET',
    }),
};

// Health check
export const systemAPI = {
  healthCheck: () =>
    apiCall('/health', {
      method: 'GET',
    }),
};
