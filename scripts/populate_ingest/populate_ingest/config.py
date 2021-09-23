import os

INGEST_API_HOST = 'http://localhost'
INGEST_API_PORT = '8080'
INGEST_API_URL = os.path.expandvars(os.environ.get('INGEST_API_URL', INGEST_API_HOST + ':' + INGEST_API_PORT))