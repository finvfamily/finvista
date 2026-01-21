# US Stocks

Guide for accessing US stock market data.

## Daily Historical Data

```python
import finvista as fv

# Get Apple daily data
df = fv.get_us_stock_daily("AAPL", start_date="2024-01-01")
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `symbol` | str | Yes | Stock ticker (e.g., "AAPL") |
| `start_date` | str | No | Start date (YYYY-MM-DD) |
| `end_date` | str | No | End date (YYYY-MM-DD) |

### Return Columns

| Column | Description |
|--------|-------------|
| `date` | Trading date |
| `open` | Opening price |
| `high` | Highest price |
| `low` | Lowest price |
| `close` | Closing price (adjusted) |
| `volume` | Trading volume |

## Real-time Quotes

```python
# Single stock
df = fv.get_us_stock_quote("AAPL")

# Multiple stocks
df = fv.get_us_stock_quote(["AAPL", "MSFT", "GOOGL", "AMZN", "META"])
```

## Company Information

```python
info = fv.get_us_stock_info("AAPL")

# Returns dict with:
# - name: Company name
# - sector: Industry sector
# - industry: Specific industry
# - market_cap: Market capitalization
# - pe_ratio: P/E ratio
# - description: Company description
```

## Search Stocks

```python
df = fv.search_us_stock("Apple")
```

## Data Source

| Source | Data Types |
|--------|------------|
| Yahoo Finance | Daily, Quote, Info, Search |

## Examples

### Tech Giants Comparison

```python
tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "META"]
df = fv.get_us_stock_quote(tickers)
print(df[['symbol', 'name', 'price', 'change_pct', 'market_cap']])
```

### Download Historical Data

```python
df = fv.get_us_stock_daily("AAPL", start_date="2020-01-01")
df.to_csv("AAPL_daily.csv", index=False)
```

### Portfolio Analysis

```python
import pandas as pd

portfolio = {
    "AAPL": 0.3,   # 30%
    "MSFT": 0.25,  # 25%
    "GOOGL": 0.25, # 25%
    "AMZN": 0.2    # 20%
}

prices = {}
for ticker in portfolio:
    df = fv.get_us_stock_daily(ticker, start_date="2024-01-01")
    prices[ticker] = df.set_index('date')['close']

price_df = pd.DataFrame(prices)
returns = price_df.pct_change()

# Portfolio weighted return
portfolio_return = sum(
    returns[ticker] * weight
    for ticker, weight in portfolio.items()
)
```

## Notes

- US market data may have 15-minute delay for real-time quotes
- Historical data is adjusted for splits and dividends
- Yahoo Finance is the primary data source
