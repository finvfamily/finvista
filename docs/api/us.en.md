# US Market API

## Stocks

### get_us_stock_daily

Get daily OHLCV data for US stocks.

```python
fv.get_us_stock_daily(
    symbol: str,
    start_date: str | None = None,
    end_date: str | None = None
) -> pd.DataFrame
```

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| `symbol` | str | Stock ticker (e.g., "AAPL") |
| `start_date` | str | Start date (YYYY-MM-DD) |
| `end_date` | str | End date (YYYY-MM-DD) |

**Returns:** DataFrame with columns: `date`, `open`, `high`, `low`, `close`, `volume`

**Example:**

```python
df = fv.get_us_stock_daily("AAPL", start_date="2024-01-01")
```

---

### get_us_stock_quote

Get real-time quotes for US stocks.

```python
fv.get_us_stock_quote(
    symbols: str | list[str]
) -> pd.DataFrame
```

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| `symbols` | str \| list | Stock ticker(s) |

**Returns:** DataFrame with columns: `symbol`, `name`, `price`, `change`, `change_pct`, `volume`, `market_cap`

**Example:**

```python
df = fv.get_us_stock_quote(["AAPL", "MSFT", "GOOGL"])
```

---

### get_us_stock_info

Get company information for US stocks.

```python
fv.get_us_stock_info(symbol: str) -> dict
```

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| `symbol` | str | Stock ticker (e.g., "AAPL") |

**Returns:** Dict with keys:

| Key | Description |
|-----|-------------|
| `name` | Company name |
| `sector` | Industry sector |
| `industry` | Specific industry |
| `market_cap` | Market capitalization |
| `pe_ratio` | Price-to-earnings ratio |
| `description` | Company description |

**Example:**

```python
info = fv.get_us_stock_info("AAPL")
print(info['name'])  # Apple Inc.
```

---

### search_us_stock

Search US stocks by keyword.

```python
fv.search_us_stock(keyword: str) -> pd.DataFrame
```

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| `keyword` | str | Search keyword |

**Example:**

```python
df = fv.search_us_stock("Apple")
```

---

## Data Source

All US market data is sourced from Yahoo Finance.

| Data Type | Delay |
|-----------|-------|
| Daily Historical | None (adjusted close) |
| Real-time Quote | 15 minutes |
| Company Info | Real-time |
