# 美国市场 API

## 股票

### get_us_stock_daily

获取美股日线数据。

```python
fv.get_us_stock_daily(
    symbol: str,
    start_date: str | None = None,
    end_date: str | None = None
) -> pd.DataFrame
```

**参数：**

| 名称 | 类型 | 说明 |
|------|------|------|
| `symbol` | str | 股票代码（如 "AAPL"） |
| `start_date` | str | 开始日期（YYYY-MM-DD） |
| `end_date` | str | 结束日期（YYYY-MM-DD） |

**返回：** DataFrame，字段：`date`, `open`, `high`, `low`, `close`, `volume`, `adj_close`

---

### get_us_stock_quote

获取美股实时行情。

```python
fv.get_us_stock_quote(symbols: str | list[str]) -> pd.DataFrame
```

**参数：**

| 名称 | 类型 | 说明 |
|------|------|------|
| `symbols` | str \| list | 股票代码 |

**返回：** DataFrame，字段：`symbol`, `name`, `price`, `change`, `change_pct`, `volume`, `market_cap`

---

### get_us_stock_info

获取美股公司信息。

```python
fv.get_us_stock_info(symbol: str) -> dict
```

**返回：** Dict，包含：

| 键 | 说明 |
|------|------|
| `name` | 公司名称 |
| `sector` | 行业板块 |
| `industry` | 细分行业 |
| `market_cap` | 市值 |
| `pe_ratio` | 市盈率 |
| `description` | 公司简介 |

---

### search_us_stock

搜索美股。

```python
fv.search_us_stock(keyword: str) -> pd.DataFrame
```

**参数：**

| 名称 | 类型 | 说明 |
|------|------|------|
| `keyword` | str | 搜索关键词 |

**返回：** DataFrame，字段：`symbol`, `name`, `exchange`

---

## 指数

### get_us_index_daily

获取美股指数日线。

```python
fv.get_us_index_daily(
    symbol: str,
    start_date: str | None = None,
    end_date: str | None = None
) -> pd.DataFrame
```

**参数：**

| 名称 | 类型 | 说明 |
|------|------|------|
| `symbol` | str | 指数代码（SPX/NDX/DJI） |
| `start_date` | str | 开始日期 |
| `end_date` | str | 结束日期 |

**常用指数：**

| 代码 | 名称 |
|------|------|
| SPX | 标普 500 指数 |
| NDX | 纳斯达克 100 指数 |
| DJI | 道琼斯工业指数 |

---

## 香港市场

### get_hk_index_daily

获取港股指数日线。

```python
fv.get_hk_index_daily(
    symbol: str,
    start_date: str | None = None,
    end_date: str | None = None
) -> pd.DataFrame
```

**常用指数：**

| 代码 | 名称 |
|------|------|
| HSI | 恒生指数 |
| HSCEI | 恒生国企指数 |
| HSTECH | 恒生科技指数 |

---

## 外汇

### get_exchange_rate

获取实时汇率。

```python
fv.get_exchange_rate(base: str, target: str) -> pd.DataFrame
```

**参数：**

| 名称 | 类型 | 说明 |
|------|------|------|
| `base` | str | 基础货币（如 "USD"） |
| `target` | str | 目标货币（如 "CNY"） |

**返回：** DataFrame，字段：`base`, `target`, `rate`, `bid`, `ask`, `update_time`

---

### get_exchange_rate_history

获取历史汇率。

```python
fv.get_exchange_rate_history(
    base: str,
    target: str,
    start_date: str | None = None,
    end_date: str | None = None
) -> pd.DataFrame
```

**返回：** DataFrame，字段：`date`, `rate`, `open`, `high`, `low`, `close`

**常用货币代码：**

| 代码 | 货币 |
|------|------|
| USD | 美元 |
| CNY | 人民币 |
| EUR | 欧元 |
| JPY | 日元 |
| GBP | 英镑 |
| HKD | 港币 |

---

## 使用示例

### 获取美股数据

```python
import finvista as fv

# 获取苹果公司日线
df = fv.get_us_stock_daily("AAPL", start_date="2024-01-01")

# 获取实时行情
df = fv.get_us_stock_quote(["AAPL", "MSFT", "GOOGL"])

# 获取公司信息
info = fv.get_us_stock_info("AAPL")
```

### 获取指数数据

```python
# 标普 500
df = fv.get_us_index_daily("SPX", start_date="2024-01-01")

# 恒生指数
df = fv.get_hk_index_daily("HSI", start_date="2024-01-01")
```

### 获取汇率

```python
# 实时汇率
df = fv.get_exchange_rate("USD", "CNY")
print(f"美元兑人民币: {df['rate'].iloc[0]}")

# 历史汇率
df = fv.get_exchange_rate_history("USD", "CNY", start_date="2024-01-01")
```
