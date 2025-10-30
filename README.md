# Quick Start Guide

## 5-Minute Setup

### 1. Initial Setup
```bash
cd C:\Users\engmo\Claude_Project\pdf_rag_mcp_server
python setup.py
```

### 2. Test with CLI Client

Create a test file `test_spec.txt`:
```
The document must have a clear title
It should include an introduction
Must contain at least one section with details
Should have a conclusion
```

```bash
# Ingest a sample PDF
python client.py ingest sample.pdf -n sample

# Query it
python client.py query sample "What is this about?"

# Compare to specification
python client.py compare sample test_spec.txt

# Generate report
python client.py report sample test_spec.txt --format text
```

### 3. Use with Claude Desktop

1. Copy `claude_desktop_config.json` content
2. Add to Claude Desktop config at:
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
3. Restart Claude
4. In Claude, ingest and query documents using the MCP tools

## Common Use Cases

### Use Case 1: Vendor Proposal Comparison

```bash
# Ingest proposals
python client.py ingest vendor_a_proposal.pdf -n vendor_a
python client.py ingest vendor_b_proposal.pdf -n vendor_b
python client.py ingest vendor_c_proposal.pdf -n vendor_c

# Compare all to RFP
python client.py compare-all rfp_requirements.txt

# Generate detailed reports
python client.py report vendor_a rfp_requirements.txt --format html
python client.py report vendor_b rfp_requirements.txt --format html
```

### Use Case 2: Compliance Verification

```bash
# Create compliance checklist
echo "Must be ISO 9001 certified
Must provide 5-year warranty
Must have 24/7 support
Must comply with GDPR" > compliance_checklist.txt

# Check document compliance
python client.py compare document.pdf compliance_checklist.txt -n "ISO Compliance"
```

### Use Case 3: Multi-Document Search

```bash
# Create analysis
python client.py batch doc1 doc2 doc3 "security requirements"
```

## Monitoring & Logs

Check `logs/` directory for:
- Server startup logs
- Processing errors
- Query execution logs

## Common Issues

| Issue | Solution |
|-------|----------|
| "File not found" | Check file path is absolute |
| "Module not found" | Run `python setup.py` again |
| Slow queries | Increase `top_k` in config, or reduce `CHUNK_SIZE` |
| Memory errors | Reduce `CHUNK_SIZE` or process smaller files |
| OCR not working | Install Tesseract separately if needed |

## Next Steps

1. ✓ Read `CONFIG.md` for detailed configuration
2. ✓ Try CLI client with your own documents
3. ✓ Integrate with Claude Desktop for AI-assisted analysis
4. ✓ Create custom specifications for your use case

## Support Files

- `CONFIG.md` - Detailed configuration and API reference
- `EXAMPLES.md` - Code examples and workflows (create as needed)
- `requirements.txt` - Python dependencies
- `setup.py` - Automated setup script
