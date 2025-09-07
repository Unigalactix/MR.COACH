import React, { createContext, useState, ReactNode, useCallback } from 'react';
import { SyllabusTopic, Question, TestResult } from '../types';

interface SyllabusContextType {
  topics: SyllabusTopic[];
  getTestForTopic: (topicId: string) => Question[] | undefined;
  getResultsForStudent: (studentId: string) => TestResult[];
  getAllResults: () => TestResult[];
  getResultById: (resultId: string) => TestResult | undefined;
  submitTest: (studentId: string, topicId: string, answers: number[]) => TestResult;
  addTopic: (title: string) => void;
}

export const SyllabusContext = createContext<SyllabusContextType | null>(null);

interface SyllabusProviderProps {
  children: ReactNode;
}

// Mock Data
const MOCK_TOPICS: SyllabusTopic[] = [
    { id: 'topic-1', title: 'Reading Comprehension' },
    { id: 'topic-2', title: 'Listening Skills' },
    { id: 'topic-3', title: 'Writing and Grammar' },
];

const MOCK_TESTS: Record<string, Question[]> = {
    'topic-1': [
        { id: 'q1-1', questionText: 'What is the main idea of a passage?', options: ['The primary point the author is making', 'A minor detail', 'The author\'s name', 'The publisher'], correctAnswerIndex: 0 },
        { id: 'q1-2', questionText: 'An inference is:', options: ['Something stated directly', 'A conclusion based on evidence', 'A summary of the plot', 'A character\'s name'], correctAnswerIndex: 1 },
    ],
    'topic-2': [
        { id: 'q2-1', questionText: 'Active listening involves:', options: ['Hearing the words', 'Waiting for your turn to speak', 'Focusing fully on the speaker', 'Ignoring non-verbal cues'], correctAnswerIndex: 2 },
    ],
    'topic-3': [
        { id: 'q3-1', questionText: 'Which of the following is a complete sentence?', options: ['Running in the park.', 'She runs.', 'Because it was raining.', 'And then went home.'], correctAnswerIndex: 1 },
        { id: 'q3-2', questionText: 'What does a noun refer to?', options: ['An action', 'A person, place, or thing', 'A descriptive word', 'A connecting word'], correctAnswerIndex: 1 },
    ]
};

const MOCK_RESULTS: TestResult[] = [];


export const SyllabusProvider: React.FC<SyllabusProviderProps> = ({ children }) => {
    const [topics, setTopics] = useState<SyllabusTopic[]>(MOCK_TOPICS);
    const [tests] = useState<Record<string, Question[]>>(MOCK_TESTS);
    const [results, setResults] = useState<TestResult[]>(MOCK_RESULTS);

    const addTopic = useCallback((title: string) => {
        const newTopic: SyllabusTopic = {
            id: `topic-${Date.now()}`,
            title,
        };
        setTopics(prev => [...prev, newTopic]);
    }, []);
    
    const getTestForTopic = useCallback((topicId: string) => {
        return tests[topicId];
    }, [tests]);

    const submitTest = useCallback((studentId: string, topicId: string, answers: number[]): TestResult => {
        const test = tests[topicId];
        const topic = topics.find(t => t.id === topicId);
        if (!test || !topic) {
            throw new Error('Test or Topic not found');
        }

        let correctAnswers = 0;
        test.forEach((question, index) => {
            if (question.correctAnswerIndex === answers[index]) {
                correctAnswers++;
            }
        });

        const score = Math.round((correctAnswers / test.length) * 100);

        const newResult: TestResult = {
            id: `result-${Date.now()}`,
            studentId,
            topicId,
            topicTitle: topic.title,
            score,
            submittedAt: new Date(),
        };

        setResults(prev => [...prev, newResult]);
        return newResult;
    }, [tests, topics]);

    const getResultsForStudent = useCallback((studentId: string) => {
        return results.filter(r => r.studentId === studentId).sort((a,b) => b.submittedAt.getTime() - a.submittedAt.getTime());
    }, [results]);

    const getAllResults = useCallback(() => {
        return [...results].sort((a,b) => b.submittedAt.getTime() - a.submittedAt.getTime());
    }, [results]);

    const getResultById = useCallback((resultId: string) => {
        return results.find(r => r.id === resultId);
    }, [results]);

    return (
        <SyllabusContext.Provider value={{ topics, getTestForTopic, getResultsForStudent, getAllResults, getResultById, submitTest, addTopic }}>
            {children}
        </SyllabusContext.Provider>
    );
};
