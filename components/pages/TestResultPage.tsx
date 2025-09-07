import React, { useEffect, useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { useSyllabus } from '../../hooks/useSyllabus';
import { useAuth } from '../../hooks/useAuth';
import { TestResult } from '../../types';

const TestResultPage: React.FC = () => {
  const { resultId } = useParams<{ resultId: string }>();
  const navigate = useNavigate();
  const { getResultById } = useSyllabus();
  const { isAuthenticated } = useAuth();

  const [result, setResult] = useState<TestResult | null>(null);

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }
    if (resultId) {
      const foundResult = getResultById(resultId);
      if (foundResult) {
        setResult(foundResult);
      } else {
        // If not found, maybe redirect to dashboard
        navigate('/dashboard');
      }
    }
  }, [resultId, getResultById, isAuthenticated, navigate]);

  if (!result) {
    return <div className="text-center p-8">Loading results...</div>;
  }

  const isSuccess = result.score >= 70;
  const scoreColor = isSuccess ? 'text-green-500' : 'text-red-500';
  const message = isSuccess ? 'Great job! Keep up the excellent work.' : 'Don\'t worry, review the material and try again!';

  return (
    <div className="flex-grow container mx-auto px-6 py-12">
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-8 max-w-2xl mx-auto text-center">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Test Results</h1>
        <p className="mt-2 text-lg text-gray-600 dark:text-gray-300">Topic: <span className="font-semibold">{result.topicTitle}</span></p>

        <div className="my-8">
          <p className="text-lg text-gray-500 dark:text-gray-400">Your Score</p>
          <p className={`text-7xl font-bold my-2 ${scoreColor}`}>{result.score}%</p>
        </div>
        
        <p className="text-gray-600 dark:text-gray-300">{message}</p>

        <div className="mt-8">
          <Link
            to="/dashboard"
            className="inline-block px-8 py-3 bg-indigo-600 text-white font-semibold rounded-lg shadow-lg hover:bg-indigo-700 transition-transform transform hover:scale-105 duration-300"
          >
            Back to Dashboard
          </Link>
        </div>
      </div>
    </div>
  );
};

export default TestResultPage;
