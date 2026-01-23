# 资金流向

A 股资金流向数据获取指南。

## 个股资金流向

### 历史资金流向

```python
import finvista as fv

# 获取近 30 天资金流向
df = fv.get_cn_stock_moneyflow("000001", days=30)

# 获取近 60 天
df = fv.get_cn_stock_moneyflow("000001", days=60)
```

### 参数说明

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `symbol` | str | 是 | 股票代码 |
| `days` | int | 否 | 获取天数，默认 30 |

### 返回字段

| 字段 | 说明 |
|------|------|
| `date` | 交易日期 |
| `main_net_inflow` | 主力净流入 |
| `main_net_inflow_pct` | 主力净流入占比 |
| `super_large_net_inflow` | 超大单净流入 |
| `large_net_inflow` | 大单净流入 |
| `medium_net_inflow` | 中单净流入 |
| `small_net_inflow` | 小单净流入 |

### 实时资金流向

```python
df = fv.get_cn_stock_moneyflow_realtime("000001")
```

## 行业资金流向

```python
# 获取最新行业资金流向
df = fv.get_cn_industry_moneyflow()

# 获取指定日期
df = fv.get_cn_industry_moneyflow(date="2024-01-15")
```

### 返回字段

| 字段 | 说明 |
|------|------|
| `industry` | 行业名称 |
| `main_net_inflow` | 主力净流入 |
| `change_pct` | 涨跌幅 |
| `leading_stock` | 领涨股 |

## 使用示例

### 分析主力动向

```python
df = fv.get_cn_stock_moneyflow("000001", days=30)

# 统计主力净流入天数
inflow_days = (df['main_net_inflow'] > 0).sum()
print(f"近 30 天主力净流入天数: {inflow_days}")

# 计算累计净流入
total_inflow = df['main_net_inflow'].sum()
print(f"累计主力净流入: {total_inflow/1e8:.2f} 亿元")
```

### 判断资金趋势

```python
df = fv.get_cn_stock_moneyflow("000001", days=30)

# 计算 5 日移动平均
df['ma5'] = df['main_net_inflow'].rolling(5).mean()

# 判断趋势
if df['ma5'].iloc[0] > df['ma5'].iloc[4]:
    print("主力资金呈流入趋势")
else:
    print("主力资金呈流出趋势")
```

### 筛选行业资金流入

```python
df = fv.get_cn_industry_moneyflow()

# 筛选主力净流入前 10 的行业
top_inflow = df.nlargest(10, 'main_net_inflow')
print(top_inflow[['industry', 'main_net_inflow', 'change_pct']])
```

### 资金与价格关系

```python
# 获取股价和资金流向
price = fv.get_cn_stock_daily("000001", start_date="2024-01-01")
flow = fv.get_cn_stock_moneyflow("000001", days=30)

# 合并数据
import pandas as pd
merged = pd.merge(price, flow, on='date')

# 计算相关性
corr = merged['close'].corr(merged['main_net_inflow'])
print(f"股价与主力资金相关性: {corr:.2f}")
```

### 批量获取资金数据

```python
symbols = ["000001", "600519", "000858"]
flows = {}

for symbol in symbols:
    flows[symbol] = fv.get_cn_stock_moneyflow(symbol, days=5)

# 比较主力资金
for symbol, df in flows.items():
    total = df['main_net_inflow'].sum()
    print(f"{symbol}: {total/1e8:.2f} 亿元")
```
