# Development Guide

## Overview
This guide provides essential information for developers working on the BookBrain-Azure project, including setup instructions, coding standards, and best practices.

## Development Environment Setup

### Prerequisites
- Python 3.8 or higher
- Visual Studio Code
- Azure Functions Core Tools
- Azure CLI
- Git
- PostgreSQL

### Initial Setup

1. **Clone Repository**
```bash
git clone https://github.com/YourUsername/BookBrain-Azure.git
cd BookBrain-Azure
```

2. **Virtual Environment**
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure Local Settings**
```bash
cp local.settings.json.example local.settings.json
# Edit local.settings.json with your development values
```

## Project Structure

```
BookBrain-Azure/
├── .venv/
├── .vscode/
├── docs/
│   ├── api_documentation.md
│   ├── deployment.md
│   └── development.md
├── src/
│   ├── functions/
│   │   ├── pdf_chunking/
│   │   ├── upload_book/
│   │   ├── study_progress/
│   │   └── hourly_digest/
│   ├── shared/
│   │   ├── database/
│   │   ├── storage/
│   │   └── utils/
│   └── tests/
├── .gitignore
├── host.json
├── local.settings.json
├── requirements.txt
└── README.md
```

## Coding Standards

### Python Style Guide

1. **Code Formatting**
   - Use [Black](https://github.com/psf/black) for code formatting
   - Maximum line length: 88 characters
   - Use 4 spaces for indentation

2. **Naming Conventions**
   - Functions: `snake_case`
   - Classes: `PascalCase`
   - Constants: `UPPER_SNAKE_CASE`
   - Variables: `snake_case`

3. **Documentation**
   - Use docstrings for all functions and classes
   - Follow Google style docstrings

Example:
```python
def process_pdf_chunk(
    chunk_text: str,
    page_number: int,
    metadata: dict
) -> dict:
    """Process a single chunk of PDF text.

    Args:
        chunk_text (str): The text content of the chunk
        page_number (int): The page number this chunk belongs to
        metadata (dict): Additional metadata about the chunk

    Returns:
        dict: Processed chunk with additional information
    """
    # Implementation
```

### Git Workflow

1. **Branch Naming**
   - Feature branches: `feature/description`
   - Bug fixes: `fix/description`
   - Documentation: `docs/description`

2. **Commit Messages**
   - Format: `type(scope): description`
   - Types: feat, fix, docs, style, refactor, test, chore
   - Keep messages clear and concise

Example:
```bash
git commit -m "feat(pdf-chunking): add overlap parameter for better context"
```

## Testing

### Unit Tests
```python
# test_pdf_chunking.py
import pytest
from src.functions.pdf_chunking import process_pdf

def test_process_pdf_valid_input():
    result = process_pdf("sample.pdf", chunk_size=500)
    assert result["status"] == "success"
    assert len(result["chunks"]) > 0

def test_process_pdf_invalid_input():
    with pytest.raises(ValueError):
        process_pdf("nonexistent.pdf")
```

### Integration Tests
```python
# test_integration.py
import pytest
from src.shared.database import Database
from src.shared.storage import Storage

@pytest.mark.integration
def test_pdf_processing_workflow():
    # Setup
    db = Database()
    storage = Storage()
    
    # Test workflow
    book_id = db.create_book({"title": "Test Book"})
    storage.upload_pdf("test.pdf", book_id)
    chunks = process_pdf_chunks(book_id)
    
    # Assertions
    assert len(chunks) > 0
    assert db.get_chunks(book_id) == chunks
```

## Local Development

### Running Functions Locally
```bash
# Start function host
func start

# Test specific function
func start --functions PdfChunkingFunction
```

### Database Setup
```bash
# Create local database
createdb bookbrain_dev

# Run migrations
python scripts/db_setup.py
```

### Environment Variables
```bash
# Required for local development
AZURE_STORAGE_CONNECTION_STRING="UseDevelopmentStorage=true"
DB_HOST="localhost"
DB_NAME="bookbrain_dev"
DB_USER="your_username"
DB_PASSWORD="your_password"
```

## Debugging

### VS Code Configuration
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Attach to Python Functions",
            "type": "python",
            "request": "attach",
            "port": 9091,
            "preLaunchTask": "func: host start"
        }
    ]
}
```

### Logging
```python
import logging

logger = logging.getLogger(__name__)

def process_chunk(chunk_data: dict):
    try:
        logger.info(f"Processing chunk: {chunk_data['id']}")
        # Processing logic
        logger.debug(f"Chunk details: {chunk_data}")
    except Exception as e:
        logger.error(f"Error processing chunk: {str(e)}")
        raise
```

## Performance Optimization

### Database Queries
```python
# Use batch operations
async def save_chunks(chunks: List[dict]):
    async with pool.acquire() as conn:
        await conn.executemany("""
            INSERT INTO chunks (book_id, content, page_number)
            VALUES ($1, $2, $3)
        """, [(c["book_id"], c["content"], c["page_number"]) for c in chunks])

# Use proper indexing
CREATE INDEX idx_chunks_book_id ON chunks(book_id);
CREATE INDEX idx_chunks_page_number ON chunks(page_number);
```

### Memory Management
```python
def process_large_pdf(file_path: str):
    chunk_size = 1024 * 1024  # 1MB chunks
    with open(file_path, "rb") as f:
        while chunk := f.read(chunk_size):
            process_chunk(chunk)
```

## Error Handling

### Custom Exceptions
```python
class BookBrainException(Exception):
    """Base exception for BookBrain application."""
    pass

class PDFProcessingError(BookBrainException):
    """Raised when PDF processing fails."""
    pass

class StorageError(BookBrainException):
    """Raised when storage operations fail."""
    pass
```

### Error Handling Pattern
```python
from typing import Optional

def handle_pdf_upload(
    file_path: str,
    metadata: dict
) -> tuple[bool, Optional[str]]:
    try:
        validate_pdf(file_path)
        process_pdf(file_path)
        return True, None
    except PDFProcessingError as e:
        logger.error(f"PDF processing failed: {str(e)}")
        return False, str(e)
    except Exception as e:
        logger.exception("Unexpected error during PDF upload")
        return False, "Internal server error"
```

## Security Best Practices

1. **Input Validation**
```python
def validate_book_data(book_data: dict):
    required_fields = ["title", "author", "isbn"]
    if not all(field in book_data for field in required_fields):
        raise ValueError("Missing required fields")
    
    if not isinstance(book_data["isbn"], str) or len(book_data["isbn"]) != 13:
        raise ValueError("Invalid ISBN format")
```

2. **File Handling**
```python
import magic
from pathlib import Path

def validate_pdf(file_path: str):
    mime = magic.Magic(mime=True)
    file_type = mime.from_file(file_path)
    
    if file_type != "application/pdf":
        raise ValueError("Invalid file type")
    
    if Path(file_path).stat().st_size > 100_000_000:  # 100MB
        raise ValueError("File too large")
```

## API Integration

### OpenAI Integration
```python
from openai import OpenAI

async def analyze_text_content(text: str) -> dict:
    client = OpenAI()
    try:
        response = await client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Analyze the following text content."},
                {"role": "user", "content": text}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"OpenAI API error: {str(e)}")
        raise
```

## Monitoring and Logging

### Application Insights
```python
from opencensus.ext.azure.log_exporter import AzureLogHandler

logger = logging.getLogger(__name__)
logger.addHandler(AzureLogHandler(
    connection_string='InstrumentationKey=<your-key-here>'
))

def track_performance(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start_time
        
        logger.info(f"Function {func.__name__} took {duration:.2f} seconds")
        return result
    return wrapper
```

## Continuous Integration

### GitHub Actions
```yaml
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.8'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Run tests
      run: |
        pytest tests/
```
