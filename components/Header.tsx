import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import BookOpenIcon from './icons/BookOpenIcon';
import { Role } from '../types';

const Header: React.FC = () => {
  const { isAuthenticated, user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <header className="bg-white dark:bg-gray-800 shadow-md sticky top-0 z-50">
      <div className="container mx-auto px-6 py-4 flex justify-between items-center">
        <Link to="/" className="flex items-center space-x-2 text-xl font-bold text-gray-800 dark:text-white">
          <BookOpenIcon className="h-6 w-6 text-indigo-500" />
          <span>WIDA Syllabus Tracker</span>
        </Link>
        <div className="flex items-center space-x-4">
          {isAuthenticated ? (
            <>
              <span className="text-gray-600 dark:text-gray-300 hidden sm:block">
                Welcome, <span className="font-semibold">{user?.uniqueId}</span>
              </span>
              {user?.role === Role.MASTER && (
                <Link
                  to="/syllabus-management"
                  className="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors duration-300 hidden sm:block"
                  aria-label="Manage Syllabus"
                >
                  Manage Syllabus
                </Link>
              )}
              <button
                onClick={handleLogout}
                className="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors duration-300"
              >
                Logout
              </button>
            </>
          ) : (
            <>
                <Link
                    to="/login"
                    className="px-4 py-2 bg-indigo-500 text-white rounded-lg hover:bg-indigo-600 transition-colors duration-300"
                >
                    Login
                </Link>
                <Link
                  to="/register"
                  className="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors duration-300 hidden sm:block"
                  aria-label="Register as a new student"
                >
                  Register
                </Link>
            </>
          )}
        </div>
      </div>
    </header>
  );
};

export default Header;
