# 期货数据

中国期货市场数据获取指南。

## 合约列表

```python
import finvista as fv

# 获取所有期货合约
df = fv.list_cn_futures_symbols()

# 按交易所筛选
df = fv.list_cn_futures_symbols(exchange="CFFEX")  # 中金所
df = fv.list_cn_futures_symbols(exchange="SHFE")   # 上期所
df = fv.list_cn_futures_symbols(exchange="DCE")    # 大商所
df = fv.list_cn_futures_symbols(exchange="CZCE")   # 郑商所
df = fv.list_cn_futures_symbols(exchange="INE")    # 上期能源
```

### 交易所说明

| 代码 | 名称 | 主要品种 |
|------|------|----------|
| CFFEX | 中国金融期货交易所 | 股指期货、国债期货 |
| SHFE | 上海期货交易所 | 金属、能源 |
| DCE | 大连商品交易所 | 农产品、化工 |
| CZCE | 郑州商品交易所 | 农产品、化工 |
| INE | 上海国际能源交易中心 | 原油、20号胶 |

## 日线数据

```python
# 获取股指期货日线
df = fv.get_cn_futures_daily("IF2401", start_date="2024-01-01")

# 获取商品期货
df = fv.get_cn_futures_daily("RB2401", start_date="2024-01-01")
```

### 参数说明

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `symbol` | str | 是 | 合约代码（如 "IF2401"） |
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
| `amount` | 成交额 |
| `open_interest` | 持仓量 |
| `settle` | 结算价 |

## 持仓排名

```python
# 获取股指期货持仓排名
df = fv.get_cn_futures_positions("IF")

# 获取指定日期
df = fv.get_cn_futures_positions("IF", date="2024-01-15")
```

### 返回字段

| 字段 | 说明 |
|------|------|
| `rank` | 排名 |
| `broker` | 期货公司 |
| `long_position` | 多单持仓 |
| `long_change` | 多单增减 |
| `short_position` | 空单持仓 |
| `short_change` | 空单增减 |

## 使用示例

### 主力合约分析

```python
# 获取 IF 当月合约
df = fv.get_cn_futures_daily("IF2401", start_date="2024-01-01")

# 计算基差
index = fv.get_cn_index_daily("000300", start_date="2024-01-01")
import pandas as pd
merged = pd.merge(df, index, on='date', suffixes=('_fut', '_idx'))
merged['basis'] = merged['close_fut'] - merged['close_idx']
```

### 持仓分析

```python
df = fv.get_cn_futures_positions("IF")

# 计算多空比
total_long = df['long_position'].sum()
total_short = df['short_position'].sum()
ratio = total_long / total_short
print(f"多空比: {ratio:.2f}")

# 前 5 大席位
top5 = df.head(5)
print(top5[['broker', 'long_position', 'short_position']])
```

### 品种筛选

```python
# 获取所有合约
all_contracts = fv.list_cn_futures_symbols()

# 筛选股指期货
index_futures = all_contracts[all_contracts['symbol'].str.startswith(('IF', 'IH', 'IC', 'IM'))]

# 筛选螺纹钢
rebar = all_contracts[all_contracts['symbol'].str.startswith('RB')]
```

### 跨期价差

```python
# 获取近月和远月合约
near = fv.get_cn_futures_daily("IF2401", start_date="2024-01-01")
far = fv.get_cn_futures_daily("IF2403", start_date="2024-01-01")

# 计算价差
import pandas as pd
merged = pd.merge(near, far, on='date', suffixes=('_near', '_far'))
merged['spread'] = merged['close_near'] - merged['close_far']
```

## 主要品种代码

### 股指期货

| 代码 | 名称 |
|------|------|
| IF | 沪深300股指期货 |
| IH | 上证50股指期货 |
| IC | 中证500股指期货 |
| IM | 中证1000股指期货 |

### 商品期货

| 代码 | 名称 | 交易所 |
|------|------|--------|
| AU | 黄金 | SHFE |
| AG | 白银 | SHFE |
| CU | 铜 | SHFE |
| RB | 螺纹钢 | SHFE |
| SC | 原油 | INE |
| I | 铁矿石 | DCE |
| M | 豆粕 | DCE |
| CF | 棉花 | CZCE |
