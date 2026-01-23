# FinVista

<p align="center">
  <img src="assets/logo.png" alt="FinVista Logo" width="200">
</p>

<p align="center">
  <strong>强大的全球金融数据 Python 库，支持多数据源自动故障转移。</strong>
</p>

<p align="center">
  <a href="https://pypi.org/project/finvista/"><img src="https://badge.fury.io/py/finvista.svg" alt="PyPI version"></a>
  <a href="https://pypi.org/project/finvista/"><img src="https://img.shields.io/pypi/pyversions/finvista.svg" alt="Python Version"></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
  <a href="https://github.com/finvfamily/finvista/actions"><img src="https://github.com/finvfamily/finvista/actions/workflows/tests.yml/badge.svg" alt="Tests"></a>
</p>

---

## 特性

<div class="grid cards" markdown>

- :material-refresh: **多数据源故障转移**

    主数据源失败时自动切换到备用源

- :material-lightning-bolt: **熔断器模式**

    智能熔断防止故障蔓延

- :material-database: **内置缓存**

    LRU 缓存减少重复 API 调用

- :material-traffic-light: **智能限流**

    自动限流避免被数据源封禁

- :material-shield-check: **类型安全**

    完整的类型提示支持，IDE 体验更佳

- :material-earth: **全球市场**

    支持中国、美国、香港等多个市场

</div>

## 快速示例

```python
import finvista as fv

# 获取 A 股日线数据
df = fv.get_cn_stock_daily("000001", start_date="2024-01-01")
print(df.head())

# 获取实时行情
df = fv.get_cn_stock_quote(["000001", "600519"])
print(df)

# 获取财务数据
df = fv.get_cn_income_statement("000001")
print(df)

# 获取资金流向
df = fv.get_cn_stock_moneyflow("000001", days=30)
print(df)

# 获取美股数据
df = fv.get_us_stock_daily("AAPL", start_date="2024-01-01")
print(df)

# 查看实际使用的数据源
print(f"数据来源: {df.attrs.get('source')}")
```

## 安装

```bash
pip install finvista
```

## 支持的数据

| 类型 | 数据内容 | 主数据源 |
|------|----------|----------|
| A 股 | 日线、实时、分钟线、搜索 | 东方财富、新浪、腾讯 |
| 指数 | 日线、实时、成分股、权重 | 东方财富、新浪 |
| 基金 | 净值、估值、信息 | 天天基金 |
| 财务数据 | 利润表、资产负债表、现金流 | 东方财富 |
| 资金流向 | 个股资金流、行业资金流 | 东方财富 |
| 期货 | 合约列表、日线、持仓排名 | 东方财富 |
| 可转债 | 列表、日线、详情 | 东方财富 |
| 龙虎榜 | 榜单、明细、机构交易 | 东方财富 |
| 期权 | 合约列表、行情 | 东方财富 |
| 股东数据 | 前十大股东、质押、解禁 | 东方财富 |
| ETF | 份额变动、折溢价 | 东方财富 |
| 美股 | 日线、实时、公司信息 | Yahoo Finance |
| 港股指数 | 恒生指数日线 | 东方财富 |
| 外汇 | 实时汇率、历史汇率 | 东方财富 |
| 宏观数据 | GDP、CPI、PPI、PMI、货币供应 | 东方财富 |

## 为什么选择 FinVista？

### 自动故障转移

```
主数据源 (东方财富) → 失败
    ↓
备用数据源 1 (新浪) → 失败
    ↓
备用数据源 2 (腾讯) → 成功 ✓
```

无需手动处理错误。FinVista 会在主数据源失败时自动尝试备用数据源。

### 熔断器模式

```
健康 → 连续 5 次失败 → 熔断 (60秒)
  ↑                        ↓
  └── 连续 3 次成功 ← 半开
```

保护您的应用程序免受级联故障，并允许自动恢复。

## 下一步

- [安装指南](getting-started/installation.md)
- [快速入门](getting-started/quickstart.md)
- [API 参考](api/overview.md)

## 开源协议

MIT License - 详见 [LICENSE](https://github.com/finvfamily/finvista/blob/main/LICENSE)
