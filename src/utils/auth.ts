// Simple authentication utilities for demo purposes
// In production, use proper authentication service

interface User {
  id: string;
  name: string;
  email: string;
  createdAt: string;
}

interface AuthData {
  user: User;
  token: string;
}

// Simulate user database (in production, use real database)
const USERS_KEY = 'job_forecaster_users';
const AUTH_KEY = 'job_forecaster_auth';

export const getStoredUsers = (): User[] => {
  const users = localStorage.getItem(USERS_KEY);
  return users ? JSON.parse(users) : [];
};

export const storeUser = (user: User): void => {
  const users = getStoredUsers();
  users.push(user);
  localStorage.setItem(USERS_KEY, JSON.stringify(users));
};

export const findUserByEmail = (email: string): User | null => {
  const users = getStoredUsers();
  return users.find(user => user.email === email) || null;
};

export const generateToken = (user: User): string => {
  // Simple token generation (in production, use JWT)
  return btoa(JSON.stringify({ userId: user.id, timestamp: Date.now() }));
};

export const validateToken = (token: string): boolean => {
  try {
    const decoded = JSON.parse(atob(token));
    // Token expires after 24 hours
    return Date.now() - decoded.timestamp < 24 * 60 * 60 * 1000;
  } catch {
    return false;
  }
};

export const login = async (email: string, password: string): Promise<AuthData | null> => {
  // Simulate API call delay
  await new Promise(resolve => setTimeout(resolve, 1000));
  
  const user = findUserByEmail(email);
  if (!user) {
    return null;
  }
  
  // In production, hash and compare passwords properly
  const storedPassword = localStorage.getItem(`password_${user.id}`);
  if (storedPassword !== password) {
    return null;
  }
  
  const token = generateToken(user);
  const authData = { user, token };
  
  localStorage.setItem(AUTH_KEY, JSON.stringify(authData));
  return authData;
};

export const signup = async (name: string, email: string, password: string): Promise<AuthData | null> => {
  // Simulate API call delay
  await new Promise(resolve => setTimeout(resolve, 1000));
  
  // Check if user already exists
  if (findUserByEmail(email)) {
    return null;
  }
  
  const user: User = {
    id: Date.now().toString(),
    name,
    email,
    createdAt: new Date().toISOString()
  };
  
  // Store user and password (in production, hash the password)
  storeUser(user);
  localStorage.setItem(`password_${user.id}`, password);
  
  const token = generateToken(user);
  const authData = { user, token };
  
  localStorage.setItem(AUTH_KEY, JSON.stringify(authData));
  return authData;
};

export const logout = (): void => {
  localStorage.removeItem(AUTH_KEY);
};

export const getCurrentAuth = (): AuthData | null => {
  const auth = localStorage.getItem(AUTH_KEY);
  if (!auth) return null;
  
  try {
    const authData = JSON.parse(auth);
    if (validateToken(authData.token)) {
      return authData;
    } else {
      logout();
      return null;
    }
  } catch {
    logout();
    return null;
  }
};