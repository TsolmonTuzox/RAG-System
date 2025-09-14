# Contributing to RAG System

First off, thank you for considering contributing to RAG System! It's people like you that make RAG System such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* **Use a clear and descriptive title** for the issue to identify the problem
* **Describe the exact steps which reproduce the problem** in as many details as possible
* **Provide specific examples to demonstrate the steps**
* **Describe the behavior you observed after following the steps**
* **Explain which behavior you expected to see instead and why**
* **Include screenshots and animated GIFs** if possible
* **Include your environment details** (OS, Python version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* **Use a clear and descriptive title** for the issue to identify the suggestion
* **Provide a step-by-step description of the suggested enhancement**
* **Provide specific examples to demonstrate the steps**
* **Describe the current behavior** and **explain which behavior you expected to see instead**
* **Explain why this enhancement would be useful**

### Your First Code Contribution

Unsure where to begin contributing? You can start by looking through these issues:

* Issues labeled `good first issue` - issues which should only require a few lines of code
* Issues labeled `help wanted` - issues which should be a bit more involved than `good first issue` issues

### Pull Requests

1. Fork the repo and create your branch from `main`
2. If you've added code that should be tested, add tests
3. If you've changed APIs, update the documentation
4. Ensure the test suite passes
5. Make sure your code follows the existing style
6. Issue that pull request!

## Development Process

### Setting Up Your Development Environment

1. **Fork and clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/RAG-System.git
cd RAG-System
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirement.txt
pip install -e .  # Install in development mode
```

4. **Set up pre-commit hooks (recommended)**
```bash
pip install pre-commit
pre-commit install
```

5. **Create a branch for your feature**
```bash
git checkout -b feature/your-feature-name
```

### Code Style

* Follow PEP 8 for Python code
* Use meaningful variable names
* Add docstrings to all functions and classes
* Keep functions small and focused
* Write self-documenting code with clear comments where needed

### Testing

* Write tests for any new functionality
* Ensure all tests pass before submitting PR
* Aim for high test coverage

Run tests with:
```bash
pytest tests/
```

Check code coverage:
```bash
pytest --cov=src tests/
```

### Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line

Example:
```
Add vector similarity search optimization

- Implement HNSW index for faster searches
- Add caching layer for frequently accessed embeddings
- Optimize batch processing for document chunks

Fixes #123
```

## Project Structure

```
RAG-System/
├── src/
│   ├── api/           # API endpoints
│   ├── core/          # Core functionality
│   ├── models/        # Data models
│   └── services/      # Business logic
├── tests/             # Test files
├── docs/              # Documentation
└── migrations/        # Database migrations
```

### Key Components

* **API Layer** (`src/api/`): FastAPI routes and endpoints
* **Core** (`src/core/`): Document processing, validation logic
* **Models** (`src/models/`): Database and Pydantic models
* **Services** (`src/services/`): Business logic and external integrations

## Documentation

* Update README.md if you change functionality
* Add docstrings to new functions/classes
* Update API documentation for endpoint changes
* Include examples for complex features

## Review Process

### What to Expect

1. **Initial Review**: Within 2-3 days
2. **Feedback**: Constructive feedback on code quality and implementation
3. **Iterations**: May require changes based on feedback
4. **Approval**: Once requirements are met
5. **Merge**: After approval and passing CI checks

### Review Criteria

* Code quality and style consistency
* Test coverage
* Documentation completeness
* Performance impact
* Security considerations

## Community

### Getting Help

* **GitHub Issues**: For bugs and feature requests
* **Discussions**: For general questions and ideas
* **Documentation**: Check `/docs` for detailed guides

### Recognition

Contributors will be recognized in:
* The project README
* Release notes
* Special contributors file

## Tools and Resources

### Recommended Tools

* **IDE**: VSCode or PyCharm
* **Linting**: pylint, flake8
* **Formatting**: black, isort
* **Type Checking**: mypy
* **Testing**: pytest

### Useful Commands

```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Run linter
flake8 src/ tests/

# Type checking
mypy src/

# Run all checks
pre-commit run --all-files
```

## Additional Notes

### Current Priority Areas

* Frontend implementation completion
* Authentication system
* Multi-language support
* Performance optimizations
* Documentation improvements

### Future Roadmap

Check our [GitHub Projects](https://github.com/TsolmonTuzox/RAG-System/projects) for planned features and current priorities.

## Questions?

Feel free to open an issue with the `question` label or start a discussion.

---

Thank you for contributing to RAG System! 🎉