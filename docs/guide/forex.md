# 外汇数据

外汇汇率数据获取指南。

## 实时汇率

```python
import finvista as fv

# 获取美元兑人民币汇率
df = fv.get_exchange_rate("USD", "CNY")

# 获取欧元兑美元
df = fv.get_exchange_rate("EUR", "USD")

# 获取日元兑人民币
df = fv.get_exchange_rate("JPY", "CNY")
```

### 参数说明

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `base` | str | 是 | 基础货币（如 "USD"） |
| `target` | str | 是 | 目标货币（如 "CNY"） |

### 返回字段

| 字段 | 说明 |
|------|------|
| `base` | 基础货币 |
| `target` | 目标货币 |
| `rate` | 汇率 |
| `bid` | 买入价 |
| `ask` | 卖出价 |
| `update_time` | 更新时间 |

## 历史汇率

```python
# 获取历史汇率
df = fv.get_exchange_rate_history("USD", "CNY", start_date="2024-01-01")

# 指定日期范围
df = fv.get_exchange_rate_history(
    "USD", "CNY",
    start_date="2024-01-01",
    end_date="2024-06-30"
)
```

### 返回字段

| 字段 | 说明 |
|------|------|
| `date` | 日期 |
| `rate` | 汇率 |
| `open` | 开盘价 |
| `high` | 最高价 |
| `low` | 最低价 |
| `close` | 收盘价 |

## 使用示例

### 汇率转换

```python
# 获取当前汇率
df = fv.get_exchange_rate("USD", "CNY")
rate = df['rate'].iloc[0]

# 转换金额
usd_amount = 1000
cny_amount = usd_amount * rate
print(f"{usd_amount} USD = {cny_amount:.2f} CNY")
```

### 汇率走势分析

```python
import matplotlib.pyplot as plt

df = fv.get_exchange_rate_history("USD", "CNY", start_date="2024-01-01")

plt.figure(figsize=(12, 6))
plt.plot(df['date'], df['rate'])
plt.title("美元兑人民币汇率走势")
plt.xlabel("日期")
plt.ylabel("汇率")
plt.grid(True)
plt.show()
```

### 多币种比较

```python
currencies = ["USD", "EUR", "JPY", "GBP", "HKD"]
rates = {}

for curr in currencies:
    df = fv.get_exchange_rate(curr, "CNY")
    rates[curr] = df['rate'].iloc[0]

import pandas as pd
result = pd.Series(rates)
print("各币种兑人民币汇率:")
print(result)
```

### 汇率波动分析

```python
df = fv.get_exchange_rate_history("USD", "CNY", start_date="2024-01-01")

# 计算日收益率
df['return'] = df['rate'].pct_change()

# 计算波动率
volatility = df['return'].std() * (252 ** 0.5)
print(f"年化波动率: {volatility:.2%}")

# 计算最大回撤
df['cummax'] = df['rate'].cummax()
df['drawdown'] = (df['rate'] - df['cummax']) / df['cummax']
max_drawdown = df['drawdown'].min()
print(f"最大回撤: {max_drawdown:.2%}")
```

### 交叉汇率计算

```python
# 计算欧元兑日元（通过美元）
eur_usd = fv.get_exchange_rate("EUR", "USD")['rate'].iloc[0]
usd_jpy = fv.get_exchange_rate("USD", "JPY")['rate'].iloc[0]

eur_jpy = eur_usd * usd_jpy
print(f"EUR/JPY = {eur_jpy:.2f}")
```

### 汇率预警

```python
import time

def monitor_rate(base, target, threshold_low, threshold_high):
    """监控汇率变动"""
    while True:
        df = fv.get_exchange_rate(base, target)
        rate = df['rate'].iloc[0]

        if rate < threshold_low:
            print(f"警告: {base}/{target} 跌破 {threshold_low}，当前 {rate}")
        elif rate > threshold_high:
            print(f"警告: {base}/{target} 突破 {threshold_high}，当前 {rate}")
        else:
            print(f"{base}/{target} = {rate}")

        time.sleep(60)  # 每分钟检查一次

# 使用示例（需手动停止）
# monitor_rate("USD", "CNY", 7.0, 7.3)
```

## 主要货币代码

| 代码 | 货币名称 |
|------|----------|
| USD | 美元 |
| CNY | 人民币 |
| EUR | 欧元 |
| JPY | 日元 |
| GBP | 英镑 |
| HKD | 港币 |
| AUD | 澳元 |
| CAD | 加元 |
| CHF | 瑞士法郎 |
| SGD | 新加坡元 |
| KRW | 韩元 |

## 数据来源

外汇数据来自东方财富，提供：

- 主要货币对实时汇率
- 历史汇率数据
- 买入价和卖出价

!!! note "注意事项"
    - 汇率数据可能有延迟
    - 实际交易汇率以银行报价为准
    - 人民币汇率受政策影响较大
