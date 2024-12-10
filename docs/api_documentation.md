# API Documentation

## Overview
BookBrain-Azure provides a comprehensive RESTful API for interacting with the platform's features. This documentation covers all available endpoints, their usage, and examples.

## Base URL
```
https://your-function-app.azurewebsites.net/api
```

## Authentication
All API endpoints require authentication using a function key passed as a query parameter:
```
?code=your-function-key
```

## Endpoints

### 1. PDF Chunking API

#### Process PDF
```http
POST /pdfchun
```

**Request Body:**
```json
{
    "book_id": "integer",
    "chunk_size": "integer (optional)",
    "overlap": "integer (optional)"
}
```

**Response:**
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

### 2. Upload Book API

#### Upload New Book
```http
POST /UploadBookFunc
```

**Request Body (multipart/form-data):**
- `file`: PDF file
- `book_data`: JSON string containing:
```json
{
    "title": "string",
    "author": "string",
    "subtitle": "string (optional)",
    "isbn": "string",
    "subject_id": "integer"
}
```

**Response:**
```json
{
    "status": "string",
    "message": "string",
    "book_id": "integer",
    "upload_details": {
        "timestamp": "string",
        "file_size": "integer",
        "processing_status": "string"
    }
}
```

### 3. Progress Tracking API

#### Update Progress
```http
POST /ProgressByChapter
```

**Request Body:**
```json
{
    "user_id": "integer",
    "book_id": "integer",
    "chapter_id": "integer",
    "progress_data": {
        "time_spent": "integer",
        "pages_read": "integer",
        "completion_status": "string",
        "comprehension_score": "float"
    }
}
```

**Response:**
```json
{
    "status": "string",
    "progress_details": {
        "overall_progress": "float",
        "chapter_progress": "float",
        "time_analysis": {
            "total_time": "integer",
            "average_speed": "float",
            "estimated_completion": "string"
        }
    }
}
```

### 4. Study Digest API

#### Get Hourly Digest
```http
GET /HourlyStudyDigest
```

**Query Parameters:**
- `user_id`: integer
- `start_time`: string (ISO date)
- `end_time`: string (ISO date)

**Response:**
```json
{
    "digest": {
        "period": "string",
        "summary": {
            "total_study_time": "integer",
            "chapters_completed": "integer",
            "pages_read": "integer",
            "average_comprehension": "float"
        },
        "achievements": [],
        "recommendations": []
    }
}
```

## Error Handling

All endpoints follow a consistent error response format:

```json
{
    "status": "error",
    "error_code": "string",
    "message": "string",
    "details": {}
}
```

### Common Error Codes
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `429`: Too Many Requests
- `500`: Internal Server Error

## Rate Limiting

- Default rate limit: 100 requests per minute
- Burst allowance: 200 requests
- Headers included in response:
  - `X-RateLimit-Limit`
  - `X-RateLimit-Remaining`
  - `X-RateLimit-Reset`

## Best Practices

1. **Authentication**
   - Store function keys securely
   - Rotate keys periodically
   - Use appropriate authorization levels

2. **Request Optimization**
   - Batch requests when possible
   - Implement retry logic
   - Handle rate limiting

3. **Error Handling**
   - Implement proper error handling
   - Log API errors
   - Provide meaningful error messages

## Examples

### cURL Examples

1. **Upload Book:**
```bash
curl -X POST https://your-function-app.azurewebsites.net/api/UploadBookFunc \
  -F "file=@book.pdf" \
  -F 'book_data={"title":"Sample Book","author":"John Doe","isbn":"123-456-789","subject_id":1}' \
  -H "Content-Type: multipart/form-data"
```

2. **Update Progress:**
```bash
curl -X POST https://your-function-app.azurewebsites.net/api/ProgressByChapter \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 123,
    "book_id": 456,
    "chapter_id": 7,
    "progress_data": {
      "time_spent": 45,
      "pages_read": 20,
      "completion_status": "completed",
      "comprehension_score": 0.85
    }
  }'
```

### Python Examples

1. **Process PDF:**
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

2. **Get Study Digest:**
```python
import requests

url = "https://your-function-app.azurewebsites.net/api/HourlyStudyDigest"
params = {
    "user_id": 123,
    "start_time": "2024-01-01T00:00:00Z",
    "end_time": "2024-01-01T23:59:59Z"
}
response = requests.get(url, params=params)
```

## SDK Support

Official SDKs are available for:
- Python
- JavaScript/Node.js
- .NET
- Java

## Webhook Integration

Endpoints support webhook notifications for:
- Processing completion
- Progress updates
- Achievement unlocks
- Digest generation

## API Versioning

- Current version: v1
- Version specified in URL: `/api/v1/endpoint`
- Deprecation notice: 6 months
- Legacy support: 12 months
