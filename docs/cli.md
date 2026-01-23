# 命令行工具

FinVista 提供命令行工具，方便快速获取数据。

## 安装

CLI 随 FinVista 自动安装：

```bash
pip install finvista
```

## 命令

### quote

获取实时行情。

```bash
# A 股（默认）
finvista quote 000001 600519

# 美股
finvista quote AAPL MSFT --market us
```

**选项：**

| 选项 | 说明 |
|------|------|
| `--market` | 市场：`cn`（默认）或 `us` |

---

### history

获取历史数据。

```bash
# 基本用法
finvista history 000001

# 指定日期范围
finvista history 000001 --start 2024-01-01 --end 2024-06-30

# 输出为 CSV
finvista history 000001 --start 2024-01-01 --format csv

# 美股
finvista history AAPL --market us --start 2024-01-01
```

**选项：**

| 选项 | 说明 |
|------|------|
| `--start` | 开始日期（YYYY-MM-DD） |
| `--end` | 结束日期（YYYY-MM-DD） |
| `--market` | 市场：`cn`（默认）或 `us` |
| `--format` | 输出格式：`table`（默认）或 `csv` |

---

### search

搜索股票。

```bash
# A 股
finvista search 银行

# 美股
finvista search Apple --market us
```

---

### health

检查数据源健康状态。

```bash
finvista health
```

**输出：**

```
数据源健康报告
========================

cn_stock_daily:
  eastmoney: 正常 (0 次失败)
  sina: 正常 (0 次失败)
  tencent: 熔断中 (5 次失败, 恢复时间 10:31:00)

cn_stock_quote:
  sina: 正常 (0 次失败)
  eastmoney: 正常 (0 次失败)
```

---

### macro

获取宏观经济数据。

```bash
# GDP
finvista macro gdp

# CPI
finvista macro cpi

# PPI
finvista macro ppi

# PMI
finvista macro pmi

# 货币供应
finvista macro money

# 社会融资
finvista macro social
```

---

## 使用示例

### 快速查看行情

```bash
# 查看主要指数
finvista quote 000001 399001 000300

# 查看科技巨头
finvista quote AAPL MSFT GOOGL AMZN --market us
```

### 导出数据

```bash
# 导出为 CSV
finvista history 000001 --start 2024-01-01 --format csv > 000001.csv

# 批量导出
for code in 000001 600519 000858; do
    finvista history $code --start 2024-01-01 --format csv > ${code}.csv
done
```

### 监控数据源

```bash
# 执行重要操作前检查健康状态
finvista health
```

---

## 全局选项

| 选项 | 说明 |
|------|------|
| `--help` | 显示帮助信息 |
| `--version` | 显示版本号 |
