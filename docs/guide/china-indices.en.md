# China Indices

Guide for accessing China stock market index data.

## Index Daily Data

```python
import finvista as fv

# SSE Composite Index (上证综指)
df = fv.get_cn_index_daily("000001", start_date="2024-01-01")

# SZSE Component Index (深证成指)
df = fv.get_cn_index_daily("399001", start_date="2024-01-01")

# CSI 300 (沪深300)
df = fv.get_cn_index_daily("000300", start_date="2024-01-01")
```

### Return Columns

| Column | Description |
|--------|-------------|
| `date` | Trading date |
| `open` | Opening value |
| `high` | Highest value |
| `low` | Lowest value |
| `close` | Closing value |
| `volume` | Trading volume |
| `amount` | Trading amount |

## Real-time Index Quotes

```python
# Get real-time quotes
df = fv.get_cn_index_quote(["000001", "399001", "000300"])
```

## Major Indices

```python
# List all major indices
df = fv.list_cn_major_indices()
```

### Common Index Codes

| Code | Name | Description |
|------|------|-------------|
| 000001 | 上证综指 | SSE Composite Index |
| 399001 | 深证成指 | SZSE Component Index |
| 000300 | 沪深300 | CSI 300 |
| 000016 | 上证50 | SSE 50 |
| 000905 | 中证500 | CSI 500 |
| 399006 | 创业板指 | ChiNext Index |
| 000688 | 科创50 | STAR 50 |

## Data Sources

| Priority | Source |
|----------|--------|
| 1 | East Money |
| 2 | Sina |

## Examples

### Market Overview

```python
indices = ["000001", "399001", "000300", "399006"]
df = fv.get_cn_index_quote(indices)
print(df[['symbol', 'name', 'price', 'change_pct']])
```

### Historical Comparison

```python
import pandas as pd

indices = {
    "000001": "上证综指",
    "399001": "深证成指",
    "000300": "沪深300"
}

data = {}
for code, name in indices.items():
    df = fv.get_cn_index_daily(code, start_date="2024-01-01")
    data[name] = df.set_index('date')['close']

combined = pd.DataFrame(data)
# Normalize to 100
normalized = combined / combined.iloc[0] * 100
```
