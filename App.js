// frontend/src/App.js
import React, { useState, useRef, useCallback } from 'react';
import Webcam from 'react-webcam';
import {
  Camera,
  Upload,
  RefreshCw,
  Activity,
  TrendingUp,
  Calendar,
  Zap,
  Award,
  BarChart2,
  PieChart,
  Download,
  Share2
} from 'lucide-react';
import EmotionChart from './components/EmotionChart';
import EmotionHistory from './components/EmotionHistory';
import { analyzeEmotion, analyzeFile } from './services/api';
import './App.css';

function App() {
  const [activeTab, setActiveTab] = useState('camera');
  const [image, setImage] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [history, setHistory] = useState([]);
  const [cameraEnabled, setCameraEnabled] = useState(true);
  const [stats, setStats] = useState({
    totalAnalyses: 0,
    mostCommonEmotion: 'neutral',
    averageConfidence: 0,
    emotionsDetected: 0
  });

  const webcamRef = useRef(null);
  const fileInputRef = useRef(null);

  const captureImage = useCallback(() => {
    if (webcamRef.current) {
      const imageSrc = webcamRef.current.getScreenshot();
      setImage(imageSrc);
      analyzeImage(imageSrc);
    }
  }, [webcamRef]);

  const analyzeImage = async (imageData) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await analyzeEmotion(imageData);
      
      if (response.success) {
        setResult(response);
        
        // Add to history
        const newEntry = {
          id: Date.now(),
          timestamp: new Date().toISOString(),
          emotion: response.dominant_emotion,
          confidence: response.confidence,
          emoji: response.config.emoji,
          color: response.config.color
        };
        
        setHistory(prev => [newEntry, ...prev].slice(0, 10));
        
        // Update stats
        updateStats(response);
      } else {
        setError(response.error || 'Analysis failed');
      }
    } catch (err) {
      setError(err.message || 'Failed to analyze image');
    } finally {
      setLoading(false);
    }
  };

  const updateStats = (newResult) => {
    setStats(prev => {
      const newTotal = prev.totalAnalyses + 1;
      
      // Calculate most common emotion
      const emotionCounts = {};
      history.forEach(entry => {
        emotionCounts[entry.emotion] = (emotionCounts[entry.emotion] || 0) + 1;
      });
      emotionCounts[newResult.dominant_emotion] = (emotionCounts[newResult.dominant_emotion] || 0) + 1;
      
      let mostCommon = 'neutral';
      let maxCount = 0;
      Object.entries(emotionCounts).forEach(([emotion, count]) => {
        if (count > maxCount) {
          maxCount = count;
          mostCommon = emotion;
        }
      });
      
      // Calculate average confidence
      const totalConfidence = history.reduce((sum, entry) => sum + entry.confidence, 0) + newResult.confidence;
      const avgConfidence = totalConfidence / newTotal;
      
      return {
        totalAnalyses: newTotal,
        mostCommonEmotion: mostCommon,
        averageConfidence: Math.round(avgConfidence * 100) / 100,
        emotionsDetected: Object.keys(emotionCounts).length
      };
    });
  };

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const response = await analyzeFile(file);
      
      if (response.success) {
        setResult(response);
        
        // Convert file to data URL for display
        const reader = new FileReader();
        reader.onloadend = () => {
          setImage(reader.result);
        };
        reader.readAsDataURL(file);
      } else {
        setError(response.error || 'Analysis failed');
      }
    } catch (err) {
      setError(err.message || 'Failed to analyze file');
    } finally {
      setLoading(false);
    }
  };

  const resetAnalysis = () => {
    setImage(null);
    setResult(null);
    setError(null);
  };

  const downloadReport = () => {
    const report = {
      timestamp: new Date().toISOString(),
      result: result,
      stats: stats,
      history: history
    };
    
    const blob = new Blob([JSON.stringify(report, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `emotion-report-${Date.now()}.json`;
    a.click();
  };

  return (
    <div className="app">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="sidebar-header">
          <Activity size={32} className="logo-icon" />
          <h1 className="logo-text">Mood<span>Sense</span></h1>
        </div>
        
        <nav className="sidebar-nav">
          <button 
            className={`nav-item ${activeTab === 'camera' ? 'active' : ''}`}
            onClick={() => setActiveTab('camera')}
          >
            <Camera size={20} />
            <span>Live Camera</span>
          </button>
          
          <button 
            className={`nav-item ${activeTab === 'upload' ? 'active' : ''}`}
            onClick={() => setActiveTab('upload')}
          >
            <Upload size={20} />
            <span>Upload Image</span>
          </button>
          
          <button 
            className={`nav-item ${activeTab === 'history' ? 'active' : ''}`}
            onClick={() => setActiveTab('history')}
          >
            <Calendar size={20} />
            <span>History</span>
          </button>
          
          <button 
            className={`nav-item ${activeTab === 'stats' ? 'active' : ''}`}
            onClick={() => setActiveTab('stats')}
          >
            <BarChart2 size={20} />
            <span>Statistics</span>
          </button>
        </nav>
        
        <div className="sidebar-footer">
          <div className="user-profile">
            <div className="avatar">
              <Zap size={20} />
            </div>
            <div className="user-info">
              <span className="user-name">Premium User</span>
              <span className="user-plan">Pro Plan</span>
            </div>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="main-content">
        <header className="content-header">
          <h2>
            {activeTab === 'camera' && 'Live Emotion Detection'}
            {activeTab === 'upload' && 'Upload Image for Analysis'}
            {activeTab === 'history' && 'Analysis History'}
            {activeTab === 'stats' && 'Emotion Statistics'}
          </h2>
          
          <div className="header-actions">
            {result && (
              <>
                <button className="btn-secondary" onClick={downloadReport}>
                  <Download size={18} />
                  Export
                </button>
                <button className="btn-secondary">
                  <Share2 size={18} />
                  Share
                </button>
              </>
            )}
          </div>
        </header>

        <div className="content-body">
          {activeTab === 'camera' && (
            <div className="camera-container">
              {cameraEnabled && (
                <div className="webcam-wrapper">
                  <Webcam
                    ref={webcamRef}
                    screenshotFormat="image/jpeg"
                    videoConstraints={{
                      width: 640,
                      height: 480,
                      facingMode: "user"
                    }}
                    className="webcam"
                  />
                </div>
              )}
              
              <div className="camera-controls">
                <button 
                  className="btn-primary"
                  onClick={captureImage}
                  disabled={loading}
                >
                  <Camera size={20} />
                  Capture & Analyze
                </button>
                
                <button 
                  className="btn-secondary"
                  onClick={resetAnalysis}
                >
                  <RefreshCw size={20} />
                  Reset
                </button>
              </div>
            </div>
          )}

          {activeTab === 'upload' && (
            <div className="upload-container">
              <div 
                className="upload-area"
                onClick={() => fileInputRef.current.click()}
              >
                <input
                  type="file"
                  ref={fileInputRef}
                  onChange={handleFileUpload}
                  accept="image/*"
                  style={{ display: 'none' }}
                />
                <Upload size={48} className="upload-icon" />
                <h3>Click to upload an image</h3>
                <p>or drag and drop</p>
                <p className="upload-hint">Supported formats: JPG, PNG, GIF</p>
              </div>
            </div>
          )}

          {activeTab === 'history' && (
            <EmotionHistory history={history} />
          )}

          {activeTab === 'stats' && (
            <div className="stats-container">
              <div className="stats-grid">
                <div className="stat-card">
                  <div className="stat-icon">
                    <Activity size={24} />
                  </div>
                  <div className="stat-content">
                    <span className="stat-label">Total Analyses</span>
                    <span className="stat-value">{stats.totalAnalyses}</span>
                  </div>
                </div>
                
                <div className="stat-card">
                  <div className="stat-icon">
                    <TrendingUp size={24} />
                  </div>
                  <div className="stat-content">
                    <span className="stat-label">Most Common</span>
                    <span className="stat-value">
                      {stats.mostCommonEmotion} {EMOTION_CONFIG[stats.mostCommonEmotion]?.emoji}
                    </span>
                  </div>
                </div>
                
                <div className="stat-card">
                  <div className="stat-icon">
                    <Award size={24} />
                  </div>
                  <div className="stat-content">
                    <span className="stat-label">Avg. Confidence</span>
                    <span className="stat-value">{stats.averageConfidence}%</span>
                  </div>
                </div>
                
                <div className="stat-card">
                  <div className="stat-icon">
                    <PieChart size={24} />
                  </div>
                  <div className="stat-content">
                    <span className="stat-label">Emotions Detected</span>
                    <span className="stat-value">{stats.emotionsDetected}</span>
                  </div>
                </div>
              </div>
              
              {history.length > 0 && (
                <div className="chart-container">
                  <h3>Emotion Distribution</h3>
                  <EmotionChart history={history} />
                </div>
              )}
            </div>
          )}

          {/* Analysis Result */}
          {image && (
            <div className="analysis-result">
              <div className="result-header">
                <h3>Analysis Result</h3>
                {loading && (
                  <div className="loading-spinner">
                    <RefreshCw size={20} className="spinning" />
                    Analyzing...
                  </div>
                )}
              </div>
              
              {error && (
                <div className="error-message">
                  {error}
                </div>
              )}
              
              {result && !loading && (
                <div className="result-content">
                  <div className="image-preview">
                    <img src={image} alt="Captured" />
                  </div>
                  
                  <div className="emotion-details">
                    <div 
                      className="dominant-emotion"
                      style={{ backgroundColor: result.config.color + '20' }}
                    >
                      <div className="emotion-emoji">{result.config.emoji}</div>
                      <div className="emotion-info">
                        <h4>{result.dominant_emotion.charAt(0).toUpperCase() + result.dominant_emotion.slice(1)}</h4>
                        <p>{result.config.description}</p>
                        <div className="confidence-bar">
                          <div 
                            className="confidence-fill"
                            style={{ 
                              width: `${result.confidence}%`,
                              backgroundColor: result.config.color
                            }}
                          />
                        </div>
                        <span className="confidence-text">{result.confidence}% confidence</span>
                      </div>
                    </div>
                    
                    <div className="emotion-breakdown">
                      <h5>Emotion Breakdown</h5>
                      {Object.entries(result.emotions).map(([emotion, value]) => (
                        <div key={emotion} className="emotion-row">
                          <span className="emotion-label">
                            {emotion.charAt(0).toUpperCase() + emotion.slice(1)}
                          </span>
                          <div className="emotion-bar-container">
                            <div 
                              className="emotion-bar"
                              style={{ 
                                width: `${value}%`,
                                backgroundColor: EMOTION_CONFIG[emotion]?.color || '#9E9E9E'
                              }}
                            />
                          </div>
                          <span className="emotion-value">{value}%</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

const EMOTION_CONFIG = {
  'angry': { emoji: '😠', color: '#FF4444', description: 'Frustrated or annoyed' },
  'disgust': { emoji: '🤢', color: '#00C851', description: 'Repulsed or offended' },
  'fear': { emoji: '😨', color: '#AA66CC', description: 'Anxious or scared' },
  'happy': { emoji: '😊', color: '#FFBB33', description: 'Joyful or pleased' },
  'sad': { emoji: '😢', color: '#33B5E5', description: 'Down or melancholy' },
  'surprise': { emoji: '😲', color: '#2BBBAD', description: 'Shocked or amazed' },
  'neutral': { emoji: '😐', color: '#9E9E9E', description: 'Calm and composed' }
};

export default App;
