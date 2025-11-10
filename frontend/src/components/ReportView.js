import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_BASE = 'http://localhost:8000/api';

function ReportView({ sessionData, report, onBack, onReportGenerated }) {
  const [loading, setLoading] = useState(false);
  const [reportData, setReportData] = useState(report);

  useEffect(() => {
    if (sessionData && !reportData) {
      generateReport();
    }
  }, [sessionData]);

  const generateReport = async () => {
    try {
      setLoading(true);
      const response = await axios.post(`${API_BASE}/report/generate`, {
        session_id: sessionData.session_id,
        session_data: sessionData,
        domain: sessionData.domain,
      });
      setReportData(response.data);
      onReportGenerated(response.data);
    } catch (error) {
      console.error('Error generating report:', error);
      alert('Failed to generate report');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="text-gray-600">Generating your personalized report...</div>
      </div>
    );
  }

  if (!reportData) {
    return null;
  }

  const summary = reportData.summary || {};
  const stats = reportData.statistics || {};
  const strengths = reportData.strengths || [];
  const weaknesses = reportData.weaknesses || [];
  const improvementPlan = reportData.improvement_plan || [];
  const recommendations = reportData.recommendations || [];

  return (
    <div className="max-w-5xl mx-auto">
      <div className="bg-white rounded-lg shadow-lg p-8">
        {/* Header */}
        <div className="flex justify-between items-center mb-6">
          <div>
            <h2 className="text-3xl font-bold text-gray-800">
              Your Interview Report
            </h2>
            <p className="text-sm text-gray-600 mt-1">
              {new Date(reportData.date).toLocaleDateString()}
            </p>
          </div>
          <button
            onClick={onBack}
            className="px-4 py-2 text-gray-600 hover:text-gray-800"
          >
            ← Back to Start
          </button>
        </div>

        {/* Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          <div className="bg-blue-50 p-6 rounded-lg border-l-4 border-blue-500">
            <p className="text-sm text-gray-600 mb-1">Overall Score</p>
            <p className="text-3xl font-bold text-blue-600">
              {(summary.overall_score * 100 || 0).toFixed(0)}%
            </p>
          </div>
          <div className="bg-green-50 p-6 rounded-lg border-l-4 border-green-500">
            <p className="text-sm text-gray-600 mb-1">Communication</p>
            <p className="text-3xl font-bold text-green-600">
              {(summary.communication_score * 100 || 0).toFixed(0)}%
            </p>
          </div>
          <div className="bg-purple-50 p-6 rounded-lg border-l-4 border-purple-500">
            <p className="text-sm text-gray-600 mb-1">Technical</p>
            <p className="text-3xl font-bold text-purple-600">
              {(summary.technical_score * 100 || 0).toFixed(0)}%
            </p>
          </div>
        </div>

        {/* Strengths */}
        <div className="mb-6 p-6 bg-green-50 rounded-lg">
          <h3 className="text-xl font-semibold text-gray-800 mb-4">
            ✓ Your Strengths
          </h3>
          <ul className="list-disc list-inside space-y-2 text-gray-700">
            {strengths.map((strength, i) => (
              <li key={i}>{strength}</li>
            ))}
          </ul>
        </div>

        {/* Weaknesses */}
        <div className="mb-6 p-6 bg-yellow-50 rounded-lg">
          <h3 className="text-xl font-semibold text-gray-800 mb-4">
            📈 Areas for Improvement
          </h3>
          <ul className="list-disc list-inside space-y-2 text-gray-700">
            {weaknesses.map((weakness, i) => (
              <li key={i}>{weakness}</li>
            ))}
          </ul>
        </div>

        {/* Improvement Plan */}
        {improvementPlan.length > 0 && (
          <div className="mb-6 p-6 bg-blue-50 rounded-lg">
            <h3 className="text-xl font-semibold text-gray-800 mb-4">
              🎯 Improvement Plan
            </h3>
            <div className="space-y-4">
              {improvementPlan.map((plan, i) => (
                <div key={i} className="bg-white p-4 rounded-lg">
                  <div className="flex items-center gap-2 mb-2">
                    <h4 className="font-semibold text-gray-800">{plan.area}</h4>
                    <span className={`px-2 py-1 text-xs rounded ${
                      plan.priority === 'High' ? 'bg-red-100 text-red-800' :
                      plan.priority === 'Medium' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-green-100 text-green-800'
                    }`}>
                      {plan.priority} Priority
                    </span>
                  </div>
                  <div className="mt-2">
                    <p className="text-sm font-medium text-gray-700 mb-1">Actions:</p>
                    <ul className="list-disc list-inside text-sm text-gray-600 space-y-1">
                      {plan.actions.map((action, j) => (
                        <li key={j}>{action}</li>
                      ))}
                    </ul>
                  </div>
                  {plan.resources && plan.resources.length > 0 && (
                    <div className="mt-2">
                      <p className="text-sm font-medium text-gray-700 mb-1">Resources:</p>
                      <ul className="list-disc list-inside text-sm text-gray-600 space-y-1">
                        {plan.resources.map((resource, j) => (
                          <li key={j}>{resource}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Recommendations */}
        <div className="mb-6 p-6 bg-indigo-50 rounded-lg">
          <h3 className="text-xl font-semibold text-gray-800 mb-4">
            💡 Recommendations
          </h3>
          <ul className="list-disc list-inside space-y-2 text-gray-700">
            {recommendations.map((rec, i) => (
              <li key={i}>{rec}</li>
            ))}
          </ul>
        </div>

        {/* Statistics */}
        <div className="p-6 bg-gray-50 rounded-lg">
          <h3 className="text-xl font-semibold text-gray-800 mb-4">
            📊 Session Statistics
          </h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
            <div>
              <p className="text-2xl font-bold text-gray-800">{summary.total_questions || 0}</p>
              <p className="text-sm text-gray-600">Questions</p>
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-800">{stats.total_filler_words || 0}</p>
              <p className="text-sm text-gray-600">Filler Words</p>
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-800">
                {(stats.avg_clarity * 100 || 0).toFixed(0)}%
              </p>
              <p className="text-sm text-gray-600">Avg Clarity</p>
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-800">{stats.sessions_completed || 0}</p>
              <p className="text-sm text-gray-600">Sessions</p>
            </div>
          </div>
        </div>

        {/* Action Button */}
        <div className="mt-8 text-center">
          <button
            onClick={onBack}
            className="px-8 py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors"
          >
            Start New Interview
          </button>
        </div>
      </div>
    </div>
  );
}

export default ReportView;

