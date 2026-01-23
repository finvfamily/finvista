#!/usr/bin/env python3
"""
量化交易示例代码
Quantitative Trading Demo

This script demonstrates how to:
1. Fetch stock data using FinVista
2. Calculate technical indicators
3. Implement trading strategies
4. Backtest and evaluate performance
"""

from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import finvista as fv

# Set Chinese font for matplotlib
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


# =============================================================================
# Technical Indicators
# =============================================================================

def add_ma(df: pd.DataFrame, windows: list[int] | None = None) -> pd.DataFrame:
    """Add Moving Averages."""
    if windows is None:
        windows = [5, 10, 20, 60]
    for w in windows:
        df[f'MA{w}'] = df['close'].rolling(window=w).mean()
    return df


def add_macd(df: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:
    """Add MACD indicator."""
    df['EMA_fast'] = df['close'].ewm(span=fast, adjust=False).mean()
    df['EMA_slow'] = df['close'].ewm(span=slow, adjust=False).mean()
    df['MACD'] = df['EMA_fast'] - df['EMA_slow']
    df['MACD_signal'] = df['MACD'].ewm(span=signal, adjust=False).mean()
    df['MACD_hist'] = df['MACD'] - df['MACD_signal']
    return df


def add_rsi(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    """Add RSI indicator."""
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    return df


def add_bollinger(df: pd.DataFrame, window: int = 20, num_std: int = 2) -> pd.DataFrame:
    """Add Bollinger Bands."""
    df['BB_middle'] = df['close'].rolling(window=window).mean()
    df['BB_std'] = df['close'].rolling(window=window).std()
    df['BB_upper'] = df['BB_middle'] + num_std * df['BB_std']
    df['BB_lower'] = df['BB_middle'] - num_std * df['BB_std']
    return df


def add_all_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Add all technical indicators."""
    df = add_ma(df)
    df = add_macd(df)
    df = add_rsi(df)
    df = add_bollinger(df)
    return df


# =============================================================================
# Strategy Classes
# =============================================================================

class Strategy:
    """Base strategy class."""

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.signals = pd.DataFrame(index=df.index)
        self.signals['signal'] = 0

    def generate_signals(self):
        raise NotImplementedError

    def get_signals(self) -> pd.DataFrame:
        self.generate_signals()
        return self.signals


class DualMAStrategy(Strategy):
    """Dual Moving Average Crossover Strategy."""

    def __init__(self, df: pd.DataFrame, short_window: int = 5, long_window: int = 20):
        super().__init__(df)
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self):
        df = self.df
        df['MA_short'] = df['close'].rolling(self.short_window).mean()
        df['MA_long'] = df['close'].rolling(self.long_window).mean()

        self.signals['signal'] = 0
        self.signals.loc[df['MA_short'] > df['MA_long'], 'signal'] = 1
        self.signals.loc[df['MA_short'] < df['MA_long'], 'signal'] = -1
        self.signals['positions'] = self.signals['signal'].diff()


class MACDStrategy(Strategy):
    """MACD Crossover Strategy."""

    def __init__(self, df: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9):
        super().__init__(df)
        self.fast = fast
        self.slow = slow
        self.signal_period = signal

    def generate_signals(self):
        df = self.df
        ema_fast = df['close'].ewm(span=self.fast).mean()
        ema_slow = df['close'].ewm(span=self.slow).mean()
        macd = ema_fast - ema_slow
        signal_line = macd.ewm(span=self.signal_period).mean()

        self.signals['signal'] = 0
        self.signals.loc[macd > signal_line, 'signal'] = 1
        self.signals.loc[macd < signal_line, 'signal'] = -1
        self.signals['positions'] = self.signals['signal'].diff()


class RSIStrategy(Strategy):
    """RSI Overbought/Oversold Strategy."""

    def __init__(self, df: pd.DataFrame, period: int = 14, oversold: int = 30, overbought: int = 70):
        super().__init__(df)
        self.period = period
        self.oversold = oversold
        self.overbought = overbought

    def generate_signals(self):
        df = self.df
        delta = df['close'].diff()
        gain = delta.where(delta > 0, 0).rolling(self.period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(self.period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))

        self.signals['signal'] = 0
        self.signals.loc[rsi < self.oversold, 'signal'] = 1
        self.signals.loc[rsi > self.overbought, 'signal'] = -1
        self.signals['positions'] = self.signals['signal'].diff()


# =============================================================================
# Backtester
# =============================================================================

@dataclass
class BacktestMetrics:
    """Backtest performance metrics."""
    total_return: float
    annual_return: float
    max_drawdown: float
    sharpe_ratio: float
    win_rate: float
    total_trades: int
    initial_capital: float
    final_capital: float


class Backtester:
    """Backtesting engine."""

    def __init__(self, df: pd.DataFrame, signals: pd.DataFrame,
                 initial_capital: float = 100000, commission: float = 0.001):
        self.df = df.copy()
        self.signals = signals
        self.initial_capital = initial_capital
        self.commission = commission
        self.results: pd.DataFrame | None = None

    def run(self) -> pd.DataFrame:
        """Run backtest."""
        df = self.df.copy()
        signals = self.signals.copy()

        df = df.join(signals)
        df['returns'] = df['close'].pct_change()
        df['strategy_returns'] = df['returns'] * df['signal'].shift(1)

        # Deduct commission on trades
        df['trade'] = df['signal'].diff().abs()
        df['strategy_returns'] -= df['trade'] * self.commission

        df['cumulative_returns'] = (1 + df['returns']).cumprod()
        df['cumulative_strategy'] = (1 + df['strategy_returns']).cumprod()
        df['portfolio_value'] = self.initial_capital * df['cumulative_strategy']

        self.results = df
        return df

    def get_metrics(self) -> BacktestMetrics:
        """Calculate backtest metrics."""
        if self.results is None:
            self.run()

        df = self.results.dropna()

        total_return = df['cumulative_strategy'].iloc[-1] - 1
        days = len(df)
        annual_return = (1 + total_return) ** (252 / days) - 1

        cummax = df['cumulative_strategy'].cummax()
        drawdown = (df['cumulative_strategy'] - cummax) / cummax
        max_drawdown = drawdown.min()

        risk_free = 0.03
        excess_returns = df['strategy_returns'] - risk_free / 252
        sharpe = np.sqrt(252) * excess_returns.mean() / excess_returns.std() if excess_returns.std() > 0 else 0

        winning_days = (df['strategy_returns'] > 0).sum()
        total_days = (df['strategy_returns'] != 0).sum()
        win_rate = winning_days / total_days if total_days > 0 else 0

        trades = (df['signal'].diff() != 0).sum()

        return BacktestMetrics(
            total_return=total_return,
            annual_return=annual_return,
            max_drawdown=max_drawdown,
            sharpe_ratio=sharpe,
            win_rate=win_rate,
            total_trades=int(trades),
            initial_capital=self.initial_capital,
            final_capital=df['portfolio_value'].iloc[-1]
        )

    def plot(self, title: str = "Backtest Results"):
        """Plot backtest results."""
        if self.results is None:
            self.run()

        df = self.results.dropna()

        fig, axes = plt.subplots(2, 1, figsize=(14, 8), sharex=True)

        # Cumulative returns
        ax1 = axes[0]
        ax1.plot(df.index, df['cumulative_returns'], label='Buy & Hold', alpha=0.7)
        ax1.plot(df.index, df['cumulative_strategy'], label='Strategy', linewidth=2)
        ax1.fill_between(df.index, 1, df['cumulative_strategy'],
                         where=df['cumulative_strategy'] >= 1, alpha=0.3, color='green')
        ax1.fill_between(df.index, 1, df['cumulative_strategy'],
                         where=df['cumulative_strategy'] < 1, alpha=0.3, color='red')
        ax1.axhline(y=1, color='gray', linestyle='--')
        ax1.legend(loc='upper left')
        ax1.set_ylabel('Cumulative Returns')
        ax1.set_title(title)

        # Drawdown
        ax2 = axes[1]
        cummax = df['cumulative_strategy'].cummax()
        drawdown = (df['cumulative_strategy'] - cummax) / cummax
        ax2.fill_between(df.index, 0, drawdown, alpha=0.5, color='red')
        ax2.set_ylabel('Drawdown')
        ax2.set_xlabel('Date')

        plt.tight_layout()
        plt.show()


# =============================================================================
# Main Demo
# =============================================================================

def main():
    """Main demo function."""
    print("=" * 60)
    print("Quantitative Trading Demo with FinVista")
    print("=" * 60)

    # 1. Fetch data
    print("\n[1] Fetching stock data...")
    symbol = "000001"  # Ping An Bank
    df = fv.get_cn_stock_daily(symbol, start_date="2023-01-01")
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    print(f"    Fetched {len(df)} days of data for {symbol}")
    print(f"    Data source: {df.attrs.get('source', 'unknown')}")

    # 2. Add technical indicators
    print("\n[2] Calculating technical indicators...")
    df = add_all_indicators(df)
    print("    Added: MA5, MA10, MA20, MA60, MACD, RSI, Bollinger Bands")

    # 3. Run strategies
    print("\n[3] Running strategies...")

    strategies = {
        'Dual MA (5/20)': DualMAStrategy(df, 5, 20),
        'MACD': MACDStrategy(df),
        'RSI': RSIStrategy(df),
    }

    results = {}
    for name, strategy in strategies.items():
        signals = strategy.get_signals()
        backtester = Backtester(df, signals)
        metrics = backtester.get_metrics()
        results[name] = metrics
        print(f"\n    {name}:")
        print(f"      Total Return: {metrics.total_return:.2%}")
        print(f"      Annual Return: {metrics.annual_return:.2%}")
        print(f"      Max Drawdown: {metrics.max_drawdown:.2%}")
        print(f"      Sharpe Ratio: {metrics.sharpe_ratio:.2f}")
        print(f"      Win Rate: {metrics.win_rate:.2%}")
        print(f"      Trades: {metrics.total_trades}")

    # 4. Compare with benchmark
    print("\n[4] Comparing with buy & hold...")
    buy_hold_return = (df['close'].iloc[-1] / df['close'].iloc[0]) - 1
    print(f"    Buy & Hold Return: {buy_hold_return:.2%}")

    # 5. Find best strategy
    best_strategy = max(results.items(), key=lambda x: x[1].sharpe_ratio)
    print(f"\n[5] Best strategy by Sharpe Ratio: {best_strategy[0]}")

    # 6. Plot best strategy
    print("\n[6] Plotting results...")
    best_strategy_obj = strategies[best_strategy[0]]
    signals = best_strategy_obj.get_signals()
    backtester = Backtester(df, signals)
    backtester.plot(f"{symbol} - {best_strategy[0]} Strategy")

    print("\nDemo completed!")


if __name__ == "__main__":
    main()
