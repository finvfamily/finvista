# Installation

## Requirements

- Python >= 3.10
- pip (Python package manager)

## Basic Installation

Install FinVista using pip:

```bash
pip install finvista
```

## Optional Dependencies

### Full Installation

Install all optional dependencies:

```bash
pip install finvista[full]
```

This includes:

- `curl-cffi` - Better HTTP client with browser impersonation
- `openpyxl` - Excel file support
- `xlrd` - Legacy Excel file support

### Async Support

For async/await functionality:

```bash
pip install finvista[async]
```

### Caching

For Redis or disk-based caching:

```bash
pip install finvista[cache]
```

### Development

For development and testing:

```bash
pip install finvista[dev]
```

## Verify Installation

```python
import finvista as fv

# Check version
print(fv.__version__)

# Quick test
df = fv.get_cn_stock_quote(["000001"])
print(df)
```

## Upgrade

```bash
pip install --upgrade finvista
```

## Uninstall

```bash
pip uninstall finvista
```
