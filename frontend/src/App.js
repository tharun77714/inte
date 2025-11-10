import React, { useState, useEffect, useRef } from 'react';
import './App.css';
import InterviewSession from './components/InterviewSession';
import DomainSelection from './components/DomainSelection';
import ReportView from './components/ReportView';

function App() {
  const [currentView, setCurrentView] = useState('domain-selection');
  const [selectedDomain, setSelectedDomain] = useState(null);
  const [sessionData, setSessionData] = useState(null);
  const [report, setReport] = useState(null);

  const handleDomainSelect = (domain) => {
    setSelectedDomain(domain);
    setCurrentView('interview');
  };

  const handleSessionComplete = (data) => {
    setSessionData(data);
    setCurrentView('report');
  };

  const handleBackToStart = () => {
    setCurrentView('domain-selection');
    setSelectedDomain(null);
    setSessionData(null);
    setReport(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        <header className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
            AI Interview Coach
          </h1>
          <p className="text-gray-600">
            Practice interviews with AI-powered feedback
          </p>
        </header>

        {currentView === 'domain-selection' && (
          <DomainSelection onSelect={handleDomainSelect} />
        )}

        {currentView === 'interview' && (
          <InterviewSession
            domain={selectedDomain}
            onComplete={handleSessionComplete}
            onBack={handleBackToStart}
          />
        )}

        {currentView === 'report' && (
          <ReportView
            sessionData={sessionData}
            report={report}
            onBack={handleBackToStart}
            onReportGenerated={setReport}
          />
        )}
      </div>
    </div>
  );
}

export default App;

