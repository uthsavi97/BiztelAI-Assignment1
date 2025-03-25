BiztelAI-Assignment/
├── app/
│   ├── __init__.py
│   ├── data_pipeline.py    # Fixed implementation
│   ├── api.py              # Enhanced API
│   ├── llm_processor.py    # New LLM integration
│   ├── requirements.txt
│   └── main.py
├── data/
│   └── BiztelAI_DS_Dataset_Mar25.json
├── notebooks/
│   └── exploratory_data_analysis.ipynb
├── Dockerfile
└── README.md

# Install dependencies
pip install -r requirements.txt

# Start the server

python -m uvicorn app.api:app --reload --port 8000


docker build -t biztelai-api .
docker run -p 8000:8000 biztelai-api