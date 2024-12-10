# PDF Chunking Function Documentation

## Overview
The PDF Chunking Function is responsible for processing PDF books into meaningful, digestible chunks for improved learning and analysis. It uses advanced text processing algorithms to break down content while maintaining context and relationships between sections.

## Technical Details

### Function Configuration
- **Name**: `pdfchun`
- **Trigger**: HTTP Trigger
- **Authorization Level**: Function

### Input Parameters
```json
{
    "book_id": "integer",
    "chunk_size": "integer (optional, default: 1000)",
    "overlap": "integer (optional, default: 100)"
}
```

### Output Format
```json
{
    "status": "string",
    "message": "string",
    "chunks": [
        {
            "id": "string",
            "content": "string",
            "page_number": "integer",
            "chapter": "string",
            "metadata": {}
        }
    ]
}
```

### Environment Variables Required
- `AZURE_STORAGE_CONNECTION_STRING`
- `DB_HOST`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`

## Processing Steps

1. **PDF Loading**
   - Retrieves PDF from Azure Storage using book_id
   - Validates PDF format and accessibility

2. **Text Extraction**
   - Extracts raw text while preserving formatting
   - Handles special characters and encodings
   - Maintains page numbers and chapter information

3. **Content Chunking**
   - Splits content into semantic chunks
   - Preserves context across chunk boundaries
   - Maintains chapter and section relationships

4. **Metadata Enhancement**
   - Adds structural metadata
   - Tags content categories
   - Indexes for search

5. **Storage**
   - Stores chunks in PostgreSQL database
   - Updates book processing status
   - Creates search indices

## Error Handling

The function implements comprehensive error handling for:
- Invalid PDF files
- Processing failures
- Database connection issues
- Storage access problems

Error responses follow this format:
```json
{
    "status": "error",
    "message": "Detailed error message",
    "error_code": "string",
    "details": {}
}
```

## Performance Considerations

- Optimized for PDFs up to 1000 pages
- Average processing time: 2-5 minutes per book
- Memory usage scales with PDF size
- Implements automatic retry for transient failures

## Usage Example

```python
import requests

url = "https://your-function-app.azurewebsites.net/api/pdfchun"
data = {
    "book_id": 123,
    "chunk_size": 800,
    "overlap": 50
}
response = requests.post(url, json=data)
```

## Monitoring and Logging

- Uses Azure Application Insights
- Logs processing steps and timing
- Tracks memory usage and performance
- Enables detailed error tracing

## Best Practices

1. **Input Validation**
   - Verify PDF file existence before processing
   - Validate chunk size parameters
   - Check database connectivity

2. **Resource Management**
   - Implement proper file cleanup
   - Monitor memory usage
   - Use connection pooling

3. **Error Recovery**
   - Implement idempotent processing
   - Store processing state
   - Enable manual retry mechanisms
