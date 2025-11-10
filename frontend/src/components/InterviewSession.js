import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import AudioRecorder from './AudioRecorder';

const API_BASE = 'http://localhost:8000/api';

function InterviewSession({ domain, onComplete, onBack }) {
  const [sessionId, setSessionId] = useState(null);
  const [currentQuestion, setCurrentQuestion] = useState('');
  const [transcript, setTranscript] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [feedback, setFeedback] = useState(null);
  const [loading, setLoading] = useState(false);
  const [questionsAsked, setQuestionsAsked] = useState(0);
  const [answers, setAnswers] = useState([]);
  const [feedbackHistory, setFeedbackHistory] = useState([]);
  const [sessionStarted, setSessionStarted] = useState(false);

  useEffect(() => {
    if (domain && !sessionStarted) {
      startSession();
    }
  }, [domain]);

  const startSession = async () => {
    try {
      setLoading(true);
      const response = await axios.post(`${API_BASE}/interview/start`, null, {
        params: {
          domain: domain.id,
          experience_level: domain.experience_level || 'fresher'
        }
      });
      
      setSessionId(response.data.session_id);
      setCurrentQuestion(response.data.question);
      setSessionStarted(true);
    } catch (error) {
      console.error('Error starting session:', error);
      alert('Failed to start interview session');
    } finally {
      setLoading(false);
    }
  };

  const handleAudioRecorded = async (audioBlob) => {
    try {
      setLoading(true);
      
      // Create form data
      const formData = new FormData();
      formData.append('audio_file', audioBlob, 'recording.webm');

      // Transcribe audio
      const transcribeResponse = await axios.post(
        `${API_BASE}/interview/transcribe`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      );

      const newTranscript = transcribeResponse.data.transcript;
      setTranscript(newTranscript);
      setAnswers([...answers, newTranscript]);

      // Evaluate response
      const evalResponse = await axios.post(`${API_BASE}/interview/evaluate`, {
        question: currentQuestion,
        transcript: newTranscript,
        domain: domain.id,
        session_id: sessionId,
      });

      const newFeedback = evalResponse.data;
      setFeedback(newFeedback);
      setFeedbackHistory([...feedbackHistory, newFeedback]);
      setQuestionsAsked(questionsAsked + 1);

    } catch (error) {
      console.error('Error processing audio:', error);
      alert('Failed to process your response');
    } finally {
      setLoading(false);
    }
  };

  const handleNextQuestion = async () => {
    try {
      setLoading(true);
      setTranscript('');
      setFeedback(null);

      const response = await axios.post(
        `${API_BASE}/interview/next-question`,
        {
          domain: domain.id,
          experience_level: domain.experience_level || 'fresher',
          previous_answers: answers,
        }
      );

      setCurrentQuestion(response.data.question);
    } catch (error) {
      console.error('Error getting next question:', error);
      alert('Failed to get next question');
    } finally {
      setLoading(false);
    }
  };

  const handleEndSession = () => {
    const sessionData = {
      session_id: sessionId,
      domain: domain.id,
      questions: Array(questionsAsked).fill(null).map((_, i) => `Question ${i + 1}`),
      answers: answers,
      feedback_history: feedbackHistory,
    };
    onComplete(sessionData);
  };

  if (!sessionStarted || loading && !currentQuestion) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="text-gray-600">Starting interview session...</div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-lg shadow-lg p-8">
        {/* Header */}
        <div className="flex justify-between items-center mb-6">
          <div>
            <h2 className="text-2xl font-semibold text-gray-800">
              {domain.name} Interview
            </h2>
            <p className="text-sm text-gray-600">
              Question {questionsAsked + 1} • {domain.experience_level}
            </p>
          </div>
          <button
            onClick={onBack}
            className="px-4 py-2 text-gray-600 hover:text-gray-800"
          >
            ← Back
          </button>
        </div>

        {/* Current Question */}
        <div className="mb-6 p-6 bg-blue-50 rounded-lg border-l-4 border-blue-500">
          <h3 className="text-lg font-medium text-gray-800 mb-2">
            Question:
          </h3>
          <p className="text-gray-700">{currentQuestion}</p>
        </div>

        {/* Audio Recorder */}
        <div className="mb-6">
          <AudioRecorder
            onRecorded={handleAudioRecorded}
            isRecording={isRecording}
            onRecordingChange={setIsRecording}
          />
        </div>

        {/* Transcript */}
        {transcript && (
          <div className="mb-6 p-4 bg-gray-50 rounded-lg">
            <h4 className="text-sm font-medium text-gray-700 mb-2">
              Your Answer:
            </h4>
            <p className="text-gray-800">{transcript}</p>
          </div>
        )}

        {/* Feedback */}
        {feedback && (
          <div className="mb-6 p-6 bg-green-50 rounded-lg border-l-4 border-green-500">
            <h4 className="text-lg font-medium text-gray-800 mb-4">
              Feedback
            </h4>
            
            <div className="grid grid-cols-2 gap-4 mb-4">
              <div>
                <p className="text-sm text-gray-600">Communication Score</p>
                <p className="text-2xl font-bold text-blue-600">
                  {(feedback.communication.score * 100).toFixed(0)}%
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Technical Score</p>
                <p className="text-2xl font-bold text-purple-600">
                  {(feedback.technical.score * 100).toFixed(0)}%
                </p>
              </div>
            </div>

            {feedback.communication.filler_words_count > 0 && (
              <div className="mb-3">
                <p className="text-sm text-gray-700">
                  Filler words detected: {feedback.communication.filler_words_count}
                </p>
                <p className="text-xs text-gray-600">
                  {feedback.communication.filler_words.join(', ')}
                </p>
              </div>
            )}

            <div className="mt-4">
              <p className="text-sm font-medium text-gray-700 mb-2">
                Suggestions:
              </p>
              <ul className="list-disc list-inside text-sm text-gray-600 space-y-1">
                {feedback.communication.suggestions.map((s, i) => (
                  <li key={i}>{s}</li>
                ))}
                {feedback.technical.suggestions.map((s, i) => (
                  <li key={i}>{s}</li>
                ))}
              </ul>
            </div>
          </div>
        )}

        {/* Actions */}
        <div className="flex gap-4">
          {feedback && questionsAsked < 4 && (
            <button
              onClick={handleNextQuestion}
              className="flex-1 px-6 py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors"
            >
              Next Question
            </button>
          )}
          
          {questionsAsked >= 4 && (
            <button
              onClick={handleEndSession}
              className="flex-1 px-6 py-3 bg-green-600 text-white rounded-lg font-medium hover:bg-green-700 transition-colors"
            >
              End Session & View Report
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

export default InterviewSession;

