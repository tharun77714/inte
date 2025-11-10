import React, { useState, useRef, useEffect } from 'react';

function AudioRecorder({ onRecorded, isRecording, onRecordingChange }) {
  const [recording, setRecording] = useState(false);
  const [audioBlob, setAudioBlob] = useState(null);
  const [recordingTime, setRecordingTime] = useState(0);
  const mediaRecorderRef = useRef(null);
  const chunksRef = useRef([]);
  const timerRef = useRef(null);

  useEffect(() => {
    if (recording) {
      timerRef.current = setInterval(() => {
        setRecordingTime((prev) => prev + 1);
      }, 1000);
    } else {
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
    }

    return () => {
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
    };
  }, [recording]);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      chunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          chunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = () => {
        const blob = new Blob(chunksRef.current, { type: 'audio/webm' });
        setAudioBlob(blob);
        onRecorded(blob);
        stream.getTracks().forEach((track) => track.stop());
      };

      mediaRecorder.start();
      setRecording(true);
      setRecordingTime(0);
      onRecordingChange(true);
    } catch (error) {
      console.error('Error accessing microphone:', error);
      alert('Please allow microphone access to record your answer');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && recording) {
      mediaRecorderRef.current.stop();
      setRecording(false);
      onRecordingChange(false);
    }
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="flex flex-col items-center gap-4">
      <div className="flex items-center gap-4">
        {!recording ? (
          <button
            onClick={startRecording}
            className="px-6 py-3 bg-red-600 text-white rounded-full font-medium hover:bg-red-700 transition-colors flex items-center gap-2"
          >
            <span className="w-3 h-3 bg-white rounded-full"></span>
            Start Recording
          </button>
        ) : (
          <button
            onClick={stopRecording}
            className="px-6 py-3 bg-gray-600 text-white rounded-full font-medium hover:bg-gray-700 transition-colors flex items-center gap-2"
          >
            <span className="w-3 h-3 bg-white rounded-full animate-pulse"></span>
            Stop Recording
          </button>
        )}
      </div>

      {recording && (
        <div className="text-center">
          <p className="text-sm text-gray-600">Recording...</p>
          <p className="text-lg font-mono text-gray-800">{formatTime(recordingTime)}</p>
        </div>
      )}

      {audioBlob && !recording && (
        <p className="text-sm text-green-600">✓ Audio recorded successfully</p>
      )}
    </div>
  );
}

export default AudioRecorder;

