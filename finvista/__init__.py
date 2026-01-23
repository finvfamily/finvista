"""
FinVista - A powerful Python library for global financial data.

FinVista provides easy access to financial market data from multiple
sources with automatic failover, caching, and rate limiting.

Quick Start:
    >>> import finvista as fv
    >>>
    >>> # Get A-share daily data
    >>> df = fv.get_cn_stock_daily("000001", start_date="2024-01-01")
    >>>
    >>> # Get real-time quotes
    >>> df = fv.get_cn_stock_quote(["000001", "600519"])
    >>>
    >>> # List all stocks
    >>> df = fv.list_cn_stock_symbols(market="main")

Configuration:
    >>> # Set proxy
    >>> fv.set_proxies({"http": "http://127.0.0.1:7890"})
    >>>
    >>> # Set timeout
    >>> fv.set_timeout(60)
    >>>
    >>> # Configure cache
    >>> fv.set_cache(enabled=True, ttl=300)
    >>>
    >>> # Check data source health
    >>> health = fv.get_source_health()

For more information, visit: https://github.com/finvista/finvista
"""

from finvista._version import __version__

# =============================================================================
# Configuration Functions
# =============================================================================
from finvista._core.config import (
    config,
    get_source_health,
    reset_source_circuit,
    set_cache,
    set_proxies,
    set_source_priority,
    set_timeout,
)

# =============================================================================
# Exceptions
# =============================================================================
from finvista._core.exceptions import (
    AllSourcesFailedError,
    AllSourcesUnavailableError,
    APIError,
    ConfigError,
    DataError,
    DataNotFoundError,
    DataParsingError,
    DateRangeError,
    FinVistaError,
    NetworkError,
    RateLimitError,
    SourceError,
    SymbolNotFoundError,
    ValidationError,
)

# =============================================================================
# China Market - Stocks
# =============================================================================
from finvista.markets.china.stock import (
    get_cn_stock_daily,
    get_cn_stock_quote,
    list_cn_stock_symbols,
    search_cn_stock,
)

# =============================================================================
# China Market - Indices
# =============================================================================
from finvista.markets.china.index import (
    get_cn_index_daily,
    get_cn_index_quote,
    list_cn_major_indices,
)

# =============================================================================
# China Market - Funds
# =============================================================================
from finvista.markets.china.fund import (
    get_cn_fund_nav,
    get_cn_fund_quote,
    list_cn_fund_symbols,
    search_cn_fund,
    get_cn_fund_info,
)

# =============================================================================
# US Market - Stocks
# =============================================================================
from finvista.markets.us.stock import (
    get_us_stock_daily,
    get_us_stock_quote,
    get_us_stock_info,
    search_us_stock,
)

# =============================================================================
# US Market - Indices
# =============================================================================
from finvista.markets.us.index import get_us_index_daily

# =============================================================================
# Hong Kong Market - Indices
# =============================================================================
from finvista.markets.hk.index import get_hk_index_daily

# =============================================================================
# China Market - Valuation
# =============================================================================
from finvista.markets.china.valuation import (
    get_index_pe,
    get_index_pb,
    get_all_a_pb,
)

# =============================================================================
# China Market - Industry (Shenwan)
# =============================================================================
from finvista.markets.china.industry import (
    get_sw_index_daily,
    get_sw_index_realtime,
    get_sw_index_analysis,
)

# =============================================================================
# Macroeconomic Data - China
# =============================================================================
from finvista.macro.china import (
    get_cn_macro_gdp,
    get_cn_macro_cpi,
    get_cn_macro_ppi,
    get_cn_macro_pmi,
    get_cn_macro_money_supply,
    get_cn_macro_social_financing,
)

# =============================================================================
# Register data sources on import
# =============================================================================
from finvista._fetchers.adapters.registry import register_all_sources as _register_sources

_register_sources()

# =============================================================================
# Public API
# =============================================================================
__all__ = [
    # Version
    "__version__",
    # Configuration
    "config",
    "set_proxies",
    "set_timeout",
    "set_cache",
    "set_source_priority",
    "get_source_health",
    "reset_source_circuit",
    # Exceptions
    "FinVistaError",
    "ConfigError",
    "NetworkError",
    "APIError",
    "RateLimitError",
    "DataError",
    "DataNotFoundError",
    "DataParsingError",
    "ValidationError",
    "SymbolNotFoundError",
    "DateRangeError",
    "SourceError",
    "AllSourcesUnavailableError",
    "AllSourcesFailedError",
    # China Stocks
    "get_cn_stock_daily",
    "get_cn_stock_quote",
    "list_cn_stock_symbols",
    "search_cn_stock",
    # China Indices
    "get_cn_index_daily",
    "get_cn_index_quote",
    "list_cn_major_indices",
    # China Funds
    "get_cn_fund_nav",
    "get_cn_fund_quote",
    "list_cn_fund_symbols",
    "search_cn_fund",
    "get_cn_fund_info",
    # US Stocks
    "get_us_stock_daily",
    "get_us_stock_quote",
    "get_us_stock_info",
    "search_us_stock",
    # US Indices
    "get_us_index_daily",
    # HK Indices
    "get_hk_index_daily",
    # China Valuation
    "get_index_pe",
    "get_index_pb",
    "get_all_a_pb",
    # China Industry (Shenwan)
    "get_sw_index_daily",
    "get_sw_index_realtime",
    "get_sw_index_analysis",
    # China Macroeconomic
    "get_cn_macro_gdp",
    "get_cn_macro_cpi",
    "get_cn_macro_ppi",
    "get_cn_macro_pmi",
    "get_cn_macro_money_supply",
    "get_cn_macro_social_financing",
]
