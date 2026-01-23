# 快速入门

本指南将帮助您在几分钟内开始使用 FinVista。

## 导入库

```python
import finvista as fv
```

## A 股数据

### 获取日线数据

```python
# 获取平安银行 (000001) 的日线数据
df = fv.get_cn_stock_daily("000001", start_date="2024-01-01")
print(df.head())
```

输出：
```
         date    open    high     low   close      volume        amount
0  2024-01-02   9.15    9.20    9.05    9.10   123456789   1123456789.0
1  2024-01-03   9.12    9.25    9.10    9.20   134567890   1234567890.0
...
```

### 获取实时行情

```python
# 获取多只股票的实时行情
df = fv.get_cn_stock_quote(["000001", "600519"])
print(df)
```

### 搜索股票

```python
# 按关键字搜索
df = fv.search_cn_stock("银行")
print(df)
```

### 股票列表

```python
# 获取所有主板股票
df = fv.list_cn_stock_symbols(market="main")
print(f"共 {len(df)} 只股票")
```

## 财务数据

```python
# 利润表
df = fv.get_cn_income_statement("000001")

# 资产负债表
df = fv.get_cn_balance_sheet("000001")

# 现金流量表
df = fv.get_cn_cash_flow("000001")

# 分红历史
df = fv.get_cn_dividend_history("000001")
```

## 资金流向

```python
# 个股资金流向（近 30 天）
df = fv.get_cn_stock_moneyflow("000001", days=30)

# 实时资金流向
df = fv.get_cn_stock_moneyflow_realtime("000001")

# 行业资金流向
df = fv.get_cn_industry_moneyflow()
```

## 分钟线数据

```python
# 5 分钟 K 线
df = fv.get_cn_stock_minute("000001", period="5", days=5)

# 1 分钟 K 线
df = fv.get_cn_stock_minute("000001", period="1", days=1)

# 支持周期: "1", "5", "15", "30", "60"
```

## 指数数据

```python
# 获取沪深 300 指数数据
df = fv.get_cn_index_daily("000300", start_date="2024-01-01")

# 获取指数实时行情
df = fv.get_cn_index_quote(["000001", "399001"])

# 获取指数成分股
df = fv.get_cn_index_constituents("000300")

# 获取成分股权重
df = fv.get_cn_index_weights("000300")

# 列出主要指数
df = fv.list_cn_major_indices()
```

## 基金数据

```python
# 获取基金净值历史
df = fv.get_cn_fund_nav("110011", start_date="2024-01-01")

# 获取实时估值
df = fv.get_cn_fund_quote(["110011", "000001"])

# 获取基金信息
info = fv.get_cn_fund_info("110011")
```

## 期货数据

```python
# 列出所有期货合约
df = fv.list_cn_futures_symbols()

# 获取期货日线
df = fv.get_cn_futures_daily("IF2401", start_date="2024-01-01")

# 获取持仓排名
df = fv.get_cn_futures_positions("IF")
```

## 可转债数据

```python
# 列出所有可转债
df = fv.list_cn_convertible_symbols()

# 获取可转债日线
df = fv.get_cn_convertible_daily("113008", start_date="2024-01-01")

# 获取可转债信息
info = fv.get_cn_convertible_info("113008")
```

## 龙虎榜数据

```python
# 获取最新龙虎榜
df = fv.get_cn_lhb_list()

# 获取交易明细
df = fv.get_cn_lhb_detail("000001", "2024-01-15")

# 获取机构买卖
df = fv.get_cn_lhb_institution()
```

## 股东数据

```python
# 获取前十大股东
df = fv.get_cn_top_shareholders("000001")

# 获取股权质押
df = fv.get_cn_stock_pledge("000001")

# 获取解禁计划
df = fv.get_cn_stock_unlock_schedule("2024-01-01", "2024-01-31")
```

## 美股数据

```python
# 获取苹果日线数据
df = fv.get_us_stock_daily("AAPL", start_date="2024-01-01")

# 获取实时行情
df = fv.get_us_stock_quote(["AAPL", "MSFT", "GOOGL"])

# 获取公司信息
info = fv.get_us_stock_info("AAPL")
```

## 外汇数据

```python
# 获取实时汇率
df = fv.get_exchange_rate("USD", "CNY")

# 获取历史汇率
df = fv.get_exchange_rate_history("USD", "CNY", start_date="2024-01-01")
```

## 宏观数据

```python
# 中国 GDP
df = fv.get_cn_macro_gdp()

# 中国 CPI
df = fv.get_cn_macro_cpi()

# 货币供应量 (M0, M1, M2)
df = fv.get_cn_macro_money_supply()
```

## 查看数据来源

每个 DataFrame 都包含实际使用的数据源信息：

```python
df = fv.get_cn_stock_daily("000001")
print(f"数据来源: {df.attrs.get('source')}")
```

## 下一步

- [配置选项](configuration.md) - 自定义 FinVista 设置
- [故障转移机制](../guide/failover.md) - 了解多数据源故障转移
- [API 参考](../api/overview.md) - 完整的 API 文档
