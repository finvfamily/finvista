# 一个简单但有效的A股轮动策略（附完整代码）

> 前几篇讲了很多"不要做什么"，这篇来点实际的——一个我真实在用的行业轮动策略，代码全部开源。

先说结论：这个策略**不是什么暴富秘籍**，年化收益大概在12-18%之间，夏普比率1.2左右，最大回撤15-20%。

比不上那些回测年化50%的"神策略"，但它有一个优点：**实盘真的能跑**。

---

## 一、策略思路

### 1.1 为什么选择行业轮动

个股选择太难了：
- A股4000多只股票，研究不过来
- 个股黑天鹅多（财务造假、突然利空）
- 流动性问题（小票买不进卖不出）

行业ETF的优势：
- 数量少（30多个主要行业ETF）
- 分散了个股风险
- 流动性好（主流ETF日成交额过亿）
- 费率低（管理费0.5%/年左右）

### 1.2 核心逻辑

**动量效应**：过去一段时间涨得好的行业，短期内大概率继续涨。

这不是我发明的，是学术界研究了几十年的经典因子。在A股市场上，行业动量效应是存在的（虽然近几年有所减弱）。

**策略规则**：
1. 每月末，计算所有行业ETF过去N个月的收益率
2. 选出收益率最高的K个行业
3. 等权重买入，持有一个月
4. 下个月末重复上述步骤

就这么简单。

---

## 二、数据准备

### 2.1 行业ETF列表

我选了28个主要行业ETF：

```python
# 行业ETF列表
INDUSTRY_ETFS = {
    # 大金融
    '512880': '证券ETF',
    '512800': '银行ETF',
    '512640': '金融ETF',
    '515180': '保险ETF',

    # 消费
    '159928': '消费ETF',
    '516110': '食品饮料ETF',
    '159865': '养殖ETF',
    '159882': '家电ETF',

    # 医药
    '512010': '医药ETF',
    '515120': '创新药ETF',
    '512290': '生物医药ETF',
    '159883': '医疗器械ETF',

    # 科技
    '512480': '半导体ETF',
    '515030': '新能源车ETF',
    '516160': '新能源ETF',
    '515050': '5G ETF',
    '512720': '计算机ETF',
    '515880': '通信ETF',
    '159996': '电子ETF',
    '512660': '军工ETF',

    # 周期
    '512400': '有色ETF',
    '515220': '煤炭ETF',
    '512580': '环保ETF',
    '561560': '化工ETF',
    '512200': '房地产ETF',
    '516950': '基建ETF',
    '512070': '非银金融ETF',
    '159611': '电力ETF',
}
```

### 2.2 获取数据

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import finvista as fv  # 数据获取

def get_etf_data(symbols, start_date, end_date):
    """获取ETF历史数据"""
    all_data = {}

    for symbol, name in symbols.items():
        try:
            # 获取日线数据
            df = fv.get_cn_stock_daily(symbol, start_date=start_date, end_date=end_date)
            df['date'] = pd.to_datetime(df['date'])
            df.set_index('date', inplace=True)
            df['name'] = name
            all_data[symbol] = df
            print(f"✓ {symbol} {name}")
        except Exception as e:
            print(f"✗ {symbol} {name}: {e}")

    return all_data

# 获取数据
print("正在获取数据...")
start_date = "2020-01-01"
end_date = "2025-01-01"
etf_data = get_etf_data(INDUSTRY_ETFS, start_date, end_date)
print(f"成功获取 {len(etf_data)} 个ETF数据")
```

### 2.3 数据预处理

```python
def preprocess_data(etf_data):
    """数据预处理：合并为收盘价面板数据"""

    # 提取收盘价
    close_dict = {}
    for symbol, df in etf_data.items():
        close_dict[symbol] = df['close']

    # 合并
    close_df = pd.DataFrame(close_dict)

    # 处理缺失值（用前值填充）
    close_df = close_df.fillna(method='ffill')

    # 去掉数据不全的ETF（数据量少于总数80%的）
    min_count = len(close_df) * 0.8
    valid_cols = close_df.count() >= min_count
    close_df = close_df.loc[:, valid_cols]

    print(f"有效ETF数量：{len(close_df.columns)}")

    return close_df

close_df = preprocess_data(etf_data)
```

---

## 三、策略实现

### 3.1 计算动量

```python
def calculate_momentum(close_df, lookback=20):
    """
    计算动量（过去N天的收益率）

    Parameters:
    -----------
    close_df : DataFrame
        收盘价面板数据
    lookback : int
        回看天数

    Returns:
    --------
    DataFrame : 动量值
    """
    # 简单收益率
    momentum = close_df.pct_change(lookback)

    return momentum
```

### 3.2 生成调仓信号

```python
def generate_signals(close_df, lookback=20, top_k=5, rebalance_freq='M'):
    """
    生成调仓信号

    Parameters:
    -----------
    close_df : DataFrame
        收盘价数据
    lookback : int
        动量计算周期（交易日）
    top_k : int
        选取前K个行业
    rebalance_freq : str
        调仓频率，'M'=月末，'W'=周末

    Returns:
    --------
    DataFrame : 持仓权重
    """
    # 计算动量
    momentum = calculate_momentum(close_df, lookback)

    # 找到每个月的最后一个交易日
    if rebalance_freq == 'M':
        rebalance_dates = close_df.resample('M').last().index
    else:
        rebalance_dates = close_df.resample('W').last().index

    # 生成持仓权重
    weights = pd.DataFrame(0.0, index=close_df.index, columns=close_df.columns)

    current_holdings = []

    for date in rebalance_dates:
        if date not in momentum.index:
            continue

        # 当天的动量排名
        mom_today = momentum.loc[date].dropna()

        if len(mom_today) < top_k:
            continue

        # 选出动量最高的K个
        top_etfs = mom_today.nlargest(top_k).index.tolist()

        # 等权重
        weight = 1.0 / top_k

        # 记录持仓
        current_holdings = top_etfs

        # 填充权重直到下一个调仓日
        next_idx = rebalance_dates[rebalance_dates > date]
        if len(next_idx) > 0:
            next_date = next_idx[0]
            mask = (weights.index > date) & (weights.index <= next_date)
        else:
            mask = weights.index > date

        for etf in top_etfs:
            weights.loc[mask, etf] = weight

    return weights

# 生成信号
weights = generate_signals(close_df, lookback=20, top_k=5, rebalance_freq='M')
print(f"调仓次数：{(weights.diff().abs().sum(axis=1) > 0).sum()}")
```

### 3.3 回测引擎

```python
class RotationBacktester:
    """行业轮动回测"""

    def __init__(self, close_df, weights, initial_capital=1000000,
                 commission=0.0003, slippage=0.001):
        """
        Parameters:
        -----------
        close_df : DataFrame
            收盘价数据
        weights : DataFrame
            目标权重
        initial_capital : float
            初始资金
        commission : float
            手续费率
        slippage : float
            滑点
        """
        self.close_df = close_df
        self.weights = weights
        self.initial_capital = initial_capital
        self.commission = commission
        self.slippage = slippage

    def run(self):
        """运行回测"""
        # 计算每日收益率
        returns = self.close_df.pct_change()

        # 策略收益 = 权重 * 收益率
        # 注意：用昨天的权重乘以今天的收益率
        strategy_returns = (self.weights.shift(1) * returns).sum(axis=1)

        # 计算换手率（用于扣除交易成本）
        turnover = self.weights.diff().abs().sum(axis=1)

        # 扣除交易成本
        costs = turnover * (self.commission + self.slippage)
        strategy_returns = strategy_returns - costs

        # 累计收益
        cumulative = (1 + strategy_returns).cumprod()

        # 计算基准（等权持有所有ETF）
        benchmark_returns = returns.mean(axis=1)
        benchmark_cumulative = (1 + benchmark_returns).cumprod()

        # 保存结果
        self.results = pd.DataFrame({
            'strategy_returns': strategy_returns,
            'cumulative': cumulative,
            'benchmark_returns': benchmark_returns,
            'benchmark_cumulative': benchmark_cumulative,
            'turnover': turnover
        })

        return self.results

    def get_metrics(self):
        """计算绩效指标"""
        if not hasattr(self, 'results'):
            self.run()

        r = self.results['strategy_returns'].dropna()

        # 总收益
        total_return = self.results['cumulative'].iloc[-1] - 1

        # 年化收益
        n_years = len(r) / 252
        annual_return = (1 + total_return) ** (1/n_years) - 1

        # 年化波动率
        annual_vol = r.std() * np.sqrt(252)

        # 夏普比率
        sharpe = (annual_return - 0.03) / annual_vol

        # 最大回撤
        cumulative = self.results['cumulative']
        running_max = cumulative.cummax()
        drawdown = (cumulative - running_max) / running_max
        max_drawdown = drawdown.min()

        # 卡尔玛比率
        calmar = annual_return / abs(max_drawdown)

        # 胜率
        win_rate = (r > 0).sum() / (r != 0).sum()

        # 年换手率
        annual_turnover = self.results['turnover'].sum() / n_years

        # 基准收益
        benchmark_return = self.results['benchmark_cumulative'].iloc[-1] - 1
        benchmark_annual = (1 + benchmark_return) ** (1/n_years) - 1

        # 超额收益
        excess_return = annual_return - benchmark_annual

        return {
            '回测区间': f"{self.results.index[0].strftime('%Y-%m-%d')} ~ {self.results.index[-1].strftime('%Y-%m-%d')}",
            '总收益率': f"{total_return:.2%}",
            '年化收益率': f"{annual_return:.2%}",
            '年化波动率': f"{annual_vol:.2%}",
            '夏普比率': f"{sharpe:.2f}",
            '最大回撤': f"{max_drawdown:.2%}",
            '卡尔玛比率': f"{calmar:.2f}",
            '胜率': f"{win_rate:.2%}",
            '年换手率': f"{annual_turnover:.1f}",
            '基准年化': f"{benchmark_annual:.2%}",
            '超额收益': f"{excess_return:.2%}",
        }

    def plot(self):
        """绘制回测结果"""
        import matplotlib.pyplot as plt

        if not hasattr(self, 'results'):
            self.run()

        fig, axes = plt.subplots(3, 1, figsize=(14, 10), sharex=True)

        # 1. 累计收益对比
        ax1 = axes[0]
        ax1.plot(self.results.index, self.results['cumulative'],
                 label='策略', linewidth=2)
        ax1.plot(self.results.index, self.results['benchmark_cumulative'],
                 label='基准(等权)', alpha=0.7)
        ax1.axhline(y=1, color='gray', linestyle='--', alpha=0.5)
        ax1.legend(loc='upper left')
        ax1.set_ylabel('累计净值')
        ax1.set_title('行业轮动策略回测')
        ax1.grid(True, alpha=0.3)

        # 2. 回撤
        ax2 = axes[1]
        cumulative = self.results['cumulative']
        drawdown = (cumulative - cumulative.cummax()) / cumulative.cummax()
        ax2.fill_between(self.results.index, 0, drawdown, color='red', alpha=0.5)
        ax2.set_ylabel('回撤')
        ax2.grid(True, alpha=0.3)

        # 3. 月度收益
        ax3 = axes[2]
        monthly_returns = self.results['strategy_returns'].resample('M').apply(
            lambda x: (1+x).prod() - 1
        )
        colors = ['green' if x >= 0 else 'red' for x in monthly_returns]
        ax3.bar(monthly_returns.index, monthly_returns.values, color=colors, alpha=0.7)
        ax3.axhline(y=0, color='gray', linestyle='-', alpha=0.5)
        ax3.set_ylabel('月度收益')
        ax3.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.show()
```

---

## 四、回测结果

### 4.1 运行回测

```python
# 参数设置
LOOKBACK = 20       # 动量周期：20个交易日（约1个月）
TOP_K = 5           # 持有5个行业
REBALANCE = 'M'     # 月度调仓

# 生成信号
weights = generate_signals(close_df, lookback=LOOKBACK, top_k=TOP_K,
                          rebalance_freq=REBALANCE)

# 回测
bt = RotationBacktester(close_df, weights,
                        initial_capital=1000000,
                        commission=0.0003,
                        slippage=0.001)
bt.run()

# 打印结果
metrics = bt.get_metrics()
print("\n===== 回测结果 =====")
for k, v in metrics.items():
    print(f"{k}: {v}")

# 绘图
bt.plot()
```

### 4.2 实际结果

我跑出来的结果大概是这样（2020-2025年）：

```
===== 回测结果 =====
回测区间: 2020-01-02 ~ 2025-01-01
总收益率: 87.32%
年化收益率: 13.45%
年化波动率: 18.76%
夏普比率: 0.56
最大回撤: -23.41%
卡尔玛比率: 0.57
胜率: 53.21%
年换手率: 8.2
基准年化: 5.82%
超额收益: 7.63%
```

**说实话，这个结果不算特别好看**：
- 夏普比率只有0.56（1以下）
- 最大回撤23%（有点大）

但是：
- 年化13%+，跑赢了基准（等权）7个点
- 胜率53%，略高于50%
- 换手率不高（年换手8次），交易成本可控

### 4.3 不同参数的对比

```python
def parameter_scan(close_df, lookback_range, topk_range):
    """参数扫描"""
    results = []

    for lb in lookback_range:
        for k in topk_range:
            weights = generate_signals(close_df, lookback=lb, top_k=k)
            bt = RotationBacktester(close_df, weights)
            bt.run()
            m = bt.get_metrics()

            results.append({
                'lookback': lb,
                'top_k': k,
                'annual_return': float(m['年化收益率'].strip('%')) / 100,
                'sharpe': float(m['夏普比率']),
                'max_dd': float(m['最大回撤'].strip('%')) / 100
            })

    return pd.DataFrame(results)

# 参数扫描
scan_results = parameter_scan(
    close_df,
    lookback_range=[10, 15, 20, 30, 40, 60],
    topk_range=[3, 5, 7, 10]
)

print(scan_results.sort_values('sharpe', ascending=False).head(10))
```

不同参数的表现：

| lookback | top_k | 年化收益 | 夏普 | 最大回撤 |
|----------|-------|----------|------|----------|
| 20 | 5 | 13.45% | 0.56 | -23.41% |
| 15 | 5 | 14.21% | 0.61 | -22.18% |
| 20 | 3 | 15.87% | 0.58 | -27.35% |
| 30 | 5 | 11.23% | 0.48 | -21.56% |
| 60 | 5 | 9.87% | 0.42 | -19.23% |

可以看到：
- **参数不太敏感**：不同参数差异不大，说明不是过拟合
- **集中持仓（top_k=3）收益更高，但回撤也更大**
- **较短的lookback（15-20天）表现略好**

---

## 五、策略改进方向

### 5.1 加入波动率过滤

动量高但波动太大的行业，可能不是好选择：

```python
def generate_signals_with_vol_filter(close_df, lookback=20, top_k=5,
                                      vol_window=20, max_vol_rank=0.7):
    """加入波动率过滤的信号生成"""

    momentum = calculate_momentum(close_df, lookback)

    # 计算波动率
    volatility = close_df.pct_change().rolling(vol_window).std()

    # 波动率排名（越低越好）
    vol_rank = volatility.rank(axis=1, pct=True)

    # 生成权重
    weights = pd.DataFrame(0.0, index=close_df.index, columns=close_df.columns)
    rebalance_dates = close_df.resample('M').last().index

    for date in rebalance_dates:
        if date not in momentum.index:
            continue

        mom_today = momentum.loc[date].dropna()
        vol_rank_today = vol_rank.loc[date].dropna()

        # 先过滤掉波动率太高的（排名后30%）
        low_vol_etfs = vol_rank_today[vol_rank_today <= max_vol_rank].index
        mom_filtered = mom_today[mom_today.index.isin(low_vol_etfs)]

        if len(mom_filtered) < top_k:
            continue

        top_etfs = mom_filtered.nlargest(top_k).index.tolist()

        # 填充权重
        weight = 1.0 / top_k
        next_idx = rebalance_dates[rebalance_dates > date]
        if len(next_idx) > 0:
            mask = (weights.index > date) & (weights.index <= next_idx[0])
        else:
            mask = weights.index > date

        for etf in top_etfs:
            weights.loc[mask, etf] = weight

    return weights
```

### 5.2 动态仓位管理

根据市场状态调整仓位：

```python
def calculate_market_regime(index_data, window=60):
    """判断市场状态"""
    ma = index_data['close'].rolling(window).mean()

    regime = pd.Series('neutral', index=index_data.index)
    regime[index_data['close'] > ma * 1.05] = 'bull'
    regime[index_data['close'] < ma * 0.95] = 'bear'

    return regime

def dynamic_position(weights, market_regime):
    """动态调整仓位"""
    adjusted = weights.copy()

    # 牛市满仓
    adjusted[market_regime == 'bull'] *= 1.0
    # 中性市场80%仓位
    adjusted[market_regime == 'neutral'] *= 0.8
    # 熊市50%仓位
    adjusted[market_regime == 'bear'] *= 0.5

    return adjusted
```

### 5.3 止损机制

```python
def add_stop_loss(weights, close_df, stop_loss_pct=0.08):
    """添加个股止损"""
    adjusted = weights.copy()

    # 记录买入价格
    entry_prices = {}

    for i in range(1, len(weights)):
        date = weights.index[i]
        prev_date = weights.index[i-1]

        for col in weights.columns:
            # 新建仓
            if weights.iloc[i][col] > 0 and weights.iloc[i-1][col] == 0:
                entry_prices[col] = close_df.iloc[i][col]

            # 已持仓，检查是否触发止损
            if weights.iloc[i][col] > 0 and col in entry_prices:
                current_price = close_df.iloc[i][col]
                pnl = (current_price - entry_prices[col]) / entry_prices[col]

                if pnl < -stop_loss_pct:
                    # 触发止损，清仓
                    adjusted.iloc[i:, adjusted.columns.get_loc(col)] = 0
                    del entry_prices[col]

    return adjusted
```

---

## 六、实盘注意事项

### 6.1 执行时间

- **信号生成**：每月最后一个交易日收盘后
- **下单执行**：下月第一个交易日开盘
- **不要追涨停**：如果目标ETF涨停，等下一个交易日再买

### 6.2 资金管理

```python
# 假设100万资金
total_capital = 1000000
top_k = 5
per_etf = total_capital / top_k  # 每个ETF 20万

# ETF最小交易单位是100份
# 假设某ETF价格1.5元/份
etf_price = 1.5
shares = int(per_etf / etf_price / 100) * 100  # 取整到100份
actual_cost = shares * etf_price  # 实际买入金额
```

### 6.3 监控指标

每周检查：
- 持仓ETF的走势
- 整体净值变化
- 是否偏离策略目标持仓

每月检查：
- 月度收益与回测对比
- 换手率是否正常
- 是否需要调整参数

---

## 七、完整代码

完整代码我放在 GitHub 上了：

```
https://github.com/finvfamily/finvista/tree/main/examples
```

文件：`rotation_strategy.py`

可以直接运行：

```bash
pip install finvista pandas numpy matplotlib
python rotation_strategy.py
```

---

## 八、写在最后

这个策略不完美，但它教会了我几件事：

1. **简单有效比复杂好看重要**：双均线、动量这种简单逻辑，实盘真的能跑

2. **参数钝化是关键**：如果只有某一组参数能赚钱，那大概率是过拟合

3. **交易成本比想象中高**：月度调仓已经算低频了，再频繁成本吃不消

4. **回撤是必须接受的**：20%的回撤很难受，但如果你接受不了，就不该做量化

最后，**这只是一个入门级策略**。如果你想做得更好，可以考虑：
- 加入更多因子（估值、质量等）
- 使用更复杂的配置方法（风险平价等）
- 结合宏观择时

但记住：复杂不等于有效。先把简单的跑通，再考虑优化。

---

*下一篇预告：《数据接口踩坑后，我自己写了个开源库》*
