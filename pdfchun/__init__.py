import logging
import os
import sys
import time
import uuid
import gc
import io
import json
import asyncpg
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient
from azure.functions import HttpRequest, HttpResponse
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from openai import OpenAI
import re
import fitz  # Replace pdfplumber with fitz
import math
import asyncio
from functools import wraps
import psutil
import random 
from pydantic import BaseModel
from typing import List, Tuple

import logging

logger = logging.getLogger(__name__)



sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config import get_config
from logger_config import setup_logger

# Initialization
load_dotenv()
config = get_config()
logger = setup_logger('PDFLogger')
client = None
db_pool = None

def setup_openai_client():
    logger.info("Setting up OpenAI client.")
    try:
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        
        return OpenAI(api_key=openai_api_key)
    except Exception as e:
        logger.error(f"Error setting up OpenAI client: {str(e)}", exc_info=True)
        raise


def get_db_connection_string(config):
    return f"postgresql://{config['db_user']}:{config['db_password']}@{config['db_host']}:{config['db_port']}/{config['db_name']}"

async def fetch_data_by_id_as_json(table_name, id_column="book_id", id_value=2):
    logger.info(f"Fetching data from {table_name} where {id_column}={id_value}")
    try:
        return await execute_with_retry(
            f"SELECT * FROM {table_name} WHERE {id_column} = $1",
            id_value,
            fetch_type='row'
        )
    except Exception as e:
        logger.error(f"Error fetching data: {str(e)}", exc_info=True)
        return None

def chunk_pdf(blob_client, n_chunks=18):
    logger.info(f"Starting PDF chunking process. Target chunks: {n_chunks}")
    try:
        blob_data = blob_client.download_blob()
        buffer = io.BytesIO()
        blob_data.readinto(buffer)
        buffer.seek(0)
        
        with fitz.open(stream=buffer, filetype="pdf") as pdf:
            num_pages = len(pdf)
            chunk_size = math.ceil(num_pages / n_chunks)
            logger.info(f"PDF has {num_pages} pages. Chunk size: {chunk_size}")
            for start in range(0, num_pages, chunk_size):
                end = min(start + chunk_size, num_pages)
                content = ''
                for page_num in range(start, end):
                    page = pdf[page_num]
                    content += page.get_text() + "\n"
                yield {'start_page': start + 1, 'end_page': end, 'content': content.strip()}

        logger.info("PDF chunking completed successfully.")
    except Exception as e:
        logger.error(f"Error chunking PDF: {str(e)}", exc_info=True)
        yield None

async def fetch_topics():
    logger.info("Fetching topic IDs from the database")
    try:
        query = "SELECT topic_id,topic FROM topic"
        topic_ids = await execute_with_retry(query, fetch_type='all')
        print("***********************************")
        print([row for row in topic_ids])
        return [row for row in topic_ids]
    except Exception as e:
        logger.error(f"Error fetching topic IDs: {str(e)}", exc_info=True)
        return []


async def insert_chunk(book_id, start_page, end_page, is_relevant, chapter_name, content, topic_id, relevance_percentage, usage_count):
    insert_query = """
        INSERT INTO chunk (book_id, startpage, endpage, is_relevant, chaptername, content, topic_id, relevance_percentage, usage_count)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
    """
    try:
        
        await execute_with_retry(insert_query, book_id, start_page, end_page, is_relevant, chapter_name, content, topic_id, relevance_percentage, usage_count)
        logger.info(f"Chunk inserted: {chapter_name} (Pages {start_page} to {end_page}, Topic ID: {topic_id})")
    except Exception as e:
        logger.error(f"Error inserting chunk: {str(e)}", exc_info=True)
        raise

def preprocess_text(text, max_length=700):
    logger.debug(f"Preprocessing text. Initial length: {len(text)}")
    
    # Entfernen von URLs und Sonderzeichen
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'[^a-zA-Z0-9äöüÄÖÜß\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Text in Wörter splitten
    words = text.split()
    total_words = len(words)
    
    # Falls der Text kürzer ist als das Limit, return ihn direkt
    if total_words <= max_length:
        logger.debug(f"Text is already short enough. Length: {total_words}")
        return text
    
    # Verhältnisse anpassen: 10% Anfang, 20% Mitte, 10% Ende
    head_ratio = 0.1
    middle_ratio = 0.2
    tail_ratio = 0.1
    
    head_length = int(max_length * head_ratio)
    tail_length = int(max_length * tail_ratio)
    
    # Berechne den Startpunkt für das Mittelstück
    middle_start = (total_words - max_length) // 2
    middle_length = int(max_length * middle_ratio)
    
    # Text zusammensetzen: Anfang, Mitte und Ende
    processed_text = ' '.join(
        words[:head_length] + 
        words[middle_start:middle_start + middle_length] + 
        words[-tail_length:]
    )
    
    logger.debug(f"Text preprocessing completed. Final length: {len(processed_text)}")
    return processed_text

class TitleAndRelevanceResponse(BaseModel):
    generated_title: str
    is_relevant: bool


async def generate_title_and_check_relevance(original_text):
    try:
        # Kombinierter Prompt für die Titelgenerierung und Relevanzprüfung
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system", "content": "Generate a title for the following  in the same language as the text and check if the text is relevant. The title should be short and concise (maximum 5 words). Relevant text means it does not contain a glossary, table of contents, or any other irrelevant content. Respond with the generated title and 'True' for relevant or 'False' for not relevant"},
                {"role": "user", "content": f"Textabschnitt:\n{original_text}..."}
            ],
            response_format=TitleAndRelevanceResponse,
        )

        # Ausgabe des API-Antworttextes
        print(f"Raw API response for content snippet:")
        print(completion.choices[0].message)

        # Extrahieren des Ergebnisses
        result = completion.choices[0].message.parsed

        print(f"Generated title: {result.generated_title}")
        print(f"Relevance: {result.is_relevant}")

        # Rückgabe des generierten Titels und der Relevanz
        return {
            "generated_title": result.generated_title,
            "is_relevant": result.is_relevant
        }

    except Exception as e:
        print(f"Error processing text: {e}")
        return None
    

async def relevanz_check(chunk):
    # relevanz check logic
    return True

async def check_if_chunks_exist(book_id):
    logger.info(f"Checking if chunks exist for book_id {book_id}.")
    try:
        exists = await execute_with_retry(
            "SELECT EXISTS (SELECT 1 FROM chunk WHERE book_id = $1)",
            book_id,
            fetch_type='value'
        )
        logger.info(f"Chunk existence check for book_id {book_id}: {'found' if exists else 'not found'}.")
        return exists
    except Exception as e:
        logger.error(f"Error checking chunk existence for book_id {book_id}: {str(e)}", exc_info=True)
        return False

async def delete_existing_chunks(book_id):
    logger.info(f"Deleting existing chunks for book_id {book_id}")
    try:
        result = await execute_with_retry("DELETE FROM chunk WHERE book_id = $1", book_id)
        logger.info(f"Deleted {result} existing chunks for book_id {book_id}.")
    except Exception as e:
        logger.error(f"Error deleting chunks for book_id {book_id}: {str(e)}", exc_info=True)

async def process_and_store_chunks(blob_client, book_id):
    logger.info(f"Starting process_and_store_chunks for book_id: {book_id}")
    steps = []
    try:
        steps.append("Initiating chunk processing.")
        chunk_count = 0
        relevant_chunk_count = 0
        
        # Fetch topic IDs at the beginning of the process
        topic_id = 1
        if not topic_id:
            logger.warning("No topic IDs found. Chunks will be inserted without topic assignment.")
        
        for chunk in chunk_pdf(blob_client):
            if chunk is None:
                continue
            content = chunk['content']
            start_page = chunk['start_page']
            end_page = chunk['end_page']
            
            result = await generate_title_and_check_relevance(content)
            chapter_name = result["generated_title"]
            is_relevant = result["is_relevant"]
            # Pass topic_ids to insert_chunk
            await insert_chunk(book_id, start_page, end_page, is_relevant, chapter_name, content, topic_id)
            
            if is_relevant:
                relevant_chunk_count += 1
            
            chunk_count += 1
            if chunk_count % 10 == 0:
                steps.append(f"Processed {chunk_count} chunks. {relevant_chunk_count} relevant chunks identified.")

        logger.info(f"Successfully processed and stored {chunk_count} chunks. {relevant_chunk_count} chunks marked as relevant.")
        steps.append(f"Completed: {chunk_count} chunks processed and stored. {relevant_chunk_count} chunks marked as relevant.")
    except Exception as e:
        logger.error(f"Failed to process and store chunks: {str(e)}", exc_info=True)
        steps.append(f"Error: {str(e)}")
    finally:
        gc.collect()
    return steps


async def init_db_pool():
    global db_pool
    if db_pool is None:
        conn_string = get_db_connection_string(config)
        db_pool = await asyncpg.create_pool(
            conn_string,
            min_size=1,
            max_size=20,  # Adjust based on your needs and database limits
            timeout=500.0
        )
    logger.info("Database connection pool initialized.")

async def close_db_pool():
    global db_pool
    if db_pool:
        await db_pool.close()
        db_pool = None
    logger.info("Database connection pool closed.")

def with_db_pool(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        await init_db_pool()
        try:
            return await func(*args, **kwargs)
        finally:
            await close_db_pool()
    return wrapper

async def execute_with_retry(query, *args, max_retries=3, retry_delay=1, fetch_type=None):
    for attempt in range(max_retries):
        try:
            async with db_pool.acquire() as conn:
                if fetch_type == 'row':
                    return await conn.fetchrow(query, *args)
                elif fetch_type == 'value':
                    return await conn.fetchval(query, *args)
                elif fetch_type == 'all':
                    return await conn.fetch(query, *args)
                else:
                    return await conn.execute(query, *args)
        except asyncpg.exceptions.TooManyConnectionsError:
            if attempt == max_retries - 1:
                raise
            await asyncio.sleep(retry_delay * (2 ** attempt))  # Exponential backoff
        except Exception as e:
            logger.error(f"Error executing query: {query}, args: {args}, error: {str(e)}")
            raise

class TOCAnalysis(BaseModel):
    is_toc_page: bool
    has_chapter_names_with_page_numbers: bool

class PageAnalysisResponse(BaseModel):
    page_number: int
    analysis: TOCAnalysis


async def analyze_page_for_toc(page_content, page_number):
    try:
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system", "content": "Analyze this page for table of contents content. Look for chapter listings WITH their corresponding page numbers. A valid TOC must have both chapter names and their respective page numbers."},
                {"role": "user", "content": f"Page {page_number} content:\n\n{page_content[:1300]}..."}
            ],
            response_format=TOCAnalysis,
        )

        print(f"Raw API response for page {page_number}:")
        print(completion.choices[0].message)

        result = completion.choices[0].message.parsed

        print(f"Processed result for page {page_number}:")
        print(result)

        # Ensure the result has the expected structure
        return {
            "is_toc_page": result.is_toc_page,
            "has_chapter_names_with_page_numbers": result.has_chapter_names_with_page_numbers
        }
        
    except Exception as e:
        logger.error(f"Error on page {page_number}: {e}")
        # Return a default structure in case of an error
        return {
            "is_toc_page": False,
            "has_chapter_names_with_page_numbers": False
        }
 
async def find_toc_in_pdf(pdf_document):
    start_page = None
    end_page = None
    max_pages = min(19, len(pdf_document))
    consecutive_toc_pages = 0
    min_consecutive_pages = 2

    for page_number in range(max_pages):
        page = pdf_document[page_number]
        page_content = page.get_text()
        
        result = await analyze_page_for_toc(page_content, page_number + 1)
        print(f"Analysis result for page {page_number + 1}: {result}")
        
        if result["has_chapter_names_with_page_numbers"]:
            consecutive_toc_pages += 1
            if start_page is None:
                start_page = page_number + 1
            end_page = page_number + 1
        else:
            if consecutive_toc_pages >= min_consecutive_pages:
                break
            else:
                start_page = None
                end_page = None
                consecutive_toc_pages = 0

    has_toc = consecutive_toc_pages >= min_consecutive_pages

    return {
        "has_toc": has_toc,
        "start_page": start_page if has_toc else None,
        "end_page": end_page if has_toc else None
    }


async def extract_text(json_input, pdf_document):
    has_toc = json_input.get('has_toc', False)
    start_page = json_input.get('start_page', 0)
    end_page = json_input.get('end_page', len(pdf_document) - 1)

    if start_page < 0 or end_page >= len(pdf_document) or start_page > end_page:
        raise ValueError("Invalid start or end page.")

    if has_toc:
        start_page -= 1 
    text = ""

    for page_num in range(start_page, end_page + 1):
        page = pdf_document[page_num]
        text += page.get_text() + "\n"

    return text

# Definiere eine Klasse für einzelne Kapitelinformationen
class ChapterInfo(BaseModel):
    chapter: str
    start_page: int

# Definiere die Klasse für strukturierte Antworten, die die Kapitelinformationen verwendet
class TOCContents(BaseModel):
    chapters: list[ChapterInfo]

# Funktion zum Extrahieren des Inhaltsverzeichnisses
async def extract_table_of_contents(text):
    try:
        system_message = (
            "Extract the main chapter names and their starting page numbers from the text."
            "Select approximately 15-30 important chapters, evenly distributed throughout the book. "
            "Each chapter should be meaningful, concise, and listed as 'chapter' (string) and 'start_page' (integer). "
            "Return the result as a structured list with 15 or more items."
            "Ensure that the selected chapters cover the entire span of the book, from beginning to end."
        )

        user_message = text

        completion = client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            response_format=TOCContents
        )

        print("Raw API response:")
        print(completion.choices[0].message)

        result = completion.choices[0].message.parsed

        print("Processed result:")
        print(result)

    except Exception as e:
        print(f"Error: {e}")
        result = TOCContents(chapters=[])

    return result

class ClassificationResult(BaseModel):
    topic_id: int  
    confidence: float 

async def classify_text(text: str, topics: List[Tuple[int, str]]) -> ClassificationResult:
    # Erstelle die Kategorienliste als String
    categories = "\n".join([f"{id}. {topic}" for id, topic in topics])

    # Systemnachricht mit Anweisungen
    system_message = (
        "You are an assistant that classifies texts. "
        "Classify the following text into one of the given categories and return only the ID and the match percentage.\n\n"
        f"Categories:\n{categories}\n\n"
        "Response format: ID,Percentage (where 1 represents 100%)"
    )

    # Benutzernachricht mit dem zu klassifizierenden Text
    user_message = text

    response = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ],
        response_format=ClassificationResult
    )

    result = response.choices[0].message.parsed

    return  {
        "topic_id": result.topic_id,
        "confidence": result.confidence
    }



async def standard_chunking(blob_client, book_id, pdf_document, n_chunks=15):
    logger.info(f"Starting standard chunking process for book_id: {book_id}")
    steps = []
    try:
        num_pages = len(pdf_document)
        chunk_size = math.ceil(num_pages / n_chunks)
        
        logger.info(f"PDF has {num_pages} pages. Chunk size: {chunk_size}")
        steps.append(f"PDF chunking into {n_chunks} chunks.")
        
        # Fetch topic IDs for classification
        topics = await fetch_topics()
        topic_ids = [int(topic[0]) for topic in topics]

        
        for start in range(0, num_pages, chunk_size):
            end = min(start + chunk_size, num_pages)
            content = ''
            for page_num in range(start, end):
                page = pdf_document[page_num]
                content += page.get_text() + "\n"
                content = content.replace('\x00', '')  # Entferne Null-Bytes
                content = content.encode('utf-8', 'replace').decode('utf-8')  # Ersetze ungültige Zeichen mit '?'

            preprocced_text = preprocess_text(content)

                
            # Generate title, classify content
            result = await generate_title_and_check_relevance(preprocced_text)
            chapter_name = result["generated_title"]
            is_relevant = result["is_relevant"]
            classification_result = await classify_text(preprocced_text, topics)
            topic_id = classification_result["topic_id"] if classification_result["topic_id"] in topic_ids else None
            confidence = classification_result["confidence"]
            usage_count = 0
            
            # Insert chunk into the database
            await insert_chunk(book_id, start + 1, end, is_relevant , chapter_name, content, topic_id, confidence, usage_count)
            steps.append(
                                f"➡️Chapter Report [Chapter: {chapter_name}]|"
                                f" Pages: {start + 1} - {end}|"
                                f" Topic ID: {topic_id}|"
                                f" Confidence: {confidence:.2f}|"
                                f" Relevant: {is_relevant}"
                                
                            )
        
    except Exception as e:
        logger.error(f"Error during standard chunking: {str(e)}", exc_info=True)
        steps.append(f"Error during standard chunking: {str(e)}")
    
    return steps


async def intelligent_chunking(blob_client, book_id):
    logger.info(f"Starting intelligent chunking for book_id: {book_id}")
    steps = []
    try:
        steps.append("Initiating intelligent chunking process.")
        logger.debug("Initiating intelligent chunking process.")
        
        # Download PDF content
        logger.info(f"Downloading PDF content for book_id: {book_id}")
        blob_data = blob_client.download_blob()
        pdf_bytes = blob_data.readall()
        logger.debug(f"PDF content downloaded successfully for book_id: {book_id}")
        
        # Open PDF document
        logger.info(f"Opening PDF document for book_id: {book_id}")
        with fitz.open(stream=pdf_bytes, filetype="pdf") as pdf_document:
            logger.debug(f"PDF document opened successfully for book_id: {book_id}")
            
            # Find table of contents
            logger.info("Searching for table of contents")
            toc_info = await find_toc_in_pdf(pdf_document)
            print("***********************************")
            print(toc_info["has_toc"], toc_info["start_page"], toc_info["end_page"])
            
            if toc_info["has_toc"]:
                logger.info(f"Table of contents found from page {toc_info['start_page']} to {toc_info['end_page']}.")
                steps.append(f"Table of contents found from page {toc_info['start_page']} to {toc_info['end_page']}.")
                
                # Extract text from table of contents
                logger.debug("Extracting text from table of contents")
                toc_text = await extract_text(toc_info, pdf_document)
                
                # Extract chapter information
                logger.info("Extracting chapter information from table of contents")
                chapter_info = await extract_table_of_contents(toc_text)
                logger.debug(f"Extracted {len(chapter_info.chapters)} chapters")

                logger.info("Fetching topics for classification")
                topics = await fetch_topics()
                topic_ids = [int(topic[0]) for topic in topics]
                print("TOPIC IDS")
                print(topic_ids)

                logger.debug(f"Fetched {len(topics)} topics for classification")

                # Process each chapter
                for chapter in chapter_info.chapters:
                    chapter_name = chapter.chapter
                    start_page = chapter.start_page - 1  # Adjust for 0-based indexing
                    end_page = len(pdf_document) - 1  # Default to last page of document
                    
                    # Find the end page (start of next chapter or end of document)
                    for next_chapter in chapter_info.chapters:
                        if next_chapter.start_page > start_page + 1:
                            end_page = next_chapter.start_page - 2
                            break
                    
                    logger.info(f"Processing chapter: {chapter_name} (Pages {start_page + 1} to {end_page + 1})")
                    
                    # Extract chapter content
                    logger.debug(f"Extracting content for chapter: {chapter_name}")
                    chapter_content = await extract_text({"start_page": start_page, "end_page": end_page}, pdf_document)
                    
                    logger.info(f"Classifying content for chapter: {chapter_name}")
                    classification_result = await classify_text(preprocess_text(chapter_content), topics)
                    print("***********************************")
                    print(classification_result)
                    topic_id = classification_result["topic_id"] if classification_result["topic_id"] in topic_ids else None
                    confidence = classification_result["confidence"]
                    usage_count = 0

                    logger.info(f"Inserting chunk for chapter: {chapter_name}")
                    # Insert chunk into database
                    await insert_chunk(book_id, start_page + 1, end_page + 1, True, chapter_name, chapter_content, topic_id, confidence, usage_count)
                    
                    steps.append(
                                f"➡️Chapter Report [Chapter: {chapter_name}]|"
                                f" Pages: {start_page} - {end_page}|"
                                f" Topic ID: {topic_id}|"
                                f" Confidence: {confidence:.2f}|"
                                
                            )


                    logger.debug(f"Processed and stored chapter: {chapter_name}")
            else:
                logger.warning("No table of contents found. Falling back to old chunking logic.")
                steps.append("No table of contents found. Falling back to old chunking logic.")
                steps.extend(await standard_chunking(blob_client, book_id, pdf_document))
        
        logger.info(f"Intelligent chunking completed successfully for book_id {book_id}")
        steps.append("Intelligent chunking process completed.")
        
    except Exception as e:
        logger.error(f"Error during intelligent chunking for book_id {book_id}: {str(e)}", exc_info=True)
        steps.append(f"Error during intelligent chunking: {str(e)}")
    
    return steps

@with_db_pool
async def main(req: HttpRequest) -> HttpResponse:
    global client
    correlation_id = str(uuid.uuid4())
    start_time = time.time()
    logger.info(f"Starting request processing. Correlation ID: {correlation_id}")

    cors_headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization'
    }

    if req.method == 'OPTIONS':
        return HttpResponse(status_code=200, headers=cors_headers)

    book_id = req.params.get('book_id')
    
    if not book_id:
        try:
            req_body = req.get_json()
            book_id = req_body.get('book_id')
        except ValueError:
            logger.error("Failed to parse request body")
    
    if not book_id:
        logger.error("No book_id provided")
        return HttpResponse(
            json.dumps({"error": "Please provide a book_id in the query string or request body"}),
            status_code=400,
            mimetype="application/json",
            headers=cors_headers
        )
    
    try:
        book_id = int(book_id)
    except ValueError:
        logger.error(f"Invalid book_id: {book_id}")
        return HttpResponse(
            json.dumps({"error": "Invalid book_id. Must be an integer."}),
            status_code=400,
            mimetype="application/json",
            headers=cors_headers
        )

    try:
        client = setup_openai_client()

        
        azure_blob = await fetch_data_by_id_as_json("book", id_value=book_id)
        if azure_blob:
            book_data = dict(azure_blob)
            book_url = book_data["url"]
            
            steps = []
            
            blob_service_client = BlobServiceClient.from_connection_string(config["azure_storage_connection_string"])
            blob_client = blob_service_client.get_blob_client(container=config["azure_container_name"], blob=book_url)
            
            overwrite_existing = os.getenv('OVERWRITE_EXISTING', 'False').lower() == 'true'
            
            if await check_if_chunks_exist(book_id):
                if overwrite_existing:
                    logger.info(f"Existing chunks found for book_id {book_id}. Overwriting as requested.")
                    steps.append("Existing chunks found. Initiating overwrite process.")
                    await delete_existing_chunks(book_id)
                    steps.append("Existing chunks deleted successfully.")
                    steps.extend(await intelligent_chunking(blob_client, book_id))
                else:
                    logger.info(f"Chunks already exist for book_id {book_id}. Skipping generation as overwrite is set to False.")
                    steps.append("Existing chunks found. Skipping generation due to overwrite settings.")
            else:
                logger.info(f"No existing chunks found for book_id {book_id}. Initiating intelligent chunk generation.")
                steps.append("No existing chunks found. Starting intelligent chunk generation process.")
                steps.extend(await intelligent_chunking(blob_client, book_id))
            
            logger.info(f"Processing completed successfully for book_id {book_id}")

            process = psutil.Process(os.getpid())
            memory_info = process.memory_info()
            ram_usage = memory_info.rss / 1024 / 1024  # Convert to MB
            logger.info(f"RAM usage at the end of processing: {ram_usage:.2f} MB")

            end_time = time.time()
            execution_time = end_time - start_time

            return HttpResponse(
                json.dumps({
                    "message": f"PDF processing completed successfully for book_id {book_id}",
                    "status": "success",
                    "book_id": book_id,
                    "steps": steps,
                    "correlation_id": correlation_id,
                    "ram_usage_mb": round(ram_usage, 2),
                    "execution_time_seconds": round(execution_time, 2)
                }),
                status_code=200,
                mimetype="application/json",
                headers=cors_headers
            )
        else:
            logger.error("Failed to retrieve book data from the database.")
            return HttpResponse(
                json.dumps({
                    "error": "Unable to retrieve book data from the database.",
                    "status": "error",
                    "book_id": book_id,
                    "correlation_id": correlation_id
                }),
                status_code=500,
                mimetype="application/json",
                headers=cors_headers
            )
    except Exception as e:
        logger.error(f"Unhandled exception in main function: {str(e)}", exc_info=True)
        return HttpResponse(
            json.dumps({
                "error": f"An unexpected error occurred during processing: {str(e)}",
                "status": "error",
                "book_id": book_id,
                "correlation_id": correlation_id
            }),
            status_code=500,
            mimetype="application/json",
            headers=cors_headers
        )
    finally:
        gc.collect()
        
# Azure Functions entry point
async def azure_function_handler(req: HttpRequest) -> HttpResponse:
    return await main(req)