# 股东数据

A 股上市公司股东数据获取指南。

## 前十大股东

```python
import finvista as fv

# 获取最新前十大股东
df = fv.get_cn_top_shareholders("000001")

# 获取指定报告期
df = fv.get_cn_top_shareholders("000001", period="2023-12-31")
```

### 返回字段

| 字段 | 说明 |
|------|------|
| `rank` | 排名 |
| `holder_name` | 股东名称 |
| `hold_amount` | 持股数量（股） |
| `hold_ratio` | 持股比例 (%) |
| `holder_type` | 股东类型 |
| `change` | 变动数量 |
| `report_date` | 报告期 |

## 股权质押

```python
df = fv.get_cn_stock_pledge("000001")
```

### 返回字段

| 字段 | 说明 |
|------|------|
| `pledge_date` | 质押日期 |
| `pledger` | 质押方 |
| `pledgee` | 质权人 |
| `pledge_amount` | 质押数量 |
| `pledge_ratio` | 质押比例 |
| `status` | 状态（质押中/解除） |

## 限售解禁

```python
# 获取一段时间内的解禁计划
df = fv.get_cn_stock_unlock_schedule("2024-01-01", "2024-01-31")
```

### 返回字段

| 字段 | 说明 |
|------|------|
| `unlock_date` | 解禁日期 |
| `symbol` | 股票代码 |
| `name` | 股票名称 |
| `unlock_amount` | 解禁数量 |
| `unlock_ratio` | 解禁比例 (%) |
| `unlock_value` | 解禁市值 |

## 使用示例

### 分析股东变化

```python
df = fv.get_cn_top_shareholders("000001")

# 计算前十大股东合计持股
total_ratio = df['hold_ratio'].sum()
print(f"前十大股东合计持股: {total_ratio:.2f}%")

# 找出增持股东
increase = df[df['change'] > 0]
print("增持股东:")
print(increase[['holder_name', 'change']])
```

### 筛选高质押风险股

```python
# 获取股权质押
df = fv.get_cn_stock_pledge("000001")

# 计算质押比例
total_pledge = df[df['status'] == '质押中']['pledge_ratio'].sum()
print(f"当前质押比例: {total_pledge:.2f}%")

# 高风险标准：质押比例 > 50%
if total_pledge > 50:
    print("警告: 质押比例较高!")
```

### 解禁日历

```python
import pandas as pd

# 获取本月解禁
df = fv.get_cn_stock_unlock_schedule("2024-01-01", "2024-01-31")

# 按解禁市值排序
df_sorted = df.sort_values('unlock_value', ascending=False)
print("本月解禁市值前 10:")
print(df_sorted.head(10)[['symbol', 'name', 'unlock_date', 'unlock_value']])

# 按日期汇总
daily_unlock = df.groupby('unlock_date')['unlock_value'].sum()
print("\\n每日解禁市值:")
print(daily_unlock)
```

### 机构持股分析

```python
df = fv.get_cn_top_shareholders("000001")

# 筛选机构投资者
institutions = df[df['holder_type'].isin(['基金', '社保', 'QFII', '保险'])]
inst_ratio = institutions['hold_ratio'].sum()
print(f"机构持股比例: {inst_ratio:.2f}%")
```

### 股东集中度

```python
df = fv.get_cn_top_shareholders("000001")

# 计算 CR5（前 5 大股东集中度）
cr5 = df.head(5)['hold_ratio'].sum()
print(f"CR5: {cr5:.2f}%")

# 计算 CR10
cr10 = df['hold_ratio'].sum()
print(f"CR10: {cr10:.2f}%")

# 第一大股东占比
first_holder_ratio = df.iloc[0]['hold_ratio']
print(f"第一大股东: {first_holder_ratio:.2f}%")
```

### 批量筛选解禁

```python
# 获取下个月大额解禁股票
df = fv.get_cn_stock_unlock_schedule("2024-02-01", "2024-02-29")

# 筛选解禁比例 > 5% 的股票
large_unlock = df[df['unlock_ratio'] > 5]
print(f"大额解禁股票数: {len(large_unlock)}")
print(large_unlock[['symbol', 'name', 'unlock_date', 'unlock_ratio']])
```

## 数据说明

### 股东类型

| 类型 | 说明 |
|------|------|
| 个人 | 自然人股东 |
| 国有 | 国有法人/国资委 |
| 基金 | 公募基金 |
| 社保 | 社保基金 |
| QFII | 合格境外机构投资者 |
| 保险 | 保险资金 |
| 券商 | 证券公司 |

!!! tip "投资提示"
    - 关注大股东减持公告
    - 高质押股票在市场下跌时风险较大
    - 解禁前后股价可能有波动
