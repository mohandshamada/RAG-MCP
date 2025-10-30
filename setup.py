#!/usr/bin/env python
"""
Setup script for RAG MCP Server
Installs dependencies and configures system
"""

import subprocess
import sys
import platform
import os
from pathlib import Path

def run_command(cmd, description=""):
    """Run a command and report status"""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"{'='*60}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"⚠️  Warning: {description} may have failed")
    return result.returncode == 0

def main():
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║         RAG MCP Server Setup                              ║
    ║    Multi-format Document Processing                        ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    # Get OS
    os_name = platform.system()
    print(f"Detected OS: {os_name}")
    
    # Step 1: Install Python dependencies
    print("\n[1/4] Installing Python dependencies...")
    run_command(
        f"{sys.executable} -m pip install --upgrade pip",
        "Upgrading pip"
    )
    run_command(
        f"{sys.executable} -m pip install -r requirements.txt",
        "Installing package dependencies"
    )
    
    # Step 2: Install system dependencies based on OS
    print("\n[2/4] Installing system dependencies...")
    
    if os_name == "Windows":
        print("Windows detected. Installing Tesseract OCR...")
        # Tesseract installation instructions for Windows
        print("""
        ℹ️  To enable OCR, download and install Tesseract:
        1. Download: https://github.com/UB-Mannheim/tesseract/wiki
        2. Run installer with default settings
        3. After installation, update pytesseract path in config
        """)
    
    elif os_name == "Darwin":  # macOS
        print("macOS detected. Installing Tesseract via Homebrew...")
        run_command("brew install tesseract", "Installing Tesseract")
    
    elif os_name == "Linux":
        print("Linux detected. Installing Tesseract...")
        run_command("sudo apt-get update", "Updating package lists")
        run_command("sudo apt-get install -y tesseract-ocr", "Installing Tesseract")
    
    # Step 3: Create directories
    print("\n[3/4] Creating data directories...")
    base_dir = Path(__file__).parent
    dirs = [
        base_dir / "data" / "vector_stores",
        base_dir / "data" / "document_cache",
        base_dir / "data" / "metadata",
        base_dir / "logs"
    ]
    
    for dir_path in dirs:
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"✓ Created: {dir_path}")
    
    # Step 4: Download embedding model
    print("\n[4/4] Downloading embedding model...")
    try:
        from langchain_community.embeddings import HuggingFaceEmbeddings
        print("Downloading all-MiniLM-L6-v2 model (~80 MB)...")
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        print("✓ Embedding model downloaded successfully")
    except Exception as e:
        print(f"⚠️  Could not download embedding model: {e}")
        print("Note: Model will be downloaded on first use")
    
    # Summary
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║           Setup Complete!                                 ║
    ╚════════════════════════════════════════════════════════════╝
    
    Next steps:
    1. Configure Claude Desktop (see CONFIG.md)
    2. Start the server: python src/rag_server.py
    3. Begin indexing documents
    
    Features:
    ✓ PDF processing
    ✓ Excel/Word support
    ✓ OCR for images
    ✓ Table extraction
    ✓ RAG-based querying
    ✓ Multi-document search
    """)

if __name__ == "__main__":
    main()
