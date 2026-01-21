# Python 量化交易入门：从数据获取到策略回测完整指南

> 本文将带你从零开始，用 Python 实现一个完整的量化交易系统，包括数据获取、技术指标计算、策略编写和回测分析。

## 目录

1. [环境准备](#环境准备)
2. [获取股票数据](#获取股票数据)
3. [技术指标计算](#技术指标计算)
4. [经典策略实现](#经典策略实现)
5. [策略回测框架](#策略回测框架)
6. [实战：双均线策略](#实战双均线策略)
7. [进阶：多因子选股](#进阶多因子选股)
8. [风险控制](#风险控制)
9. [总结与展望](#总结与展望)

---

## 环境准备

首先安装必要的库：

```bash
pip install finvista pandas numpy matplotlib
```

导入库：

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False
```

---

## 获取股票数据

量化交易的第一步是获取可靠的数据。这里我们使用 `finvista` 库，它的优势是支持多数据源自动切换，不用担心单一数据源挂掉导致程序崩溃。

```python
import finvista as fv

# 获取平安银行近一年日线数据
df = fv.get_cn_stock_daily("000001", start_date="2024-01-01")
print(df.head())
```

```
         date   open   high    low  close      volume        amount
0  2024-01-02   9.15   9.20   9.05   9.10   123456789   1123456789.0
1  2024-01-03   9.12   9.25   9.10   9.20   134567890   1234567890.0
...
```

### 批量获取多只股票

```python
def get_stocks_data(symbols, start_date):
    """批量获取股票数据"""
    data = {}
    for symbol in symbols:
        try:
            df = fv.get_cn_stock_daily(symbol, start_date=start_date)
            df['date'] = pd.to_datetime(df['date'])
            df.set_index('date', inplace=True)
            data[symbol] = df
            print(f"✓ {symbol}")
        except Exception as e:
            print(f"✗ {symbol}: {e}")
    return data

# 获取几只蓝筹股数据
symbols = ["000001", "600519", "000858", "601318", "600036"]
stocks_data = get_stocks_data(symbols, "2023-01-01")
```

### 获取指数数据作为基准

```python
# 获取沪深300作为基准
benchmark = fv.get_cn_index_daily("000300", start_date="2023-01-01")
benchmark['date'] = pd.to_datetime(benchmark['date'])
benchmark.set_index('date', inplace=True)
```

---

## 技术指标计算

### 移动平均线 (MA)

```python
def add_ma(df, windows=[5, 10, 20, 60]):
    """添加移动平均线"""
    for w in windows:
        df[f'MA{w}'] = df['close'].rolling(window=w).mean()
    return df

df = add_ma(df)
```

### MACD 指标

```python
def add_macd(df, fast=12, slow=26, signal=9):
    """计算 MACD 指标"""
    df['EMA_fast'] = df['close'].ewm(span=fast, adjust=False).mean()
    df['EMA_slow'] = df['close'].ewm(span=slow, adjust=False).mean()
    df['MACD'] = df['EMA_fast'] - df['EMA_slow']
    df['MACD_signal'] = df['MACD'].ewm(span=signal, adjust=False).mean()
    df['MACD_hist'] = df['MACD'] - df['MACD_signal']
    return df

df = add_macd(df)
```

### RSI 指标

```python
def add_rsi(df, period=14):
    """计算 RSI 指标"""
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    return df

df = add_rsi(df)
```

### 布林带 (Bollinger Bands)

```python
def add_bollinger(df, window=20, num_std=2):
    """计算布林带"""
    df['BB_middle'] = df['close'].rolling(window=window).mean()
    df['BB_std'] = df['close'].rolling(window=window).std()
    df['BB_upper'] = df['BB_middle'] + num_std * df['BB_std']
    df['BB_lower'] = df['BB_middle'] - num_std * df['BB_std']
    return df

df = add_bollinger(df)
```

### 可视化技术指标

```python
def plot_technical(df, title="技术分析图"):
    """绘制技术分析图"""
    fig, axes = plt.subplots(3, 1, figsize=(14, 10), sharex=True)

    # 价格和均线
    ax1 = axes[0]
    ax1.plot(df.index, df['close'], label='收盘价', linewidth=1.5)
    ax1.plot(df.index, df['MA5'], label='MA5', alpha=0.7)
    ax1.plot(df.index, df['MA20'], label='MA20', alpha=0.7)
    ax1.fill_between(df.index, df['BB_lower'], df['BB_upper'], alpha=0.2)
    ax1.legend(loc='upper left')
    ax1.set_ylabel('价格')
    ax1.set_title(title)

    # MACD
    ax2 = axes[1]
    ax2.plot(df.index, df['MACD'], label='MACD')
    ax2.plot(df.index, df['MACD_signal'], label='Signal')
    ax2.bar(df.index, df['MACD_hist'], alpha=0.3, label='Histogram')
    ax2.axhline(y=0, color='gray', linestyle='--')
    ax2.legend(loc='upper left')
    ax2.set_ylabel('MACD')

    # RSI
    ax3 = axes[2]
    ax3.plot(df.index, df['RSI'], label='RSI')
    ax3.axhline(y=70, color='r', linestyle='--', alpha=0.5)
    ax3.axhline(y=30, color='g', linestyle='--', alpha=0.5)
    ax3.fill_between(df.index, 30, 70, alpha=0.1)
    ax3.legend(loc='upper left')
    ax3.set_ylabel('RSI')
    ax3.set_ylim(0, 100)

    plt.tight_layout()
    plt.show()

plot_technical(df.tail(120), "平安银行技术分析")
```

---

## 经典策略实现

### 策略基类

```python
class Strategy:
    """策略基类"""

    def __init__(self, df):
        self.df = df.copy()
        self.signals = pd.DataFrame(index=df.index)
        self.signals['signal'] = 0  # 1: 买入, -1: 卖出, 0: 持有

    def generate_signals(self):
        """生成交易信号 - 子类实现"""
        raise NotImplementedError

    def get_signals(self):
        self.generate_signals()
        return self.signals
```

### 双均线策略

```python
class DualMAStrategy(Strategy):
    """双均线策略: 短期均线上穿长期均线买入，下穿卖出"""

    def __init__(self, df, short_window=5, long_window=20):
        super().__init__(df)
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self):
        df = self.df

        # 计算均线
        df['MA_short'] = df['close'].rolling(self.short_window).mean()
        df['MA_long'] = df['close'].rolling(self.long_window).mean()

        # 生成信号
        self.signals['signal'] = 0
        self.signals.loc[df['MA_short'] > df['MA_long'], 'signal'] = 1
        self.signals.loc[df['MA_short'] < df['MA_long'], 'signal'] = -1

        # 只在变化点产生交易信号
        self.signals['positions'] = self.signals['signal'].diff()
```

### MACD 策略

```python
class MACDStrategy(Strategy):
    """MACD 策略: MACD 上穿信号线买入，下穿卖出"""

    def __init__(self, df, fast=12, slow=26, signal=9):
        super().__init__(df)
        self.fast = fast
        self.slow = slow
        self.signal_period = signal

    def generate_signals(self):
        df = self.df

        # 计算 MACD
        ema_fast = df['close'].ewm(span=self.fast).mean()
        ema_slow = df['close'].ewm(span=self.slow).mean()
        macd = ema_fast - ema_slow
        signal_line = macd.ewm(span=self.signal_period).mean()

        # 生成信号
        self.signals['signal'] = 0
        self.signals.loc[macd > signal_line, 'signal'] = 1
        self.signals.loc[macd < signal_line, 'signal'] = -1
        self.signals['positions'] = self.signals['signal'].diff()
```

### RSI 策略

```python
class RSIStrategy(Strategy):
    """RSI 策略: RSI < 30 买入（超卖），RSI > 70 卖出（超买）"""

    def __init__(self, df, period=14, oversold=30, overbought=70):
        super().__init__(df)
        self.period = period
        self.oversold = oversold
        self.overbought = overbought

    def generate_signals(self):
        df = self.df

        # 计算 RSI
        delta = df['close'].diff()
        gain = delta.where(delta > 0, 0).rolling(self.period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(self.period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))

        # 生成信号
        self.signals['signal'] = 0
        self.signals.loc[rsi < self.oversold, 'signal'] = 1
        self.signals.loc[rsi > self.overbought, 'signal'] = -1
        self.signals['positions'] = self.signals['signal'].diff()
```

---

## 策略回测框架

```python
class Backtester:
    """回测引擎"""

    def __init__(self, df, signals, initial_capital=100000, commission=0.001):
        self.df = df.copy()
        self.signals = signals
        self.initial_capital = initial_capital
        self.commission = commission  # 手续费率
        self.results = None

    def run(self):
        """运行回测"""
        df = self.df.copy()
        signals = self.signals.copy()

        # 合并数据
        df = df.join(signals)

        # 计算每日收益
        df['returns'] = df['close'].pct_change()

        # 计算策略收益（考虑持仓）
        df['strategy_returns'] = df['returns'] * df['signal'].shift(1)

        # 扣除手续费
        df['trade'] = df['signal'].diff().abs()
        df['strategy_returns'] -= df['trade'] * self.commission

        # 计算累计收益
        df['cumulative_returns'] = (1 + df['returns']).cumprod()
        df['cumulative_strategy'] = (1 + df['strategy_returns']).cumprod()

        # 计算资金曲线
        df['portfolio_value'] = self.initial_capital * df['cumulative_strategy']

        self.results = df
        return df

    def get_metrics(self):
        """计算回测指标"""
        if self.results is None:
            self.run()

        df = self.results.dropna()

        # 总收益率
        total_return = df['cumulative_strategy'].iloc[-1] - 1

        # 年化收益率
        days = len(df)
        annual_return = (1 + total_return) ** (252 / days) - 1

        # 最大回撤
        cummax = df['cumulative_strategy'].cummax()
        drawdown = (df['cumulative_strategy'] - cummax) / cummax
        max_drawdown = drawdown.min()

        # 夏普比率 (假设无风险利率为3%)
        risk_free = 0.03
        excess_returns = df['strategy_returns'] - risk_free / 252
        sharpe = np.sqrt(252) * excess_returns.mean() / excess_returns.std()

        # 胜率
        winning_days = (df['strategy_returns'] > 0).sum()
        total_days = (df['strategy_returns'] != 0).sum()
        win_rate = winning_days / total_days if total_days > 0 else 0

        # 交易次数
        trades = (df['signal'].diff() != 0).sum()

        metrics = {
            '总收益率': f"{total_return:.2%}",
            '年化收益率': f"{annual_return:.2%}",
            '最大回撤': f"{max_drawdown:.2%}",
            '夏普比率': f"{sharpe:.2f}",
            '胜率': f"{win_rate:.2%}",
            '交易次数': trades,
            '初始资金': f"¥{self.initial_capital:,.0f}",
            '最终资金': f"¥{df['portfolio_value'].iloc[-1]:,.0f}"
        }

        return metrics

    def plot(self, title="策略回测结果"):
        """绘制回测结果"""
        if self.results is None:
            self.run()

        df = self.results.dropna()

        fig, axes = plt.subplots(2, 1, figsize=(14, 8), sharex=True)

        # 收益曲线
        ax1 = axes[0]
        ax1.plot(df.index, df['cumulative_returns'], label='买入持有', alpha=0.7)
        ax1.plot(df.index, df['cumulative_strategy'], label='策略收益', linewidth=2)
        ax1.fill_between(df.index, 1, df['cumulative_strategy'],
                         where=df['cumulative_strategy'] >= 1, alpha=0.3, color='green')
        ax1.fill_between(df.index, 1, df['cumulative_strategy'],
                         where=df['cumulative_strategy'] < 1, alpha=0.3, color='red')
        ax1.axhline(y=1, color='gray', linestyle='--')
        ax1.legend(loc='upper left')
        ax1.set_ylabel('累计收益')
        ax1.set_title(title)

        # 回撤
        ax2 = axes[1]
        cummax = df['cumulative_strategy'].cummax()
        drawdown = (df['cumulative_strategy'] - cummax) / cummax
        ax2.fill_between(df.index, 0, drawdown, alpha=0.5, color='red')
        ax2.set_ylabel('回撤')
        ax2.set_xlabel('日期')

        plt.tight_layout()
        plt.show()
```

---

## 实战：双均线策略

让我们完整运行一个双均线策略的回测：

```python
import finvista as fv

# 1. 获取数据
print("正在获取数据...")
df = fv.get_cn_stock_daily("000001", start_date="2023-01-01")
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)
print(f"获取到 {len(df)} 条数据")

# 2. 生成策略信号
strategy = DualMAStrategy(df, short_window=5, long_window=20)
signals = strategy.get_signals()

# 3. 运行回测
backtester = Backtester(df, signals, initial_capital=100000)
results = backtester.run()

# 4. 查看回测指标
metrics = backtester.get_metrics()
print("\n===== 回测结果 =====")
for key, value in metrics.items():
    print(f"{key}: {value}")

# 5. 绘制回测图表
backtester.plot("平安银行 - 双均线策略 (MA5/MA20)")
```

### 参数优化

```python
def optimize_ma_strategy(df, short_range, long_range):
    """网格搜索最优均线参数"""
    results = []

    for short in short_range:
        for long in long_range:
            if short >= long:
                continue

            strategy = DualMAStrategy(df, short_window=short, long_window=long)
            signals = strategy.get_signals()

            backtester = Backtester(df, signals)
            backtester.run()
            metrics = backtester.get_metrics()

            results.append({
                'short': short,
                'long': long,
                'return': float(metrics['总收益率'].strip('%')) / 100,
                'sharpe': float(metrics['夏普比率']),
                'max_dd': float(metrics['最大回撤'].strip('%')) / 100
            })

    return pd.DataFrame(results).sort_values('sharpe', ascending=False)

# 寻找最优参数
print("正在优化参数...")
optimization = optimize_ma_strategy(df, range(3, 15), range(10, 60, 5))
print("\nTop 10 参数组合:")
print(optimization.head(10))
```

---

## 进阶：多因子选股

```python
def calculate_factors(symbol, start_date):
    """计算选股因子"""
    df = fv.get_cn_stock_daily(symbol, start_date=start_date)
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)

    if len(df) < 60:
        return None

    latest = df.iloc[-1]

    factors = {
        'symbol': symbol,
        # 动量因子
        'momentum_20': df['close'].pct_change(20).iloc[-1],
        'momentum_60': df['close'].pct_change(60).iloc[-1],
        # 波动率因子
        'volatility': df['close'].pct_change().rolling(20).std().iloc[-1],
        # 均线偏离
        'ma_bias': (latest['close'] - df['close'].rolling(20).mean().iloc[-1]) / df['close'].rolling(20).mean().iloc[-1],
        # 成交量变化
        'volume_ratio': df['volume'].iloc[-5:].mean() / df['volume'].iloc[-20:].mean(),
        # 价格位置
        'price_position': (latest['close'] - df['close'].rolling(60).min().iloc[-1]) / (df['close'].rolling(60).max().iloc[-1] - df['close'].rolling(60).min().iloc[-1])
    }

    return factors

def multi_factor_screen(symbols, start_date):
    """多因子选股"""
    factor_data = []

    for symbol in symbols:
        try:
            factors = calculate_factors(symbol, start_date)
            if factors:
                factor_data.append(factors)
        except Exception as e:
            continue

    df = pd.DataFrame(factor_data)

    # 因子标准化
    for col in df.columns[1:]:
        df[f'{col}_rank'] = df[col].rank(pct=True)

    # 综合评分 (动量 + 低波动 + 放量)
    df['score'] = (
        df['momentum_20_rank'] * 0.3 +
        (1 - df['volatility_rank']) * 0.3 +
        df['volume_ratio_rank'] * 0.2 +
        df['price_position_rank'] * 0.2
    )

    return df.sort_values('score', ascending=False)

# 获取股票列表
print("获取股票列表...")
stock_list = fv.list_cn_stock_symbols(market="main")
symbols = stock_list['symbol'].head(100).tolist()  # 取前100只测试

# 多因子选股
print("计算因子中...")
ranking = multi_factor_screen(symbols, "2024-01-01")
print("\n===== 多因子选股结果 Top 10 =====")
print(ranking[['symbol', 'momentum_20', 'volatility', 'volume_ratio', 'score']].head(10))
```

---

## 风险控制

### 止损止盈

```python
class StopLossStrategy(Strategy):
    """带止损止盈的策略"""

    def __init__(self, df, base_strategy, stop_loss=0.05, take_profit=0.10):
        super().__init__(df)
        self.base_strategy = base_strategy
        self.stop_loss = stop_loss
        self.take_profit = take_profit

    def generate_signals(self):
        base_signals = self.base_strategy.get_signals()
        df = self.df

        position = 0
        entry_price = 0
        signals = []

        for i, (date, row) in enumerate(df.iterrows()):
            signal = 0
            base_signal = base_signals.loc[date, 'signal'] if date in base_signals.index else 0

            if position == 0:
                # 无持仓，看是否有买入信号
                if base_signal == 1:
                    position = 1
                    entry_price = row['close']
                    signal = 1
            else:
                # 有持仓，检查止损止盈
                pnl = (row['close'] - entry_price) / entry_price

                if pnl <= -self.stop_loss:  # 止损
                    position = 0
                    signal = -1
                elif pnl >= self.take_profit:  # 止盈
                    position = 0
                    signal = -1
                elif base_signal == -1:  # 基础策略卖出信号
                    position = 0
                    signal = -1

            signals.append(signal)

        self.signals['signal'] = signals
        self.signals['positions'] = self.signals['signal'].diff()
```

### 仓位管理

```python
def kelly_position(win_rate, win_loss_ratio):
    """凯利公式计算最优仓位"""
    kelly = win_rate - (1 - win_rate) / win_loss_ratio
    return max(0, min(kelly, 1))  # 限制在 0-100%

def calculate_position_size(capital, price, risk_per_trade=0.02, stop_loss_pct=0.05):
    """基于风险的仓位计算"""
    risk_amount = capital * risk_per_trade
    shares = risk_amount / (price * stop_loss_pct)
    position_value = shares * price
    position_pct = position_value / capital
    return min(position_pct, 0.25)  # 单只股票最多25%仓位
```

---

## 总结与展望

本文介绍了一个完整的量化交易系统：

1. **数据获取** - 使用可靠的数据源获取股票数据
2. **技术指标** - MA、MACD、RSI、布林带等
3. **策略编写** - 双均线、MACD、RSI 策略
4. **回测框架** - 计算收益、回撤、夏普比率等指标
5. **选股模型** - 多因子选股
6. **风险控制** - 止损止盈、仓位管理

### 进一步学习方向

- **机器学习**: 使用 LSTM、XGBoost 预测股价
- **因子挖掘**: 研究更多有效因子
- **高频交易**: 分钟级别的策略
- **期权策略**: Delta 对冲、波动率交易
- **实盘对接**: 连接券商 API 自动交易

### 完整代码

本文完整代码已整理，获取方式：

```python
# 安装数据获取库
pip install finvista

# GitHub 获取示例代码
# https://github.com/finvfamily/finvista/tree/main/examples
```

---

*如果觉得本文有帮助，欢迎点赞收藏。有问题欢迎评论区讨论！*
