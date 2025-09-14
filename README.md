# RAG System

An open-source Retrieval-Augmented Generation (RAG) system for intelligent document processing and information retrieval.

## Features

- **Document Processing**: Automatically process and index documents for intelligent retrieval
- **Supported Formats**: Markdown (`.md`), PDF (`.pdf`), and Word (`.docx`) files
- **Semantic Search**: Find relevant information using natural language queries
- **Chat Interface**: Interactive Q&A based on your document corpus
- **Validation Framework**: Built-in validation system for custom data types
- **REST API**: Full-featured API for integration with other systems
- **Vector Storage**: Efficient semantic search using vector embeddings

## Tech Stack

### Backend
- **FastAPI** - High-performance Python web framework
- **PostgreSQL** - Relational database for structured data
- **Pinecone** - Vector database for semantic search
- **OpenAI API** - Language model integration
- **Alembic** - Database migration management

### Frontend (In Development)
- **React** with TypeScript
- **Chakra UI** - Component library
- **Real-time updates** via WebSocket

## Quick Start

### Prerequisites

- Python 3.8 or higher
- PostgreSQL database
- Node.js 18+ (for frontend)
- OpenAI API key
- Pinecone account (free tier available)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/rag-system.git
cd rag-system
```

2. **Set up Python environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirement.txt
```

3. **Configure environment variables**

The backend requires the following environment variables:

- `OPENAI_API_KEY` – your OpenAI API key used for language model access.
- `DATABASE_URL` – PostgreSQL connection string for the application database.

Create a `.env` file in the root directory:
```env
# Required
OPENAI_API_KEY=your_openai_api_key
DATABASE_URL=postgresql://username:password@localhost:5432/dbname

# Pinecone Configuration
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENV=your_pinecone_environment
PINECONE_INDEX=your_index_name

# Optional
API_PORT=8000
DEBUG=False
```

4. **Initialize the database**
```bash
alembic upgrade head
```

5. **Run the application**
```bash
uvicorn src.api.main:app --reload
```

The API will be available at `http://localhost:8000`

## Usage

### Processing Documents

Place your Markdown, PDF, or DOCX documents in the `docs/` directory and process them:

```bash
curl -X POST http://localhost:8000/process-docs
```

### API Endpoints

| Endpoint | Method | Description |
|----------|---------|------------|
| `/chat` | POST | Send a message and get AI response |
| `/validate` | POST | Validate data against defined rules |
| `/chat/history` | GET | Retrieve chat history |
| `/validate/history` | GET | Get validation history |
| `/health` | GET | Check system status |
| `/docs` | GET | API documentation (Swagger UI) |

### Example: Chat API

```python
import requests

response = requests.post(
    "http://localhost:8000/chat",
    json={"message": "What is in the documentation about user authentication?"}
)
print(response.json())
```

## Project Structure

```
rag-system/
├── src/
│   ├── api/           # FastAPI routes and endpoints
│   ├── core/          # Core functionality
│   ├── models/        # Database models
│   └── services/      # Business logic
├── docs/              # Document storage
├── migrations/        # Database migrations
├── tests/             # Test suite
├── frontend/          # React frontend (in development)
└── deployment/        # Deployment configurations
```

## Configuration

### Custom Document Processing

You can customize document processing by modifying `src/core/document_processor.py`:

- Adjust chunk size and overlap
- Add custom metadata extraction
- Implement different embedding strategies

### Database Schema

The system uses the following main tables:
- `documents` - Stored document metadata
- `embeddings` - Vector embeddings for semantic search
- `chat_history` - Conversation logs
- `validation_history` - Validation audit trail

## Development

### Running Tests
```bash
pytest tests/
```

### Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Deployment

### Docker

```bash
docker build -t rag-system .
docker run -p 8000:8000 --env-file .env rag-system
```

### Production Considerations

- Use environment variables for all sensitive data
- Enable HTTPS in production
- Set up proper logging and monitoring
- Configure rate limiting
- Use a production WSGI server (e.g., Gunicorn)

## Roadmap

- [ ] Complete frontend implementation
- [ ] Add authentication and authorization
- [ ] Support for multiple file formats (PDF, DOCX, etc.)
- [ ] Batch document processing
- [ ] Export functionality
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] Self-hosted LLM support

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with FastAPI and OpenAI
- Vector search powered by Pinecone
- UI components from Chakra UI

## Support

- **Issues**: Please report bugs via [GitHub Issues](https://github.com/yourusername/rag-system/issues)
- **Discussions**: Join our [GitHub Discussions](https://github.com/yourusername/rag-system/discussions)
- **Documentation**: Full docs available at `/docs` endpoint when running

## Disclaimer

This is an open-source project. Please ensure you comply with OpenAI's usage policies and your local data protection regulations when deploying this system.

---

**Note**: Remember to never commit your `.env` file or any files containing API keys to version control.
