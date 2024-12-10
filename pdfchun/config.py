import os
from dotenv import load_dotenv

load_dotenv()

def get_config():
    print("PDF_FILE_PATH from .env:", os.getenv("PDF_PATH"))  # Debugging output
    print("DB_HOST from .env:", os.getenv("DB_HOST"))  # Debugging output

    return {
        "pdf_path": os.getenv("PDF_PATH"),
        "db_host": os.getenv("DB_HOST"),
        "db_name": os.getenv("DB_NAME"),
        "db_user": os.getenv("DB_USER"),
        "db_password": os.getenv("DB_PASSWORD"),
        "db_port": os.getenv("DB_PORT"),
        "sslmode": os.getenv("DB_SSLMODE"),
        "azure_storage_connection_string": os.getenv("AZURE_STORAGE_CONNECTION_STRING"),
        "azure_container_name": os.getenv("AZURE_CONTAINER_NAME"),
        "azure_blob_name": os.getenv("AZURE_BLOB_NAME"),
        "overwrite_existing": os.getenv("OVERWRITE_EXISTING"),
        "key_vault_name": os.getenv("KEY_VAULT_NAME"),
        "key_secret_name": os.getenv("KEY_SECRET_NAME"),
        "endpoint_secret_name": os.getenv("ENDPOINT_SECRET_NAME")
    }
