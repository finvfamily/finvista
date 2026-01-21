# FinVista

[English](README.md) | [中文](README_zh.md)

> A powerful Python library for global financial data with multi-source failover.

[![PyPI version](https://badge.fury.io/py/finvista.svg)](https://badge.fury.io/py/finvista)
[![Python Version](https://img.shields.io/pypi/pyversions/finvista.svg)](https://pypi.org/project/finvista/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/finvfamily/finvista/actions/workflows/tests.yml/badge.svg)](https://github.com/finvfamily/finvista/actions)

## Features

- 🔄 **Multi-Source Failover**: Automatically switches to backup data sources when primary fails
- ⚡ **Circuit Breaker Pattern**: Prevents cascade failures with smart circuit breaking
- 💾 **Built-in Caching**: LRU cache reduces redundant API calls
- 🚦 **Rate Limiting**: Intelligent rate limiting to avoid being blocked
- 🔒 **Type Safe**: Full type hints support for better IDE experience
- 🎯 **Easy to Use**: Simple functional API design
- 🌍 **Global Markets**: Support for China, US, and more markets
- 📊 **Comprehensive Data**: Stocks, indices, funds, and macroeconomic data

## Installation

```bash
pip install finvista
```

## Quick Start

### China A-Share Stocks

```python
import finvista as fv

# Get daily historical data
df = fv.get_cn_stock_daily("000001", start_date="2024-01-01")
print(df.head())

# Get real-time quotes
df = fv.get_cn_stock_quote(["000001", "600519"])
print(df)

# List all stocks
df = fv.list_cn_stock_symbols(market="main")
print(f"Found {len(df)} stocks")

# Search stocks by keyword
df = fv.search_cn_stock("银行")
print(df)
```

### China Indices

```python
# Get SSE Composite Index data
df = fv.get_cn_index_daily("000001", start_date="2024-01-01")

# Get real-time index quotes
df = fv.get_cn_index_quote(["000001", "399001"])

# List major indices
df = fv.list_cn_major_indices()
```

### China Funds

```python
# Get fund NAV history
df = fv.get_cn_fund_nav("110011", start_date="2024-01-01")

# Get real-time fund estimates
df = fv.get_cn_fund_quote(["110011", "000001"])

# List all funds by type
df = fv.list_cn_fund_symbols(fund_type="stock")

# Search funds
df = fv.search_cn_fund("沪深300")

# Get fund information
info = fv.get_cn_fund_info("110011")
```

### US Stocks

```python
# Get US stock daily data
df = fv.get_us_stock_daily("AAPL", start_date="2024-01-01")

# Get real-time quotes
df = fv.get_us_stock_quote(["AAPL", "MSFT", "GOOGL"])

# Get company information
info = fv.get_us_stock_info("AAPL")

# Search US stocks
df = fv.search_us_stock("Apple")
```

### Macroeconomic Data

```python
# China GDP
df = fv.get_cn_macro_gdp()

# China CPI
df = fv.get_cn_macro_cpi()

# China PPI
df = fv.get_cn_macro_ppi()

# China PMI
df = fv.get_cn_macro_pmi()

# Money Supply (M0, M1, M2)
df = fv.get_cn_macro_money_supply()

# Social Financing
df = fv.get_cn_macro_social_financing()
```

## Command Line Interface

```bash
# Get real-time quotes
finvista quote 000001 600519

# Get US stock quotes
finvista quote AAPL MSFT --market us

# Get historical data
finvista history 000001 --start 2024-01-01 --format csv

# Search stocks
finvista search 银行

# Check data source health
finvista health

# Get macroeconomic data
finvista macro gdp
```

## Configuration

```python
import finvista as fv

# Set HTTP proxy
fv.set_proxies({"http": "http://127.0.0.1:7890"})

# Set request timeout
fv.set_timeout(60)

# Configure caching
fv.set_cache(enabled=True, ttl=300)

# Check data source health
health = fv.get_source_health()
print(health)

# Reset circuit breaker for a source
fv.reset_source_circuit("cn_stock_daily", "eastmoney")

# Set custom source priority
fv.set_source_priority("cn_stock_daily", ["sina", "eastmoney"])
```

## Data Source Failover

FinVista automatically handles data source failures:

```python
import finvista as fv

# Automatic failover - if eastmoney fails, tries sina, then tencent
df = fv.get_cn_stock_daily("000001")

# Check which source was used
print(f"Data from: {df.attrs.get('source')}")

# Force specific source (no failover)
df = fv.get_cn_stock_daily("000001", source="eastmoney")
```

## Data Sources

| Data Type | Primary Source | Backup Sources |
|-----------|---------------|----------------|
| China Stock Daily | East Money | Sina, Tencent |
| China Stock Quote | Sina | Tencent, East Money |
| China Index | East Money | Sina |
| China Fund | Tiantian Fund | - |
| US Stock | Yahoo Finance | - |
| China Macro | East Money | - |

## API Reference

### China Stocks

| Function | Description |
|----------|-------------|
| `get_cn_stock_daily()` | Get daily historical data |
| `get_cn_stock_quote()` | Get real-time quotes |
| `list_cn_stock_symbols()` | List all stock symbols |
| `search_cn_stock()` | Search stocks by keyword |

### China Indices

| Function | Description |
|----------|-------------|
| `get_cn_index_daily()` | Get daily index data |
| `get_cn_index_quote()` | Get real-time index quotes |
| `list_cn_major_indices()` | List major indices |

### China Funds

| Function | Description |
|----------|-------------|
| `get_cn_fund_nav()` | Get fund NAV history |
| `get_cn_fund_quote()` | Get real-time fund estimates |
| `list_cn_fund_symbols()` | List all funds |
| `search_cn_fund()` | Search funds by keyword |
| `get_cn_fund_info()` | Get fund information |

### US Stocks

| Function | Description |
|----------|-------------|
| `get_us_stock_daily()` | Get daily historical data |
| `get_us_stock_quote()` | Get real-time quotes |
| `get_us_stock_info()` | Get company information |
| `search_us_stock()` | Search stocks by keyword |

### Macroeconomic Data

| Function | Description |
|----------|-------------|
| `get_cn_macro_gdp()` | China GDP data |
| `get_cn_macro_cpi()` | China CPI data |
| `get_cn_macro_ppi()` | China PPI data |
| `get_cn_macro_pmi()` | China PMI data |
| `get_cn_macro_money_supply()` | Money supply (M0/M1/M2) |
| `get_cn_macro_social_financing()` | Social financing data |

### Configuration

| Function | Description |
|----------|-------------|
| `set_proxies()` | Set HTTP proxy |
| `set_timeout()` | Set request timeout |
| `set_cache()` | Configure caching |
| `get_source_health()` | Get data source health status |
| `reset_source_circuit()` | Reset circuit breaker |
| `set_source_priority()` | Set source priority order |

## Requirements

- Python >= 3.10
- pandas >= 2.0.0
- requests >= 2.28.0
- httpx >= 0.24.0

## License

MIT License - see [LICENSE](LICENSE) for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

FinVista is designed for reliable financial data access with automatic failover capabilities, serving quantitative researchers, traders, and financial analysts.
