// frontend/src/components/EmotionChart.js
import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell
} from 'recharts';

const EmotionChart = ({ history }) => {
  // Calculate emotion frequencies
  const emotionCounts = {};
  history.forEach(entry => {
    emotionCounts[entry.emotion] = (emotionCounts[entry.emotion] || 0) + 1;
  });
  
  const data = Object.entries(emotionCounts).map(([emotion, count]) => ({
    emotion: emotion.charAt(0).toUpperCase() + emotion.slice(1),
    count,
    color: getEmotionColor(emotion)
  }));
  
  const getEmotionColor = (emotion) => {
    const colors = {
      angry: '#FF4444',
      disgust: '#00C851',
      fear: '#AA66CC',
      happy: '#FFBB33',
      sad: '#33B5E5',
      surprise: '#2BBBAD',
      neutral: '#9E9E9E'
    };
    return colors[emotion] || '#9E9E9E';
  };
  
  if (data.length === 0) {
    return (
      <div className="empty-chart">
        <p>No data available yet</p>
      </div>
    );
  }
  
  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#444" />
        <XAxis dataKey="emotion" stroke="#888" />
        <YAxis stroke="#888" />
        <Tooltip 
          contentStyle={{ 
            backgroundColor: '#1e1e1e', 
            border: '1px solid #333',
            borderRadius: '8px'
          }}
          labelStyle={{ color: '#fff' }}
        />
        <Bar dataKey="count" radius={[4, 4, 0, 0]}>
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={entry.color} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
};

export default EmotionChart;
