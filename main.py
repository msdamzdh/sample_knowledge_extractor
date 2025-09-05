from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import re
import uuid
import uvicorn
from typing import List, Dict, Any, Optional
import os
import llm_service

# This acts as a mock LLM.
class MockLLM:
    def __init__(self, fail_on_keyword: str = "fail"):
        self.fail_on_keyword = fail_on_keyword
    
    def analyze_text(self, text: str):
        if self.fail_on_keyword in text.lower():
            raise Exception("Mock LLM API failure triggered by keyword 'fail'")
        
        words = re.findall(r'\b\w+\b', text.lower())
        word_counts = {}
        for word in words:
            word_counts[word] = word_counts.get(word, 0) + 1
        
        sorted_words = sorted(word_counts.items(), key=lambda item: item[1], reverse=True)
        keywords = [word for word, count in sorted_words[:3]]

        summary = f"A summary of the provided text. It covers key topics like {keywords[0]} and {keywords[1]}."
        
        sentiment = "neutral"
        if "great" in text.lower() or "awesome" in text.lower():
            sentiment = "positive"
        elif "bad" in text.lower() or "terrible" in text.lower():
            sentiment = "negative"
            
        confidence_score = 0.95 if sentiment != "neutral" else 0.85

        metadata = {
            "title": text.split('\n')[0].strip() if '\n' in text else "Untitled Document",
            "topics": [keywords[0], "llm", "prototype"],
            "sentiment": sentiment,
            "keywords": keywords,
            "confidence_score": confidence_score
        }

        return {"summary": summary, "metadata": metadata}

# This class defines the data model for the request body
class TextRequest(BaseModel):
    text: str
    model_choice: str
    api_key: Optional[str] = None

# In-memory storage acting as a lightweight database
analyses_db: List[Dict[str, Any]] = []

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def get_index_page():
    """
    Serves the main HTML page.
    """
    html_file_path = "index.html"
    if not os.path.exists(html_file_path):
        raise HTTPException(status_code=404, detail="index.html not found.")
    
    with open(html_file_path, "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read())

@app.post("/analyze")
async def analyze_text(text_request: TextRequest):
    """
    Analyzes a block of text and stores the result using the selected LLM.
    """
    if not text_request.text.strip():
        raise HTTPException(status_code=400, detail="Empty input text.")
    
    try:
        # The keywords are extracted here as per the assignment's instructions.
        words = re.findall(r'\b\w+\b', text_request.text.lower())
        word_counts = {}
        for word in words:
            word_counts[word] = word_counts.get(word, 0) + 1
        sorted_words = sorted(word_counts.items(), key=lambda item: item[1], reverse=True)
        keywords = [word for word, count in sorted_words[:3]]
        
        # Use a single mock LLM instance to avoid re-creation on each call
        if text_request.model_choice == "mock":
            mock_llm = MockLLM()
            llm_result = mock_llm.analyze_text(text_request.text)
            metadata = llm_result["metadata"]
            metadata["keywords"] = keywords
            summary = llm_result["summary"]
            
        else:
            llm_output = llm_service.get_llm_analysis(
                text=text_request.text, 
                model_choice=text_request.model_choice, 
                api_key=text_request.api_key
            )
            metadata = {
                "title": llm_output.get("title"),
                "topics": llm_output.get("topics"),
                "sentiment": llm_output.get("sentiment"),
                "keywords": keywords,
                "confidence_score": 0.95 # A simple heuristic for real LLMs
            }
            summary = llm_output.get("summary")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM analysis failed: {str(e)}")
    
    analysis_id = str(uuid.uuid4())
    full_analysis = {
        "id": analysis_id,
        "input_text": text_request.text,
        "summary": summary,
        "metadata": metadata
    }
    
    analyses_db.append(full_analysis)
    return full_analysis

@app.get("/search")
async def search_analyses(topic: Optional[str] = None):
    """
    Searches for analyses by topic or keyword.
    """
    if not topic:
        return {"results": analyses_db}

    results = [
        analysis for analysis in analyses_db
        if topic.lower() in [t.lower() for t in analysis["metadata"]["topics"]]
        or topic.lower() in [k.lower() for k in analysis["metadata"]["keywords"]]
    ]
    
    return {"results": results}

# This block allows you to run the script directly with `python main.py`
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
