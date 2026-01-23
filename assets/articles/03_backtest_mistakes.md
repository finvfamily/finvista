# 为什么你的回测结果不可信？量化回测的7个致命错误

> 回测年化50%，实盘亏成狗——这种事我见过太多了，自己也经历过。问题往往不在策略本身，而在回测方法。

我刚开始做量化的时候，写了个策略，回测三年年化收益60%，夏普比率2.8。当时觉得自己发现了圣杯。

实盘跑了半年，亏了18%。

后来花了很长时间复盘，才发现回测里藏着好几个"作弊"——不是故意的，是我根本不知道那些是错的。

这篇文章总结7个最常见的回测错误，每个都配代码说明，希望能帮你避坑。

---

## 错误1：使用未来数据（Look-Ahead Bias）

这是最隐蔽、也是最致命的错误。

### 什么是未来数据

在回测的某个时间点，使用了那个时间点之后才能获得的信息。

### 典型场景

**场景A：用当天收盘价判断当天能否买入**

```python
# ❌ 错误写法
for i in range(len(data)):
    if data['close'].iloc[i] > data['ma20'].iloc[i]:  # 用收盘价判断
        buy(data['close'].iloc[i])  # 以收盘价买入

# 问题：收盘价是收盘后才知道的，你不可能在收盘前用收盘价做决策
```

```python
# ✅ 正确写法
for i in range(1, len(data)):
    # 用昨天的收盘价判断，今天开盘买入
    if data['close'].iloc[i-1] > data['ma20'].iloc[i-1]:
        buy(data['open'].iloc[i])
```

**场景B：财报数据的发布时间**

```python
# ❌ 错误写法
# 假设在3月1日，使用2月28日的财报数据选股
# 但实际上，2月28日的财报可能要到4月才发布

# ✅ 正确写法
# 使用财报的"发布日期"而不是"报告期"
# 只在发布日期之后才能使用该财报数据
```

**场景C：指数成分股的调整**

```python
# ❌ 错误写法
# 用"当前"的沪深300成分股回测2020年的策略
# 但2020年的成分股和现在不一样

# ✅ 正确写法
# 使用历史成分股数据，每个时间点只用当时的成分股
```

### 如何检测

```python
def check_look_ahead_bias(signals, data):
    """
    检测是否存在未来数据偏差
    方法：打乱未来数据，看信号是否变化
    """
    original_signals = signals.copy()

    # 打乱未来10天的数据
    for i in range(len(data) - 10):
        shuffled_data = data.copy()
        shuffled_data.iloc[i+1:i+10] = np.random.permutation(
            shuffled_data.iloc[i+1:i+10].values
        )

        # 重新计算第i天的信号
        new_signal = calculate_signal(shuffled_data, i)

        if new_signal != original_signals.iloc[i]:
            print(f"警告：第{i}天的信号可能使用了未来数据")
            return True

    return False
```

---

## 错误2：幸存者偏差（Survivorship Bias）

### 什么是幸存者偏差

只用"活下来"的股票做回测，忽略了退市、停牌的股票。

### 为什么这是个问题

假设你在2015年选了10只"高成长"股票：
- 其中3只后来退市了
- 2只长期停牌
- 剩下5只表现还不错

如果你的回测数据只包含现在还在交易的股票，那3只退市的、2只停牌的都不会出现在你的股票池里。你的策略"神奇地"避开了所有雷。

### 实际影响有多大

我做过一个测试：

```python
# 测试幸存者偏差的影响

# 方法1：用2025年的股票池回测2020-2025年
result_biased = backtest(
    stock_pool=get_current_stocks(),  # 当前可交易的股票
    start='2020-01-01',
    end='2025-01-01'
)
print(f"有偏差的结果：年化 {result_biased['annual_return']:.2%}")

# 方法2：用历史时点数据回测
result_unbiased = backtest(
    stock_pool=get_historical_stocks,  # 每个时点用当时的股票池
    start='2020-01-01',
    end='2025-01-01'
)
print(f"无偏差的结果：年化 {result_unbiased['annual_return']:.2%}")

# 实测差异：有偏差的年化收益比无偏差的高5-15个百分点
```

### 正确做法

1. 使用包含退市股的全量历史数据库
2. 在每个回测时点，只用当时可交易的股票
3. 正确处理退市：退市前一天强制卖出

```python
def get_tradable_stocks(date):
    """获取某一天可交易的股票列表"""
    all_stocks = get_all_historical_stocks()

    tradable = []
    for stock in all_stocks:
        # 检查上市日期
        if stock['list_date'] > date:
            continue
        # 检查退市日期
        if stock['delist_date'] and stock['delist_date'] <= date:
            continue
        # 检查是否停牌
        if is_suspended(stock['code'], date):
            continue
        tradable.append(stock['code'])

    return tradable
```

---

## 错误3：忽略交易成本

### 实际成本有多少

很多人回测时手续费设成万一甚至不设，但实际成本远不止这些：

| 成本项 | 比例 | 说明 |
|--------|------|------|
| 佣金 | 万2.5~万3 | 买卖双向收取 |
| 印花税 | 千1 | 仅卖出收取 |
| 过户费 | 万0.2 | 仅上海市场 |
| 滑点 | 0.1%~0.5% | 取决于流动性 |

**单次交易（买+卖）的真实成本**：
- 低估版：0.1%（很多回测用这个）
- 实际版：0.3%~0.5%

### 滑点被严重低估

滑点是买卖价差 + 冲击成本。

```python
# 理想情况
buy_price = data['close']  # 以收盘价买入

# 实际情况
# 你挂单的时候，价格可能已经动了
# 特别是小市值、低流动性股票

def estimate_slippage(data, order_size):
    """估算滑点"""
    # 买一卖一价差
    spread = (data['ask1'] - data['bid1']) / data['close']

    # 冲击成本：订单越大，冲击越大
    daily_volume = data['volume'] * data['close']
    impact = 0.1 * (order_size / daily_volume) ** 0.5

    return spread / 2 + impact
```

### 高频换手的成本陷阱

```python
# 假设策略每周换手一次，年换手52次
turnover = 52
cost_per_trade = 0.004  # 单边成本0.4%

annual_cost = turnover * cost_per_trade * 2  # 买+卖
print(f"年度交易成本：{annual_cost:.2%}")  # 41.6%！

# 这意味着你的策略必须年化41.6%以上，才能打平成本
```

### 正确做法

```python
class RealisticBacktester:
    def __init__(self):
        self.commission_rate = 0.00025  # 万2.5
        self.stamp_tax = 0.001          # 千1印花税
        self.transfer_fee = 0.00002     # 万0.2过户费
        self.slippage = 0.002           # 0.2%滑点

    def execute_buy(self, price, shares, market='SH'):
        cost = shares * price
        commission = max(cost * self.commission_rate, 5)  # 最低5元
        slippage_cost = cost * self.slippage
        transfer = cost * self.transfer_fee if market == 'SH' else 0

        total_cost = cost + commission + slippage_cost + transfer
        actual_price = total_cost / shares
        return actual_price

    def execute_sell(self, price, shares, market='SH'):
        revenue = shares * price
        commission = max(revenue * self.commission_rate, 5)
        stamp = revenue * self.stamp_tax
        slippage_cost = revenue * self.slippage
        transfer = revenue * self.transfer_fee if market == 'SH' else 0

        net_revenue = revenue - commission - stamp - slippage_cost - transfer
        actual_price = net_revenue / shares
        return actual_price
```

---

## 错误4：过度优化（Curve Fitting）

### 什么是过度优化

通过不断调参，让策略完美拟合历史数据，但对未来毫无预测能力。

### 典型案例

```python
# 某人的"优化"过程

# 第1版：MA5/MA20，回测收益15%
# "感觉还可以优化"

# 第2版：MA5/MA17，回测收益22%
# "继续调"

# 第3版：MA6/MA17，回测收益28%
# "再试试"

# 第10版：MA7/MA13，回测收益45%
# "完美！就用这个参数"

# 结果：实盘亏钱，因为MA7/MA13只是在这段历史数据上"碰巧"表现好
```

### 如何判断是否过度优化

**方法1：参数热力图**

```python
def parameter_heatmap(data, param1_range, param2_range):
    """绘制参数热力图"""
    results = np.zeros((len(param1_range), len(param2_range)))

    for i, p1 in enumerate(param1_range):
        for j, p2 in enumerate(param2_range):
            ret = backtest(data, p1, p2)
            results[i, j] = ret['sharpe']

    plt.figure(figsize=(10, 8))
    plt.imshow(results, cmap='RdYlGn')
    plt.colorbar(label='Sharpe Ratio')
    plt.xlabel('Param 2')
    plt.ylabel('Param 1')
    plt.title('Parameter Sensitivity')
    plt.show()

    return results

# 如果只有一小块区域是绿的（表现好），其他都是红的（表现差）
# 说明参数敏感，大概率是过度优化
```

**方法2：样本外测试**

```python
def out_of_sample_test(data, strategy, params):
    """样本外测试"""
    # 数据分成三份
    n = len(data)
    train = data[:int(n*0.6)]      # 60% 训练
    valid = data[int(n*0.6):int(n*0.8)]  # 20% 验证
    test = data[int(n*0.8):]       # 20% 测试

    # 在训练集上调参
    best_params = optimize(train, strategy, params)

    # 在验证集上检验
    valid_result = backtest(valid, strategy, best_params)

    # 在测试集上最终验证（只能用一次）
    test_result = backtest(test, strategy, best_params)

    print(f"训练集夏普：{train_result['sharpe']:.2f}")
    print(f"验证集夏普：{valid_result['sharpe']:.2f}")
    print(f"测试集夏普：{test_result['sharpe']:.2f}")

    # 如果训练集 >> 验证集 >> 测试集，说明过拟合
```

### 正确做法

1. **先定逻辑，再选参数**
   - MA20有经济含义（约一个月），比MA17更有道理

2. **参数要钝化**
   - 如果MA20表现好，MA18和MA22应该也不差

3. **滚动窗口优化**
   - 不要用全部数据一次性优化

---

## 错误5：忽略流动性限制

### 问题描述

回测假设你可以以任意价格、任意数量成交。实际上：
- 小市值股票你买不到那么多
- 跌停板你卖不出去
- 大单会冲击市场价格

### 实际影响

```python
# 案例：某小市值策略

# 回测
target_position = 1000000  # 想买100万
buy_price = data['close']  # 以收盘价买入
# 回测里，100万瞬间成交，价格就是收盘价

# 现实
daily_volume = 5000000  # 日成交额500万
my_order = 1000000      # 我要买100万

# 问题1：100万占日成交的20%，你的买入本身就会拉升股价
# 问题2：你可能买不到那么多，尤其是涨停的时候
```

### 流动性过滤

```python
def liquidity_filter(stock_pool, date, min_amount=100000000):
    """
    流动性过滤
    min_amount: 最低日成交额，默认1亿
    """
    filtered = []
    for stock in stock_pool:
        # 过去20日平均成交额
        avg_amount = get_average_amount(stock, date, window=20)
        if avg_amount >= min_amount:
            filtered.append(stock)
    return filtered

def max_position_size(stock, date, max_ratio=0.1):
    """
    计算最大可买入金额
    max_ratio: 最多占日成交额的比例
    """
    avg_amount = get_average_amount(stock, date, window=20)
    return avg_amount * max_ratio
```

### 冲击成本模型

```python
def market_impact(order_size, daily_volume, volatility):
    """
    市场冲击模型（简化版）

    参考：Almgren-Chriss模型
    """
    participation_rate = order_size / daily_volume

    # 临时冲击：与参与率的平方根成正比
    temporary_impact = 0.1 * volatility * np.sqrt(participation_rate)

    # 永久冲击：与参与率成正比
    permanent_impact = 0.05 * volatility * participation_rate

    return temporary_impact + permanent_impact

# 示例
order = 1000000
volume = 5000000
vol = 0.02  # 日波动率2%

impact = market_impact(order, volume, vol)
print(f"预估冲击成本：{impact:.2%}")  # 约0.9%
```

---

## 错误6：样本量不足

### 问题描述

用太短的历史数据做回测，结果不具备统计意义。

### 错误示例

```python
# ❌ 只用3个月数据回测
data = get_data('2024-10-01', '2024-12-31')  # 60个交易日
result = backtest(data, strategy)
print(f"年化收益：{result['annual_return']:.2%}")  # 意义不大

# 问题：
# 1. 样本量太小，随机性太大
# 2. 没有覆盖不同市场环境（牛市、熊市、震荡）
# 3. 统计指标不可靠
```

### 多少数据才够

| 策略类型 | 建议样本量 | 说明 |
|----------|------------|------|
| 日线策略 | 3-5年 | 至少500-1000个交易日 |
| 周线策略 | 5-10年 | 至少250-500个数据点 |
| 月线策略 | 10年+ | 至少120个数据点 |

### 统计显著性检验

```python
def statistical_significance(returns, benchmark_returns=None):
    """
    检验策略收益是否具有统计显著性
    """
    n = len(returns)

    # 方法1：t检验（收益是否显著大于0）
    t_stat, p_value = stats.ttest_1samp(returns, 0)

    # 方法2：如果有基准，检验超额收益
    if benchmark_returns is not None:
        excess = returns - benchmark_returns
        t_stat_excess, p_value_excess = stats.ttest_1samp(excess, 0)
    else:
        p_value_excess = None

    # 方法3：计算所需样本量
    # 假设年化收益10%，波动率20%，要达到5%显著性水平
    effect_size = 0.10 / 0.20  # 0.5
    required_n = (2.8 / effect_size) ** 2  # 约31个数据点

    return {
        'n': n,
        'p_value': p_value,
        'p_value_excess': p_value_excess,
        'significant': p_value < 0.05,
        'required_n': required_n
    }
```

### 不同市场环境的测试

```python
def multi_regime_test(data, strategy):
    """
    在不同市场环境下测试策略
    """
    results = {}

    # 识别市场环境
    data['regime'] = classify_market_regime(data)

    # 牛市
    bull_data = data[data['regime'] == 'bull']
    results['bull'] = backtest(bull_data, strategy)

    # 熊市
    bear_data = data[data['regime'] == 'bear']
    results['bear'] = backtest(bear_data, strategy)

    # 震荡市
    range_data = data[data['regime'] == 'range']
    results['range'] = backtest(range_data, strategy)

    # 打印对比
    for regime, r in results.items():
        print(f"{regime}: 年化{r['annual_return']:.2%}, "
              f"夏普{r['sharpe']:.2f}, "
              f"最大回撤{r['max_drawdown']:.2%}")

    return results
```

---

## 错误7：忽略市场微观结构

### 问题描述

回测假设市场是"理想"的，但真实市场有很多细节：
- 涨跌停限制
- T+1交易制度
- 集合竞价
- 临时停牌

### 涨跌停处理

```python
def handle_limit_up_down(order, data):
    """处理涨跌停"""

    # 涨停买不进
    if data['close'] == data['limit_up']:
        if order['side'] == 'buy':
            return None  # 无法买入

    # 跌停卖不出
    if data['close'] == data['limit_down']:
        if order['side'] == 'sell':
            return None  # 无法卖出

    return order

# ❌ 错误：回测里涨停也能买到
# ✅ 正确：涨停的股票买单要排队，很可能买不到
```

### T+1制度

```python
# ❌ 错误
if signal == 'buy':
    buy(stock)
if signal == 'sell':
    sell(stock)  # A股不能当天买当天卖！

# ✅ 正确
class Position:
    def __init__(self):
        self.holdings = {}  # {stock: {'shares': 100, 'buy_date': date}}

    def can_sell(self, stock, current_date):
        if stock not in self.holdings:
            return False
        buy_date = self.holdings[stock]['buy_date']
        return current_date > buy_date  # 必须隔天才能卖
```

### 集合竞价

```python
# 集合竞价（9:15-9:25）期间：
# - 9:15-9:20 可以撤单
# - 9:20-9:25 不能撤单
# - 开盘价在9:25确定

# 如果策略依赖开盘价买入，要注意：
# 1. 你挂的单可能成交不了
# 2. 开盘价可能跟你预期的不一样

def execute_at_open(order, data):
    """模拟集合竞价成交"""
    open_price = data['open']

    # 买单：如果你出价低于开盘价，成交不了
    if order['side'] == 'buy' and order['price'] < open_price:
        return None

    # 卖单：如果你出价高于开盘价，成交不了
    if order['side'] == 'sell' and order['price'] > open_price:
        return None

    return {'price': open_price, 'shares': order['shares']}
```

---

## 如何验证你的回测是否可靠

### 检查清单

```markdown
□ 是否使用了未来数据
□ 是否存在幸存者偏差
□ 交易成本是否合理（建议至少千三）
□ 是否做了样本外测试
□ 参数是否敏感
□ 是否考虑了流动性限制
□ 样本量是否足够（建议3年以上）
□ 是否在不同市场环境下测试
□ 是否正确处理涨跌停、T+1等规则
```

### 回测结果折扣

根据我的经验，回测结果要打折：

| 情况 | 折扣系数 |
|------|----------|
| 完美回测（上述都做到了） | 70-80% |
| 普通回测 | 50-60% |
| 新手回测 | 30%以下 |

也就是说，回测年化30%的策略，实盘能有15-20%就不错了。

---

## 总结

7个致命错误：

1. **未来数据**：用了还没发生的信息
2. **幸存者偏差**：只看活着的股票
3. **忽略成本**：手续费、滑点被低估
4. **过度优化**：在历史数据上凑参数
5. **流动性幻觉**：以为什么都能买到/卖掉
6. **样本量不足**：数据太短没有统计意义
7. **微观结构**：忽略涨跌停、T+1等规则

**回测不是目的，实盘赚钱才是目的。**

一个保守但可靠的回测，比一个漂亮但不可靠的回测，有价值得多。

---

*下一篇预告：《一个简单但有效的A股轮动策略（附完整代码）》*
