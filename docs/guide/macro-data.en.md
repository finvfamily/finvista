# Macroeconomic Data

Guide for accessing China macroeconomic data.

## GDP Data

```python
import finvista as fv

df = fv.get_cn_macro_gdp()
```

### Return Columns

| Column | Description |
|--------|-------------|
| `date` | Quarter end date |
| `gdp` | GDP value (billion CNY) |
| `gdp_yoy` | Year-over-year growth rate |

## CPI Data

Consumer Price Index:

```python
df = fv.get_cn_macro_cpi()
```

### Return Columns

| Column | Description |
|--------|-------------|
| `date` | Month |
| `cpi` | CPI value |
| `cpi_yoy` | Year-over-year change |
| `cpi_mom` | Month-over-month change |

## PPI Data

Producer Price Index:

```python
df = fv.get_cn_macro_ppi()
```

## PMI Data

Purchasing Managers' Index:

```python
df = fv.get_cn_macro_pmi()
```

### Return Columns

| Column | Description |
|--------|-------------|
| `date` | Month |
| `pmi` | Manufacturing PMI |
| `pmi_non_mfg` | Non-manufacturing PMI |

## Money Supply

M0, M1, M2 data:

```python
df = fv.get_cn_macro_money_supply()
```

### Return Columns

| Column | Description |
|--------|-------------|
| `date` | Month |
| `m0` | Currency in circulation |
| `m0_yoy` | M0 YoY growth |
| `m1` | Narrow money |
| `m1_yoy` | M1 YoY growth |
| `m2` | Broad money |
| `m2_yoy` | M2 YoY growth |

## Social Financing

Total Social Financing:

```python
df = fv.get_cn_macro_social_financing()
```

## Data Source

| Source | Data Types |
|--------|------------|
| East Money | All macro data |

## Examples

### Economic Dashboard

```python
import finvista as fv

# Get latest data
gdp = fv.get_cn_macro_gdp()
cpi = fv.get_cn_macro_cpi()
pmi = fv.get_cn_macro_pmi()

print("=== China Economic Dashboard ===")
print(f"Latest GDP Growth: {gdp.iloc[-1]['gdp_yoy']:.1f}%")
print(f"Latest CPI: {cpi.iloc[-1]['cpi_yoy']:.1f}%")
print(f"Latest PMI: {pmi.iloc[-1]['pmi']:.1f}")
```

### Plot Money Supply Growth

```python
import matplotlib.pyplot as plt

df = fv.get_cn_macro_money_supply()

plt.figure(figsize=(12, 6))
plt.plot(df['date'], df['m0_yoy'], label='M0')
plt.plot(df['date'], df['m1_yoy'], label='M1')
plt.plot(df['date'], df['m2_yoy'], label='M2')
plt.legend()
plt.title('China Money Supply Growth')
plt.ylabel('YoY Growth (%)')
plt.show()
```

### Inflation Trend

```python
df = fv.get_cn_macro_cpi()

# Last 12 months
recent = df.tail(12)
avg_cpi = recent['cpi_yoy'].mean()
print(f"Average CPI (last 12 months): {avg_cpi:.2f}%")
```
