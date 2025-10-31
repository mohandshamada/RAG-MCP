#!/usr/bin/env python3
"""
Main entry point for the RAG MCP Server
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

def main():
    """Start the MCP server"""
    try:
        from src.rag_server import mcp

        print("Starting RAG MCP Server...")
        print("Server is ready to accept connections via MCP protocol.")

        # Run the MCP server
        mcp.run()

    except KeyboardInterrupt:
        print("\nServer stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"Error starting server: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
