# RAG MCP Server Configuration

# Server Settings
SERVER_NAME = "RAG Multi-Format Document Server"
SERVER_VERSION = "1.0.0"
LOG_LEVEL = "INFO"

# Embedding Model
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
EMBEDDING_DIM = 384

# Vector Store Settings
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
TOP_K_DEFAULT = 5

# File Processing
MAX_FILE_SIZE_MB = 500
SUPPORTED_FORMATS = ["pdf", "xlsx", "xls", "docx", "doc", "png", "jpg", "jpeg", "bmp", "gif", "tiff"]

# OCR Settings
ENABLE_OCR = True
OCR_LANGUAGE = "eng"
# For Windows, set this path to your Tesseract installation:
# TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Database Paths (relative to project root)
VECTOR_STORE_DIR = "data/vector_stores"
DOCUMENT_CACHE_DIR = "data/document_cache"
METADATA_DIR = "data/metadata"
LOG_DIR = "logs"

# Performance Settings
NUM_WORKERS = 4
CACHE_SIZE_MB = 1000

# Development Settings
DEBUG_MODE = False
SAVE_INTERMEDIATE_RESULTS = True
