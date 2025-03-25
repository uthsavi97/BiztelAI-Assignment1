from fastapi import FastAPI, HTTPException
from app.data_pipeline import DataLoader, DataCleaner, DataTransformer
from app.llm_processor import process_chat_transcript
import logging

app = FastAPI()
logger = logging.getLogger("api")

# Initialize pipeline
from pathlib import Path


file_path = Path(r"C:\udemy\BiztelAI-Assignment\app\data\BiztelAI_DS_Dataset_Mar25.json")
data = DataLoader(file_path).load_data()
df = DataCleaner(data).clean()
transformed_data = DataTransformer(df).transform()

@app.get("/")
async def root():
    return {"message": "BiztelAI Chat Analysis API"}

@app.get("/summary/")
async def get_summary():
    try:
        return {
            "total_conversations": transformed_data['conv_id'].nunique(),
            "avg_messages_per_conv": transformed_data.groupby('conv_id').size().mean(),
            "sentiment_distribution": transformed_data['sentiment'].value_counts().to_dict()
        }
    except Exception as e:
        logger.error(f"Summary error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/analyze/")
async def analyze_transcript(transcript: dict):
    try:
        return process_chat_transcript(transcript)
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))