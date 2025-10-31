# Contributing to PDF RAG MCP Server

Thank you for your interest in contributing to the PDF RAG MCP Server! We welcome contributions from the community.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)

## 📜 Code of Conduct

This project and everyone participating in it is governed by respect, professionalism, and collaboration. Please be kind and constructive in all interactions.

## 🤝 How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the issue tracker to avoid duplicates. When you create a bug report, include:

- **Clear title and description**
- **Steps to reproduce** the issue
- **Expected behavior**
- **Actual behavior**
- **Environment details** (OS, Python version, etc.)
- **Relevant logs** or error messages

### Suggesting Enhancements

Enhancement suggestions are welcome! Please provide:

- **Clear use case** for the enhancement
- **Detailed description** of the proposed feature
- **Possible implementation** approach (if you have ideas)

### Pull Requests

We actively welcome your pull requests:

1. Fork the repo and create your branch from `master`
2. If you've added code, add tests
3. If you've changed APIs, update the documentation
4. Ensure the test suite passes
5. Make sure your code follows the existing style
6. Issue your pull request!

## 🔧 Development Setup

### Prerequisites

- Python 3.9 or higher
- UV package manager (recommended) or pip
- Git

### Setup Steps

1. **Fork and clone the repository**

```bash
git clone https://github.com/your-username/pdf-rag-mcp-server.git
cd pdf-rag-mcp-server
```

2. **Install dependencies**

With UV (recommended - 10x faster):
```bash
./install_uv.sh  # Unix/Linux/macOS
.\install_uv.ps1  # Windows
```

Or with pip:
```bash
pip install -e ".[dev]"
```

3. **Verify installation**

```bash
python verify_installation.py
```

4. **Run tests**

```bash
python run_tests.py
```

### Development Workflow

1. Create a new branch for your feature:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes

3. Run tests:
```bash
uv run pytest
```

4. Run code formatters:
```bash
uv run black .
uv run ruff check --fix .
```

5. Commit your changes:
```bash
git add .
git commit -m "Add feature: description"
```

6. Push to your fork:
```bash
git push origin feature/your-feature-name
```

7. Create a Pull Request

## 🎨 Coding Standards

### Python Style

- Follow [PEP 8](https://pep8.org/) style guide
- Use [Black](https://black.readthedocs.io/) for code formatting (line length: 100)
- Use [Ruff](https://github.com/astral-sh/ruff) for linting
- Use type hints where appropriate
- Write docstrings for all public functions and classes

### Code Format

```python
def function_name(param1: str, param2: int = 5) -> dict:
    """
    Brief description of what the function does.

    Args:
        param1: Description of param1
        param2: Description of param2 (default: 5)

    Returns:
        Description of return value

    Raises:
        ValueError: When invalid input is provided
    """
    # Implementation
    return {"result": "value"}
```

### Commit Messages

Follow conventional commits format:

```
type(scope): brief description

Longer description if needed

Fixes #issue_number
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:
```
feat(rag): add batch query support

fix(docker): correct build order in Dockerfile

docs(readme): update installation instructions
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python run_tests.py

# Run specific test
python -m pytest tests/test_specific.py

# Run with coverage
pytest --cov=src --cov-report=html
```

### Writing Tests

- Write tests for all new features
- Ensure tests are independent and can run in any order
- Use descriptive test names
- Include both positive and negative test cases

Example:
```python
def test_document_ingestion_success():
    """Test successful document ingestion"""
    result = ingest_document("test.pdf", "test_doc")
    assert result["success"] == True
    assert "vector_store_path" in result

def test_document_ingestion_invalid_file():
    """Test ingestion with invalid file raises error"""
    with pytest.raises(FileNotFoundError):
        ingest_document("nonexistent.pdf", "test")
```

## 📚 Documentation

### Updating Documentation

- Update README.md for user-facing changes
- Update docstrings for code changes
- Add examples to EXAMPLES.md if applicable
- Update relevant .md files in docs/

### Documentation Style

- Use clear, concise language
- Include code examples where helpful
- Use proper markdown formatting
- Add links to related documentation

## 🔍 Review Process

### What We Look For

- **Functionality**: Does it work as intended?
- **Tests**: Are there adequate tests?
- **Documentation**: Is it well documented?
- **Code Quality**: Does it follow our standards?
- **Performance**: Does it maintain or improve performance?
- **Security**: Are there any security concerns?

### Review Timeline

- Initial response: Within 48 hours
- Full review: Within 1 week
- We may request changes or ask questions

## 📦 Release Process

Releases are handled by maintainers:

1. Version bump in `pyproject.toml`
2. Update CHANGELOG.md
3. Create release tag
4. Build and publish to PyPI
5. Update documentation

## 🏆 Recognition

Contributors are recognized in:
- GitHub contributors page
- CHANGELOG.md for significant contributions
- README.md acknowledgments section

## ❓ Questions?

- Open an issue for questions about contributing
- Check existing issues and documentation first
- Be patient and respectful

## 📝 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to PDF RAG MCP Server!** 🎉
