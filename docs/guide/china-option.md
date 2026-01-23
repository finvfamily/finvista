# 期权数据

中国期权市场数据获取指南。

## 合约列表

```python
import finvista as fv

# 获取 50ETF 期权合约
df = fv.list_cn_option_contracts("510050")

# 获取沪深 300ETF 期权
df = fv.list_cn_option_contracts("510300")
```

### 返回字段

| 字段 | 说明 |
|------|------|
| `symbol` | 合约代码 |
| `name` | 合约名称 |
| `underlying` | 标的代码 |
| `type` | 期权类型（C/P） |
| `strike` | 行权价 |
| `expiry` | 到期日 |

## 期权行情

```python
# 获取期权实时行情
df = fv.get_cn_option_quote("10004456")
```

### 返回字段

| 字段 | 说明 |
|------|------|
| `symbol` | 合约代码 |
| `price` | 最新价 |
| `change` | 涨跌额 |
| `change_pct` | 涨跌幅 |
| `volume` | 成交量 |
| `open_interest` | 持仓量 |
| `bid` | 买一价 |
| `ask` | 卖一价 |

## 日线数据

```python
df = fv.get_cn_option_daily("10004456", start_date="2024-01-01")
```

### 返回字段

| 字段 | 说明 |
|------|------|
| `date` | 交易日期 |
| `open` | 开盘价 |
| `high` | 最高价 |
| `low` | 最低价 |
| `close` | 收盘价 |
| `settle` | 结算价 |
| `volume` | 成交量 |
| `open_interest` | 持仓量 |

## 使用示例

### 构建 T 型报价

```python
# 获取所有合约
contracts = fv.list_cn_option_contracts("510050")

# 筛选当月合约
import pandas as pd
from datetime import datetime

current_month = datetime.now().strftime("%Y%m")
monthly = contracts[contracts['expiry'].str.contains(current_month)]

# 分离认购和认沽
calls = monthly[monthly['type'] == 'C'].sort_values('strike')
puts = monthly[monthly['type'] == 'P'].sort_values('strike')

# 构建 T 型报价
t_quote = pd.merge(
    calls[['strike', 'symbol']].rename(columns={'symbol': 'call_symbol'}),
    puts[['strike', 'symbol']].rename(columns={'symbol': 'put_symbol'}),
    on='strike'
)
print(t_quote)
```

### 计算隐含波动率（简化）

```python
# 获取期权价格
option = fv.get_cn_option_quote("10004456")
option_price = option['price'].iloc[0]

# 获取标的价格
etf = fv.get_cn_stock_quote("510050")
spot_price = etf['price'].iloc[0]

# 获取合约信息
contracts = fv.list_cn_option_contracts("510050")
contract = contracts[contracts['symbol'] == "10004456"].iloc[0]
strike = contract['strike']

# 简化的隐含波动率估算（实际应使用 Black-Scholes）
moneyness = spot_price / strike - 1
print(f"虚实程度: {moneyness:.2%}")
```

### PCR 比率

```python
contracts = fv.list_cn_option_contracts("510050")

# 获取所有合约行情
total_call_volume = 0
total_put_volume = 0

for _, row in contracts.head(20).iterrows():
    try:
        quote = fv.get_cn_option_quote(row['symbol'])
        if row['type'] == 'C':
            total_call_volume += quote['volume'].iloc[0]
        else:
            total_put_volume += quote['volume'].iloc[0]
    except:
        continue

pcr = total_put_volume / total_call_volume if total_call_volume > 0 else 0
print(f"成交量 PCR: {pcr:.2f}")
```

### 期权策略分析

```python
# 获取平值期权
contracts = fv.list_cn_option_contracts("510050")
etf = fv.get_cn_stock_quote("510050")
spot = etf['price'].iloc[0]

# 找到最接近平值的合约
contracts['atm_diff'] = abs(contracts['strike'] - spot)
atm_call = contracts[contracts['type'] == 'C'].nsmallest(1, 'atm_diff')
atm_put = contracts[contracts['type'] == 'P'].nsmallest(1, 'atm_diff')

print(f"平值认购: {atm_call['symbol'].iloc[0]}")
print(f"平值认沽: {atm_put['symbol'].iloc[0]}")
```

## 可交易标的

### 上交所

| 标的 | 代码 | 说明 |
|------|------|------|
| 50ETF | 510050 | 上证50ETF期权 |
| 300ETF | 510300 | 沪深300ETF期权 |
| 500ETF | 510500 | 中证500ETF期权 |

### 深交所

| 标的 | 代码 | 说明 |
|------|------|------|
| 300ETF | 159919 | 沪深300ETF期权 |
| 创业板ETF | 159915 | 创业板ETF期权 |

### 中金所

| 标的 | 代码 | 说明 |
|------|------|------|
| 沪深300 | IO | 沪深300股指期权 |
| 中证1000 | MO | 中证1000股指期权 |

!!! warning "风险提示"
    期权交易具有杠杆效应，风险较高：

    - 期权可能归零，损失全部权利金
    - 卖方面临无限亏损风险
    - 需要开通期权交易权限
