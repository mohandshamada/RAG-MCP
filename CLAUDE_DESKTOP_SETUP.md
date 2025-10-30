# Claude Desktop Configuration Guide

## Quick Setup (2 minutes)

### 1. Get the Full Path

Navigate to your installation folder and copy the full path:

**Windows PowerShell:**
```powershell
cd path\to\pdf_rag_mcp_server
pwd
# Copy the path that appears
```

**Mac/Linux Terminal:**
```bash
cd path/to/pdf_rag_mcp_server
pwd
# Copy the path that appears
```

### 2. Edit Claude Desktop Config

**Windows:**
1. Open: `%APPDATA%\Claude\claude_desktop_config.json`
2. (Or: `C:\Users\[YourUsername]\AppData\Roaming\Claude\claude_desktop_config.json`)

**Mac:**
1. Open: `~/.config/Claude/claude_desktop_config.json`

**Linux:**
1. Open: `~/.config/Claude/claude_desktop_config.json`

### 3. Update the Configuration

Replace `/path/to/pdf_rag_mcp_server` with your actual path from step 1:

```json
{
  "mcpServers": {
    "rag-multi-format-server": {
      "command": "python",
      "args": [
        "/full/path/to/pdf_rag_mcp_server/src/rag_server.py"
      ],
      "env": {
        "PYTHONPATH": "/full/path/to/pdf_rag_mcp_server"
      }
    }
  }
}
```

**Example (Windows):**
```json
{
  "mcpServers": {
    "rag-multi-format-server": {
      "command": "python",
      "args": [
        "C:\\Users\\YourName\\Projects\\pdf_rag_mcp_server\\src\\rag_server.py"
      ],
      "env": {
        "PYTHONPATH": "C:\\Users\\YourName\\Projects\\pdf_rag_mcp_server"
      }
    }
  }
}
```

**Example (Mac/Linux):**
```json
{
  "mcpServers": {
    "rag-multi-format-server": {
      "command": "python",
      "args": [
        "/Users/username/projects/pdf_rag_mcp_server/src/rag_server.py"
      ],
      "env": {
        "PYTHONPATH": "/Users/username/projects/pdf_rag_mcp_server"
      }
    }
  }
}
```

### 4. Restart Claude Desktop

1. Fully close Claude Desktop
2. Reopen Claude Desktop
3. The MCP server should initialize automatically

## Verification

Once restarted, you should see the MCP tools available in Claude:

- `ingest_document` - Add documents to the system
- `rag_query` - Query documents with natural language
- `compare_document_to_specification` - Check compliance
- `generate_compliance_report` - Create detailed reports
- And more...

Try in Claude:
> "Please ingest this PDF and tell me what it's about"

## Troubleshooting

**"No tools available" or "Cannot find module"**
- Verify the path is correct in the config
- Run `python setup.py` to ensure dependencies are installed
- Check that Python is in your PATH: `python --version`

**"Permission denied" or "File not found"**
- Make sure you used the full absolute path, not a relative path
- On Windows, use forward slashes or escaped backslashes: `C:\\Users\\...`

**"Connection refused"**
- Make sure the previous Claude process is fully closed
- Try restarting your computer if issues persist

**Slow to start**
- First startup downloads the embedding model (~80 MB)
- Subsequent starts are much faster

## Features Available in Claude

Once connected, you can use these commands naturally:

```
"Analyze this PDF for compliance with our standards"
"Compare these three proposals against our RFP requirements"
"Extract all the requirements from this document"
"Generate a compliance report in HTML format"
"Search for security requirements across all documents"
```

## Need Help?

- Check `CONFIG.md` for detailed configuration options
- See `EXAMPLES.md` for code samples and workflows
- Run `python verify_installation.py` for diagnostics
- Check `README.md` for quick start guide
