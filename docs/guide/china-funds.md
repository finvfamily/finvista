# 基金数据

中国公募基金数据获取指南。

## 净值历史

```python
import finvista as fv

# 获取易方达中小盘混合的净值历史
df = fv.get_cn_fund_nav("110011", start_date="2024-01-01")
```

### 参数说明

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `symbol` | str | 是 | 基金代码 |
| `start_date` | str | 否 | 开始日期 |
| `end_date` | str | 否 | 结束日期 |

### 返回字段

| 字段 | 说明 |
|------|------|
| `date` | 净值日期 |
| `nav` | 单位净值 |
| `acc_nav` | 累计净值 |
| `change_pct` | 日涨跌幅 |

## 实时估值

```python
# 获取基金实时估值
df = fv.get_cn_fund_quote(["110011", "000001"])
```

## 基金信息

```python
info = fv.get_cn_fund_info("110011")
```

### 返回字段

| 字段 | 说明 |
|------|------|
| `name` | 基金名称 |
| `type` | 基金类型 |
| `manager` | 基金经理 |
| `company` | 基金公司 |
| `size` | 基金规模 |
| `inception_date` | 成立日期 |

## 基金列表

```python
# 股票型基金
df = fv.list_cn_fund_symbols(fund_type="stock")

# 债券型基金
df = fv.list_cn_fund_symbols(fund_type="bond")

# 货币型基金
df = fv.list_cn_fund_symbols(fund_type="money")

# 指数基金
df = fv.list_cn_fund_symbols(fund_type="index")

# 全部基金
df = fv.list_cn_fund_symbols()
```

## 搜索基金

```python
# 搜索沪深 300 相关基金
df = fv.search_cn_fund("沪深300")

# 搜索基金公司
df = fv.search_cn_fund("易方达")
```

## 使用示例

### 计算基金收益

```python
df = fv.get_cn_fund_nav("110011", start_date="2024-01-01")
total_return = (df['nav'].iloc[-1] / df['nav'].iloc[0] - 1) * 100
print(f"区间收益率: {total_return:.2f}%")
```

### 比较多只基金

```python
funds = ["110011", "000001", "519300"]
data = {}

for fund in funds:
    data[fund] = fv.get_cn_fund_nav(fund, start_date="2024-01-01")
```

### 筛选优质基金

```python
# 获取所有股票型基金
df = fv.list_cn_fund_symbols(fund_type="stock")

# 获取基金信息并筛选规模大于 10 亿的
large_funds = []
for _, row in df.head(100).iterrows():
    info = fv.get_cn_fund_info(row['symbol'])
    if info.get('size', 0) > 10:
        large_funds.append(info)
```
