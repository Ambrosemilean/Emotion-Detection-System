"""
Flask server for emotion detection API
File: server.py
"""

from flask import Flask, request, jsonify, render_template_string
from emotion_detection import EmotionDetector, emotion_predictor
import json

app = Flask(__name__)
detector = EmotionDetector()

# HTML template for the web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Emotion Detection System</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            text-align: center;
        }
        textarea {
            width: 100%;
            height: 100px;
            padding: 10px;
            margin: 10px 0;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
        }
        button {
            background-color: #4CAF50;
            color: white;
            padding: 12px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            width: 100%;
        }
        button:hover {
            background-color: #45a049;
        }
        .result {
            margin-top: 20px;
            padding: 20px;
            border-radius: 5px;
            background-color: #f9f9f9;
            display: none;
        }
        .emotion-bar {
            margin: 10px 0;
        }
        .bar-label {
            display: inline-block;
            width: 80px;
        }
        .bar-container {
            display: inline-block;
            width: 300px;
            height: 20px;
            background-color: #eee;
            border-radius: 10px;
            overflow: hidden;
        }
        .bar-fill {
            height: 100%;
            background-color: #4CAF50;
            transition: width 0.3s ease;
        }
        .dominant {
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            color: #333;
            margin: 20px 0;
        }
        .error {
            color: red;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎭 Emotion Detection System</h1>
        <form id="emotionForm">
            <textarea id="textInput" placeholder="Enter text to analyze emotions..."></textarea>
            <button type="submit">Analyze Emotions</button>
        </form>
        <div id="result" class="result"></div>
    </div>

    <script>
        document.getElementById('emotionForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const text = document.getElementById('textInput').value;
            const resultDiv = document.getElementById('result');
            
            try {
                const response = await fetch('/analyze', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ text: text })
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    displayResults(data);
                } else {
                    resultDiv.innerHTML = `<div class="error">Error: ${data.error}</div>`;
                    resultDiv.style.display = 'block';
                }
            } catch (error) {
                resultDiv.innerHTML = `<div class="error">Error: ${error.message}</div>`;
                resultDiv.style.display = 'block';
            }
        });
        
        function displayResults(data) {
            const resultDiv = document.getElementById('result');
            let html = '<h2>Analysis Results</h2>';
            
            // Display dominant emotion
            html += `<div class="dominant">Dominant Emotion: ${data.dominant_emotion.toUpperCase()}</div>`;
            
            // Display emotion bars
            const emotions = ['anger', 'disgust', 'fear', 'joy', 'sadness'];
            emotions.forEach(emotion => {
                const score = data[emotion];
                const percentage = score * 100;
                html += `
                    <div class="emotion-bar">
                        <span class="bar-label">${emotion.charAt(0).toUpperCase() + emotion.slice(1)}</span>
                        <div class="bar-container">
                            <div class="bar-fill" style="width: ${percentage}%"></div>
                        </div>
                        <span>${percentage.toFixed(1)}%</span>
                    </div>
                `;
            });
            
            resultDiv.innerHTML = html;
            resultDiv.style.display = 'block';
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Render the main page"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/analyze', methods=['POST'])
def analyze():
    """API endpoint for emotion analysis"""
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400
        
        text = data['text']
        
        if not text or not text.strip():
            return jsonify({'error': 'Empty text provided'}), 400
        
        # Analyze emotions
        result = detector.emotion_detector(text)
        
        if result is None:
            return jsonify({'error': 'Emotion analysis failed'}), 500
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'emotion-detection'})

@app.route('/api/v1/analyze', methods=['POST'])
def api_analyze():
    """Versioned API endpoint for emotion analysis"""
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                'status': 'error',
                'message': 'No text provided',
                'data': None
            }), 400
        
        text = data['text']
        result = detector.emotion_detector(text)
        
        if result is None:
            return jsonify({
                'status': 'error',
                'message': 'Emotion analysis failed',
                'data': None
            }), 500
        
        return jsonify({
            'status': 'success',
            'message': 'Emotion analysis completed',
            'data': result
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'data': None
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
