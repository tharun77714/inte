import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_BASE = 'http://localhost:8000/api';

function DomainSelection({ onSelect }) {
  const [domains, setDomains] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedLevel, setSelectedLevel] = useState('fresher');

  useEffect(() => {
    fetchDomains();
  }, []);

  const fetchDomains = async () => {
    try {
      const response = await axios.get(`${API_BASE}/domains`);
      setDomains(response.data.domains);
    } catch (error) {
      console.error('Error fetching domains:', error);
      // Fallback domains
      setDomains([
        { id: 'software', name: 'Software Engineering', description: 'Coding, algorithms, system design' },
        { id: 'data_science', name: 'Data Science', description: 'ML, statistics, data analysis' },
        { id: 'electronics', name: 'Electronics', description: 'Circuit design, embedded systems' },
        { id: 'general', name: 'General', description: 'Behavioral and general questions' },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleSelect = (domain) => {
    onSelect({ ...domain, experience_level: selectedLevel });
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="text-gray-600">Loading domains...</div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-lg shadow-lg p-8">
        <h2 className="text-2xl font-semibold text-gray-800 mb-6">
          Select Your Interview Domain
        </h2>

        {/* Experience Level Selection */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Experience Level
          </label>
          <div className="flex gap-4">
            {['fresher', 'intermediate', 'senior'].map((level) => (
              <button
                key={level}
                onClick={() => setSelectedLevel(level)}
                className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                  selectedLevel === level
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                {level.charAt(0).toUpperCase() + level.slice(1)}
              </button>
            ))}
          </div>
        </div>

        {/* Domain Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {domains.map((domain) => (
            <button
              key={domain.id}
              onClick={() => handleSelect(domain)}
              className="text-left p-6 bg-gradient-to-br from-blue-50 to-indigo-50 rounded-lg border-2 border-transparent hover:border-blue-400 transition-all hover:shadow-lg"
            >
              <h3 className="text-xl font-semibold text-gray-800 mb-2">
                {domain.name}
              </h3>
              <p className="text-gray-600 text-sm">{domain.description}</p>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}

export default DomainSelection;

