# Macroeconomic Data API

## China Macro

### get_cn_macro_gdp

Get China GDP data.

```python
fv.get_cn_macro_gdp() -> pd.DataFrame
```

**Returns:** DataFrame with columns:

| Column | Description |
|--------|-------------|
| `date` | Quarter end date |
| `gdp` | GDP value (billion CNY) |
| `gdp_yoy` | Year-over-year growth (%) |

---

### get_cn_macro_cpi

Get China Consumer Price Index data.

```python
fv.get_cn_macro_cpi() -> pd.DataFrame
```

**Returns:** DataFrame with columns:

| Column | Description |
|--------|-------------|
| `date` | Month |
| `cpi` | CPI value |
| `cpi_yoy` | Year-over-year change (%) |
| `cpi_mom` | Month-over-month change (%) |

---

### get_cn_macro_ppi

Get China Producer Price Index data.

```python
fv.get_cn_macro_ppi() -> pd.DataFrame
```

**Returns:** DataFrame with columns:

| Column | Description |
|--------|-------------|
| `date` | Month |
| `ppi` | PPI value |
| `ppi_yoy` | Year-over-year change (%) |

---

### get_cn_macro_pmi

Get China Purchasing Managers' Index data.

```python
fv.get_cn_macro_pmi() -> pd.DataFrame
```

**Returns:** DataFrame with columns:

| Column | Description |
|--------|-------------|
| `date` | Month |
| `pmi` | Manufacturing PMI |
| `pmi_non_mfg` | Non-manufacturing PMI |

---

### get_cn_macro_money_supply

Get China money supply data (M0, M1, M2).

```python
fv.get_cn_macro_money_supply() -> pd.DataFrame
```

**Returns:** DataFrame with columns:

| Column | Description |
|--------|-------------|
| `date` | Month |
| `m0` | Currency in circulation |
| `m0_yoy` | M0 YoY growth (%) |
| `m1` | Narrow money supply |
| `m1_yoy` | M1 YoY growth (%) |
| `m2` | Broad money supply |
| `m2_yoy` | M2 YoY growth (%) |

---

### get_cn_macro_social_financing

Get China total social financing data.

```python
fv.get_cn_macro_social_financing() -> pd.DataFrame
```

**Returns:** DataFrame with columns:

| Column | Description |
|--------|-------------|
| `date` | Month |
| `total` | Total social financing |
| `stock` | Stock financing |

---

## Data Source

All China macroeconomic data is sourced from East Money (东方财富).

## Example Usage

```python
import finvista as fv

# Economic snapshot
gdp = fv.get_cn_macro_gdp()
cpi = fv.get_cn_macro_cpi()
pmi = fv.get_cn_macro_pmi()
money = fv.get_cn_macro_money_supply()

# Latest values
print(f"GDP Growth: {gdp.iloc[-1]['gdp_yoy']:.1f}%")
print(f"CPI: {cpi.iloc[-1]['cpi_yoy']:.1f}%")
print(f"PMI: {pmi.iloc[-1]['pmi']:.1f}")
print(f"M2 Growth: {money.iloc[-1]['m2_yoy']:.1f}%")
```
