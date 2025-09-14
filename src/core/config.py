"""Configuration validation and management"""
import os
from typing import Optional
from dotenv import load_dotenv

class Config:
    """Centralized configuration with validation"""
    
    def __init__(self):
        load_dotenv()
        
        # Required environment variables
        self.OPENAI_API_KEY = self._get_required("OPENAI_API_KEY")
        self.DATABASE_URL = self._get_required("DATABASE_URL")
        self.PINECONE_API_KEY = self._get_required("PINECONE_API_KEY")
        self.PINECONE_INDEX = self._get_required("PINECONE_INDEX")
        
        # Optional with defaults
        self.PINECONE_ENV = os.getenv("PINECONE_ENV", "us-east-1")
        self.API_PORT = int(os.getenv("API_PORT", "8000"))
        self.DEBUG = os.getenv("DEBUG", "False").lower() == "true"
        
    def _get_required(self, key: str) -> str:
        """Get required environment variable or raise error"""
        value = os.getenv(key)
        if not value:
            raise ValueError(f"Required environment variable {key} is not set")
        return value
    
    @classmethod
    def validate(cls):
        """Validate all required configs on startup"""
        try:
            config = cls()
            print("✅ Configuration validated successfully")
            return config
        except ValueError as e:
            print(f"❌ Configuration error: {e}")
            print("Please check your .env file")
            raise

# Create singleton instance
config = Config.validate()
