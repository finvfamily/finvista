# 龙虎榜数据

A 股龙虎榜数据获取指南。

## 龙虎榜列表

```python
import finvista as fv

# 获取最新龙虎榜
df = fv.get_cn_lhb_list()

# 获取指定日期
df = fv.get_cn_lhb_list(date="2024-01-15")
```

### 返回字段

| 字段 | 说明 |
|------|------|
| `date` | 交易日期 |
| `symbol` | 股票代码 |
| `name` | 股票名称 |
| `close` | 收盘价 |
| `change_pct` | 涨跌幅 |
| `turnover_rate` | 换手率 |
| `net_buy` | 净买入额 |
| `reason` | 上榜原因 |

## 交易明细

```python
# 获取某股票龙虎榜交易明细
df = fv.get_cn_lhb_detail("000001", "2024-01-15")
```

### 返回字段

| 字段 | 说明 |
|------|------|
| `rank` | 排名 |
| `trader` | 营业部名称 |
| `buy_amount` | 买入金额 |
| `sell_amount` | 卖出金额 |
| `net_amount` | 净买入金额 |

## 机构买卖

```python
# 获取最新机构交易
df = fv.get_cn_lhb_institution()

# 获取指定日期
df = fv.get_cn_lhb_institution(date="2024-01-15")
```

### 返回字段

| 字段 | 说明 |
|------|------|
| `date` | 交易日期 |
| `symbol` | 股票代码 |
| `name` | 股票名称 |
| `inst_buy` | 机构买入额 |
| `inst_sell` | 机构卖出额 |
| `inst_net` | 机构净买入 |

## 使用示例

### 筛选机构买入

```python
# 获取龙虎榜
df = fv.get_cn_lhb_list()

# 筛选机构净买入
inst = fv.get_cn_lhb_institution()
inst_buy = inst[inst['inst_net'] > 0]
print(f"机构净买入股票数: {len(inst_buy)}")
```

### 分析游资席位

```python
# 获取交易明细
df = fv.get_cn_lhb_detail("000001", "2024-01-15")

# 统计营业部
from collections import Counter
traders = df['trader'].tolist()
counter = Counter(traders)
print("活跃营业部:", counter.most_common(5))
```

### 追踪知名游资

```python
# 定义知名游资营业部
famous_traders = [
    "华泰证券深圳益田路",
    "东方财富拉萨团结路",
    "中信证券上海分公司",
]

# 获取龙虎榜数据
lhb = fv.get_cn_lhb_list()

# 查找知名游资参与的股票
for _, row in lhb.iterrows():
    detail = fv.get_cn_lhb_detail(row['symbol'], row['date'])
    for trader in famous_traders:
        if trader in detail['trader'].values:
            print(f"{row['symbol']} {row['name']}: {trader}")
```

### 龙虎榜选股策略

```python
# 获取近期龙虎榜
lhb = fv.get_cn_lhb_list()

# 筛选条件
# 1. 涨停（涨幅 > 9.5%）
# 2. 机构净买入
inst = fv.get_cn_lhb_institution()
inst_buy_symbols = set(inst[inst['inst_net'] > 0]['symbol'])

candidates = lhb[
    (lhb['change_pct'] > 9.5) &
    (lhb['symbol'].isin(inst_buy_symbols))
]
print("涨停+机构买入:")
print(candidates[['symbol', 'name', 'change_pct']])
```

### 统计上榜频率

```python
import pandas as pd
from datetime import datetime, timedelta

# 获取最近 5 个交易日的龙虎榜
all_lhb = []
for i in range(5):
    date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
    try:
        df = fv.get_cn_lhb_list(date=date)
        all_lhb.append(df)
    except:
        continue

combined = pd.concat(all_lhb, ignore_index=True)

# 统计上榜次数
freq = combined['symbol'].value_counts()
print("近期频繁上榜股票:")
print(freq.head(10))
```

## 龙虎榜规则

### 上榜条件

1. **日涨跌幅偏离值 ≥ 7%**
2. **日振幅 ≥ 15%**
3. **日换手率 ≥ 20%**
4. **连续三日涨跌幅偏离值 ≥ 20%**

### 信息披露

- 买入/卖出金额前 5 名营业部
- 机构专用席位单独列示
- T+1 日收盘后公布

!!! tip "投资提示"
    - 关注机构席位的买入情况
    - 知名游资席位可作为短线参考
    - 结合成交量和换手率综合判断
