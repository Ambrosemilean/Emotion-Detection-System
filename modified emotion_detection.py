"""
Emotion Detection Module with Enhanced Output Formatting
File: emotion_detection_formatted.py
"""

import json
from emotion_detection import EmotionDetector

def format_emotion_output(emotion_scores):
    """
    Format emotion scores for better readability
    
    Args:
        emotion_scores (dict): Raw emotion scores
        
    Returns:
        str: Formatted string output
    """
    if not emotion_scores:
        return "No emotion data available"
    
    formatted = []
    formatted.append("=" * 50)
    formatted.append("EMOTION ANALYSIS RESULTS")
    formatted.append("=" * 50)
    
    # Format each emotion score
    for emotion, score in emotion_scores.items():
        if emotion != 'dominant_emotion' and score is not None:
            # Create visual bar representation
            bar_length = int(score * 50)
            bar = "█" * bar_length + "░" * (50 - bar_length)
            formatted.append(f"{emotion.capitalize():10} [{bar}] {score:.2f}")
    
    # Add dominant emotion
    if emotion_scores.get('dominant_emotion'):
        formatted.append("-" * 50)
        formatted.append(f"Dominant Emotion: {emotion_scores['dominant_emotion'].upper()}")
        formatted.append("=" * 50)
    
    return "\n".join(formatted)


def save_emotion_report(emotion_scores, filename="emotion_report.json"):
    """
    Save emotion scores to a JSON file
    
    Args:
        emotion_scores (dict): Emotion scores to save
        filename (str): Output filename
    """
    with open(filename, 'w') as f:
        json.dump(emotion_scores, f, indent=2)
    print(f"Report saved to {filename}")


if __name__ == "__main__":
    # Test the formatted output
    detector = EmotionDetector()
    test_texts = [
        "I am so happy today!",
        "This is absolutely disgusting!",
        "I'm scared of what might happen",
        "I feel so sad and lonely",
        "This makes me so angry!"
    ]
    
    print("Testing Emotion Detection with Formatted Output\n")
    
    for text in test_texts:
        print(f"\nAnalyzing: '{text}'")
        result = detector.emotion_detector(text)
        formatted_output = format_emotion_output(result)
        print(formatted_output)
        save_emotion_report(result, f"emotion_report_{test_texts.index(text)}.json")
