# China Funds

Guide for accessing China mutual fund data.

## Fund NAV History

```python
import finvista as fv

# Get NAV history
df = fv.get_cn_fund_nav("110011", start_date="2024-01-01")
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `symbol` | str | Yes | Fund code (e.g., "110011") |
| `start_date` | str | No | Start date (YYYY-MM-DD) |
| `end_date` | str | No | End date (YYYY-MM-DD) |

### Return Columns

| Column | Description |
|--------|-------------|
| `date` | Date |
| `nav` | Net Asset Value |
| `acc_nav` | Accumulated NAV |
| `change_pct` | Daily change percentage |

## Real-time Fund Estimates

```python
# Get estimated NAV
df = fv.get_cn_fund_quote(["110011", "000001"])
```

## Fund Information

```python
info = fv.get_cn_fund_info("110011")

# Returns dict with:
# - name: Fund name
# - type: Fund type
# - manager: Fund manager
# - company: Fund company
# - size: Fund size
# - inception_date: Inception date
```

## List Funds by Type

```python
# Stock funds
df = fv.list_cn_fund_symbols(fund_type="stock")

# Bond funds
df = fv.list_cn_fund_symbols(fund_type="bond")

# Money market funds
df = fv.list_cn_fund_symbols(fund_type="money")

# Index funds
df = fv.list_cn_fund_symbols(fund_type="index")

# All funds
df = fv.list_cn_fund_symbols()
```

## Search Funds

```python
df = fv.search_cn_fund("沪深300")
```

## Data Source

| Source | Data Types |
|--------|------------|
| Tiantian Fund (天天基金) | NAV, Quotes, Info, List |

## Examples

### Track Fund Performance

```python
df = fv.get_cn_fund_nav("110011", start_date="2024-01-01")

# Calculate total return
first_nav = df.iloc[0]['nav']
last_nav = df.iloc[-1]['nav']
total_return = (last_nav - first_nav) / first_nav * 100
print(f"Total return: {total_return:.2f}%")
```

### Compare Multiple Funds

```python
funds = ["110011", "000001", "519300"]
data = {}

for fund in funds:
    df = fv.get_cn_fund_nav(fund, start_date="2024-01-01")
    data[fund] = df

# Combine into single DataFrame
import pandas as pd
combined = pd.DataFrame({
    fund: data[fund].set_index('date')['nav']
    for fund in funds
})
```
