# 🚀 RAG MCP Server - START HERE

Welcome! Your MCP server for document processing and compliance checking is ready.

## In 2 Minutes

### 1️⃣ Verify Installation
```bash
python verify_installation.py
```
This checks all dependencies and confirms everything is set up correctly.

### 2️⃣ Try the CLI Client
```bash
# List example files
python client.py list

# Or test with your own PDF
python client.py ingest your_document.pdf -n my_doc
python client.py query my_doc "What is the main topic?"
```

### 3️⃣ Try Comparison
Create a file `my_spec.txt`:
```
The document must have a clear title
It should include an introduction
Must contain analysis and findings
Should have a conclusion
```

Then:
```bash
python client.py compare my_doc my_spec.txt
```

## What You Have

| File | Purpose |
|------|---------|
| **README.md** | Quick start guide |
| **CONFIG.md** | Complete documentation |
| **EXAMPLES.md** | Code examples & workflows |
| **BUILD_SUMMARY.md** | Architecture overview |
| **client.py** | Command-line interface |
| **verify_installation.py** | System checker |
| **examples/** | Sample specs and configs |

## Main Features

✅ **Ingest Documents** - PDF, Word, Excel, Images with OCR
✅ **Semantic Search** - Query documents with natural language
✅ **Compliance Checking** - Compare documents against specifications
✅ **Report Generation** - Text, JSON, or HTML output
✅ **Multi-Document** - Analyze and compare multiple files

## Common Tasks

### Process a Document
```bash
python client.py ingest document.pdf -n doc_name
```

### Search a Document
```bash
python client.py query doc_name "What are the key points?"
```

### Check Compliance
```bash
python client.py compare doc_name requirements.txt
```

### Generate Report
```bash
python client.py report doc_name requirements.txt --format html
```

### Compare Multiple Documents
```bash
# All indexed documents vs same spec
python client.py compare-all requirements.txt
```

## With Claude Desktop

1. Open Claude Desktop config:
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
   - **Mac**: `~/.config/Claude/claude_desktop_config.json`

2. Paste content from `claude_desktop_config.json`

3. Update path to match your installation

4. Restart Claude

5. Use in conversation:
   > "Can you analyze this proposal and check it against our requirements?"

Claude will use the MCP tools automatically!

## Troubleshooting

**"Module not found"**
```bash
python setup.py
```

**"File not found"**
- Use absolute paths for files
- Check file exists: `dir document.pdf`

**"Need help?"**
- Read `CONFIG.md` for detailed docs
- Check `EXAMPLES.md` for code samples
- Run `python client.py --help` for commands

## Architecture

```
Your Documents → PDF/Word/Excel Parser
                      ↓
              Text Extraction & Chunking
                      ↓
              Embedding & Vector Store (FAISS)
                      ↓
          Semantic Search & Comparison Engine
                      ↓
        Text/JSON/HTML Reports & Analysis
```

## Next Steps

1. ✅ Run `verify_installation.py`
2. ✅ Try `client.py list` 
3. ✅ Read `README.md` for examples
4. ✅ Check `CONFIG.md` for advanced options
5. → Integrate with Claude Desktop
6. → Create custom workflows

## Example Workflow

**Vendor Proposal Evaluation:**

```bash
# 1. Ingest proposals
python client.py ingest vendor_a_proposal.pdf -n vendor_a
python client.py ingest vendor_b_proposal.pdf -n vendor_b
python client.py ingest vendor_c_proposal.pdf -n vendor_c

# 2. Compare to RFP
python client.py compare-all rfp_requirements.txt

# 3. Generate reports
python client.py report vendor_a rfp_requirements.txt --format html
python client.py report vendor_b rfp_requirements.txt --format html
python client.py report vendor_c rfp_requirements.txt --format html

# 4. View rankings - automatically sorted by compliance %
```

## Command Reference

```bash
# Document Management
python client.py list                    # Show all documents
python client.py summary doc_name        # Get document info
python client.py delete doc_name         # Remove document

# Ingestion
python client.py ingest file.pdf -n name  # Add document

# Search
python client.py query doc "question"     # Query one document
python client.py batch doc1 doc2 "query"  # Query multiple

# Comparison
python client.py compare doc spec.txt     # Check one document
python client.py compare-all spec.txt     # Check all documents

# Reports
python client.py report doc spec.txt --format text    # Text report
python client.py report doc spec.txt --format html    # HTML report
python client.py report doc spec.txt --format json    # JSON report
```

## File Structure
```
pdf_rag_mcp_server/
├── src/                    ← Core server code
├── config/                 ← Settings
├── data/                   ← Indices & cache
├── examples/               ← Sample files
├── client.py               ← CLI tool
├── setup.py                ← Installation
├── verify_installation.py  ← Diagnostics
├── README.md               ← Start here
├── CONFIG.md               ← Full docs
├── EXAMPLES.md             ← Code samples
└── BUILD_SUMMARY.md        ← Architecture
```

## Getting Help

- **Quick reference**: `python client.py --help`
- **Detailed docs**: Read `CONFIG.md`
- **Code examples**: See `EXAMPLES.md`
- **Diagnostics**: Run `verify_installation.py`
- **Architecture**: Check `BUILD_SUMMARY.md`

---

## Ready? 🎯

```bash
# Start here:
python verify_installation.py

# Then try:
python client.py --help

# Or jump to advanced:
python client.py compare document.pdf requirements.txt
```

**Questions?** Everything is documented in this folder. Start with `README.md` or `CONFIG.md`.

**Happy analyzing!** 📚
