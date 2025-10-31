# Multi-stage build for optimized image size with UV
# Stage 1: Builder
FROM python:3.12-slim AS builder

WORKDIR /app

# Install system dependencies needed for building
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install UV - the fast Python package manager
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files
COPY pyproject.toml ./

# Install dependencies with UV (much faster than pip)
RUN uv pip install --system --no-cache -r pyproject.toml

# Stage 2: Runtime
FROM python:3.12-slim

WORKDIR /app

# Install only runtime dependencies (OCR)
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# Copy all site-packages from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DATA_DIR=/app/data \
    LOG_DIR=/app/logs \
    PYTHONPATH=/app

# Copy application code
COPY src /app/src
COPY config /app/config
COPY client.py /app/
COPY pyproject.toml /app/

# Create necessary directories for runtime data
RUN mkdir -p /app/data/vector_stores \
    && mkdir -p /app/data/document_cache \
    && mkdir -p /app/data/metadata \
    && mkdir -p /app/logs \
    && chmod -R 755 /app/data /app/logs

# Health check - verify Python can import the main modules
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "from src.rag_server import mcp; print('healthy')" || exit 1

# Expose port for MCP server
EXPOSE 8000

# Default command - run the MCP server
CMD ["python", "-m", "src.rag_server"]
