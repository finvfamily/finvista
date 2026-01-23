# 更新日志

所有重要更改都会记录在此文件中。

本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [Unreleased]

### 新增

- 财务数据模块
  - `get_cn_income_statement` - 利润表
  - `get_cn_balance_sheet` - 资产负债表
  - `get_cn_cash_flow` - 现金流量表
  - `get_cn_dividend_history` - 分红历史
  - `get_cn_performance_forecast` - 业绩预告

- 资金流向模块
  - `get_cn_stock_moneyflow` - 个股资金流向
  - `get_cn_stock_moneyflow_realtime` - 实时资金流向
  - `get_cn_industry_moneyflow` - 行业资金流向

- 分钟线数据
  - `get_cn_stock_minute` - 支持 1/5/15/30/60 分钟 K 线

- 期货数据模块
  - `list_cn_futures_symbols` - 期货合约列表
  - `get_cn_futures_daily` - 期货日线数据
  - `get_cn_futures_positions` - 持仓排名

- 可转债数据模块
  - `list_cn_convertible_symbols` - 可转债列表
  - `get_cn_convertible_daily` - 可转债日线
  - `get_cn_convertible_info` - 可转债信息

- 龙虎榜数据模块
  - `get_cn_lhb_list` - 龙虎榜列表
  - `get_cn_lhb_detail` - 交易明细
  - `get_cn_lhb_institution` - 机构买卖

- 期权数据模块
  - `list_cn_option_contracts` - 期权合约列表
  - `get_cn_option_quote` - 期权行情
  - `get_cn_option_daily` - 期权日线

- 股东数据模块
  - `get_cn_top_shareholders` - 前十大股东
  - `get_cn_stock_pledge` - 股权质押
  - `get_cn_stock_unlock_schedule` - 解禁计划

- ETF 增强模块
  - `get_cn_etf_share_change` - ETF 份额变动
  - `get_cn_etf_premium_discount` - ETF 折溢价

- 外汇数据模块
  - `get_exchange_rate` - 实时汇率
  - `get_exchange_rate_history` - 历史汇率

- 指数增强
  - `get_cn_index_constituents` - 指数成分股
  - `get_cn_index_weights` - 成分股权重

- 文档更新
  - 新增中文文档
  - 默认显示中文
  - 支持中英文切换

---

## [0.2.0] - 2024-01-20

### 新增

- 美股/港股指数数据
  - `get_us_index_daily` - 美股指数日线
  - `get_hk_index_daily` - 港股指数日线

- 估值数据
  - `get_index_pe` - 指数市盈率
  - `get_index_pb` - 指数市净率
  - `get_all_a_pb` - 全 A 股市净率

- 申万行业数据
  - `get_sw_index_daily` - 申万行业指数日线
  - `get_sw_index_realtime` - 申万行业实时行情
  - `get_sw_index_analysis` - 申万行业分析

### 改进

- 优化数据源故障转移逻辑
- 改进错误提示信息
- 增强类型提示支持

---

## [0.1.0] - 2024-01-01

### 新增

- A 股数据
  - `get_cn_stock_daily` - 日线数据
  - `get_cn_stock_quote` - 实时行情
  - `list_cn_stock_symbols` - 股票列表
  - `search_cn_stock` - 股票搜索

- 指数数据
  - `get_cn_index_daily` - 指数日线
  - `get_cn_index_quote` - 指数实时行情
  - `list_cn_major_indices` - 主要指数列表

- 基金数据
  - `get_cn_fund_nav` - 基金净值
  - `get_cn_fund_quote` - 基金估值
  - `get_cn_fund_info` - 基金信息
  - `list_cn_fund_symbols` - 基金列表
  - `search_cn_fund` - 基金搜索

- 美股数据
  - `get_us_stock_daily` - 日线数据
  - `get_us_stock_quote` - 实时行情
  - `get_us_stock_info` - 公司信息
  - `search_us_stock` - 股票搜索

- 宏观数据
  - `get_cn_macro_gdp` - GDP
  - `get_cn_macro_cpi` - CPI
  - `get_cn_macro_ppi` - PPI
  - `get_cn_macro_pmi` - PMI
  - `get_cn_macro_money_supply` - 货币供应
  - `get_cn_macro_social_financing` - 社会融资

- 配置功能
  - `set_proxies` - 代理设置
  - `set_timeout` - 超时设置
  - `set_cache` - 缓存配置
  - `get_source_health` - 数据源健康
  - `reset_source_circuit` - 重置熔断器
  - `set_source_priority` - 设置优先级

- 多数据源故障转移
- 熔断器模式
- 内置缓存
- 命令行工具

---

## 版本格式

- **MAJOR**: 不兼容的 API 修改
- **MINOR**: 向下兼容的功能性新增
- **PATCH**: 向下兼容的问题修正
