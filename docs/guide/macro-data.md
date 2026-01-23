# 宏观数据

中国宏观经济数据获取指南。

## GDP 数据

```python
import finvista as fv

df = fv.get_cn_macro_gdp()
```

### 返回字段

| 字段 | 说明 |
|------|------|
| `date` | 统计日期 |
| `gdp` | GDP 总量（亿元） |
| `gdp_yoy` | GDP 同比增速 (%) |

## CPI 数据

```python
df = fv.get_cn_macro_cpi()
```

### 返回字段

| 字段 | 说明 |
|------|------|
| `date` | 统计月份 |
| `cpi` | CPI 指数 |
| `cpi_yoy` | CPI 同比 (%) |
| `cpi_mom` | CPI 环比 (%) |

## PPI 数据

```python
df = fv.get_cn_macro_ppi()
```

### 返回字段

| 字段 | 说明 |
|------|------|
| `date` | 统计月份 |
| `ppi` | PPI 指数 |
| `ppi_yoy` | PPI 同比 (%) |

## PMI 数据

```python
df = fv.get_cn_macro_pmi()
```

### 返回字段

| 字段 | 说明 |
|------|------|
| `date` | 统计月份 |
| `pmi` | 制造业 PMI |
| `pmi_non_mfg` | 非制造业 PMI |

## 货币供应量

```python
df = fv.get_cn_macro_money_supply()
```

### 返回字段

| 字段 | 说明 |
|------|------|
| `date` | 统计月份 |
| `m0` | M0（流通中货币） |
| `m0_yoy` | M0 同比 (%) |
| `m1` | M1（狭义货币） |
| `m1_yoy` | M1 同比 (%) |
| `m2` | M2（广义货币） |
| `m2_yoy` | M2 同比 (%) |

## 社会融资

```python
df = fv.get_cn_macro_social_financing()
```

### 返回字段

| 字段 | 说明 |
|------|------|
| `date` | 统计月份 |
| `total` | 社融规模增量 |
| `loan` | 人民币贷款 |
| `bond` | 企业债券 |

## 使用示例

### 绘制 GDP 增速趋势

```python
import matplotlib.pyplot as plt

df = fv.get_cn_macro_gdp()
plt.plot(df['date'], df['gdp_yoy'])
plt.title("中国 GDP 同比增速")
plt.ylabel("同比增速 (%)")
plt.show()
```

### 分析通胀趋势

```python
cpi = fv.get_cn_macro_cpi()
ppi = fv.get_cn_macro_ppi()

# 合并数据
import pandas as pd
merged = pd.merge(cpi, ppi, on='date')

# CPI-PPI 剪刀差
merged['scissors'] = merged['cpi_yoy'] - merged['ppi_yoy']
```

### 货币政策分析

```python
money = fv.get_cn_macro_money_supply()

# M2-M1 增速差（活期化指标）
money['m2_m1_gap'] = money['m2_yoy'] - money['m1_yoy']
```

### 经济周期判断

```python
pmi = fv.get_cn_macro_pmi()

# PMI > 50 表示扩张
pmi['expansion'] = pmi['pmi'] > 50
expansion_rate = pmi['expansion'].mean()
print(f"扩张期占比: {expansion_rate:.1%}")
```
