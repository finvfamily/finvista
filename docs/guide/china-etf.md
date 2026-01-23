# ETF 数据

A 股 ETF 增强数据获取指南。

## 份额变动

```python
import finvista as fv

# 获取 50ETF 份额变动（近 30 天）
df = fv.get_cn_etf_share_change("510050", days=30)

# 获取更长时间
df = fv.get_cn_etf_share_change("510050", days=60)
```

### 参数说明

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `symbol` | str | 是 | ETF 代码 |
| `days` | int | 否 | 获取天数，默认 30 |

### 返回字段

| 字段 | 说明 |
|------|------|
| `date` | 日期 |
| `shares` | 总份额（亿份） |
| `share_change` | 份额变动 |
| `share_change_pct` | 变动比例 (%) |

## 折溢价

```python
# 获取 ETF 折溢价
df = fv.get_cn_etf_premium_discount("510050")
```

### 返回字段

| 字段 | 说明 |
|------|------|
| `date` | 日期 |
| `price` | 市场价格 |
| `nav` | 净值 |
| `premium` | 溢价率 (%) |
| `discount` | 折价率 (%) |

## 使用示例

### 分析资金流向

```python
df = fv.get_cn_etf_share_change("510050", days=30)

# 统计净申购/净赎回
net_change = df['share_change'].sum()
if net_change > 0:
    print(f"近 30 天净申购: {net_change:.2f} 亿份")
else:
    print(f"近 30 天净赎回: {abs(net_change):.2f} 亿份")

# 计算累计变动
df['cumulative_change'] = df['share_change'].cumsum()
```

### 折溢价套利判断

```python
df = fv.get_cn_etf_premium_discount("510050")

# 获取最新数据
latest = df.iloc[0]
premium = latest['premium']

if premium > 0.5:
    print(f"溢价 {premium:.2f}%，可考虑申购套利")
elif premium < -0.5:
    print(f"折价 {abs(premium):.2f}%，可考虑赎回套利")
else:
    print("无明显套利机会")
```

### 比较多只 ETF

```python
etfs = ["510050", "510300", "510500"]
share_data = {}

for etf in etfs:
    df = fv.get_cn_etf_share_change(etf, days=30)
    share_data[etf] = df['share_change'].sum()

# 按净申购排序
import pandas as pd
result = pd.Series(share_data).sort_values(ascending=False)
print("近 30 天净申购排名:")
print(result)
```

### ETF 规模变化趋势

```python
import matplotlib.pyplot as plt

df = fv.get_cn_etf_share_change("510050", days=60)

plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plt.plot(df['date'], df['shares'])
plt.title("50ETF 总份额")
plt.ylabel("份额（亿份）")

plt.subplot(2, 1, 2)
plt.bar(df['date'], df['share_change'])
plt.title("每日份额变动")
plt.ylabel("变动（亿份）")
plt.tight_layout()
plt.show()
```

### 结合行情分析

```python
# 获取 ETF 份额和价格
shares = fv.get_cn_etf_share_change("510050", days=30)
price = fv.get_cn_stock_daily("510050", start_date="2024-01-01")

import pandas as pd
merged = pd.merge(shares, price, on='date')

# 分析价格与份额的关系
corr = merged['close'].corr(merged['share_change'])
print(f"价格与份额变动相关性: {corr:.2f}")
```

## 主要 ETF 代码

### 宽基指数

| 代码 | 名称 | 标的指数 |
|------|------|----------|
| 510050 | 华夏上证50ETF | 上证50 |
| 510300 | 华泰柏瑞沪深300ETF | 沪深300 |
| 510500 | 南方中证500ETF | 中证500 |
| 159915 | 易方达创业板ETF | 创业板指 |
| 588000 | 华夏上证科创板50ETF | 科创50 |

### 行业/主题

| 代码 | 名称 | 主题 |
|------|------|------|
| 512880 | 国泰中证全指证券公司ETF | 证券 |
| 512690 | 鹏华中证酒ETF | 白酒 |
| 515790 | 华宝中证银行ETF | 银行 |
| 512760 | 国泰中证半导体芯片ETF | 芯片 |
| 515030 | 华夏中证新能源汽车ETF | 新能源车 |

### 跨境 ETF

| 代码 | 名称 | 标的 |
|------|------|------|
| 513050 | 易方达中概互联网ETF | 中概互联 |
| 513500 | 博时标普500ETF | 标普500 |
| 513100 | 国泰纳斯达克100ETF | 纳斯达克100 |

!!! tip "投资提示"
    - ETF 份额增加通常表示资金看好后市
    - 折溢价过大时可能存在套利机会
    - 跨境 ETF 受汇率影响
