# China A-Share Stocks

Complete guide for accessing China A-share stock data.

## Daily Historical Data

### Basic Usage

```python
import finvista as fv

# Get daily data
df = fv.get_cn_stock_daily("000001", start_date="2024-01-01")
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `symbol` | str | Yes | Stock code (e.g., "000001") |
| `start_date` | str | No | Start date (YYYY-MM-DD) |
| `end_date` | str | No | End date (YYYY-MM-DD) |
| `source` | str | No | Force specific source |

### Return Columns

| Column | Description |
|--------|-------------|
| `date` | Trading date |
| `open` | Opening price |
| `high` | Highest price |
| `low` | Lowest price |
| `close` | Closing price |
| `volume` | Trading volume |
| `amount` | Trading amount |

## Real-time Quotes

```python
# Single stock
df = fv.get_cn_stock_quote("000001")

# Multiple stocks
df = fv.get_cn_stock_quote(["000001", "600519", "000858"])
```

### Return Columns

| Column | Description |
|--------|-------------|
| `symbol` | Stock code |
| `name` | Stock name |
| `price` | Current price |
| `change` | Price change |
| `change_pct` | Change percentage |
| `open` | Opening price |
| `high` | Highest price |
| `low` | Lowest price |
| `volume` | Trading volume |

## Stock List

```python
# Main board stocks
df = fv.list_cn_stock_symbols(market="main")

# ChiNext (创业板)
df = fv.list_cn_stock_symbols(market="chinext")

# STAR Market (科创板)
df = fv.list_cn_stock_symbols(market="star")

# All stocks
df = fv.list_cn_stock_symbols()
```

## Search Stocks

```python
# Search by keyword
df = fv.search_cn_stock("银行")

# Search by code prefix
df = fv.search_cn_stock("600")
```

## Data Sources

| Priority | Source | Speed | Reliability |
|----------|--------|-------|-------------|
| 1 | East Money | Fast | High |
| 2 | Sina | Medium | High |
| 3 | Tencent | Medium | Medium |

## Examples

### Download and Save to CSV

```python
df = fv.get_cn_stock_daily("000001", start_date="2020-01-01")
df.to_csv("000001_daily.csv", index=False)
```

### Calculate Moving Average

```python
import pandas as pd

df = fv.get_cn_stock_daily("000001", start_date="2024-01-01")
df['MA5'] = df['close'].rolling(5).mean()
df['MA20'] = df['close'].rolling(20).mean()
```

### Get Multiple Stocks

```python
symbols = ["000001", "600519", "000858"]
data = {}

for symbol in symbols:
    data[symbol] = fv.get_cn_stock_daily(symbol, start_date="2024-01-01")
```
