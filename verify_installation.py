#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RAG MCP Server - Verification Script
Tests all major components to ensure proper installation
"""

import sys
import os
from pathlib import Path
import subprocess

# Fix Windows console encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

def check_python_version():
    """Verify Python version >= 3.9"""
    print("Checking Python version...", end=" ")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 9:
        print(f"✓ ({version.major}.{version.minor}.{version.micro})")
        return True
    else:
        print(f"✗ (Found {version.major}.{version.minor}, need >= 3.9)")
        return False


def check_dependencies():
    """Verify all required packages are installed"""
    print("\nChecking Python dependencies...")
    
    packages = {
        'mcp': 'Model Context Protocol',
        'PyPDF2': 'PDF Processing',
        'langchain': 'Language Chain',
        'faiss': 'FAISS Vector Store',
        'sentence_transformers': 'Embeddings',
        'openpyxl': 'Excel Support',
        'docx': 'Word Document Support',
        'PIL': 'Image Support',
    }
    
    all_good = True
    for module, description in packages.items():
        try:
            __import__(module)
            print(f"  ✓ {module:20} ({description})")
        except ImportError:
            print(f"  ✗ {module:20} ({description}) - MISSING")
            all_good = False
    
    return all_good


def check_directories():
    """Verify required directories exist"""
    print("\nChecking directory structure...")
    
    required_dirs = [
        "src",
        "config",
        "data",
        "data/vector_stores",
        "data/document_cache",
        "data/metadata",
        "logs",
        "examples"
    ]
    
    base_dir = Path(__file__).parent
    all_good = True
    
    for dir_name in required_dirs:
        dir_path = base_dir / dir_name
        if dir_path.exists() and dir_path.is_dir():
            print(f"  ✓ {dir_name}")
        else:
            print(f"  ✗ {dir_name} - MISSING")
            all_good = False
    
    return all_good


def check_files():
    """Verify required files exist"""
    print("\nChecking required files...")
    
    required_files = [
        "src/rag_server.py",
        "src/comparison_engine.py",
        "config/config.py",
        "requirements.txt",
        "setup.py",
        "client.py",
        "CONFIG.md",
        "README.md",
        "EXAMPLES.md",
        "claude_desktop_config.json",
    ]
    
    base_dir = Path(__file__).parent
    all_good = True
    
    for file_name in required_files:
        file_path = base_dir / file_name
        if file_path.exists() and file_path.is_file():
            print(f"  ✓ {file_name}")
        else:
            print(f"  ✗ {file_name} - MISSING")
            all_good = False
    
    return all_good


def check_rag_server():
    """Verify RAG server can be imported"""
    print("\nTesting RAG server import...", end=" ")
    try:
        from src.rag_server import (
            ingest_document, rag_query, 
            compare_document_to_specification,
            list_indexed_documents
        )
        print("✓")
        return True
    except Exception as e:
        print(f"✗\n  Error: {e}")
        return False


def check_comparison_engine():
    """Verify comparison engine works"""
    print("Testing comparison engine...", end=" ")
    try:
        from src.comparison_engine import ComparisonEngine
        print("✓")
        return True
    except Exception as e:
        print(f"✗\n  Error: {e}")
        return False


def check_embeddings():
    """Verify embeddings model can be loaded"""
    print("Testing embeddings model...", end=" ")
    try:
        from src.rag_server import get_embeddings
        embeddings = get_embeddings()
        print("✓")
        return True
    except Exception as e:
        print(f"✗\n  Error: {e}")
        print("  Note: Model will be downloaded on first use")
        return False


def check_tesseract():
    """Check if Tesseract OCR is installed"""
    print("\nChecking Tesseract OCR...", end=" ")
    try:
        import pytesseract
        from PIL import Image
        # Try to get tesseract version
        result = subprocess.run(
            ['tesseract', '--version'],
            capture_output=True,
            timeout=5
        )
        if result.returncode == 0:
            print("✓")
            return True
        else:
            print("⚠ (Not found in PATH)")
            return False
    except Exception as e:
        print(f"⚠ (Not installed)")
        print("  Note: OCR optional - install Tesseract separately if needed")
        return False


def check_cli_client():
    """Verify CLI client works"""
    print("\nTesting CLI client...", end=" ")
    try:
        result = subprocess.run(
            [sys.executable, "client.py", "--help"],
            capture_output=True,
            timeout=5,
            cwd=Path(__file__).parent
        )
        if result.returncode == 0:
            print("✓")
            return True
        else:
            print("✗")
            return False
    except Exception as e:
        print(f"✗\n  Error: {e}")
        return False


def generate_report(results):
    """Generate verification report"""
    print("\n" + "="*60)
    print("VERIFICATION REPORT")
    print("="*60)
    
    total = len(results)
    passed = sum(1 for r in results.values() if r)
    
    print(f"\nResults: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n✓ All checks passed! System is ready to use.")
        print("\nNext steps:")
        print("  1. Review CONFIG.md for configuration options")
        print("  2. Try the CLI client: python client.py --help")
        print("  3. Test with sample documents in examples/")
        print("  4. Integrate with Claude Desktop (see CONFIG.md)")
        return True
    else:
        print("\n⚠ Some checks failed. Please fix issues above.")
        print("\nCommon solutions:")
        print("  - Run: python setup.py")
        print("  - Or: pip install -r requirements.txt --force-reinstall")
        return False


def main():
    print("""
╔════════════════════════════════════════════════════════════╗
║     RAG MCP Server - Verification Script                   ║
╚════════════════════════════════════════════════════════════╝
    """)
    
    results = {}
    
    # Run all checks
    results["Python Version"] = check_python_version()
    results["Dependencies"] = check_dependencies()
    results["Directories"] = check_directories()
    results["Files"] = check_files()
    results["RAG Server"] = check_rag_server()
    results["Comparison Engine"] = check_comparison_engine()
    results["Embeddings Model"] = check_embeddings()
    results["Tesseract OCR"] = check_tesseract()
    results["CLI Client"] = check_cli_client()
    
    # Generate report
    success = generate_report(results)
    
    print("\n" + "="*60)
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
