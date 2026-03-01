// frontend/src/components/EmotionHistory.js
import React from 'react';
import { Clock, ChevronRight } from 'lucide-react';

const EmotionHistory = ({ history }) => {
  if (history.length === 0) {
    return (
      <div className="empty-history">
        <Clock size={48} className="empty-icon" />
        <h3>No History Yet</h3>
        <p>Start analyzing emotions to build your history</p>
      </div>
    );
  }
  
  const formatDate = (timestamp) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diff = now - date;
    
    if (diff < 60000) return 'Just now';
    if (diff < 3600000) return `${Math.floor(diff / 60000)} minutes ago`;
    if (diff < 86400000) return `${Math.floor(diff / 3600000)} hours ago`;
    return date.toLocaleDateString();
  };
  
  return (
    <div className="history-list">
      {history.map((entry) => (
        <div key={entry.id} className="history-item">
          <div 
            className="history-emotion-indicator"
            style={{ backgroundColor: entry.color }}
          >
            <span className="history-emoji">{entry.emoji}</span>
          </div>
          
          <div className="history-info">
            <h4>{entry.emotion.charAt(0).toUpperCase() + entry.emotion.slice(1)}</h4>
            <span className="history-time">{formatDate(entry.timestamp)}</span>
          </div>
          
          <div className="history-confidence">
            <div className="confidence-indicator">
              <div 
                className="confidence-fill"
                style={{ 
                  width: `${entry.confidence}%`,
                  backgroundColor: entry.color
                }}
              />
            </div>
            <span className="confidence-value">{entry.confidence}%</span>
          </div>
          
          <ChevronRight size={20} className="history-arrow" />
        </div>
      ))}
    </div>
  );
};

export default EmotionHistory;
