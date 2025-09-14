from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from openai import OpenAI
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from src.models.models import User, ValidationHistory, ChatHistory
from src.utils.database import get_db
from src.services.retrieval_service import RetrievalService
from src.core.document_processor import DocumentProcessor
from src.core.validation.validation import ValidationService

# Load environment variables and setup
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize services
retrieval_service = RetrievalService()
validation_service = ValidationService()

app = FastAPI(title="Omnizon RAG")

# CORS middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True, 
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class ChatMessage(BaseModel):
    content: str
    role: str = "user"
    timestamp: datetime = datetime.now()

class ValidationRequest(BaseModel):
    ein: Optional[str] = None
    duns: Optional[str] = None

# System prompt for OpenAI
SYSTEM_PROMPT = """You are an AI assistant for Omnizon, specialized in helping users with:
- EIN (Employer Identification Number) validation
- D-U-N-S number validation
- Invoice compliance
- Platform features
Be helpful and provide specific guidance about Omnizon's platform."""

# Endpoints
@app.get("/")
async def root():
    return {"message": "Welcome to Omnizon RAG API"}

@app.post("/validate")
async def validate_compliance(
    request: ValidationRequest,
    db: Session = Depends(get_db)
):
    try:
        # Perform validation using ValidationService
        ein_valid = await validation_service.validate_ein(request.ein)
        duns_valid = await validation_service.validate_duns(request.duns)
        
        # Store validation history
        validation = ValidationHistory(
            ein=request.ein,
            duns=request.duns,
            is_valid=ein_valid and duns_valid
        )
        db.add(validation)
        db.commit()
        
        return {
            "valid": ein_valid and duns_valid,
            "details": {
                "ein": ein_valid if request.ein else None,
                "duns": duns_valid if request.duns else None
            }
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat(
    message: ChatMessage,
    db: Session = Depends(get_db)
):
    try:
        # Get relevant context from documents
        context = await retrieval_service.get_relevant_context(message.content)
        
        # Get response from OpenAI with context
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Context:\n{context}\n\nQuery: {message.content}"}
            ],
            temperature=0.7
        )
        
        response_content = response.choices[0].message.content

        # Store chat history
        chat_history = ChatHistory(
            message=message.content,
            response=response_content
        )
        db.add(chat_history)
        db.commit()

        return {
            "content": response_content,
            "role": "assistant",
            "timestamp": datetime.now()
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/chat/history")
async def get_chat_history(db: Session = Depends(get_db)):
    chats = db.query(ChatHistory).order_by(ChatHistory.created_at.desc()).all()
    return chats

@app.get("/validate/history")
async def get_validation_history(db: Session = Depends(get_db)):
    validations = db.query(ValidationHistory).order_by(ValidationHistory.created_at.desc()).all()
    return validations

@app.post("/process-docs")
async def process_documents():
    try:
        processor = DocumentProcessor()
        texts = await processor.process_documents()
        return {"message": f"Processed {len(texts)} document chunks successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))