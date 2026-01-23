# A 股数据

A 股数据获取完整指南。

## 日线数据

### 基本用法

```python
import finvista as fv

# 获取日线数据
df = fv.get_cn_stock_daily("000001", start_date="2024-01-01")
```

### 参数说明

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `symbol` | str | 是 | 股票代码（如 "000001"） |
| `start_date` | str | 否 | 开始日期（YYYY-MM-DD） |
| `end_date` | str | 否 | 结束日期（YYYY-MM-DD） |
| `source` | str | 否 | 强制指定数据源 |

### 返回字段

| 字段 | 说明 |
|------|------|
| `date` | 交易日期 |
| `open` | 开盘价 |
| `high` | 最高价 |
| `low` | 最低价 |
| `close` | 收盘价 |
| `volume` | 成交量 |
| `amount` | 成交额 |

## 实时行情

```python
# 单只股票
df = fv.get_cn_stock_quote("000001")

# 多只股票
df = fv.get_cn_stock_quote(["000001", "600519", "000858"])
```

### 返回字段

| 字段 | 说明 |
|------|------|
| `symbol` | 股票代码 |
| `name` | 股票名称 |
| `price` | 当前价格 |
| `change` | 涨跌额 |
| `change_pct` | 涨跌幅 |
| `open` | 开盘价 |
| `high` | 最高价 |
| `low` | 最低价 |
| `volume` | 成交量 |

## 股票列表

```python
# 主板股票
df = fv.list_cn_stock_symbols(market="main")

# 创业板
df = fv.list_cn_stock_symbols(market="chinext")

# 科创板
df = fv.list_cn_stock_symbols(market="star")

# 全部股票
df = fv.list_cn_stock_symbols()
```

## 搜索股票

```python
# 按关键字搜索
df = fv.search_cn_stock("银行")

# 按代码前缀搜索
df = fv.search_cn_stock("600")
```

## 数据源

| 优先级 | 数据源 | 速度 | 稳定性 |
|--------|--------|------|--------|
| 1 | 东方财富 | 快 | 高 |
| 2 | 新浪 | 中 | 高 |
| 3 | 腾讯 | 中 | 中 |

## 使用示例

### 下载并保存为 CSV

```python
df = fv.get_cn_stock_daily("000001", start_date="2020-01-01")
df.to_csv("000001_daily.csv", index=False)
```

### 计算移动均线

```python
import pandas as pd

df = fv.get_cn_stock_daily("000001", start_date="2024-01-01")
df['MA5'] = df['close'].rolling(5).mean()
df['MA20'] = df['close'].rolling(20).mean()
```

### 批量获取多只股票

```python
symbols = ["000001", "600519", "000858"]
data = {}

for symbol in symbols:
    data[symbol] = fv.get_cn_stock_daily(symbol, start_date="2024-01-01")
```
