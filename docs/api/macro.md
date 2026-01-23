# 宏观数据 API

## GDP

### get_cn_macro_gdp

获取中国 GDP 数据。

```python
fv.get_cn_macro_gdp() -> pd.DataFrame
```

**返回：** DataFrame，字段：

| 字段 | 说明 |
|------|------|
| `date` | 统计日期 |
| `gdp` | GDP 总量（亿元） |
| `gdp_yoy` | GDP 同比增速 (%) |
| `primary_industry` | 第一产业增加值 |
| `secondary_industry` | 第二产业增加值 |
| `tertiary_industry` | 第三产业增加值 |

---

## CPI

### get_cn_macro_cpi

获取中国 CPI 数据。

```python
fv.get_cn_macro_cpi() -> pd.DataFrame
```

**返回：** DataFrame，字段：

| 字段 | 说明 |
|------|------|
| `date` | 统计月份 |
| `cpi` | CPI 指数 |
| `cpi_yoy` | CPI 同比 (%) |
| `cpi_mom` | CPI 环比 (%) |

---

## PPI

### get_cn_macro_ppi

获取中国 PPI 数据。

```python
fv.get_cn_macro_ppi() -> pd.DataFrame
```

**返回：** DataFrame，字段：

| 字段 | 说明 |
|------|------|
| `date` | 统计月份 |
| `ppi` | PPI 指数 |
| `ppi_yoy` | PPI 同比 (%) |

---

## PMI

### get_cn_macro_pmi

获取中国 PMI 数据。

```python
fv.get_cn_macro_pmi() -> pd.DataFrame
```

**返回：** DataFrame，字段：

| 字段 | 说明 |
|------|------|
| `date` | 统计月份 |
| `pmi` | 制造业 PMI |
| `pmi_non_mfg` | 非制造业 PMI |
| `pmi_composite` | 综合 PMI |

---

## 货币供应

### get_cn_macro_money_supply

获取中国货币供应量数据。

```python
fv.get_cn_macro_money_supply() -> pd.DataFrame
```

**返回：** DataFrame，字段：

| 字段 | 说明 |
|------|------|
| `date` | 统计月份 |
| `m0` | M0（流通中货币） |
| `m0_yoy` | M0 同比 (%) |
| `m1` | M1（狭义货币） |
| `m1_yoy` | M1 同比 (%) |
| `m2` | M2（广义货币） |
| `m2_yoy` | M2 同比 (%) |

---

## 社会融资

### get_cn_macro_social_financing

获取社会融资规模数据。

```python
fv.get_cn_macro_social_financing() -> pd.DataFrame
```

**返回：** DataFrame，字段：

| 字段 | 说明 |
|------|------|
| `date` | 统计月份 |
| `total` | 社融规模增量 |
| `loan` | 人民币贷款 |
| `fx_loan` | 外币贷款 |
| `bond` | 企业债券 |
| `equity` | 股票融资 |
| `trust_loan` | 委托贷款 |

---

## 使用示例

### 获取宏观数据

```python
import finvista as fv

# GDP 数据
gdp = fv.get_cn_macro_gdp()
print(gdp.head())

# CPI 数据
cpi = fv.get_cn_macro_cpi()
print(cpi.head())

# 货币供应
money = fv.get_cn_macro_money_supply()
print(money.head())
```

### 分析通胀趋势

```python
cpi = fv.get_cn_macro_cpi()
ppi = fv.get_cn_macro_ppi()

import pandas as pd
merged = pd.merge(cpi, ppi, on='date')

# CPI-PPI 剪刀差
merged['scissors'] = merged['cpi_yoy'] - merged['ppi_yoy']
print(merged[['date', 'cpi_yoy', 'ppi_yoy', 'scissors']].head())
```

### 货币政策分析

```python
money = fv.get_cn_macro_money_supply()

# M2-M1 增速差（活期化指标）
money['m2_m1_gap'] = money['m2_yoy'] - money['m1_yoy']

# 判断资金活跃度
latest = money.iloc[0]
if latest['m2_m1_gap'] > 0:
    print("资金活期化程度较低，企业投资意愿不强")
else:
    print("资金活期化程度较高，企业投资意愿较强")
```

### 经济周期判断

```python
pmi = fv.get_cn_macro_pmi()

# PMI > 50 表示扩张
latest_pmi = pmi['pmi'].iloc[0]
if latest_pmi > 50:
    print(f"当前 PMI {latest_pmi}，经济处于扩张期")
else:
    print(f"当前 PMI {latest_pmi}，经济处于收缩期")
```
