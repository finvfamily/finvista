# 美股数据

美股数据获取指南。

## 日线数据

```python
import finvista as fv

# 获取苹果公司日线数据
df = fv.get_us_stock_daily("AAPL", start_date="2024-01-01")
```

### 参数说明

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `symbol` | str | 是 | 股票代码（如 "AAPL"） |
| `start_date` | str | 否 | 开始日期 |
| `end_date` | str | 否 | 结束日期 |

### 返回字段

| 字段 | 说明 |
|------|------|
| `date` | 交易日期 |
| `open` | 开盘价 |
| `high` | 最高价 |
| `low` | 最低价 |
| `close` | 收盘价 |
| `volume` | 成交量 |
| `adj_close` | 复权价 |

## 实时行情

```python
# 获取多只美股实时行情
df = fv.get_us_stock_quote(["AAPL", "MSFT", "GOOGL"])
```

## 公司信息

```python
info = fv.get_us_stock_info("AAPL")
```

### 返回字段

| 字段 | 说明 |
|------|------|
| `name` | 公司名称 |
| `sector` | 行业板块 |
| `industry` | 细分行业 |
| `market_cap` | 市值 |
| `pe_ratio` | 市盈率 |
| `description` | 公司简介 |

## 搜索股票

```python
# 搜索美股
df = fv.search_us_stock("Apple")
df = fv.search_us_stock("Tesla")
```

## 美股指数

```python
# 标普 500 指数
df = fv.get_us_index_daily("SPX", start_date="2024-01-01")

# 纳斯达克 100 指数
df = fv.get_us_index_daily("NDX", start_date="2024-01-01")

# 道琼斯工业指数
df = fv.get_us_index_daily("DJI", start_date="2024-01-01")
```

## 港股指数

```python
# 恒生指数
df = fv.get_hk_index_daily("HSI", start_date="2024-01-01")
```

## 使用示例

### 下载科技股数据

```python
tech_stocks = ["AAPL", "MSFT", "GOOGL", "AMZN", "META"]
data = {}

for symbol in tech_stocks:
    data[symbol] = fv.get_us_stock_daily(symbol, start_date="2024-01-01")
```

### 计算收益率

```python
df = fv.get_us_stock_daily("AAPL", start_date="2024-01-01")
df['return'] = df['close'].pct_change()
print(f"平均日收益率: {df['return'].mean():.4f}")
print(f"波动率: {df['return'].std():.4f}")
```

### 获取市场概况

```python
# 获取科技巨头行情
df = fv.get_us_stock_quote(["AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA"])
print(df[['symbol', 'name', 'price', 'change_pct']])
```

## 数据源

美股数据来源于 Yahoo Finance，提供：

- 历史日线数据
- 实时行情（延迟约 15 分钟）
- 公司基本信息

!!! note "注意"
    美股实时行情可能有 15 分钟延迟，如需实时数据请使用专业数据源。
