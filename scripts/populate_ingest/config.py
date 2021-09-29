# --- core imports
import os

# --- third party library imports
from dotenv import load_dotenv

load_dotenv()

INGEST_API_HOST = 'http://localhost'
INGEST_API_PORT = '8080'
INGEST_API_URL = os.getenv('INGEST_API_URL', INGEST_API_HOST + ':' + INGEST_API_PORT)
INGEST_API_TOKEN = os.getenv('INGEST_API_TOKEN')
