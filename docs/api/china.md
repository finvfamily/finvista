# 中国市场 API

## 股票

### get_cn_stock_daily

获取 A 股日线数据。

```python
fv.get_cn_stock_daily(
    symbol: str,
    start_date: str | None = None,
    end_date: str | None = None,
    source: str | None = None
) -> pd.DataFrame
```

**参数：**

| 名称 | 类型 | 说明 |
|------|------|------|
| `symbol` | str | 股票代码（如 "000001"） |
| `start_date` | str | 开始日期（YYYY-MM-DD） |
| `end_date` | str | 结束日期（YYYY-MM-DD） |
| `source` | str | 强制指定数据源 |

**返回：** DataFrame，字段：`date`, `open`, `high`, `low`, `close`, `volume`, `amount`

---

### get_cn_stock_quote

获取 A 股实时行情。

```python
fv.get_cn_stock_quote(symbols: str | list[str]) -> pd.DataFrame
```

**返回：** DataFrame，字段：`symbol`, `name`, `price`, `change`, `change_pct`, `volume`

---

### get_cn_stock_minute

获取 A 股分钟线数据。

```python
fv.get_cn_stock_minute(
    symbol: str,
    period: Literal["1", "5", "15", "30", "60"] = "5",
    days: int = 5
) -> pd.DataFrame
```

**返回：** DataFrame，字段：`datetime`, `open`, `high`, `low`, `close`, `volume`, `amount`

---

### list_cn_stock_symbols

列出 A 股股票代码。

```python
fv.list_cn_stock_symbols(market: str | None = None) -> pd.DataFrame
```

**参数：** `market` - "main"（主板）、"chinext"（创业板）、"star"（科创板）

---

### search_cn_stock

搜索股票。

```python
fv.search_cn_stock(keyword: str) -> pd.DataFrame
```

---

## 指数

### get_cn_index_daily

```python
fv.get_cn_index_daily(symbol: str, start_date: str = None, end_date: str = None) -> pd.DataFrame
```

---

### get_cn_index_quote

```python
fv.get_cn_index_quote(symbols: str | list[str]) -> pd.DataFrame
```

---

### get_cn_index_constituents

获取指数成分股。

```python
fv.get_cn_index_constituents(symbol: str) -> pd.DataFrame
```

---

### get_cn_index_weights

获取指数成分股权重。

```python
fv.get_cn_index_weights(symbol: str) -> pd.DataFrame
```

---

## 基金

### get_cn_fund_nav

```python
fv.get_cn_fund_nav(symbol: str, start_date: str = None, end_date: str = None) -> pd.DataFrame
```

**返回：** DataFrame，字段：`date`, `nav`, `acc_nav`, `change_pct`

---

### get_cn_fund_info

```python
fv.get_cn_fund_info(symbol: str) -> dict
```

**返回：** Dict，键：`name`, `type`, `manager`, `company`, `size`, `inception_date`

---

## 财务数据

### get_cn_income_statement

获取利润表。

```python
fv.get_cn_income_statement(
    symbol: str,
    period: Literal["yearly", "quarterly"] = "yearly"
) -> pd.DataFrame
```

---

### get_cn_balance_sheet

获取资产负债表。

```python
fv.get_cn_balance_sheet(
    symbol: str,
    period: Literal["yearly", "quarterly"] = "yearly"
) -> pd.DataFrame
```

---

### get_cn_cash_flow

获取现金流量表。

```python
fv.get_cn_cash_flow(
    symbol: str,
    period: Literal["yearly", "quarterly"] = "yearly"
) -> pd.DataFrame
```

---

### get_cn_dividend_history

获取分红历史。

```python
fv.get_cn_dividend_history(symbol: str) -> pd.DataFrame
```

---

### get_cn_performance_forecast

获取业绩预告。

```python
fv.get_cn_performance_forecast(date: str = None) -> pd.DataFrame
```

---

## 资金流向

### get_cn_stock_moneyflow

```python
fv.get_cn_stock_moneyflow(symbol: str, days: int = 30) -> pd.DataFrame
```

---

### get_cn_stock_moneyflow_realtime

```python
fv.get_cn_stock_moneyflow_realtime(symbol: str) -> pd.DataFrame
```

---

### get_cn_industry_moneyflow

```python
fv.get_cn_industry_moneyflow(date: str = None) -> pd.DataFrame
```

---

## 期货

### list_cn_futures_symbols

```python
fv.list_cn_futures_symbols(exchange: str = "all") -> pd.DataFrame
```

**参数：** `exchange` - "CFFEX", "SHFE", "DCE", "CZCE", "INE", 或 "all"

---

### get_cn_futures_daily

```python
fv.get_cn_futures_daily(symbol: str, start_date: str = None, end_date: str = None) -> pd.DataFrame
```

---

### get_cn_futures_positions

```python
fv.get_cn_futures_positions(symbol: str, date: str = None) -> pd.DataFrame
```

---

## 可转债

### list_cn_convertible_symbols

```python
fv.list_cn_convertible_symbols() -> pd.DataFrame
```

---

### get_cn_convertible_daily

```python
fv.get_cn_convertible_daily(symbol: str, start_date: str = None, end_date: str = None) -> pd.DataFrame
```

---

### get_cn_convertible_info

```python
fv.get_cn_convertible_info(symbol: str) -> dict
```

---

## 龙虎榜

### get_cn_lhb_list

```python
fv.get_cn_lhb_list(date: str = None) -> pd.DataFrame
```

---

### get_cn_lhb_detail

```python
fv.get_cn_lhb_detail(symbol: str, date: str) -> pd.DataFrame
```

---

### get_cn_lhb_institution

```python
fv.get_cn_lhb_institution(date: str = None) -> pd.DataFrame
```

---

## 期权

### list_cn_option_contracts

```python
fv.list_cn_option_contracts(underlying: str = "510050") -> pd.DataFrame
```

---

### get_cn_option_quote

```python
fv.get_cn_option_quote(symbol: str) -> pd.DataFrame
```

---

### get_cn_option_daily

```python
fv.get_cn_option_daily(symbol: str, start_date: str = None, end_date: str = None) -> pd.DataFrame
```

---

## 股东数据

### get_cn_top_shareholders

```python
fv.get_cn_top_shareholders(symbol: str, period: str = None) -> pd.DataFrame
```

---

### get_cn_stock_pledge

```python
fv.get_cn_stock_pledge(symbol: str) -> pd.DataFrame
```

---

### get_cn_stock_unlock_schedule

```python
fv.get_cn_stock_unlock_schedule(start_date: str, end_date: str) -> pd.DataFrame
```

---

## ETF

### get_cn_etf_share_change

```python
fv.get_cn_etf_share_change(symbol: str, days: int = 30) -> pd.DataFrame
```

---

### get_cn_etf_premium_discount

```python
fv.get_cn_etf_premium_discount(symbol: str) -> pd.DataFrame
```
