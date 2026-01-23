# FinVista

[English](README.md) | [中文](README_zh.md)

> 强大的全球金融数据 Python 库，支持多数据源自动故障转移。

[![PyPI version](https://badge.fury.io/py/finvista.svg)](https://badge.fury.io/py/finvista)
[![Python Version](https://img.shields.io/pypi/pyversions/finvista.svg)](https://pypi.org/project/finvista/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/finvfamily/finvista/actions/workflows/tests.yml/badge.svg)](https://github.com/finvfamily/finvista/actions)
[![Documentation](https://img.shields.io/badge/docs-online-blue.svg)](https://finvfamily.github.io/finvista/)

📖 **[在线文档](https://finvfamily.github.io/finvista/)** | 🐛 **[问题反馈](https://github.com/finvfamily/finvista/issues)** | 💬 **[讨论区](https://github.com/finvfamily/finvista/discussions)**

## 特性

- 🔄 **多数据源故障转移**: 主数据源失败时自动切换到备用源
- ⚡ **熔断器模式**: 智能熔断防止故障蔓延
- 💾 **内置缓存**: LRU 缓存减少重复 API 调用
- 🚦 **智能限流**: 自动限流避免被数据源封禁
- 🔒 **类型安全**: 完整的类型提示支持，IDE 体验更佳
- 🎯 **简单易用**: 函数式 API 设计，一行代码获取数据
- 🌍 **全球市场**: 支持中国、美国、香港等多个市场
- 📊 **数据全面**: 股票、指数、基金、期货、期权、债券、宏观经济数据

## 安装

```bash
pip install finvista
```

## 快速开始

### A 股数据

```python
import finvista as fv

# 获取日线历史数据
df = fv.get_cn_stock_daily("000001", start_date="2024-01-01")
print(df.head())

# 获取实时行情
df = fv.get_cn_stock_quote(["000001", "600519"])
print(df)

# 获取股票列表
df = fv.list_cn_stock_symbols(market="main")
print(f"共 {len(df)} 只股票")

# 搜索股票
df = fv.search_cn_stock("银行")
print(df)
```

### 财务数据

```python
# 利润表
df = fv.get_cn_income_statement("000001")

# 资产负债表
df = fv.get_cn_balance_sheet("000001")

# 现金流量表
df = fv.get_cn_cash_flow("000001")

# 分红历史
df = fv.get_cn_dividend_history("000001")

# 业绩预告
df = fv.get_cn_performance_forecast()
```

### 资金流向

```python
# 个股资金流向（近30天）
df = fv.get_cn_stock_moneyflow("000001", days=30)

# 实时资金流向
df = fv.get_cn_stock_moneyflow_realtime("000001")

# 行业资金流向
df = fv.get_cn_industry_moneyflow()
```

### 分钟线数据

```python
# 5分钟K线数据
df = fv.get_cn_stock_minute("000001", period="5", days=5)

# 1分钟数据
df = fv.get_cn_stock_minute("000001", period="1", days=1)

# 支持的周期: "1", "5", "15", "30", "60"
```

### 期货数据

```python
# 获取所有期货合约
df = fv.list_cn_futures_symbols()

# 只获取中金所合约
df = fv.list_cn_futures_symbols(exchange="CFFEX")

# 获取期货日线数据
df = fv.get_cn_futures_daily("IF2401", start_date="2024-01-01")

# 获取持仓排名
df = fv.get_cn_futures_positions("IF")
```

### 可转债数据

```python
# 获取所有可转债列表
df = fv.list_cn_convertible_symbols()

# 获取可转债日线数据
df = fv.get_cn_convertible_daily("113008", start_date="2024-01-01")

# 获取可转债信息
info = fv.get_cn_convertible_info("113008")
```

### 龙虎榜数据

```python
# 获取最新龙虎榜
df = fv.get_cn_lhb_list()

# 获取指定日期
df = fv.get_cn_lhb_list(date="2024-01-15")

# 获取交易明细
df = fv.get_cn_lhb_detail("000001", "2024-01-15")

# 获取机构买卖
df = fv.get_cn_lhb_institution()
```

### 期权数据

```python
# 获取期权合约列表
df = fv.list_cn_option_contracts("510050")

# 获取期权日线数据
df = fv.get_cn_option_daily("10004456", start_date="2024-01-01")
```

### 股东/股权数据

```python
# 获取前十大股东
df = fv.get_cn_top_shareholders("000001")

# 获取股权质押数据
df = fv.get_cn_stock_pledge("000001")

# 获取限售解禁日历
df = fv.get_cn_stock_unlock_schedule("2024-01-01", "2024-01-31")
```

### 指数数据

```python
# 获取指数日线数据
df = fv.get_cn_index_daily("000300", start_date="2024-01-01")

# 获取指数成分股
df = fv.get_cn_index_constituents("000300")

# 获取指数权重
df = fv.get_cn_index_weights("000300")

# 获取主要指数列表
df = fv.list_cn_major_indices()
```

### ETF 数据

```python
# 获取ETF份额变动
df = fv.get_cn_etf_share_change("510050", days=30)

# 获取ETF折溢价
df = fv.get_cn_etf_premium_discount("510050")
```

### 基金数据

```python
# 获取基金净值历史
df = fv.get_cn_fund_nav("110011", start_date="2024-01-01")

# 获取实时基金估值
df = fv.get_cn_fund_quote(["110011", "000001"])

# 按类型获取基金列表
df = fv.list_cn_fund_symbols(fund_type="stock")

# 搜索基金
df = fv.search_cn_fund("沪深300")

# 获取基金信息
info = fv.get_cn_fund_info("110011")
```

### 美股数据

```python
# 获取美股日线数据
df = fv.get_us_stock_daily("AAPL", start_date="2024-01-01")

# 获取实时行情
df = fv.get_us_stock_quote(["AAPL", "MSFT", "GOOGL"])

# 获取公司信息
info = fv.get_us_stock_info("AAPL")

# 搜索美股
df = fv.search_us_stock("Apple")
```

### 外汇数据

```python
# 获取当前汇率
df = fv.get_exchange_rate("USD", "CNY")

# 获取历史汇率
df = fv.get_exchange_rate_history("USD", "CNY", start_date="2024-01-01")
```

### 宏观经济数据

```python
# 中国 GDP
df = fv.get_cn_macro_gdp()

# 中国 CPI
df = fv.get_cn_macro_cpi()

# 中国 PPI
df = fv.get_cn_macro_ppi()

# 中国 PMI
df = fv.get_cn_macro_pmi()

# 货币供应量 (M0, M1, M2)
df = fv.get_cn_macro_money_supply()

# 社会融资规模
df = fv.get_cn_macro_social_financing()
```

## 命令行工具

```bash
# 获取实时行情
finvista quote 000001 600519

# 获取美股行情
finvista quote AAPL MSFT --market us

# 获取历史数据
finvista history 000001 --start 2024-01-01 --format csv

# 搜索股票
finvista search 银行

# 查看数据源健康状态
finvista health

# 获取宏观经济数据
finvista macro gdp
```

## 配置

```python
import finvista as fv

# 设置 HTTP 代理
fv.set_proxies({"http": "http://127.0.0.1:7890"})

# 设置请求超时
fv.set_timeout(60)

# 配置缓存
fv.set_cache(enabled=True, ttl=300)

# 查看数据源健康状态
health = fv.get_source_health()
print(health)

# 重置某个数据源的熔断器
fv.reset_source_circuit("cn_stock_daily", "eastmoney")

# 设置数据源优先级
fv.set_source_priority("cn_stock_daily", ["sina", "eastmoney"])
```

## 数据源故障转移

FinVista 自动处理数据源故障：

```python
import finvista as fv

# 自动故障转移 - 如果东方财富失败，自动尝试新浪，然后腾讯
df = fv.get_cn_stock_daily("000001")

# 查看实际使用的数据源
print(f"数据来源: {df.attrs.get('source')}")

# 指定数据源（不使用故障转移）
df = fv.get_cn_stock_daily("000001", source="eastmoney")
```

## 数据源

| 数据类型 | 主数据源 | 备用数据源 |
|----------|----------|------------|
| A 股日线 | 东方财富 | 新浪、腾讯 |
| A 股实时 | 新浪 | 腾讯、东方财富 |
| 指数数据 | 东方财富 | 新浪 |
| 基金数据 | 天天基金 | - |
| 财务数据 | 东方财富 | - |
| 资金流向 | 东方财富 | - |
| 期货数据 | 东方财富 | - |
| 可转债 | 东方财富 | - |
| 期权数据 | 东方财富 | - |
| 美股数据 | Yahoo Finance | - |
| 外汇数据 | 东方财富 | - |
| 宏观数据 | 东方财富 | - |

## API 参考

### A 股数据

| 函数 | 说明 |
|------|------|
| `get_cn_stock_daily()` | 获取日线历史数据 |
| `get_cn_stock_quote()` | 获取实时行情 |
| `list_cn_stock_symbols()` | 获取股票列表 |
| `search_cn_stock()` | 搜索股票 |
| `get_cn_stock_minute()` | 获取分钟线数据 |

### 财务数据

| 函数 | 说明 |
|------|------|
| `get_cn_income_statement()` | 获取利润表 |
| `get_cn_balance_sheet()` | 获取资产负债表 |
| `get_cn_cash_flow()` | 获取现金流量表 |
| `get_cn_performance_forecast()` | 获取业绩预告 |
| `get_cn_dividend_history()` | 获取分红历史 |

### 资金流向

| 函数 | 说明 |
|------|------|
| `get_cn_stock_moneyflow()` | 获取历史资金流向 |
| `get_cn_stock_moneyflow_realtime()` | 获取实时资金流向 |
| `get_cn_industry_moneyflow()` | 获取行业资金流向 |

### 指数数据

| 函数 | 说明 |
|------|------|
| `get_cn_index_daily()` | 获取指数日线数据 |
| `get_cn_index_quote()` | 获取实时指数行情 |
| `list_cn_major_indices()` | 获取主要指数列表 |
| `get_cn_index_constituents()` | 获取指数成分股 |
| `get_cn_index_weights()` | 获取指数权重 |

### 期货数据

| 函数 | 说明 |
|------|------|
| `list_cn_futures_symbols()` | 获取期货合约列表 |
| `get_cn_futures_daily()` | 获取期货日线数据 |
| `get_cn_futures_positions()` | 获取持仓排名 |

### 可转债数据

| 函数 | 说明 |
|------|------|
| `list_cn_convertible_symbols()` | 获取可转债列表 |
| `get_cn_convertible_daily()` | 获取可转债日线 |
| `get_cn_convertible_info()` | 获取可转债信息 |

### 龙虎榜数据

| 函数 | 说明 |
|------|------|
| `get_cn_lhb_list()` | 获取龙虎榜列表 |
| `get_cn_lhb_detail()` | 获取交易明细 |
| `get_cn_lhb_institution()` | 获取机构买卖 |

### 期权数据

| 函数 | 说明 |
|------|------|
| `list_cn_option_contracts()` | 获取期权合约列表 |
| `get_cn_option_quote()` | 获取期权行情 |
| `get_cn_option_daily()` | 获取期权日线数据 |

### 股东/股权数据

| 函数 | 说明 |
|------|------|
| `get_cn_top_shareholders()` | 获取前十大股东 |
| `get_cn_stock_pledge()` | 获取股权质押数据 |
| `get_cn_stock_unlock_schedule()` | 获取限售解禁日历 |

### ETF 数据

| 函数 | 说明 |
|------|------|
| `get_cn_etf_share_change()` | 获取ETF份额变动 |
| `get_cn_etf_premium_discount()` | 获取ETF折溢价 |

### 基金数据

| 函数 | 说明 |
|------|------|
| `get_cn_fund_nav()` | 获取基金净值历史 |
| `get_cn_fund_quote()` | 获取实时基金估值 |
| `list_cn_fund_symbols()` | 获取基金列表 |
| `search_cn_fund()` | 搜索基金 |
| `get_cn_fund_info()` | 获取基金信息 |

### 美股数据

| 函数 | 说明 |
|------|------|
| `get_us_stock_daily()` | 获取日线历史数据 |
| `get_us_stock_quote()` | 获取实时行情 |
| `get_us_stock_info()` | 获取公司信息 |
| `search_us_stock()` | 搜索美股 |

### 外汇数据

| 函数 | 说明 |
|------|------|
| `get_exchange_rate()` | 获取当前汇率 |
| `get_exchange_rate_history()` | 获取历史汇率 |

### 宏观经济数据

| 函数 | 说明 |
|------|------|
| `get_cn_macro_gdp()` | 中国 GDP 数据 |
| `get_cn_macro_cpi()` | 中国 CPI 数据 |
| `get_cn_macro_ppi()` | 中国 PPI 数据 |
| `get_cn_macro_pmi()` | 中国 PMI 数据 |
| `get_cn_macro_money_supply()` | 货币供应量 (M0/M1/M2) |
| `get_cn_macro_social_financing()` | 社会融资规模数据 |

### 配置函数

| 函数 | 说明 |
|------|------|
| `set_proxies()` | 设置 HTTP 代理 |
| `set_timeout()` | 设置请求超时 |
| `set_cache()` | 配置缓存 |
| `get_source_health()` | 获取数据源健康状态 |
| `reset_source_circuit()` | 重置熔断器 |
| `set_source_priority()` | 设置数据源优先级 |

## 系统要求

- Python >= 3.10
- pandas >= 2.0.0
- requests >= 2.28.0
- httpx >= 0.24.0

## 贡献者

<a href="https://github.com/finvfamily/finvista/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=finvfamily/finvista" />
</a>

## 开源协议

MIT License - 详见 [LICENSE](LICENSE)

## 贡献

欢迎贡献代码！请随时提交 Pull Request。

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 发起 Pull Request

## 致谢

FinVista 专为可靠的金融数据访问而设计，具备自动故障转移能力，服务于量化研究员、交易员和金融分析师。

## Star 趋势

<a href="https://github.com/finvfamily/finvista/stargazers">
  <img src="https://starchart.cc/finvfamily/finvista.svg?variant=adaptive" alt="Star History Chart" width="600">
</a>
