# 我的量化交易工作流：从想法到实盘的完整流程

> 上一篇分享了踩坑经历，这篇讲讲我现在的工作流程。不一定是最优解，但至少是踩完坑之后沉淀下来的方法。

很多人觉得量化交易就是"写个策略→回测→上实盘"，三步搞定。

实际上，一个靠谱的量化策略从想法到实盘，中间至少要经过7个阶段。跳过任何一个，大概率会在实盘时付出代价。

---

## 整体流程概览

```
想法产生 → 数据准备 → 策略开发 → 回测验证 → 参数优化 → 模拟盘 → 实盘
   ↑                                                              │
   └──────────────── 复盘迭代 ←────────────────────────────────────┘
```

下面逐个阶段展开。

---

## 一、想法产生：别从"我觉得"出发

### 1.1 想法来源

好的策略想法一般来自这几个地方：

**学术论文**
- SSRN、arXiv 上有大量因子研究论文
- 重点看近3年的，太老的可能已经失效
- 注意区分"样本内"和"样本外"结果

**经典书籍**
- 《量化交易》（Ernest Chan）
- 《主动投资组合管理》
- 《因子投资》

**市场观察**
- 某类事件发生后，市场有规律性反应
- 比如：财报发布后的漂移、节假日效应

**同行交流**
- 量化社区、论坛
- 但要独立验证，别人赚钱的策略不一定适合你

### 1.2 想法筛选

不是每个想法都值得花时间验证。我的筛选标准：

| 标准 | 说明 |
|------|------|
| **逻辑自洽** | 能解释清楚为什么能赚钱 |
| **可验证** | 有数据可以回测 |
| **可执行** | 不需要超高频、不需要巨额资金 |
| **有壁垒** | 不是随便搜一下就能找到的策略 |

举个反例：
> "我觉得股价跌多了就会涨"

这种想法没有明确定义（跌多少算"多"？），无法验证，不值得继续。

举个正例：
> "财报超预期的股票，在财报发布后5天内有超额收益"

这个想法有明确定义，可以用数据验证，值得深入研究。

---

## 二、数据准备：地基不牢，地动山摇

### 2.1 确定数据需求

根据策略想法，列出需要的数据：

```
策略：财报超预期
需要数据：
  - 股票日线行情（价格、成交量）
  - 财报发布日期
  - 财报实际值
  - 分析师预期值
  - 股票基本信息（行业、市值）
```

### 2.2 数据获取

数据来源选择原则：
- **稳定性优先**：接口动不动挂的，不能用
- **准确性验证**：抽样对比多个数据源
- **成本考量**：能免费搞定的，不花冤枉钱

我现在的数据来源组合：
- 日线行情：多个源互备，哪个稳定用哪个
- 财务数据：东方财富为主
- 另类数据：自己爬取 + 清洗

### 2.3 数据清洗

原始数据一定有问题，清洗是必须的：

```python
def clean_stock_data(df):
    """股票数据清洗"""

    # 1. 去除空值
    df = df.dropna(subset=['open', 'high', 'low', 'close'])

    # 2. 去除明显异常值（涨跌超过20%的，A股不可能）
    df = df[df['close'].pct_change().abs() < 0.2]

    # 3. 处理停牌（成交量为0）
    df['is_trade'] = df['volume'] > 0

    # 4. 检查OHLC逻辑
    # high >= low, high >= open, high >= close 等
    df = df[df['high'] >= df['low']]
    df = df[df['high'] >= df['open']]
    df = df[df['high'] >= df['close']]
    df = df[df['low'] <= df['open']]
    df = df[df['low'] <= df['close']]

    return df
```

### 2.4 数据验证

清洗完不代表没问题，还要抽样验证：

```python
# 随机抽10只股票，对比官方数据
import random

symbols = random.sample(all_symbols, 10)
for symbol in symbols:
    my_data = get_my_data(symbol, '2024-01-15')
    official_data = get_official_data(symbol, '2024-01-15')  # 比如去看行情软件

    if abs(my_data['close'] - official_data['close']) > 0.01:
        print(f"警告：{symbol} 数据不一致")
```

---

## 三、策略开发：先写伪代码，再写真代码

### 3.1 伪代码阶段

在写代码之前，先用自然语言把策略逻辑写清楚：

```
策略：双均线突破

买入条件：
  - MA5 上穿 MA20
  - 当日成交量 > 过去20日平均成交量
  - 股票未停牌

卖出条件：
  - MA5 下穿 MA20
  - 或者亏损超过5%（止损）
  - 或者盈利超过15%（止盈）

仓位管理：
  - 单只股票最多10%仓位
  - 最多同时持有10只股票
```

### 3.2 模块化设计

我的策略代码结构：

```
strategy/
├── signals/          # 信号生成
│   ├── base.py       # 信号基类
│   ├── ma_cross.py   # 均线交叉信号
│   └── momentum.py   # 动量信号
├── filters/          # 过滤条件
│   ├── liquidity.py  # 流动性过滤
│   └── industry.py   # 行业过滤
├── position/         # 仓位管理
│   ├── equal.py      # 等权重
│   └── risk_parity.py # 风险平价
├── risk/             # 风险控制
│   ├── stop_loss.py  # 止损
│   └── max_drawdown.py
└── executor.py       # 执行引擎
```

模块化的好处：
- 同一个信号模块可以复用到不同策略
- 方便单独测试每个模块
- 修改一处不影响其他部分

### 3.3 核心代码示例

```python
class Strategy:
    """策略基类"""

    def __init__(self, config):
        self.config = config
        self.signals = []
        self.filters = []
        self.position_manager = None
        self.risk_manager = None

    def add_signal(self, signal):
        self.signals.append(signal)

    def add_filter(self, filter):
        self.filters.append(filter)

    def generate_signals(self, data):
        """生成原始信号"""
        combined = None
        for signal in self.signals:
            s = signal.calculate(data)
            if combined is None:
                combined = s
            else:
                combined = combined & s  # 多个信号取交集
        return combined

    def apply_filters(self, signals, data):
        """应用过滤条件"""
        filtered = signals.copy()
        for f in self.filters:
            filtered = f.apply(filtered, data)
        return filtered

    def calculate_positions(self, signals, data):
        """计算目标仓位"""
        return self.position_manager.calculate(signals, data)

    def apply_risk_control(self, positions, current_holdings):
        """应用风险控制"""
        return self.risk_manager.adjust(positions, current_holdings)


class MACrossSignal:
    """均线交叉信号"""

    def __init__(self, short_window=5, long_window=20):
        self.short = short_window
        self.long = long_window

    def calculate(self, data):
        ma_short = data['close'].rolling(self.short).mean()
        ma_long = data['close'].rolling(self.long).mean()

        # 上穿
        cross_up = (ma_short > ma_long) & (ma_short.shift(1) <= ma_long.shift(1))
        # 下穿
        cross_down = (ma_short < ma_long) & (ma_short.shift(1) >= ma_long.shift(1))

        signal = pd.Series(0, index=data.index)
        signal[cross_up] = 1   # 买入信号
        signal[cross_down] = -1  # 卖出信号

        return signal
```

---

## 四、回测验证：你的回测框架靠谱吗

### 4.1 回测框架选择

我用过的回测框架：
- **自己写**：灵活，但要造很多轮子
- **Backtrader**：功能全，但学习曲线陡
- **自研简化版**：够用，好维护

对于大多数日线策略，自己写一个简单的回测框架就够了：

```python
class SimpleBacktester:
    """简易回测框架"""

    def __init__(self, initial_capital=1000000, commission=0.001):
        self.initial_capital = initial_capital
        self.commission = commission

    def run(self, data, signals):
        """
        data: DataFrame with OHLCV
        signals: Series, 1=买入, -1=卖出, 0=持有
        """
        capital = self.initial_capital
        position = 0
        entry_price = 0

        records = []

        for i, (date, row) in enumerate(data.iterrows()):
            signal = signals.iloc[i] if i < len(signals) else 0

            # 执行交易
            if signal == 1 and position == 0:  # 买入
                shares = int(capital * 0.95 / row['close'] / 100) * 100
                cost = shares * row['close'] * (1 + self.commission)
                if cost <= capital:
                    position = shares
                    entry_price = row['close']
                    capital -= cost

            elif signal == -1 and position > 0:  # 卖出
                revenue = position * row['close'] * (1 - self.commission)
                capital += revenue
                position = 0

            # 记录每日状态
            portfolio_value = capital + position * row['close']
            records.append({
                'date': date,
                'capital': capital,
                'position': position,
                'price': row['close'],
                'portfolio_value': portfolio_value
            })

        return pd.DataFrame(records)
```

### 4.2 关键回测指标

```python
def calculate_metrics(returns):
    """计算回测指标"""

    # 总收益
    total_return = (1 + returns).prod() - 1

    # 年化收益
    n_years = len(returns) / 252
    annual_return = (1 + total_return) ** (1 / n_years) - 1

    # 年化波动率
    annual_volatility = returns.std() * np.sqrt(252)

    # 夏普比率（假设无风险利率3%）
    sharpe_ratio = (annual_return - 0.03) / annual_volatility

    # 最大回撤
    cumulative = (1 + returns).cumprod()
    running_max = cumulative.cummax()
    drawdown = (cumulative - running_max) / running_max
    max_drawdown = drawdown.min()

    # 卡尔玛比率
    calmar_ratio = annual_return / abs(max_drawdown) if max_drawdown != 0 else 0

    # 胜率
    win_rate = (returns > 0).sum() / (returns != 0).sum()

    # 盈亏比
    avg_win = returns[returns > 0].mean()
    avg_loss = abs(returns[returns < 0].mean())
    profit_loss_ratio = avg_win / avg_loss if avg_loss != 0 else 0

    return {
        '总收益率': f'{total_return:.2%}',
        '年化收益率': f'{annual_return:.2%}',
        '年化波动率': f'{annual_volatility:.2%}',
        '夏普比率': f'{sharpe_ratio:.2f}',
        '最大回撤': f'{max_drawdown:.2%}',
        '卡尔玛比率': f'{calmar_ratio:.2f}',
        '胜率': f'{win_rate:.2%}',
        '盈亏比': f'{profit_loss_ratio:.2f}'
    }
```

### 4.3 我关注的指标优先级

1. **夏普比率 > 1.5**：风险调整后收益要够好
2. **最大回撤 < 20%**：能扛得住
3. **卡尔玛比率 > 1**：收益/回撤要合理
4. **胜率 × 盈亏比**：这个乘积决定长期能不能赚钱

---

## 五、参数优化：小心过拟合陷阱

### 5.1 正确的优化方法

```python
def walk_forward_optimization(data, strategy, param_grid,
                               train_period=252, test_period=63):
    """
    滚动窗口优化
    - 用过去1年训练，未来1季度测试
    - 避免一次性用全部数据优化
    """
    results = []

    for i in range(train_period, len(data) - test_period, test_period):
        # 划分训练集和测试集
        train_data = data.iloc[i-train_period:i]
        test_data = data.iloc[i:i+test_period]

        # 在训练集上寻找最优参数
        best_param = None
        best_sharpe = -np.inf

        for params in param_grid:
            perf = backtest(train_data, strategy, params)
            if perf['sharpe'] > best_sharpe:
                best_sharpe = perf['sharpe']
                best_param = params

        # 用最优参数在测试集上验证
        test_perf = backtest(test_data, strategy, best_param)
        results.append({
            'period': f"{test_data.index[0]} - {test_data.index[-1]}",
            'train_sharpe': best_sharpe,
            'test_sharpe': test_perf['sharpe'],
            'params': best_param
        })

    return pd.DataFrame(results)
```

### 5.2 参数敏感性分析

```python
def sensitivity_analysis(data, strategy, base_params, param_name, param_range):
    """
    检验参数是否过度敏感
    """
    results = []

    for value in param_range:
        params = base_params.copy()
        params[param_name] = value
        perf = backtest(data, strategy, params)
        results.append({
            param_name: value,
            'sharpe': perf['sharpe'],
            'return': perf['total_return']
        })

    df = pd.DataFrame(results)

    # 如果结果波动太大，说明参数敏感，策略不稳健
    sharpe_std = df['sharpe'].std()
    if sharpe_std > 0.5:
        print(f"警告：{param_name} 参数敏感，夏普比率标准差 = {sharpe_std:.2f}")

    return df
```

---

## 六、模拟盘：实盘前的最后一关

### 6.1 为什么要跑模拟盘

回测再好看，也有几个问题没法验证：
- 信号实时生成有没有bug
- 数据延迟有没有影响
- 执行逻辑对不对

模拟盘就是用真实行情、不用真钱，跑一遍完整流程。

### 6.2 模拟盘运行流程

```python
# 每日运行脚本示例

def daily_run():
    """每日定时任务"""

    # 1. 获取最新数据
    logger.info("开始获取数据...")
    data = fetch_latest_data()

    # 2. 生成信号
    logger.info("生成交易信号...")
    signals = strategy.generate_signals(data)

    # 3. 计算目标仓位
    target_positions = strategy.calculate_positions(signals)

    # 4. 与当前持仓对比，生成交易指令
    current_positions = load_current_positions()
    orders = generate_orders(current_positions, target_positions)

    # 5. 记录交易指令（模拟盘不真正下单）
    logger.info(f"今日交易指令：{orders}")
    save_orders(orders)

    # 6. 更新模拟持仓
    update_simulated_positions(orders, data)

    # 7. 记录每日净值
    nav = calculate_nav()
    save_daily_nav(nav)

    # 8. 发送日报
    send_daily_report(orders, nav)
```

### 6.3 模拟盘要跑多久

我的标准：
- **最少1个月**：覆盖月初/月末效应
- **最好3个月**：覆盖一个季度的各种行情
- **经历一次回撤**：没见过回撤的策略不敢上实盘

---

## 七、实盘：小心翼翼地开始

### 7.1 实盘原则

1. **小资金起步**：先用计划资金的10%试跑
2. **保持记录**：每笔交易都记录原因
3. **不改策略**：实盘期间不要动核心逻辑
4. **定期复盘**：每周/每月回顾

### 7.2 监控体系

```python
# 实盘监控要点

def monitor():
    # 1. 持仓监控
    positions = get_positions()
    for p in positions:
        if p['pnl_pct'] < -0.05:  # 单只亏损超5%
            alert(f"警告：{p['symbol']} 亏损 {p['pnl_pct']:.2%}")

    # 2. 整体回撤监控
    nav = get_current_nav()
    max_nav = get_max_nav()
    drawdown = (nav - max_nav) / max_nav
    if drawdown < -0.10:  # 回撤超10%
        alert(f"警告：整体回撤 {drawdown:.2%}")

    # 3. 策略执行监控
    expected_positions = strategy.calculate_positions()
    actual_positions = get_positions()
    if not positions_match(expected_positions, actual_positions):
        alert("警告：实际持仓与策略目标不一致")

    # 4. 数据监控
    if data_source_is_down():
        alert("警告：数据源异常")
```

### 7.3 什么时候停止策略

- 回撤超过预设阈值（比如20%）
- 策略逻辑失效（市场结构变化）
- 连续N个月跑输基准
- 发现代码bug

---

## 八、复盘迭代：持续进化

### 8.1 每周复盘

```markdown
# 周复盘模板

## 本周表现
- 策略收益：+1.2%
- 基准收益：+0.8%
- 超额收益：+0.4%

## 交易记录
| 日期 | 操作 | 股票 | 盈亏 |
|------|------|------|------|
| 周一 | 买入 | 000001 | - |
| 周三 | 卖出 | 600519 | +3.2% |

## 信号回顾
- 产生了哪些信号
- 哪些执行了，哪些没执行
- 没执行的原因

## 问题与思考
- 本周有什么异常情况
- 策略表现是否符合预期
- 有什么需要调整的
```

### 8.2 每月复盘

- 月度收益归因（alpha来自哪里）
- 与回测结果对比
- 参数是否需要微调
- 市场环境变化分析

### 8.3 迭代原则

- **不要频繁改动**：至少跑完一个完整周期再改
- **改一处测一处**：不要同时改多个地方
- **保留历史版本**：万一改坏了能回滚

---

## 总结

一个完整的量化工作流：

```
想法 → 数据 → 开发 → 回测 → 优化 → 模拟 → 实盘 → 复盘
                                                    ↓
                              发现问题 ← ← ← ← ← ← ←┘
```

每个环节都不能跳过，跳过的代价就是在实盘时用真金白银来补课。

**没有完美的策略，只有持续迭代的系统。**

---

*下一篇预告：《为什么你的回测结果不可信？量化回测的7个致命错误》*
