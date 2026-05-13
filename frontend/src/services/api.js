const API = 'http://localhost:8002';

const request = async (endpoint, method = 'GET', body = null) => {
  const opts = { method, headers: { 'Content-Type': 'application/json' } };
  if (body) opts.body = JSON.stringify(body);
  
  const res = await fetch(API + endpoint, opts);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
};

export const authAPI = {
  register: (username, password) => request('/register', 'POST', { username, password }),
  login: (username, password) => request('/login', 'POST', { username, password }),
};

export const userAPI = {
  getUser: (id) => request(`/user/${id}`),
};

export const queueAPI = {
  join: (userId) => request('/queue/join', 'POST', { user_id: userId }),
  getStatus: (userId) => request(`/queue/status/${userId}`),
  leave: (userId) => request(`/queue/leave/${userId}`, 'POST'),
};

export const matchAPI = {
  getMatch: (matchId) => request(`/match/${matchId}`),
  endMatch: (matchId, userId) => request(`/match/${matchId}/end`, 'POST', { user_id: userId }),
  getHistory: (userId) => request(`/match/history/${userId}`),
};


