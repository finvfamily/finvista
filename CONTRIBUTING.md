# Contributing to FinVista

First off, thank you for considering contributing to FinVista! 🎉

## Ways to Contribute

### 🐛 Report Bugs
- Use [GitHub Issues](https://github.com/finvfamily/finvista/issues)
- Include Python version, OS, and steps to reproduce

### 💡 Suggest Features
- Open an issue with `[Feature Request]` prefix
- Describe the use case and expected behavior

### 📝 Improve Documentation
- Fix typos, improve examples
- Add translations

### 🔧 Submit Code
- Bug fixes
- New data sources
- New market support
- Performance improvements

## Good First Issues

Look for issues labeled [`good first issue`](https://github.com/finvfamily/finvista/labels/good%20first%20issue) - these are beginner-friendly!

## Development Setup

```bash
# Clone the repo
git clone https://github.com/finvfamily/finvista.git
cd finvista

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest tests/ -v
```

## Code Style

- Use [ruff](https://github.com/astral-sh/ruff) for linting
- Use type hints
- Write docstrings in English
- Follow existing code patterns

```bash
# Format code
ruff check --fix finvista/
ruff format finvista/

# Type check
mypy finvista/
```

## Pull Request Process

1. Fork the repo and create your branch from `main`
2. Make your changes
3. Add tests if applicable
4. Ensure tests pass: `pytest tests/ -v`
5. Update documentation if needed
6. Submit PR with clear description

## Commit Messages

Follow conventional commits:
```
feat: add Hong Kong market support
fix: handle empty API response
docs: update installation guide
test: add unit tests for cache
```

## Need Help?

- Open a [Discussion](https://github.com/finvfamily/finvista/discussions)
- Check existing issues and PRs

## Recognition

All contributors will be:
- Listed in README contributors section
- Mentioned in release notes

Thank you for making FinVista better! 🚀
