# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import numpy as np
import cv2
from deepface import DeepFace
import os
from werkzeug.utils import secure_filename
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Emotion labels with corresponding emojis and colors
EMOTION_CONFIG = {
    'angry': {'emoji': '😠', 'color': '#FF4444', 'description': 'Frustrated or annoyed'},
    'disgust': {'emoji': '🤢', 'color': '#00C851', 'description': 'Repulsed or offended'},
    'fear': {'emoji': '😨', 'color': '#AA66CC', 'description': 'Anxious or scared'},
    'happy': {'emoji': '😊', 'color': '#FFBB33', 'description': 'Joyful or pleased'},
    'sad': {'emoji': '😢', 'color': '#33B5E5', 'description': 'Down or melancholy'},
    'surprise': {'emoji': '😲', 'color': '#2BBBAD', 'description': 'Shocked or amazed'},
    'neutral': {'emoji': '😐', 'color': '#9E9E9E', 'description': 'Calm and composed'}
}

def decode_image(image_data):
    """Decode base64 image data"""
    try:
        # Remove data URL prefix if present
        if ',' in image_data:
            image_data = image_data.split(',')[1]
        
        # Decode base64
        image_bytes = base64.b64decode(image_data)
        
        # Convert to numpy array
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        return img
    except Exception as e:
        logger.error(f"Error decoding image: {str(e)}")
        return None

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Emotion detection API is running'})

@app.route('/analyze', methods=['POST'])
def analyze_emotion():
    """Analyze emotion from uploaded image"""
    try:
        data = request.get_json()
        
        if not data or 'image' not in data:
            return jsonify({'error': 'No image provided'}), 400
        
        # Decode image
        img = decode_image(data['image'])
        
        if img is None:
            return jsonify({'error': 'Invalid image data'}), 400
        
        # Analyze emotion using DeepFace
        try:
            result = DeepFace.analyze(img, 
                                     actions=['emotion'], 
                                     enforce_detection=False,
                                     silent=True)
            
            # Handle multiple faces - take the first one
            if isinstance(result, list):
                result = result[0]
            
            # Get dominant emotion and confidence scores
            dominant_emotion = result['dominant_emotion']
            emotions = result['emotion']
            
            # Calculate confidence percentage
            confidence = emotions[dominant_emotion]
            
            # Prepare response
            response = {
                'success': True,
                'dominant_emotion': dominant_emotion,
                'confidence': round(confidence, 2),
                'emotions': {k: round(v, 2) for k, v in emotions.items()},
                'config': EMOTION_CONFIG.get(dominant_emotion, {
                    'emoji': '🤔',
                    'color': '#9E9E9E',
                    'description': 'Unknown emotion'
                })
            }
            
            logger.info(f"Emotion detected: {dominant_emotion} with {confidence}% confidence")
            return jsonify(response)
            
        except Exception as e:
            logger.error(f"DeepFace analysis error: {str(e)}")
            return jsonify({'error': 'Could not detect face or analyze emotion. Please ensure your face is clearly visible.'}), 400
            
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred'}), 500

@app.route('/analyze-file', methods=['POST'])
def analyze_file():
    """Analyze emotion from uploaded file"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Secure filename and save temporarily
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Analyze emotion
        try:
            result = DeepFace.analyze(filepath, 
                                     actions=['emotion'], 
                                     enforce_detection=False,
                                     silent=True)
            
            # Clean up
            os.remove(filepath)
            
            # Handle multiple faces - take the first one
            if isinstance(result, list):
                result = result[0]
            
            # Get dominant emotion and confidence scores
            dominant_emotion = result['dominant_emotion']
            emotions = result['emotion']
            
            # Calculate confidence percentage
            confidence = emotions[dominant_emotion]
            
            # Prepare response
            response = {
                'success': True,
                'dominant_emotion': dominant_emotion,
                'confidence': round(confidence, 2),
                'emotions': {k: round(v, 2) for k, v in emotions.items()},
                'config': EMOTION_CONFIG.get(dominant_emotion, {
                    'emoji': '🤔',
                    'color': '#9E9E9E',
                    'description': 'Unknown emotion'
                })
            }
            
            return jsonify(response)
            
        except Exception as e:
            # Clean up if file exists
            if os.path.exists(filepath):
                os.remove(filepath)
            
            logger.error(f"DeepFace analysis error: {str(e)}")
            return jsonify({'error': 'Could not detect face or analyze emotion. Please ensure the image contains a clear face.'}), 400
            
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
