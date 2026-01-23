# 可转债数据

中国可转债市场数据获取指南。

## 可转债列表

```python
import finvista as fv

# 获取所有可转债
df = fv.list_cn_convertible_symbols()
```

### 返回字段

| 字段 | 说明 |
|------|------|
| `symbol` | 可转债代码 |
| `name` | 可转债名称 |
| `stock_symbol` | 正股代码 |
| `stock_name` | 正股名称 |
| `list_date` | 上市日期 |
| `maturity_date` | 到期日期 |

## 日线数据

```python
# 获取可转债日线
df = fv.get_cn_convertible_daily("113008", start_date="2024-01-01")
```

### 参数说明

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `symbol` | str | 是 | 可转债代码 |
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

## 可转债信息

```python
info = fv.get_cn_convertible_info("113008")
```

### 返回字段

| 字段 | 说明 |
|------|------|
| `symbol` | 可转债代码 |
| `name` | 可转债名称 |
| `stock_symbol` | 正股代码 |
| `convert_price` | 转股价格 |
| `convert_value` | 转股价值 |
| `premium_rate` | 转股溢价率 |
| `ytm` | 到期收益率 |
| `rating` | 债券评级 |
| `issue_size` | 发行规模 |
| `maturity_date` | 到期日期 |

## 使用示例

### 筛选低溢价转债

```python
# 获取所有可转债
bonds = fv.list_cn_convertible_symbols()

low_premium = []
for _, row in bonds.iterrows():
    info = fv.get_cn_convertible_info(row['symbol'])
    if info.get('premium_rate', 100) < 10:  # 溢价率 < 10%
        low_premium.append(info)

print(f"低溢价转债数量: {len(low_premium)}")
```

### 计算转股价值

```python
# 获取可转债信息
info = fv.get_cn_convertible_info("113008")
convert_price = info['convert_price']

# 获取正股价格
stock_symbol = info['stock_symbol']
quote = fv.get_cn_stock_quote(stock_symbol)
stock_price = quote['price'].iloc[0]

# 计算转股价值
convert_value = stock_price / convert_price * 100
print(f"转股价值: {convert_value:.2f} 元")
```

### 双低策略

```python
bonds = fv.list_cn_convertible_symbols()

double_low = []
for _, row in bonds.head(50).iterrows():
    info = fv.get_cn_convertible_info(row['symbol'])
    quote = fv.get_cn_stock_quote(row['symbol'].replace('11', 'SH').replace('12', 'SZ'))

    price = quote['price'].iloc[0] if not quote.empty else 0
    premium = info.get('premium_rate', 100)

    # 双低 = 价格 + 溢价率
    double_low_score = price + premium
    if double_low_score < 130:  # 双低值 < 130
        double_low.append({
            'symbol': row['symbol'],
            'name': row['name'],
            'price': price,
            'premium': premium,
            'score': double_low_score
        })

# 按双低值排序
import pandas as pd
df = pd.DataFrame(double_low).sort_values('score')
print(df.head(10))
```

### 正股联动分析

```python
# 获取转债和正股数据
bond = fv.get_cn_convertible_daily("113008", start_date="2024-01-01")
info = fv.get_cn_convertible_info("113008")
stock = fv.get_cn_stock_daily(info['stock_symbol'], start_date="2024-01-01")

# 合并计算相关性
import pandas as pd
merged = pd.merge(bond, stock, on='date', suffixes=('_bond', '_stock'))
corr = merged['close_bond'].corr(merged['close_stock'])
print(f"转债与正股相关性: {corr:.2f}")
```

## 投资提示

!!! warning "风险提示"
    可转债投资需注意：

    - 信用风险：关注发行人评级
    - 强赎风险：正股涨幅过大可能触发强赎
    - 回售风险：正股跌幅过大的回售条款
    - 流动性风险：部分转债成交量较小

!!! tip "常用指标"
    - **转股溢价率**：越低越好，表示转股价值高
    - **到期收益率**：越高安全边际越大
    - **双低值**：价格+溢价率，越低越安全
