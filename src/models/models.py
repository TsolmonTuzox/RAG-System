# src/models/models.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from ..utils.database import Base

class User(Base):
    """User model for storing user information"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    validations = relationship("ValidationHistory", back_populates="user")
    chats = relationship("ChatHistory", back_populates="user")

class ValidationHistory(Base):
    """Model for storing generic validation history"""
    __tablename__ = "validation_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    validation_data = Column(Text)  # JSON string of validated data
    validation_rules = Column(Text)  # JSON string of rules applied
    is_valid = Column(Boolean)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    user = relationship("User", back_populates="validations")

class ChatHistory(Base):
    """Model for storing chat history"""
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    message = Column(Text)
    response = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    user = relationship("User", back_populates="chats")

class DocumentEmbedding(Base):
    """Model for storing document embeddings metadata"""
    __tablename__ = "document_embeddings"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(String, unique=True, index=True)
    source_file = Column(String)
    chunk_text = Column(Text)
    chunk_index = Column(Integer)
    embedding_id = Column(String)  # Pinecone vector ID
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
