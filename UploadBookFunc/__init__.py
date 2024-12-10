import logging
import os
import json
from typing import Dict, Any

import fitz  # PyMuPDF
import requests
from azure.functions import HttpRequest, HttpResponse
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import AzureError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
CONTAINER_NAME = "dokumente"
CORS_HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Origin'
}

# Load configuration from environment variables
CHECK_URL = os.getenv("CHECK_URL")
METADATA_API_URL = os.getenv("METADATA_API_URL")
CHUNKING_URL = os.getenv("CHUNKING_URL")
API_KEY = os.getenv("API_KEY")

def main(req: HttpRequest) -> HttpResponse:
    logger.info('Processing HTTP request in Azure Function.')

    if req.method == 'OPTIONS':
        logger.info('Handling OPTIONS request for CORS preflight.')
        return HttpResponse(status_code=200, headers=CORS_HEADERS)

    try:
        # Azure Blob Storage setup
        connect_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        if not connect_str:
            raise ValueError("Azure Storage connection string is not set.")
        
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        container_client = blob_service_client.get_container_client(CONTAINER_NAME)
        logger.info(f"Connected to Azure Blob Storage container: {CONTAINER_NAME}")

        # Process the uploaded file
        file = req.files['file']
        file_name = file.filename
        logger.info(f"Processing uploaded file: {file_name}")

        if not file_name.lower().endswith('.pdf'):
            return create_response("error", "Uploaded file is not a PDF.", 400)

        file_content = file.read()
        pdf_text = extract_pdf_text(file_content)
        
        if not pdf_text.strip():
            return create_response("error", "Uploaded PDF does not contain text. Please perform OCR.", 400)

        # Process book metadata
        book_data = process_book_metadata(req)
        
        # Check for existing file
        if file_exists(file_name):
            return create_response("error", "This file has already been uploaded.", 400)

        # Upload file to Blob Storage
        blob_client = container_client.get_blob_client(file_name)
        blob_client.upload_blob(file_content, overwrite=True)
        logger.info(f"File uploaded successfully: {file_name}")

        # Save metadata and get book ID
        book_id = save_metadata(book_data, file_name)
        
        # Initiate chunking process
        initiate_chunking(book_id)

        logger.info(f"File processing completed successfully for: {file_name}")
        return create_response("success", f"File {file_name} uploaded successfully to container {CONTAINER_NAME}, metadata saved, and chunking process initiated.", 200, book_id)

    except ValueError as ve:
        logger.error(f"ValueError: {str(ve)}")
        return create_response("error", str(ve), 400)
    except AzureError as ae:
        logger.error(f"Azure Storage error: {str(ae)}")
        return create_response("error", f"Azure Storage error: {str(ae)}", 500)
    except Exception as e:
        logger.exception(f"Unexpected error during file processing: {str(e)}")
        return create_response("error", f"Unexpected error: {str(e)}", 500)

def create_response(status: str, message: str, status_code: int, return_val: Any = 0) -> HttpResponse:
    response_body = {
        "result": {
            "status": status,
            "message": message,
            "return_val": return_val
        }
    }
    return HttpResponse(json.dumps(response_body), status_code=status_code, headers=CORS_HEADERS, mimetype="application/json")



def extract_pdf_text(file_content: bytes) -> str:
    logger.info("Extracting text from PDF")
    pdf_document = fitz.open(stream=file_content, filetype="pdf")
    pdf_text = ""
    for page_num, page in enumerate(pdf_document):
        pdf_text += page.get_text()
        logger.debug(f"Extracted text from page {page_num + 1}")
    return pdf_text

def process_book_metadata(req: HttpRequest) -> Dict[str, Any]:
    logger.info("Processing book metadata")
    try:
        book_data = json.loads(req.form['book_data'])
        required_fields = ['title', 'author', 'subtitle', 'isbn']
        for field in required_fields:
            if not book_data.get(field):
                raise ValueError(f"Missing required metadata field: {field}")
        return book_data
    except (json.JSONDecodeError, KeyError) as e:
        logger.error(f"Error processing book metadata: {str(e)}")
        raise ValueError("Invalid book metadata format.") from e

def file_exists(file_name: str) -> bool:
    logger.info(f"Checking if file already exists: {file_name}")
    check_params = {
        'action': 'check_url',
        'url': file_name,
        'code': API_KEY
    }
    response = requests.get(CHECK_URL, params=check_params)
    if response.status_code == 200:
        return response.json().get('url_exists', True)
    logger.warning(f"Failed to check file existence. Status code: {response.status_code}")
    return False

def save_metadata(metadata: Dict[str, Any], file_name: str) -> str:
    logger.info("Saving book metadata")
    metadata['url'] = file_name
    headers = {'Content-Type': 'application/json'}
    params = {'action': 'create', 'code': API_KEY}
    response = requests.post(METADATA_API_URL, headers=headers, json=metadata, params=params)
    
    if response.status_code != 200:
        logger.error(f"Error saving metadata. Status code: {response.status_code}, Response: {response.text}")
        raise ValueError(f"Error saving metadata: {response.text}")
    
    response_data = response.json()
    book_id = response_data.get('return_val')
    if not book_id:
        logger.error("Book ID not found in the response")
        raise ValueError("Error: Book ID not found in the response.")
    
    logger.info(f"Metadata saved successfully. Book ID: {book_id}")
    return book_id

def initiate_chunking(book_id: str) -> None:
    logger.info(f"Initiating chunking process for book ID: {book_id}")
    headers = {'Content-Type': 'application/json'}
    payload = {"book_id": book_id}
    response = requests.post(CHUNKING_URL, headers=headers, json=payload)
    
    if response.status_code != 200:
        logger.error(f"Error initiating chunking process. Status code: {response.status_code}, Response: {response.text}")
        raise ValueError(f"Error initiating chunking process: {response.text}")
    
    logger.info("Chunking process initiated successfully")