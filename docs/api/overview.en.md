# API Overview

FinVista provides a simple functional API for accessing financial data.

## Import

```python
import finvista as fv
```

## Naming Convention

Functions follow the pattern: `<action>_<market>_<asset>_<data_type>`

Examples:
- `get_cn_stock_daily` - Get China stock daily data
- `get_us_stock_quote` - Get US stock quotes
- `list_cn_fund_symbols` - List China funds

## Return Types

All data functions return `pandas.DataFrame` with:
- Consistent column names
- Datetime index (when applicable)
- Metadata in `df.attrs` (e.g., data source)

## Quick Reference

### China Stocks

| Function | Description |
|----------|-------------|
| `get_cn_stock_daily(symbol, start_date, end_date)` | Daily OHLCV data |
| `get_cn_stock_quote(symbols)` | Real-time quotes |
| `list_cn_stock_symbols(market)` | List all stocks |
| `search_cn_stock(keyword)` | Search stocks |

### China Indices

| Function | Description |
|----------|-------------|
| `get_cn_index_daily(symbol, start_date, end_date)` | Daily index data |
| `get_cn_index_quote(symbols)` | Real-time index quotes |
| `list_cn_major_indices()` | List major indices |

### China Funds

| Function | Description |
|----------|-------------|
| `get_cn_fund_nav(symbol, start_date, end_date)` | NAV history |
| `get_cn_fund_quote(symbols)` | Real-time estimates |
| `list_cn_fund_symbols(fund_type)` | List funds |
| `search_cn_fund(keyword)` | Search funds |
| `get_cn_fund_info(symbol)` | Fund information |

### US Stocks

| Function | Description |
|----------|-------------|
| `get_us_stock_daily(symbol, start_date, end_date)` | Daily OHLCV data |
| `get_us_stock_quote(symbols)` | Real-time quotes |
| `get_us_stock_info(symbol)` | Company info |
| `search_us_stock(keyword)` | Search stocks |

### Macroeconomic Data

| Function | Description |
|----------|-------------|
| `get_cn_macro_gdp()` | China GDP data |
| `get_cn_macro_cpi()` | China CPI data |
| `get_cn_macro_ppi()` | China PPI data |
| `get_cn_macro_pmi()` | China PMI data |
| `get_cn_macro_money_supply()` | Money supply (M0/M1/M2) |
| `get_cn_macro_social_financing()` | Social financing |

### Configuration

| Function | Description |
|----------|-------------|
| `set_proxies(proxies)` | Set HTTP proxy |
| `set_timeout(seconds)` | Set request timeout |
| `set_cache(enabled, ttl)` | Configure caching |
| `get_source_health()` | Get source health status |
| `reset_source_circuit(data_type, source)` | Reset circuit breaker |
| `set_source_priority(data_type, sources)` | Set source priority |

## Error Handling

```python
from finvista.exceptions import (
    FinVistaError,           # Base exception
    NetworkError,            # Network issues
    DataNotFoundError,       # Data not found
    AllSourcesFailedError,   # All sources failed
)

try:
    df = fv.get_cn_stock_daily("000001")
except AllSourcesFailedError as e:
    print(f"All sources failed: {e}")
except NetworkError as e:
    print(f"Network error: {e}")
except FinVistaError as e:
    print(f"FinVista error: {e}")
```
