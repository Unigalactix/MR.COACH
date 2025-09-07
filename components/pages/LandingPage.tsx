
import React from 'react';
import { Link } from 'react-router-dom';

const LandingPage: React.FC = () => {
  return (
    <div className="flex-grow flex items-center justify-center bg-gray-50 dark:bg-gray-900">
      <div className="text-center p-8">
        <div 
          className="relative inline-block p-10 bg-white dark:bg-gray-800 rounded-xl shadow-2xl overflow-hidden"
          style={{ backgroundImage: 'radial-gradient(circle at top left, rgba(129, 140, 248, 0.1), transparent 40%), radial-gradient(circle at bottom right, rgba(244, 114, 182, 0.1), transparent 40%)' }}
        >
          <h1 className="text-4xl md:text-6xl font-extrabold text-gray-900 dark:text-white mb-4 leading-tight">
            Welcome to the <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-500 to-pink-500">WIDA</span> Syllabus Tracker
          </h1>
          <p className="text-lg md:text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto mb-8">
            Your centralized platform for WIDA screener test preparation. Master your syllabus, track student progress, and achieve success together.
          </p>
          <Link
            to="/login"
            className="inline-block px-8 py-4 bg-indigo-600 text-white font-semibold rounded-lg shadow-lg hover:bg-indigo-700 transition-transform transform hover:scale-105 duration-300 ease-in-out"
          >
            Get Started
          </Link>
        </div>
      </div>
    </div>
  );
};

export default LandingPage;
