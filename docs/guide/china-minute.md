# 分钟线数据

A 股分钟级 K 线数据获取指南。

## 基本用法

```python
import finvista as fv

# 获取 5 分钟 K 线（最近 5 天）
df = fv.get_cn_stock_minute("000001", period="5", days=5)
```

## 参数说明

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `symbol` | str | 是 | 股票代码 |
| `period` | str | 否 | K 线周期，默认 "5" |
| `days` | int | 否 | 获取天数，默认 5 |

### 支持的周期

| 周期 | 说明 |
|------|------|
| "1" | 1 分钟 K 线 |
| "5" | 5 分钟 K 线 |
| "15" | 15 分钟 K 线 |
| "30" | 30 分钟 K 线 |
| "60" | 60 分钟 K 线 |

## 返回字段

| 字段 | 说明 |
|------|------|
| `datetime` | 时间戳 |
| `open` | 开盘价 |
| `high` | 最高价 |
| `low` | 最低价 |
| `close` | 收盘价 |
| `volume` | 成交量 |
| `amount` | 成交额 |

## 使用示例

### 获取不同周期数据

```python
# 1 分钟 K 线（日内交易）
df_1min = fv.get_cn_stock_minute("000001", period="1", days=1)

# 5 分钟 K 线
df_5min = fv.get_cn_stock_minute("000001", period="5", days=5)

# 15 分钟 K 线
df_15min = fv.get_cn_stock_minute("000001", period="15", days=5)

# 30 分钟 K 线
df_30min = fv.get_cn_stock_minute("000001", period="30", days=10)

# 60 分钟 K 线
df_60min = fv.get_cn_stock_minute("000001", period="60", days=20)
```

### 日内交易分析

```python
# 获取今日 1 分钟数据
df = fv.get_cn_stock_minute("000001", period="1", days=1)

# 找出最高价和最低价时间
max_idx = df['high'].idxmax()
min_idx = df['low'].idxmin()

print(f"最高价时间: {df.loc[max_idx, 'datetime']}")
print(f"最低价时间: {df.loc[min_idx, 'datetime']}")
```

### 计算分钟级指标

```python
df = fv.get_cn_stock_minute("000001", period="5", days=5)

# 计算 MACD
import pandas as pd

exp12 = df['close'].ewm(span=12).mean()
exp26 = df['close'].ewm(span=26).mean()
df['macd'] = exp12 - exp26
df['signal'] = df['macd'].ewm(span=9).mean()
df['histogram'] = df['macd'] - df['signal']
```

### 成交量分析

```python
df = fv.get_cn_stock_minute("000001", period="5", days=1)

# 计算平均成交量
avg_volume = df['volume'].mean()

# 找出放量时段
high_volume = df[df['volume'] > avg_volume * 2]
print(f"放量时段数: {len(high_volume)}")
```

### 波动率计算

```python
df = fv.get_cn_stock_minute("000001", period="5", days=5)

# 计算收益率
df['return'] = df['close'].pct_change()

# 计算波动率（年化）
volatility = df['return'].std() * (252 * 48) ** 0.5  # 假设每天 48 个 5 分钟
print(f"年化波动率: {volatility:.2%}")
```

### 批量获取

```python
symbols = ["000001", "600519", "000858"]
minute_data = {}

for symbol in symbols:
    minute_data[symbol] = fv.get_cn_stock_minute(symbol, period="5", days=1)
```

## 注意事项

!!! warning "数据量提示"
    分钟级数据量较大，建议：

    - 1 分钟数据仅获取 1-2 天
    - 5 分钟数据建议 5-10 天
    - 适当使用缓存减少重复请求

!!! note "交易时间"
    A 股交易时间：

    - 上午：09:30 - 11:30
    - 下午：13:00 - 15:00
    - 每天约 240 分钟交易时间
