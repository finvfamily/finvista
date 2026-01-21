"""
China market data module.

This module provides access to Chinese financial market data including:
- A-share stocks (Shanghai, Shenzhen, Beijing exchanges)
- Funds (mutual funds, ETFs)
- Futures
- Bonds
- Indices
"""

from finvista.markets.china.stock import (
    get_cn_stock_daily,
    get_cn_stock_quote,
    list_cn_stock_symbols,
    search_cn_stock,
)

from finvista.markets.china.index import (
    get_cn_index_daily,
    get_cn_index_quote,
    list_cn_major_indices,
)

from finvista.markets.china.fund import (
    get_cn_fund_nav,
    get_cn_fund_quote,
    list_cn_fund_symbols,
    search_cn_fund,
    get_cn_fund_info,
)

__all__ = [
    # Stock
    "get_cn_stock_daily",
    "get_cn_stock_quote",
    "list_cn_stock_symbols",
    "search_cn_stock",
    # Index
    "get_cn_index_daily",
    "get_cn_index_quote",
    "list_cn_major_indices",
    # Fund
    "get_cn_fund_nav",
    "get_cn_fund_quote",
    "list_cn_fund_symbols",
    "search_cn_fund",
    "get_cn_fund_info",
]
