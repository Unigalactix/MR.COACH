import React, { createContext, useState, ReactNode, useCallback } from 'react';
import { User, Role } from '../types';

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  login: (uniqueId: string) => Promise<User>;
  logout: () => void;
  register: (uniqueId: string) => Promise<void>;
  getUsers: () => User[];
  removeUser: (uniqueId: string) => Promise<void>;
}

export const AuthContext = createContext<AuthContextType | null>(null);

interface AuthProviderProps {
  children: ReactNode;
}

// Mock users database
const INITIAL_MOCK_USERS: Record<string, { role: Role }> = {
  'KRURA': { role: Role.MASTER },
  'student1': { role: Role.STUDENT },
  'student2': { role: Role.STUDENT },
};

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [users, setUsers] = useState(INITIAL_MOCK_USERS);
  const [user, setUser] = useState<User | null>(() => {
    const storedUser = localStorage.getItem('user');
    try {
      if (storedUser) {
        return JSON.parse(storedUser);
      }
    } catch (error) {
      console.error("Failed to parse user from localStorage", error);
    }
    return null;
  });

  const login = useCallback((uniqueId: string): Promise<User> => {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        if (uniqueId in users) {
          const loggedInUser: User = {
            uniqueId: uniqueId,
            role: users[uniqueId].role,
          };
          setUser(loggedInUser);
          localStorage.setItem('user', JSON.stringify(loggedInUser));
          resolve(loggedInUser);
        } else {
          reject(new Error('Invalid Unique ID'));
        }
      }, 500);
    });
  }, [users]);

  const logout = useCallback(() => {
    setUser(null);
    localStorage.removeItem('user');
  }, []);

  const register = useCallback((uniqueId: string): Promise<void> => {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        if (!uniqueId) {
          return reject(new Error('Unique ID cannot be empty.'));
        }
        if (uniqueId in users) {
          return reject(new Error('This Unique ID is already taken.'));
        }
        
        setUsers(prevUsers => ({
          ...prevUsers,
          [uniqueId]: { role: Role.STUDENT }
        }));
        
        resolve();
      }, 500);
    });
  }, [users]);

  const getUsers = useCallback((): User[] => {
    return Object.entries(users).map(([uniqueId, data]) => ({
        uniqueId,
        role: data.role
    }));
  }, [users]);

  const removeUser = useCallback((uniqueId: string): Promise<void> => {
    return new Promise((resolve, reject) => {
        if (!(uniqueId in users)) {
            return reject(new Error("User not found."));
        }
        if (users[uniqueId].role === Role.MASTER) {
            return reject(new Error("Cannot remove a master user."));
        }
        setUsers(prevUsers => {
            const newUsers = { ...prevUsers };
            delete newUsers[uniqueId];
            return newUsers;
        });
        resolve();
    });
  }, [users]);


  const isAuthenticated = !!user;

  return (
    <AuthContext.Provider value={{ user, isAuthenticated, login, logout, register, getUsers, removeUser }}>
      {children}
    </AuthContext.Provider>
  );
};
