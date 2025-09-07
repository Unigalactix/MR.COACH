import React from 'react';
import { HashRouter, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { SyllabusProvider } from './context/SyllabusContext';
import Header from './components/Header';
import Footer from './components/Footer';
import LandingPage from './components/pages/LandingPage';
import LoginPage from './components/pages/LoginPage';
import DashboardPage from './components/pages/DashboardPage';
import SyllabusManagementPage from './components/pages/SyllabusManagementPage';
import RegisterPage from './components/pages/RegisterPage';
import TestPage from './components/pages/TestPage';
import TestResultPage from './components/pages/TestResultPage';

const App: React.FC = () => {
  return (
    <AuthProvider>
      <SyllabusProvider>
        <HashRouter>
          <div className="min-h-screen flex flex-col bg-gray-50 dark:bg-gray-900 text-gray-800 dark:text-gray-200">
            <Header />
            <main className="flex-grow flex flex-col">
              <Routes>
                <Route path="/" element={<LandingPage />} />
                <Route path="/login" element={<LoginPage />} />
                <Route path="/register" element={<RegisterPage />} />
                <Route path="/dashboard" element={<DashboardPage />} />
                <Route path="/syllabus-management" element={<SyllabusManagementPage />} />
                <Route path="/test/:topicId" element={<TestPage />} />
                <Route path="/results/:resultId" element={<TestResultPage />} />
              </Routes>
            </main>
            <Footer />
          </div>
        </HashRouter>
      </SyllabusProvider>
    </AuthProvider>
  );
};

export default App;
