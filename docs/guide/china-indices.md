# 指数数据

中国市场指数数据获取指南。

## 日线数据

```python
import finvista as fv

# 获取沪深 300 指数
df = fv.get_cn_index_daily("000300", start_date="2024-01-01")

# 获取上证指数
df = fv.get_cn_index_daily("000001", start_date="2024-01-01")
```

### 参数说明

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `symbol` | str | 是 | 指数代码 |
| `start_date` | str | 否 | 开始日期 |
| `end_date` | str | 否 | 结束日期 |

## 实时行情

```python
# 获取多个指数的实时行情
df = fv.get_cn_index_quote(["000001", "399001", "000300"])
```

## 主要指数列表

```python
df = fv.list_cn_major_indices()
```

返回主要指数信息：

| 代码 | 名称 |
|------|------|
| 000001 | 上证指数 |
| 399001 | 深证成指 |
| 000300 | 沪深300 |
| 000016 | 上证50 |
| 000905 | 中证500 |
| 399006 | 创业板指 |

## 指数成分股

```python
# 获取沪深 300 成分股
df = fv.get_cn_index_constituents("000300")
```

### 返回字段

| 字段 | 说明 |
|------|------|
| `symbol` | 成分股代码 |
| `name` | 成分股名称 |
| `weight` | 权重（如有） |

## 指数权重

```python
# 获取成分股权重
df = fv.get_cn_index_weights("000300")
```

### 返回字段

| 字段 | 说明 |
|------|------|
| `symbol` | 成分股代码 |
| `name` | 成分股名称 |
| `weight` | 权重比例 (%) |

## 使用示例

### 绘制指数走势

```python
import matplotlib.pyplot as plt

df = fv.get_cn_index_daily("000300", start_date="2024-01-01")
plt.plot(df['date'], df['close'])
plt.title("沪深 300 指数走势")
plt.show()
```

### 计算指数收益率

```python
df = fv.get_cn_index_daily("000300", start_date="2024-01-01")
df['return'] = df['close'].pct_change()
print(f"年化收益率: {df['return'].mean() * 252:.2%}")
```

### 比较多个指数

```python
indices = ["000001", "399001", "000300"]
data = {}

for idx in indices:
    data[idx] = fv.get_cn_index_daily(idx, start_date="2024-01-01")
```
