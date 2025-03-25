import json
import pandas as pd
from pathlib import Path
from typing import Dict, Any

class DataLoader:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        
    def load_data(self) -> Dict[str, Any]:
        with open(self.file_path, 'r') as f:
            return json.load(f)

class DataCleaner:
    def __init__(self, data: Dict[str, Any]):
        self.raw_data = data
        
    def clean(self) -> pd.DataFrame:
        # Flatten nested JSON structure
        cleaned = []
        for conv_id, details in self.raw_data.items():
            for msg in details['content']:
                cleaned.append({
                    'conv_id': conv_id,
                    'article_url': details['article_url'],
                    'config': details['config'],
                    'agent': msg['agent'],
                    'message': msg['message'],
                    'sentiment': msg['sentiment'],
                    'turn_rating': msg['turn_rating']
                })
        return pd.DataFrame(cleaned)

class DataTransformer:
    def __init__(self, data: pd.DataFrame):
        self.data = data
        
    def transform(self) -> pd.DataFrame:
        # Convert categorical variables
        self.data['sentiment'] = pd.Categorical(self.data['sentiment'])
        self.data['config'] = pd.Categorical(self.data['config'])
        return self.data