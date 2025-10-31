# PDF RAG MCP Server - UV Quick Start

⚡ **Now 10-100x faster with UV!**

## Instant Setup

### One Command Install

**Unix/Linux/macOS:**
```bash
./install_uv.sh
```

**Windows:**
```powershell
.\install_uv.ps1
```

That's it! Everything is installed and ready to go.

## Usage

### Run the Server
```bash
uv run python main.py
```

### Use CLI
```bash
uv run python client.py ingest document.pdf -n doc1
uv run python client.py query doc1 "What is this about?"
```

### Run Tests
```bash
uv run python run_tests.py
```

## What is UV?

UV is a blazing-fast Python package manager (10-100x faster than pip) written in Rust by the creators of Ruff.

## Benefits

- ⚡ **10-100x faster** installations
- 🔒 **Better dependency** resolution
- 🐳 **Faster Docker** builds (5x improvement)
- 💯 **100% compatible** with existing code

## More Info

- **Setup Guide:** [UV_SETUP.md](UV_SETUP.md)
- **Integration Details:** [UV_INTEGRATION_COMPLETE.md](UV_INTEGRATION_COMPLETE.md)
- **Bug Fixes:** [BUG_FIXES_SUMMARY.md](BUG_FIXES_SUMMARY.md)

---

**Ready to go!** 🚀
