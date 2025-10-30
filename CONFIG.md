# RAG MCP Server - Complete Setup & Usage Guide

## Overview

The RAG Multi-Format Document Server is a Model Context Protocol (MCP) server that enables:

- **Document Ingestion**: PDFs, Excel, Word, Images (with OCR)
- **Semantic Search**: RAG-based querying with FAISS vector store
- **Compliance Checking**: Compare documents against specifications
- **Multi-Document Analysis**: Query and compare multiple documents simultaneously
- **Report Generation**: Text, JSON, and HTML compliance reports

## Architecture

```
┌─────────────────────────────────────────┐
│     Claude Desktop / MCP Client         │
└────────────────┬────────────────────────┘
                 │
         ┌───────▼────────┐
         │  MCP Server    │
         │ (FastMCP)      │
         └───────┬────────┘
                 │
    ┌────────────┼────────────┐
    │            │            │
    ▼            ▼            ▼
┌────────┐ ┌──────────┐ ┌────────────┐
│ RAG    │ │Document  │ │ Comparison │
│Engine  │ │Processor │ │   Engine   │
└────────┘ └──────────┘ └────────────┘
    │            │            │
    └────────────┼────────────┘
                 │
    ┌────────────┴────────────┐
    │                         │
    ▼                         ▼
┌──────────────┐    ┌──────────────────┐
│ FAISS Index  │    │ File System      │
│ (Vector DB)  │    │ (Cache/Metadata) │
└──────────────┘    └──────────────────┘
```

## Installation

### Prerequisites

- Python 3.9+
- pip
- For OCR: Tesseract OCR (Windows/Mac/Linux)

### Setup Steps

1. **Navigate to project directory**:
```bash
cd C:\Users\engmo\Claude_Project\pdf_rag_mcp_server
```

2. **Install dependencies**:
```bash
python setup.py
```

This will:
- Install all Python packages
- Download the embedding model (all-MiniLM-L6-v2)
- Create necessary directories
- Install system dependencies (Tesseract on Windows/Mac/Linux)

3. **Verify installation**:
```bash
python -m pip list | grep -E "mcp|faiss|langchain"
```

### Windows Tesseract Setup

If OCR doesn't work automatically:

1. Download installer: https://github.com/UB-Mannheim/tesseract/wiki
2. Install to default location
3. Update `config/config.py`:
```python
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

## Configuration

Edit `config/config.py` for:

- **Embedding Model**: Change from `all-MiniLM-L6-v2` to other sentence-transformers
- **Chunk Size**: Adjust text splitting (default: 1000 chars)
- **Top-K Results**: Number of similar chunks to retrieve
- **File Size Limits**: Modify `MAX_FILE_SIZE_MB`
- **Vector Store Location**: Change data directory paths

## Usage

### Option 1: Claude Desktop Integration

1. Add to Claude Desktop config:
   - **Mac**: `~/.config/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
   - **Linux**: `~/.config/Claude/claude_desktop_config.json`

2. Copy content from `claude_desktop_config.json` in this project

3. Restart Claude Desktop

4. Use in Claude by referencing the tools:
   - `ingest_document`
   - `rag_query`
   - `compare_document_to_specification`
   - etc.

### Option 2: CLI Client

Use `client.py` for command-line access:

```bash
python client.py --help
```

#### Common Commands

**Ingest a document**:
```bash
python client.py ingest /path/to/document.pdf -n my_document
```

**Query a document**:
```bash
python client.py query my_document "What are the main requirements?"
```

**Query multiple documents**:
```bash
python client.py batch doc1 doc2 doc3 "Common topic to search"
```

**Compare to specification**:
```bash
python client.py compare my_document specification.txt
```

**Generate compliance report**:
```bash
python client.py report my_document specification.txt --format html
```

**List all indexed documents**:
```bash
python client.py list
```

**Get document summary**:
```bash
python client.py summary my_document
```

**Delete document index**:
```bash
python client.py delete my_document
```

### Option 3: Direct Python Import

```python
from src.rag_server import ingest_document, rag_query, compare_document_to_specification

# Ingest a document
result = ingest_document("/path/to/file.pdf", "my_document")

# Query it
results = rag_query("my_document", "What is X?", top_k=5)

# Compare to specification
spec = ["Requirement 1", "Requirement 2", "Requirement 3"]
comparison = compare_document_to_specification("my_document", spec)
```

## Available MCP Tools

### Document Management

#### `ingest_document(file_path, document_name)`
- Ingest and process documents
- Supports: PDF, Excel, Word, PNG, JPG, GIF, BMP, TIFF
- Creates FAISS index and metadata
- **Returns**: Ingestion status with chunk count

#### `list_indexed_documents()`
- List all indexed documents with metadata
- **Returns**: Dictionary of documents with stats

#### `get_document_summary(document_name)`
- Get metadata and statistics for a document
- **Returns**: File type, chunks, content length, etc.

#### `delete_document_index(document_name)`
- Delete document index and metadata
- **Returns**: Deletion confirmation

### Querying & Search

#### `rag_query(document_name, query, top_k=5)`
- Query single document using RAG
- **Returns**: Retrieved chunks with similarity scores

#### `rag_batch_query(document_names, query, top_k=3)`
- Query multiple documents simultaneously
- **Returns**: Results from all documents

#### `extract_tables_from_document(document_name)`
- Extract all tables from a document
- **Returns**: Structured table data

#### `extract_images_from_document(document_name)`
- Get OCR data from images in documents
- **Returns**: OCR extracted text and metadata

### Comparison & Compliance

#### `compare_document_to_specification(document_name, specifications, spec_name, threshold=0.7)`
- Compare document against requirements
- Specification: List of requirement strings
- **Returns**: Compliance percentage, item-by-item status

#### `compare_multiple_documents_to_spec(document_names, specifications, spec_name)`
- Compare multiple documents to same specification
- **Returns**: Comparative compliance results

#### `generate_compliance_report(document_name, specifications, spec_name, format)`
- Generate detailed compliance report
- **Format**: 'text', 'json', or 'html'
- **Returns**: Formatted report string

#### `generate_rag_report(document_name, queries)`
- Generate multi-query report
- **Returns**: Results for multiple queries

## Specification Format

Specifications can be provided as:

### As a List (CLI/API):
```python
[
    "The document must include a title page",
    "Must contain at least 3 chapters",
    "All claims must be cited",
    "Document must include references"
]
```

### As JSON File:
```json
{
    "requirements": [
        {
            "id": "REQ_001",
            "text": "The document must include a title page",
            "expected": "Yes"
        },
        {
            "id": "REQ_002",
            "text": "Must contain at least 3 chapters",
            "expected": ">= 3"
        }
    ]
}
```

### As Plain Text File:
```
Each line is a requirement
The document must include a title page
Must contain at least 3 chapters
All claims must be cited
Document must include references
```

## Example Workflows

### Workflow 1: Simple Document Ingestion & Query

```bash
# Ingest a PDF
python client.py ingest contract.pdf -n legal_contract

# Query it
python client.py query legal_contract "What are the payment terms?"
```

### Workflow 2: Compliance Checking

```bash
# Create specification file (spec.txt)
# Each line is a requirement

# Compare document to specification
python client.py compare legal_contract spec.txt -n "Legal Requirements"

# Generate detailed report
python client.py report legal_contract spec.txt -n "Legal Requirements" --format html
```

### Workflow 3: Multi-Document Comparison

```bash
# Ingest multiple vendor proposals
python client.py ingest proposal1.pdf -n vendor_a
python client.py ingest proposal2.pdf -n vendor_b
python client.py ingest proposal3.pdf -n vendor_c

# Compare all to RFP specification
python client.py compare-all rfp_requirements.txt -n "RFP Compliance"
```

### Workflow 4: Detailed Analysis with Claude

1. Add MCP server to Claude Desktop
2. In Claude, use the tools to:
   - Ingest documents
   - Query for specific information
   - Generate compliance reports
   - Compare multiple submissions
3. Claude synthesizes findings into analysis

## Performance Tuning

### For Large Documents

```python
# In config/config.py
CHUNK_SIZE = 2000        # Larger chunks
CHUNK_OVERLAP = 400      # More context
TOP_K_DEFAULT = 10       # More results
```

### For Fast Queries

```python
# In config/config.py
CHUNK_SIZE = 500         # Smaller chunks
CHUNK_OVERLAP = 100      # Less overlap
TOP_K_DEFAULT = 3        # Fewer results
```

### Memory Optimization

```python
# Limit vector store size
MAX_FILE_SIZE_MB = 200
CACHE_SIZE_MB = 500
```

## Troubleshooting

### "Module not found" errors

```bash
# Reinstall dependencies
python -m pip install -r requirements.txt --force-reinstall
```

### FAISS index errors

```bash
# Rebuild FAISS
python -m pip install --upgrade faiss-cpu
# Or for GPU:
python -m pip install --upgrade faiss-gpu
```

### OCR not working

1. Verify Tesseract installation
2. Check `TESSERACT_PATH` in `config/config.py`
3. On Windows, ensure installed to Program Files
4. On Mac/Linux, verify via: `which tesseract`

### Memory issues with large files

- Reduce `CHUNK_SIZE` in config
- Increase `NUM_WORKERS` for parallel processing
- Split large documents before ingestion

## File Structure

```
pdf_rag_mcp_server/
├── src/
│   ├── rag_server.py              # Main MCP server
│   ├── comparison_engine.py       # Comparison logic
│   └── __init__.py
├── config/
│   └── config.py                  # Configuration settings
├── data/
│   ├── vector_stores/             # FAISS indices
│   ├── document_cache/            # Processed documents
│   └── metadata/                  # Document metadata
├── logs/                          # Server logs
├── client.py                      # CLI client
├── setup.py                       # Installation script
├── requirements.txt               # Python dependencies
├── claude_desktop_config.json     # MCP config for Claude
└── CONFIG.md                      # This file
```

## Advanced Features

### Custom Embedding Model

Change in `get_embeddings()`:
```python
from langchain_community.embeddings import HuggingFaceEmbeddings
embeddings = HuggingFaceEmbeddings(model_name="all-mpnet-base-v2")
```

### Add Custom File Type Support

1. Create extraction function:
```python
def extract_custom_content(file_path):
    # Your extraction logic
    return {"text": content, "metadata": {...}}
```

2. Register in `detect_file_type()` and `ingest_document()`

### Custom Comparison Logic

Subclass `ComparisonEngine`:
```python
class CustomComparison(ComparisonEngine):
    def _check_requirement(self, document_name, requirement, threshold):
        # Custom logic here
        pass
```

## Support & Next Steps

- Check logs in `logs/` directory for detailed error messages
- Review comparison results in generated reports
- Adjust `threshold` parameter based on your needs
- Start with small documents for testing

## License

This project uses open-source libraries. See requirements.txt for dependencies.
