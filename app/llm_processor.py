from transformers import pipeline
from typing import Dict, Any

# Initialize lightweight models
sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def process_chat_transcript(transcript: Dict[str, Any]) -> Dict[str, Any]:
    # Process with LLMs
    messages = [f"{msg['agent']}: {msg['message']}" for msg in transcript['content']]
    full_text = "\n".join(messages)
    
    # Get summary
    summary = summarizer(full_text, max_length=150, min_length=30, do_sample=False)[0]['summary_text']
    
    # Sentiment analysis
    sentiments = sentiment_analyzer(messages)
    
    # Count messages
    agent_counts = {
        'agent_1': sum(1 for msg in transcript['content'] if msg['agent'] == 'agent_1'),
        'agent_2': sum(1 for msg in transcript['content'] if msg['agent'] == 'agent_2')
    }
    
    return {
        'predicted_article': transcript.get('article_url', ''),
        'message_counts': agent_counts,
        'sentiment_distribution': {
            'agent_1': most_common_sentiment([s for i, s in enumerate(sentiments) 
                                           if transcript['content'][i]['agent'] == 'agent_1']),
            'agent_2': most_common_sentiment([s for i, s in enumerate(sentiments) 
                                           if transcript['content'][i]['agent'] == 'agent_2'])
        },
        'summary': summary
    }

def most_common_sentiment(sentiments):
    labels = [s['label'] for s in sentiments]
    return max(set(labels), key=labels.count) if labels else 'NEUTRAL'