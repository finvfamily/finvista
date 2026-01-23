# Quick Start

This guide will help you get started with FinVista in minutes.

## Import the Library

```python
import finvista as fv
```

## China A-Share Stocks

### Get Daily Historical Data

```python
# Get daily data for Ping An Bank (000001)
df = fv.get_cn_stock_daily("000001", start_date="2024-01-01")
print(df.head())
```

Output:
```
         date    open    high     low   close      volume        amount
0  2024-01-02   9.15    9.20    9.05    9.10   123456789   1123456789.0
1  2024-01-03   9.12    9.25    9.10    9.20   134567890   1234567890.0
...
```

### Get Real-time Quotes

```python
# Get quotes for multiple stocks
df = fv.get_cn_stock_quote(["000001", "600519"])
print(df)
```

### Search Stocks

```python
# Search by keyword
df = fv.search_cn_stock("银行")
print(df)
```

### List All Stocks

```python
# Get all main board stocks
df = fv.list_cn_stock_symbols(market="main")
print(f"Found {len(df)} stocks")
```

## China Indices

```python
# Get SSE Composite Index (000001)
df = fv.get_cn_index_daily("000001", start_date="2024-01-01")

# Get real-time index quotes
df = fv.get_cn_index_quote(["000001", "399001"])

# List major indices
df = fv.list_cn_major_indices()
```

## China Funds

```python
# Get fund NAV history
df = fv.get_cn_fund_nav("110011", start_date="2024-01-01")

# Get real-time estimates
df = fv.get_cn_fund_quote(["110011", "000001"])

# Get fund information
info = fv.get_cn_fund_info("110011")
```

## US Stocks

```python
# Get Apple daily data
df = fv.get_us_stock_daily("AAPL", start_date="2024-01-01")

# Get real-time quotes
df = fv.get_us_stock_quote(["AAPL", "MSFT", "GOOGL"])

# Get company info
info = fv.get_us_stock_info("AAPL")
```

## Macroeconomic Data

```python
# China GDP
df = fv.get_cn_macro_gdp()

# China CPI
df = fv.get_cn_macro_cpi()

# Money Supply (M0, M1, M2)
df = fv.get_cn_macro_money_supply()
```

## Check Data Source

Every DataFrame includes metadata about which source was used:

```python
df = fv.get_cn_stock_daily("000001")
print(f"Data from: {df.attrs.get('source')}")
```

## Next Steps

- [Configuration Guide](configuration.md) - Customize FinVista settings
- [Failover Guide](../guide/failover.md) - Understand multi-source failover
- [API Reference](../api/overview.md) - Complete API documentation
