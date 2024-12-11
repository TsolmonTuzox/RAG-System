Omnizon RAG System
Overview
Omnizon RAG is an intelligent document retrieval and validation system that helps users with:

EIN (Employer Identification Number) validation
D-U-N-S number validation
Invoice compliance checks
Smart document search and retrieval

System Architecture
Backend

FastAPI server
PostgreSQL database
RAG (Retrieval Augmented Generation) with Pinecone
OpenAI integration for intelligent responses

Frontend (In Progress)

React TypeScript application
Chakra UI components
Real-time validation
Interactive chat interface

Setup Instructions
Prerequisites

Python 3.8+
Node.js 18+
PostgreSQL
OpenAI API key
Pinecone API key

Backend Setup

Create virtual environment:

bashCopypython -m venv venv
venv\Scripts\activate  # Windows

Install dependencies:

bashCopypip install -r requirements.txt

Configure environment variables (.env):

CopyOPENAI_API_KEY=your_openai_key
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/omnizon
PINECONE_API_KEY=your_pinecone_key
PINECONE_ENV=your_environment
PINECONE_INDEX=omnizon-docs

Initialize database:

bashCopyalembic upgrade head

Run the server:

bashCopyuvicorn src.api.main:app --reload
Documentation Processing
Project documentation is stored in markdown files under the docs/ directory:

ein_validation.md
duns_validation.md
invoice_compliance.md
platform_features.md
user_guide.md

Process documentation using the /process-docs endpoint.
API Endpoints
Validation

POST /validate

Validates EIN and D-U-N-S numbers
Stores validation history



Chat

POST /chat

Provides intelligent responses based on documentation
Uses RAG for accurate information retrieval



History

GET /chat/history

Retrieves chat conversation history


GET /validate/history

Retrieves validation history



Database Schema

Users
ValidationHistory
ChatHistory
DocumentEmbeddings

Vector Search
The system uses Pinecone for:

Document embeddings storage
Semantic search
Relevant context retrieval

Next Steps

Complete frontend implementation
Add user authentication
Enhance validation rules
Add more documentation
Deploy to production

Contributing
Please read through our contributing guidelines before making any changes.
License
MIT License