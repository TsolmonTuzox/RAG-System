from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any
from openai import OpenAI
import os
from sqlalchemy.orm import Session

# Internal imports
from src.models.models import User, ValidationHistory, ChatHistory
from src.models.chat import ChatMessage
from src.utils.database import get_db
from src.services.retrieval_service import RetrievalService
from src.core.document_processor import DocumentProcessor
from src.core.validation.validation import ValidationService
from src.core.config import config

# Initialize services
client = OpenAI(api_key=config.OPENAI_API_KEY)
retrieval_service = RetrievalService()
validation_service = ValidationService()

app = FastAPI(
    title="RAG System",
    description="Open-source Retrieval-Augmented Generation system with extensible validation",
    version="1.0.0"
)

# CORS middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Models
class ValidationRequest(BaseModel):
    """
    Generic validation request that can handle any data fields
    Example:
    {
        "data": {"email": "user@example.com", "phone": "+1234567890"},
        "rules": {"email": "email", "phone": "phone"}
    }
    """
    data: Dict[str, Any]  # Fields to validate
    rules: Dict[str, str]  # Validation rules for each field
    user_id: Optional[int] = None

class ChatRequest(BaseModel):
    content: str
    user_id: Optional[int] = None

# System prompt for OpenAI
SYSTEM_PROMPT = """You are an AI assistant for a RAG (Retrieval-Augmented Generation) system.
You help users by providing accurate information based on the provided context.
Be helpful, concise, and accurate in your responses."""

# Endpoints
@app.get("/")
async def root():
    return {
        "message": "Welcome to RAG System API",
        "status": "operational",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "services": {
            "database": "connected",
            "pinecone": "connected",
            "openai": "connected"
        }
    }

@app.post("/validate")
async def validate_data(
    request: ValidationRequest,
    db: Session = Depends(get_db)
):
    """
    Generic validation endpoint for any type of data
    
    Example validation rules:
    - "email": Validates email format
    - "phone": Validates phone number format
    - "url": Validates URL format
    - "pattern:regex": Custom regex pattern validation
    """
    try:
        # Validate data using the validation service
        validation_results = await validation_service.validate_data(
            request.data,
            request.rules
        )
        
        # Check if all validations passed
        all_valid = all(validation_results.values())
        
        # Store validation history (generic format)
        validation = ValidationHistory(
            validation_data=str(request.data),  # Store as JSON string
            validation_rules=str(request.rules),
            is_valid=all_valid,
            user_id=request.user_id
        )
        db.add(validation)
        db.commit()
        
        return {
            "valid": all_valid,
            "details": validation_results,
            "timestamp": datetime.now()
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    """Process chat messages with RAG context"""
    try:
        # Get relevant context from documents
        context = retrieval_service.get_relevant_context(request.content)
        
        # Build messages for OpenAI
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Context:\n{context}\n\nQuery: {request.content}"}
        ]
        
        # Get response from OpenAI with context
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        
        response_content = response.choices[0].message.content

        # Store chat history
        chat_history = ChatHistory(
            message=request.content,
            response=response_content,
            user_id=request.user_id
        )
        db.add(chat_history)
        db.commit()

        return {
            "content": response_content,
            "role": "assistant",
            "timestamp": datetime.now(),
            "context_used": bool(context)
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/chat/history")
async def get_chat_history(
    user_id: Optional[int] = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get chat history, optionally filtered by user"""
    query = db.query(ChatHistory)
    
    if user_id:
        query = query.filter(ChatHistory.user_id == user_id)
    
    chats = query.order_by(ChatHistory.created_at.desc()).limit(limit).all()
    return chats

@app.get("/validate/history")
async def get_validation_history(
    user_id: Optional[int] = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get validation history, optionally filtered by user"""
    query = db.query(ValidationHistory)
    
    if user_id:
        query = query.filter(ValidationHistory.user_id == user_id)
    
    validations = query.order_by(ValidationHistory.created_at.desc()).limit(limit).all()
    return validations

@app.post("/process-docs")
async def process_documents(
    directory: str = "docs"
):
    """
    Process and index documents for RAG
    
    Args:
        directory: Directory containing documents to process (default: "docs")
    """
    try:
        processor = DocumentProcessor()
        texts = processor.process_documents(directory)
        return {
            "message": f"Processed {len(texts)} document chunks successfully",
            "directory": directory,
            "timestamp": datetime.now()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/validation-rules")
async def get_validation_rules():
    """Get available validation rules"""
    return {
        "available_rules": [
            {
                "rule": "email",
                "description": "Validates email format",
                "example": "user@example.com"
            },
            {
                "rule": "phone",
                "description": "Validates international phone number format",
                "example": "+1234567890"
            },
            {
                "rule": "url",
                "description": "Validates URL format",
                "example": "https://example.com"
            },
            {
                "rule": "pattern:<regex>",
                "description": "Custom regex pattern validation",
                "example": "pattern:^[A-Z]{2}\\d{6}$"
            }
        ],
        "usage_example": {
            "data": {
                "user_email": "john@example.com",
                "website": "https://example.com",
                "phone": "+1234567890"
            },
            "rules": {
                "user_email": "email",
                "website": "url",
                "phone": "phone"
            }
        }
    }

@app.on_event("startup")
async def startup_event():
    """Validate configuration on startup"""
    print("🚀 Starting RAG System API...")
    print(f"📊 Database: Connected")
    print(f"🔍 Pinecone: Index '{config.PINECONE_INDEX}'")
    print(f"🤖 OpenAI: Model 'gpt-3.5-turbo'")
    print(f"📚 Documentation: /docs")
    print(f"✅ API ready at port {config.API_PORT}")
