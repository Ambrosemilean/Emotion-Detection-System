
## Task 2: emotion_detection.py (2a_emotion_detection)

```python
"""
Emotion Detection Module using IBM Watson NLP Library
File: emotion_detection.py
"""

import json
import requests

class EmotionDetector:
    """Emotion Detection class using IBM Watson NLP"""
    
    def __init__(self, api_key=None, url=None):
        """
        Initialize the EmotionDetector with IBM Watson credentials
        
        Args:
            api_key (str): IBM Watson API key
            url (str): IBM Watson service URL
        """
        self.api_key = api_key
        self.url = url
        self.headers = {
            "Content-Type": "application/json"
        }
        
    def emotion_detector(self, text_to_analyze):
        """
        Analyze text and return emotion scores
        
        Args:
            text_to_analyze (str): Text to analyze for emotions
            
        Returns:
            dict: Dictionary containing emotion scores and dominant emotion
        """
        if not text_to_analyze:
            return {
                'anger': None,
                'disgust': None,
                'fear': None,
                'joy': None,
                'sadness': None,
                'dominant_emotion': None
            }
        
        try:
            # Simulated API call for demonstration
            # In production, replace with actual IBM Watson API call
            response_data = self._mock_emotion_analysis(text_to_analyze)
            
            # Extract emotion scores
            emotions = response_data.get('emotion', {})
            
            # Find dominant emotion
            if emotions:
                dominant_emotion = max(emotions, key=emotions.get)
            else:
                dominant_emotion = None
            
            return {
                'anger': emotions.get('anger', 0),
                'disgust': emotions.get('disgust', 0),
                'fear': emotions.get('fear', 0),
                'joy': emotions.get('joy', 0),
                'sadness': emotions.get('sadness', 0),
                'dominant_emotion': dominant_emotion
            }
            
        except Exception as e:
            print(f"Error in emotion detection: {e}")
            return None
    
    def _mock_emotion_analysis(self, text):
        """
        Mock function to simulate IBM Watson API response
        
        Args:
            text (str): Input text
            
        Returns:
            dict: Mock emotion analysis data
        """
        # Simple keyword-based mock emotion detection
        emotions = {
            'anger': 0.1,
            'disgust': 0.1,
            'fear': 0.1,
            'joy': 0.1,
            'sadness': 0.1
        }
        
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['happy', 'great', 'excellent', 'joy']):
            emotions['joy'] = 0.9
        elif any(word in text_lower for word in ['sad', 'unhappy', 'depressed']):
            emotions['sadness'] = 0.8
        elif any(word in text_lower for word in ['angry', 'mad', 'furious']):
            emotions['anger'] = 0.85
        elif any(word in text_lower for word in ['scared', 'afraid', 'terrified']):
            emotions['fear'] = 0.75
        elif any(word in text_lower for word in ['disgusting', 'gross', 'repulsive']):
            emotions['disgust'] = 0.7
            
        return {'emotion': emotions}


def emotion_predictor(text):
    """
    Convenience function for emotion prediction
    
    Args:
        text (str): Text to analyze
        
    Returns:
        dict: Emotion analysis results
    """
    detector = EmotionDetector()
    return detector.emotion_detector(text)


if __name__ == "__main__":
    # Example usage
    detector = EmotionDetector()
    result = detector.emotion_detector("I am so happy today!")
    print(json.dumps(result, indent=2))
