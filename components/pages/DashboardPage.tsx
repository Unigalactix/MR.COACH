import React, { useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import { useSyllabus } from '../../hooks/useSyllabus';
import { Role } from '../../types';

const MasterDashboardContent: React.FC = () => (
  <>
    <h2 className="text-xl font-semibold text-gray-800 dark:text-white mb-4">Syllabus Management</h2>
    <div className="text-center py-16 border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg">
      <p className="text-gray-500 dark:text-gray-400">Manage syllabus content and track all student progress.</p>
      <Link
        to="/syllabus-management"
        className="mt-4 inline-block px-6 py-2 bg-indigo-600 text-white font-semibold rounded-lg shadow-md hover:bg-indigo-700 transition-colors duration-300"
      >
        Go to Management
      </Link>
    </div>
  </>
);

const StudentDashboardContent: React.FC = () => {
  const { user } = useAuth();
  const { topics, getResultsForStudent } = useSyllabus();
  const studentResults = user ? getResultsForStudent(user.uniqueId) : [];

  return (
    <>
      <div className="mb-8">
        <h2 className="text-xl font-semibold text-gray-800 dark:text-white mb-4">Syllabus Topics</h2>
        <div className="bg-gray-50 dark:bg-gray-900 rounded-lg shadow-inner p-4 space-y-3">
          {topics.length > 0 ? (
            topics.map(topic => (
              <Link 
                key={topic.id} 
                to={`/test/${topic.id}`}
                className="block p-4 bg-white dark:bg-gray-800 rounded-lg shadow-sm hover:shadow-md hover:bg-indigo-50 dark:hover:bg-gray-700 transition-all duration-300"
              >
                <h3 className="font-semibold text-indigo-600 dark:text-indigo-400">{topic.title}</h3>
              </Link>
            ))
          ) : (
            <p className="text-gray-500 dark:text-gray-400">No syllabus topics available yet.</p>
          )}
        </div>
      </div>

      <div>
        <h2 className="text-xl font-semibold text-gray-800 dark:text-white mb-4">Your Progress</h2>
        <div className="text-center py-10 border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg">
          <p className="text-lg text-gray-600 dark:text-gray-300">
            You have completed <span className="font-bold text-indigo-500">{studentResults.length}</span> {studentResults.length === 1 ? 'test' : 'tests'}.
          </p>
          <p className="text-gray-500 dark:text-gray-400 mt-2">Keep up the great work!</p>
        </div>
      </div>
    </>
  );
};


const DashboardPage: React.FC = () => {
  const { user, isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login');
    }
  }, [isAuthenticated, navigate]);

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  if (!user) {
    return null; // or a loading spinner
  }

  const roleText = user.role === Role.MASTER ? 'Master' : 'Student';
  const roleColor = user.role === Role.MASTER ? 'bg-green-100 text-green-800' : 'bg-blue-100 text-blue-800';

  return (
    <div className="flex-grow container mx-auto px-6 py-12">
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-8 max-w-3xl mx-auto">
        <div className="flex justify-between items-start">
            <div>
                 <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Dashboard</h1>
                 <p className="mt-2 text-gray-600 dark:text-gray-300">Welcome back, {user.uniqueId}</p>
            </div>
            <span className={`px-3 py-1 text-sm font-semibold rounded-full ${roleColor}`}>{roleText}</span>
        </div>
       
        <div className="mt-8 border-t border-gray-200 dark:border-gray-700 pt-8">
            {user.role === Role.MASTER ? <MasterDashboardContent /> : <StudentDashboardContent />}
        </div>

        <div className="mt-8 text-right">
             <button
                onClick={handleLogout}
                className="px-6 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors duration-300"
              >
                Logout
              </button>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;
