"""
Data source registration for FinVista.

This module registers all available data sources with the source manager,
setting up the failover chain for each data type.
"""

from __future__ import annotations

import logging

from finvista._fetchers.source_manager import source_manager

logger = logging.getLogger(__name__)

_registered = False


def register_all_sources() -> None:
    """
    Register all data sources with the source manager.

    This function is called automatically when the library is imported.
    It sets up the failover chain for each data type.
    """
    global _registered

    if _registered:
        return

    logger.debug("Registering data sources...")

    # Import adapters
    from finvista._fetchers.adapters.eastmoney import eastmoney_adapter
    from finvista._fetchers.adapters.sina import sina_adapter
    from finvista._fetchers.adapters.tencent import tencent_adapter
    from finvista._fetchers.adapters.tiantian import tiantian_adapter
    from finvista._fetchers.adapters.yahoo import yahoo_adapter

    # =========================================================================
    # China Stock Daily - with failover chain
    # =========================================================================
    source_manager.register(
        data_type="cn_stock_daily",
        name="eastmoney",
        fetcher=eastmoney_adapter.fetch_stock_daily,
        priority=0,
    )
    source_manager.register(
        data_type="cn_stock_daily",
        name="sina",
        fetcher=sina_adapter.fetch_stock_daily,
        priority=1,
    )
    source_manager.register(
        data_type="cn_stock_daily",
        name="tencent",
        fetcher=tencent_adapter.fetch_stock_daily,
        priority=2,
    )

    # =========================================================================
    # China Stock Quote (Real-time) - Sina is faster for quotes
    # =========================================================================
    source_manager.register(
        data_type="cn_stock_quote",
        name="sina",
        fetcher=sina_adapter.fetch_stock_quote,
        priority=0,
    )
    source_manager.register(
        data_type="cn_stock_quote",
        name="tencent",
        fetcher=tencent_adapter.fetch_stock_quote,
        priority=1,
    )
    source_manager.register(
        data_type="cn_stock_quote",
        name="eastmoney",
        fetcher=eastmoney_adapter.fetch_stock_quote,
        priority=2,
    )

    # =========================================================================
    # China Stock List
    # =========================================================================
    source_manager.register(
        data_type="cn_stock_list",
        name="eastmoney",
        fetcher=eastmoney_adapter.fetch_stock_list,
        priority=0,
    )
    source_manager.register(
        data_type="cn_stock_list",
        name="tencent",
        fetcher=tencent_adapter.fetch_stock_list,
        priority=1,
    )

    # =========================================================================
    # China Index Daily
    # =========================================================================
    source_manager.register(
        data_type="cn_index_daily",
        name="eastmoney",
        fetcher=eastmoney_adapter.fetch_index_daily,
        priority=0,
    )

    # =========================================================================
    # China Index Quote (Real-time)
    # =========================================================================
    source_manager.register(
        data_type="cn_index_quote",
        name="sina",
        fetcher=sina_adapter.fetch_index_quote,
        priority=0,
    )

    # =========================================================================
    # China Fund NAV
    # =========================================================================
    source_manager.register(
        data_type="cn_fund_nav",
        name="tiantian",
        fetcher=tiantian_adapter.fetch_fund_nav,
        priority=0,
    )

    # =========================================================================
    # China Fund List
    # =========================================================================
    source_manager.register(
        data_type="cn_fund_list",
        name="tiantian",
        fetcher=tiantian_adapter.fetch_fund_list,
        priority=0,
    )

    # =========================================================================
    # China Fund Quote (Real-time estimate)
    # =========================================================================
    source_manager.register(
        data_type="cn_fund_quote",
        name="tiantian",
        fetcher=tiantian_adapter.fetch_fund_quote,
        priority=0,
    )

    # =========================================================================
    # US Stock Daily
    # =========================================================================
    source_manager.register(
        data_type="us_stock_daily",
        name="yahoo",
        fetcher=yahoo_adapter.fetch_stock_daily,
        priority=0,
    )

    # =========================================================================
    # US Stock Quote (Real-time)
    # =========================================================================
    source_manager.register(
        data_type="us_stock_quote",
        name="yahoo",
        fetcher=yahoo_adapter.fetch_stock_quote,
        priority=0,
    )

    _registered = True
    logger.debug("Data source registration complete")


def get_registered_sources() -> dict[str, list[str]]:
    """
    Get all registered data sources.

    Returns:
        Dictionary mapping data types to lists of source names.
    """
    # Ensure sources are registered
    register_all_sources()

    result = {}
    for data_type in [
        "cn_stock_daily",
        "cn_stock_quote",
        "cn_stock_list",
        "cn_index_daily",
        "cn_index_quote",
        "cn_fund_nav",
        "cn_fund_list",
        "cn_fund_quote",
        "us_stock_daily",
        "us_stock_quote",
    ]:
        result[data_type] = source_manager.get_sources(data_type)

    return result
