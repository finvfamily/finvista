# Command Line Interface

FinVista includes a CLI for quick data access.

## Installation

The CLI is automatically installed with FinVista:

```bash
pip install finvista
```

## Commands

### quote

Get real-time quotes.

```bash
# China A-shares (default)
finvista quote 000001 600519

# US stocks
finvista quote AAPL MSFT --market us
```

**Options:**

| Option | Description |
|--------|-------------|
| `--market` | Market: `cn` (default) or `us` |

---

### history

Get historical data.

```bash
# Basic usage
finvista history 000001

# With date range
finvista history 000001 --start 2024-01-01 --end 2024-06-30

# Output to CSV
finvista history 000001 --start 2024-01-01 --format csv

# US stocks
finvista history AAPL --market us --start 2024-01-01
```

**Options:**

| Option | Description |
|--------|-------------|
| `--start` | Start date (YYYY-MM-DD) |
| `--end` | End date (YYYY-MM-DD) |
| `--market` | Market: `cn` (default) or `us` |
| `--format` | Output format: `table` (default) or `csv` |

---

### search

Search stocks by keyword.

```bash
# China stocks
finvista search 银行

# US stocks
finvista search Apple --market us
```

---

### health

Check data source health status.

```bash
finvista health
```

**Output:**

```
Data Source Health Report
========================

cn_stock_daily:
  eastmoney: healthy (0 failures)
  sina: healthy (0 failures)
  tencent: circuit_open (5 failures, recover at 10:31:00)

cn_stock_quote:
  sina: healthy (0 failures)
  eastmoney: healthy (0 failures)
```

---

### macro

Get macroeconomic data.

```bash
# GDP
finvista macro gdp

# CPI
finvista macro cpi

# PPI
finvista macro ppi

# PMI
finvista macro pmi

# Money supply
finvista macro money

# Social financing
finvista macro social
```

---

## Examples

### Quick Market Check

```bash
# Check major indices
finvista quote 000001 399001 000300

# Check tech giants
finvista quote AAPL MSFT GOOGL AMZN --market us
```

### Export Data

```bash
# Export to CSV
finvista history 000001 --start 2024-01-01 --format csv > 000001.csv

# Export multiple stocks
for code in 000001 600519 000858; do
    finvista history $code --start 2024-01-01 --format csv > ${code}.csv
done
```

### Monitor Source Health

```bash
# Check health before important operations
finvista health
```

---

## Global Options

| Option | Description |
|--------|-------------|
| `--help` | Show help message |
| `--version` | Show version |
