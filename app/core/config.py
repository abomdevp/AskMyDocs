from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
PDF_DIR = DATA_DIR / "pdfs"
CHROMA_DIR = DATA_DIR / "chroma"

APP_NAME = "RAG PDF API"
APP_VERSION = "0.3.0"

CHROMA_COLLECTION_NAME = "pdf_chunks"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
OLLAMA_MODEL_NAME = "llama3.2"
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

DEFAULT_N_RESULTS = 3
CHUNK_SIZE = 800
CHUNK_OVERLAP = 150