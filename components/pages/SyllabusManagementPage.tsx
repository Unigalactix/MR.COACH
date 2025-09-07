import React, { useEffect, useState, useCallback, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import { useSyllabus } from '../../hooks/useSyllabus';
import { Role, User, TestResult } from '../../types';
import BarChart from '../analytics/BarChart';

const UserManagementSection: React.FC = () => {
    const { getUsers, removeUser, user: currentUser } = useAuth();
    const [users, setUsers] = useState<User[]>([]);
    const [error, setError] = useState('');
    const [message, setMessage] = useState('');

    const fetchUsers = useCallback(() => {
        const allUsers = getUsers().filter(u => u.uniqueId !== currentUser?.uniqueId);
        setUsers(allUsers);
    }, [getUsers, currentUser]);

    useEffect(() => {
        fetchUsers();
    }, [fetchUsers]);

    const handleRemoveUser = async (uniqueId: string) => {
        if (window.confirm(`Are you sure you want to remove user "${uniqueId}"?`)) {
            try {
                await removeUser(uniqueId);
                setMessage(`User "${uniqueId}" has been removed.`);
                setError('');
                fetchUsers(); 
            } catch (err) {
                setError(err instanceof Error ? err.message : 'Failed to remove user.');
                setMessage('');
            }
        }
    };

    return (
        <div className="mt-8 border-t border-gray-200 dark:border-gray-700 pt-8">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">User Management</h2>
            {error && <p className="text-red-500 bg-red-100 p-3 rounded-md mb-4">{error}</p>}
            {message && <p className="text-green-500 bg-green-100 p-3 rounded-md mb-4">{message}</p>}
            
            <div className="bg-gray-50 dark:bg-gray-900 rounded-lg shadow-inner p-4">
                {users.length > 0 ? (
                     <ul className="divide-y divide-gray-200 dark:divide-gray-700">
                        {users.map((user) => (
                             <li key={user.uniqueId} className="py-3 flex justify-between items-center">
                                <div>
                                    <p className="text-md font-semibold text-gray-800 dark:text-gray-200">{user.uniqueId}</p>
                                    <p className="text-sm text-gray-500 dark:text-gray-400 capitalize">{user.role}</p>
                                </div>
                                <button
                                    onClick={() => handleRemoveUser(user.uniqueId)}
                                    className="px-4 py-2 bg-red-600 text-white text-sm font-medium rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                                    aria-label={`Remove user ${user.uniqueId}`}
                                >
                                    Remove
                                </button>
                             </li>
                        ))}
                     </ul>
                ) : (
                    <p className="text-gray-500 dark:text-gray-400 text-center py-4">No other users found.</p>
                )}
            </div>
        </div>
    )
}

const SyllabusEditor: React.FC = () => {
    const { topics, addTopic } = useSyllabus();
    const [newTopicTitle, setNewTopicTitle] = useState('');
    const [error, setError] = useState('');

    const handleAddTopic = (e: React.FormEvent) => {
        e.preventDefault();
        if (!newTopicTitle.trim()) {
            setError('Topic title cannot be empty.');
            return;
        }
        try {
            addTopic(newTopicTitle);
            setNewTopicTitle('');
            setError('');
        } catch(err) {
            setError(err instanceof Error ? err.message : 'An error occurred.');
        }
    };

    return (
        <div className="mt-8 border-t border-gray-200 dark:border-gray-700 pt-8">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Syllabus Editor</h2>
            
            <form onSubmit={handleAddTopic} className="flex items-center space-x-2 mb-4">
                <input 
                    type="text"
                    value={newTopicTitle}
                    onChange={(e) => setNewTopicTitle(e.target.value)}
                    placeholder="Enter new topic title"
                    className="flex-grow p-2 border border-gray-300 dark:border-gray-600 rounded-md bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white"
                />
                <button type="submit" className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700">Add Topic</button>
            </form>
            {error && <p className="text-red-500 text-sm">{error}</p>}
            
            <div className="bg-gray-50 dark:bg-gray-900 rounded-lg shadow-inner p-4 mt-4">
                <h3 className="text-lg font-semibold mb-2">Existing Topics</h3>
                {topics.length > 0 ? (
                    <ul className="list-disc list-inside space-y-1">
                        {topics.map(topic => <li key={topic.id}>{topic.title}</li>)}
                    </ul>
                ) : (
                    <p className="text-gray-500 dark:text-gray-400">No topics created yet.</p>
                )}
            </div>
        </div>
    );
};

const StudentAnalytics: React.FC = () => {
    const { getAllResults, topics } = useSyllabus();
    const [results, setResults] = useState<TestResult[]>([]);
    const [filteredResults, setFilteredResults] = useState<TestResult[]>([]);
    
    const [selectedStudent, setSelectedStudent] = useState<string>('');
    const [selectedTopic, setSelectedTopic] = useState<string>('');

    useEffect(() => {
        const allResults = getAllResults();
        setResults(allResults);
    }, [getAllResults]);

    useEffect(() => {
        const filtered = results.filter(result => {
            const studentMatch = selectedStudent ? result.studentId === selectedStudent : true;
            const topicMatch = selectedTopic ? result.topicId === selectedTopic : true;
            return studentMatch && topicMatch;
        });
        setFilteredResults(filtered);
    }, [selectedStudent, selectedTopic, results]);

    const uniqueStudentIds = useMemo(() => [...new Set(results.map(r => r.studentId))].sort(), [results]);

    const chartData = useMemo(() => {
        if (results.length === 0) return [];

        const topicScores = new Map<string, { totalScore: number; count: number; title: string }>();

        topics.forEach(topic => {
            topicScores.set(topic.id, { totalScore: 0, count: 0, title: topic.title });
        });

        results.forEach(result => {
            const entry = topicScores.get(result.topicId);
            if (entry) {
                entry.totalScore += result.score;
                entry.count += 1;
            }
        });

        return Array.from(topicScores.values()).map(data => ({
            topicTitle: data.title,
            averageScore: data.count > 0 ? Math.round(data.totalScore / data.count) : 0,
        }));
    }, [results, topics]);
    
    return (
        <div className="mt-8 border-t border-gray-200 dark:border-gray-700 pt-8">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Student Analytics</h2>
            
            <div className="mb-8">
                <BarChart data={chartData} />
            </div>

            <div className="mb-6 grid grid-cols-1 md:grid-cols-3 gap-4 p-4 bg-gray-100 dark:bg-gray-900 rounded-lg">
                <div>
                    <label htmlFor="student-filter" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Filter by Student</label>
                    <select 
                        id="student-filter"
                        value={selectedStudent}
                        onChange={(e) => setSelectedStudent(e.target.value)}
                        className="block w-full pl-3 pr-10 py-2 text-base border-gray-300 dark:border-gray-600 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                    >
                        <option value="">All Students</option>
                        {uniqueStudentIds.map(id => <option key={id} value={id}>{id}</option>)}
                    </select>
                </div>
                <div>
                    <label htmlFor="topic-filter" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Filter by Topic</label>
                    <select 
                        id="topic-filter"
                        value={selectedTopic}
                        onChange={(e) => setSelectedTopic(e.target.value)}
                        className="block w-full pl-3 pr-10 py-2 text-base border-gray-300 dark:border-gray-600 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                    >
                        <option value="">All Topics</option>
                        {topics.map(topic => <option key={topic.id} value={topic.id}>{topic.title}</option>)}
                    </select>
                </div>
                <div className="flex items-end">
                    <button 
                        onClick={() => {setSelectedStudent(''); setSelectedTopic('');}}
                        className="w-full h-10 px-4 py-2 bg-gray-500 text-white rounded-md hover:bg-gray-600 transition-colors"
                    >
                        Reset Filters
                    </button>
                </div>
            </div>

            <div className="bg-gray-50 dark:bg-gray-900 rounded-lg shadow-inner overflow-x-auto">
                {filteredResults.length > 0 ? (
                    <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                        <thead className="bg-gray-100 dark:bg-gray-800">
                            <tr>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Student ID</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Topic</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Score</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Date</th>
                            </tr>
                        </thead>
                        <tbody className="bg-white dark:bg-gray-900 divide-y divide-gray-200 dark:divide-gray-700">
                            {filteredResults.map(result => (
                                <tr key={result.id}>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">{result.studentId}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300">{result.topicTitle}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm">
                                        <span className={`font-semibold ${result.score >= 70 ? 'text-green-600' : 'text-red-600'}`}>{result.score}%</span>
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300">{new Date(result.submittedAt).toLocaleDateString()}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                ) : (
                    <p className="text-gray-500 dark:text-gray-400 text-center py-8">No results for the selected filters.</p>
                )}
            </div>
        </div>
    );
};


const SyllabusManagementPage: React.FC = () => {
  const { user, isAuthenticated } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!isAuthenticated || user?.role !== Role.MASTER) {
      navigate('/dashboard');
    }
  }, [isAuthenticated, user, navigate]);

  if (!isAuthenticated || user?.role !== Role.MASTER) {
    return null;
  }

  return (
    <div className="flex-grow container mx-auto px-6 py-12">
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-8 max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Syllabus & User Hub</h1>
        <p className="mt-2 text-gray-600 dark:text-gray-300">
          Manage syllabus topics, track student analytics, and administer user accounts.
        </p>
        
        <SyllabusEditor />
        <StudentAnalytics />
        <UserManagementSection />

      </div>
    </div>
  );
};

export default SyllabusManagementPage;