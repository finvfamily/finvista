# API 概览

FinVista 提供简洁的函数式 API，所有函数都返回 pandas DataFrame。

## 命名规范

### 函数命名

```
{操作}_{市场}_{数据类型}
```

示例：

- `get_cn_stock_daily` - 获取中国股票日线
- `list_cn_fund_symbols` - 列出中国基金代码
- `search_us_stock` - 搜索美股

### 市场代码

| 代码 | 市场 |
|------|------|
| `cn` | 中国 A 股 |
| `us` | 美国 |
| `hk` | 香港 |

## 通用参数

### 日期参数

```python
# 支持的日期格式
start_date="2024-01-01"  # 字符串
start_date="20240101"    # 无分隔符
start_date=datetime(2024, 1, 1)  # datetime 对象
```

### 数据源参数

```python
# 使用默认数据源（自动故障转移）
df = fv.get_cn_stock_daily("000001")

# 强制指定数据源
df = fv.get_cn_stock_daily("000001", source="eastmoney")
```

## 返回值

所有数据获取函数返回 `pandas.DataFrame`，并附带元数据：

```python
df = fv.get_cn_stock_daily("000001")

# 查看数据源
print(df.attrs.get('source'))  # 输出: eastmoney

# 查看获取时间
print(df.attrs.get('fetch_time'))
```

## API 分类

### 中国市场

| 模块 | 函数 | 说明 |
|------|------|------|
| 股票 | `get_cn_stock_daily` | 日线数据 |
| | `get_cn_stock_quote` | 实时行情 |
| | `get_cn_stock_minute` | 分钟线 |
| | `list_cn_stock_symbols` | 股票列表 |
| | `search_cn_stock` | 搜索 |
| 指数 | `get_cn_index_daily` | 日线数据 |
| | `get_cn_index_quote` | 实时行情 |
| | `get_cn_index_constituents` | 成分股 |
| | `get_cn_index_weights` | 权重 |
| 基金 | `get_cn_fund_nav` | 净值历史 |
| | `get_cn_fund_quote` | 实时估值 |
| | `get_cn_fund_info` | 基金信息 |
| 财务 | `get_cn_income_statement` | 利润表 |
| | `get_cn_balance_sheet` | 资产负债表 |
| | `get_cn_cash_flow` | 现金流量表 |
| | `get_cn_dividend_history` | 分红历史 |
| 资金流向 | `get_cn_stock_moneyflow` | 资金流向 |
| | `get_cn_industry_moneyflow` | 行业资金 |
| 期货 | `list_cn_futures_symbols` | 合约列表 |
| | `get_cn_futures_daily` | 日线数据 |
| | `get_cn_futures_positions` | 持仓排名 |
| 可转债 | `list_cn_convertible_symbols` | 可转债列表 |
| | `get_cn_convertible_daily` | 日线数据 |
| | `get_cn_convertible_info` | 详情信息 |
| 龙虎榜 | `get_cn_lhb_list` | 龙虎榜列表 |
| | `get_cn_lhb_detail` | 交易明细 |
| | `get_cn_lhb_institution` | 机构交易 |
| 期权 | `list_cn_option_contracts` | 合约列表 |
| | `get_cn_option_quote` | 实时行情 |
| | `get_cn_option_daily` | 日线数据 |
| 股东 | `get_cn_top_shareholders` | 前十大股东 |
| | `get_cn_stock_pledge` | 股权质押 |
| | `get_cn_stock_unlock_schedule` | 解禁计划 |
| ETF | `get_cn_etf_share_change` | 份额变动 |
| | `get_cn_etf_premium_discount` | 折溢价 |

### 美国市场

| 函数 | 说明 |
|------|------|
| `get_us_stock_daily` | 日线数据 |
| `get_us_stock_quote` | 实时行情 |
| `get_us_stock_info` | 公司信息 |
| `search_us_stock` | 搜索 |
| `get_us_index_daily` | 指数日线 |

### 香港市场

| 函数 | 说明 |
|------|------|
| `get_hk_index_daily` | 恒生指数日线 |

### 外汇

| 函数 | 说明 |
|------|------|
| `get_exchange_rate` | 实时汇率 |
| `get_exchange_rate_history` | 历史汇率 |

### 宏观数据

| 函数 | 说明 |
|------|------|
| `get_cn_macro_gdp` | GDP |
| `get_cn_macro_cpi` | CPI |
| `get_cn_macro_ppi` | PPI |
| `get_cn_macro_pmi` | PMI |
| `get_cn_macro_money_supply` | 货币供应 |
| `get_cn_macro_social_financing` | 社会融资 |

### 配置函数

| 函数 | 说明 |
|------|------|
| `set_proxies` | 设置代理 |
| `set_timeout` | 设置超时 |
| `set_cache` | 配置缓存 |
| `get_source_health` | 数据源健康 |
| `reset_source_circuit` | 重置熔断器 |
| `set_source_priority` | 设置优先级 |

## 错误处理

```python
from finvista import (
    FinVistaError,
    NetworkError,
    DataNotFoundError,
    AllSourcesFailedError
)

try:
    df = fv.get_cn_stock_daily("000001")
except NetworkError as e:
    print(f"网络错误: {e}")
except DataNotFoundError as e:
    print(f"数据不存在: {e}")
except AllSourcesFailedError as e:
    print(f"所有数据源失败: {e}")
except FinVistaError as e:
    print(f"其他错误: {e}")
```
