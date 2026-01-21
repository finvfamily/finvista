# FinVista

<p align="center">
  <img src="assets/logo.png" alt="FinVista Logo" width="200">
</p>

<p align="center">
  <strong>A powerful Python library for global financial data with multi-source failover.</strong>
</p>

<p align="center">
  <a href="https://pypi.org/project/finvista/"><img src="https://badge.fury.io/py/finvista.svg" alt="PyPI version"></a>
  <a href="https://pypi.org/project/finvista/"><img src="https://img.shields.io/pypi/pyversions/finvista.svg" alt="Python Version"></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
  <a href="https://github.com/finvfamily/finvista/actions"><img src="https://github.com/finvfamily/finvista/actions/workflows/tests.yml/badge.svg" alt="Tests"></a>
</p>

---

## Features

<div class="grid cards" markdown>

- :material-refresh: **Multi-Source Failover**

    Automatically switches to backup data sources when primary fails

- :material-lightning-bolt: **Circuit Breaker**

    Prevents cascade failures with smart circuit breaking

- :material-database: **Built-in Caching**

    LRU cache reduces redundant API calls

- :material-traffic-light: **Rate Limiting**

    Intelligent rate limiting to avoid being blocked

- :material-shield-check: **Type Safe**

    Full type hints support for better IDE experience

- :material-earth: **Global Markets**

    Support for China, US, and more markets

</div>

## Quick Example

```python
import finvista as fv

# Get China A-share daily data
df = fv.get_cn_stock_daily("000001", start_date="2024-01-01")
print(df.head())

# Get real-time quotes
df = fv.get_cn_stock_quote(["000001", "600519"])
print(df)

# Get US stock data
df = fv.get_us_stock_daily("AAPL", start_date="2024-01-01")
print(df)

# Check which data source was used
print(f"Data from: {df.attrs.get('source')}")
```

## Installation

```bash
pip install finvista
```

## Supported Markets

| Market | Data Types | Primary Source |
|--------|------------|----------------|
| China A-Shares | Daily, Quote, Search | East Money, Sina, Tencent |
| China Indices | Daily, Quote | East Money, Sina |
| China Funds | NAV, Quote, Info | Tiantian Fund |
| US Stocks | Daily, Quote, Info | Yahoo Finance |
| China Macro | GDP, CPI, PPI, PMI | East Money |

## Why FinVista?

### Automatic Failover

```
Primary Source (East Money) → Failed
    ↓
Backup Source 1 (Sina) → Failed
    ↓
Backup Source 2 (Tencent) → Success ✓
```

No more manual error handling. FinVista automatically tries backup sources when the primary fails.

### Circuit Breaker Pattern

```
HEALTHY → 5 consecutive failures → CIRCUIT OPEN (60s)
    ↑                                    ↓
    └── 3 consecutive successes ← HALF OPEN
```

Protects your application from cascading failures and allows automatic recovery.

## Next Steps

- [Installation Guide](getting-started/installation.md)
- [Quick Start Tutorial](getting-started/quickstart.md)
- [API Reference](api/overview.md)

## License

MIT License - see [LICENSE](https://github.com/finvfamily/finvista/blob/main/LICENSE) for details.
