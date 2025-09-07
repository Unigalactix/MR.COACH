import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useSyllabus } from '../../hooks/useSyllabus';
import { useAuth } from '../../hooks/useAuth';
import { Question } from '../../types';

const TestPage: React.FC = () => {
  const { topicId } = useParams<{ topicId: string }>();
  const navigate = useNavigate();
  const { getTestForTopic, submitTest, topics } = useSyllabus();
  const { user, isAuthenticated } = useAuth();
  
  const [test, setTest] = useState<Question[] | null>(null);
  const [answers, setAnswers] = useState<number[]>([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [error, setError] = useState('');

  const topic = topics.find(t => t.id === topicId);

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }
    if (topicId) {
      const foundTest = getTestForTopic(topicId);
      if (foundTest) {
        setTest(foundTest);
        setAnswers(new Array(foundTest.length).fill(-1));
      } else {
        setError('Test not found.');
      }
    }
  }, [topicId, getTestForTopic, isAuthenticated, navigate]);

  const handleAnswerSelect = (optionIndex: number) => {
    const newAnswers = [...answers];
    newAnswers[currentQuestionIndex] = optionIndex;
    setAnswers(newAnswers);
  };

  const handleNext = () => {
    if (test && currentQuestionIndex < test.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
    }
  };

  const handleBack = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(currentQuestionIndex - 1);
    }
  };
  
  const handleSubmit = () => {
    if (answers.includes(-1)) {
        if (!window.confirm("You have unanswered questions. Are you sure you want to submit?")) {
            return;
        }
    }
    if (user && topicId) {
        const finalAnswers = answers.map(a => a === -1 ? -1 : a); // Ensure -1 for unanswered
        const result = submitTest(user.uniqueId, topicId, finalAnswers);
        navigate(`/results/${result.id}`);
    } else {
        setError("Could not submit test. User not found.");
    }
  };

  if (error) {
    return <div className="text-red-500 text-center p-8">{error}</div>;
  }
  if (!test || !topic) {
    return <div className="text-center p-8">Loading test...</div>;
  }

  const currentQuestion = test[currentQuestionIndex];
  const isLastQuestion = currentQuestionIndex === test.length - 1;

  return (
    <div className="flex-grow container mx-auto px-6 py-12">
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-8 max-w-2xl mx-auto">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">{topic.title}</h1>
        <p className="text-gray-500 dark:text-gray-400 mb-6">Question {currentQuestionIndex + 1} of {test.length}</p>

        <div className="border-t border-gray-200 dark:border-gray-700 pt-6">
            <h2 className="text-xl font-semibold mb-4">{currentQuestion.questionText}</h2>
            <div className="space-y-3">
                {currentQuestion.options.map((option, index) => (
                    <label key={index} className={`flex items-center p-3 rounded-lg border-2 cursor-pointer transition-colors ${answers[currentQuestionIndex] === index ? 'bg-indigo-100 dark:bg-indigo-900 border-indigo-500' : 'bg-gray-50 dark:bg-gray-700 border-gray-200 dark:border-gray-600'}`}>
                        <input
                            type="radio"
                            name={`question-${currentQuestion.id}`}
                            checked={answers[currentQuestionIndex] === index}
                            onChange={() => handleAnswerSelect(index)}
                            className="h-4 w-4 text-indigo-600 border-gray-300 focus:ring-indigo-500"
                        />
                        <span className="ml-3 text-gray-800 dark:text-gray-200">{option}</span>
                    </label>
                ))}
            </div>
        </div>
        
        <div className="mt-8 flex justify-between items-center">
            <button
                onClick={handleBack}
                disabled={currentQuestionIndex === 0}
                className="px-6 py-2 bg-gray-200 dark:bg-gray-600 text-gray-800 dark:text-white rounded-lg hover:bg-gray-300 dark:hover:bg-gray-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
                Back
            </button>
            
            {isLastQuestion ? (
                 <button
                    onClick={handleSubmit}
                    className="px-6 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors"
                >
                    Submit
                </button>
            ) : (
                <button
                    onClick={handleNext}
                    className="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
                >
                    Next
                </button>
            )}
        </div>
      </div>
    </div>
  );
};

export default TestPage;
