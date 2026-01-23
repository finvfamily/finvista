# 财务数据

A 股上市公司财务数据获取指南。

## 利润表

```python
import finvista as fv

# 获取年报利润表
df = fv.get_cn_income_statement("000001", period="yearly")

# 获取季报利润表
df = fv.get_cn_income_statement("000001", period="quarterly")
```

### 参数说明

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `symbol` | str | 是 | 股票代码 |
| `period` | str | 否 | "yearly" 或 "quarterly"，默认 "yearly" |

### 主要字段

| 字段 | 说明 |
|------|------|
| `report_date` | 报告期 |
| `revenue` | 营业收入 |
| `operating_profit` | 营业利润 |
| `net_profit` | 净利润 |
| `eps` | 每股收益 |

## 资产负债表

```python
# 获取年报资产负债表
df = fv.get_cn_balance_sheet("000001", period="yearly")
```

### 主要字段

| 字段 | 说明 |
|------|------|
| `report_date` | 报告期 |
| `total_assets` | 总资产 |
| `total_liabilities` | 总负债 |
| `shareholders_equity` | 股东权益 |
| `cash` | 货币资金 |

## 现金流量表

```python
df = fv.get_cn_cash_flow("000001", period="yearly")
```

### 主要字段

| 字段 | 说明 |
|------|------|
| `report_date` | 报告期 |
| `operating_cf` | 经营活动现金流 |
| `investing_cf` | 投资活动现金流 |
| `financing_cf` | 筹资活动现金流 |
| `net_cf` | 现金净增加额 |

## 分红历史

```python
df = fv.get_cn_dividend_history("000001")
```

### 返回字段

| 字段 | 说明 |
|------|------|
| `announce_date` | 公告日期 |
| `ex_date` | 除权除息日 |
| `dividend` | 每股股利 |
| `bonus_shares` | 每股送股 |
| `convert_shares` | 每股转增 |

## 业绩预告

```python
# 获取最新业绩预告
df = fv.get_cn_performance_forecast()

# 获取指定日期的业绩预告
df = fv.get_cn_performance_forecast(date="2024-01-15")
```

### 返回字段

| 字段 | 说明 |
|------|------|
| `symbol` | 股票代码 |
| `name` | 股票名称 |
| `report_date` | 报告期 |
| `type` | 预告类型（预增/预减/扭亏等） |
| `change_pct_min` | 变动幅度下限 (%) |
| `change_pct_max` | 变动幅度上限 (%) |
| `summary` | 业绩摘要 |

## 使用示例

### 分析盈利能力

```python
# 获取三年利润表
df = fv.get_cn_income_statement("000001", period="yearly")

# 计算净利润增长率
df['profit_growth'] = df['net_profit'].pct_change()
print(df[['report_date', 'net_profit', 'profit_growth']])
```

### 计算 ROE

```python
income = fv.get_cn_income_statement("000001")
balance = fv.get_cn_balance_sheet("000001")

# 简化计算
latest_profit = income['net_profit'].iloc[0]
latest_equity = balance['shareholders_equity'].iloc[0]
roe = latest_profit / latest_equity
print(f"ROE: {roe:.2%}")
```

### 筛选高分红股票

```python
# 获取某只股票的分红历史
df = fv.get_cn_dividend_history("601398")

# 计算近 5 年平均股息率
recent = df.head(5)
avg_dividend = recent['dividend'].mean()
print(f"近 5 年平均每股分红: {avg_dividend:.2f} 元")
```

### 业绩预告策略

```python
# 获取业绩预增股票
df = fv.get_cn_performance_forecast()
pre_increase = df[df['type'] == '预增']
print(f"业绩预增股票数: {len(pre_increase)}")
```
