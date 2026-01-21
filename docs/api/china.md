# China Market API

## Stocks

### get_cn_stock_daily

Get daily OHLCV data for China A-shares.

```python
fv.get_cn_stock_daily(
    symbol: str,
    start_date: str | None = None,
    end_date: str | None = None,
    source: str | None = None
) -> pd.DataFrame
```

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| `symbol` | str | Stock code (e.g., "000001") |
| `start_date` | str | Start date (YYYY-MM-DD) |
| `end_date` | str | End date (YYYY-MM-DD) |
| `source` | str | Force specific source |

**Returns:** DataFrame with columns: `date`, `open`, `high`, `low`, `close`, `volume`, `amount`

---

### get_cn_stock_quote

Get real-time quotes for China A-shares.

```python
fv.get_cn_stock_quote(
    symbols: str | list[str]
) -> pd.DataFrame
```

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| `symbols` | str \| list | Stock code(s) |

**Returns:** DataFrame with columns: `symbol`, `name`, `price`, `change`, `change_pct`, `open`, `high`, `low`, `volume`, `amount`

---

### list_cn_stock_symbols

List China A-share stock symbols.

```python
fv.list_cn_stock_symbols(
    market: str | None = None
) -> pd.DataFrame
```

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| `market` | str | Market filter: "main", "chinext", "star", or None for all |

---

### search_cn_stock

Search stocks by keyword.

```python
fv.search_cn_stock(keyword: str) -> pd.DataFrame
```

---

## Indices

### get_cn_index_daily

```python
fv.get_cn_index_daily(
    symbol: str,
    start_date: str | None = None,
    end_date: str | None = None
) -> pd.DataFrame
```

---

### get_cn_index_quote

```python
fv.get_cn_index_quote(symbols: str | list[str]) -> pd.DataFrame
```

---

### list_cn_major_indices

```python
fv.list_cn_major_indices() -> pd.DataFrame
```

---

## Funds

### get_cn_fund_nav

```python
fv.get_cn_fund_nav(
    symbol: str,
    start_date: str | None = None,
    end_date: str | None = None
) -> pd.DataFrame
```

**Returns:** DataFrame with columns: `date`, `nav`, `acc_nav`, `change_pct`

---

### get_cn_fund_quote

```python
fv.get_cn_fund_quote(symbols: str | list[str]) -> pd.DataFrame
```

---

### get_cn_fund_info

```python
fv.get_cn_fund_info(symbol: str) -> dict
```

**Returns:** Dict with keys: `name`, `type`, `manager`, `company`, `size`, `inception_date`

---

### list_cn_fund_symbols

```python
fv.list_cn_fund_symbols(fund_type: str | None = None) -> pd.DataFrame
```

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| `fund_type` | str | Filter: "stock", "bond", "money", "index", or None |

---

### search_cn_fund

```python
fv.search_cn_fund(keyword: str) -> pd.DataFrame
```
