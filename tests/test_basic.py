"""
Basic tests for FinVista.

Run with: pytest tests/test_basic.py -v
"""

import pytest

import finvista as fv
from finvista._core.exceptions import FinVistaError, ValidationError


class TestImport:
    """Test library import."""

    def test_version(self):
        """Test version is accessible."""
        assert fv.__version__ is not None
        assert isinstance(fv.__version__, str)

    def test_public_api(self):
        """Test public API is accessible."""
        # China Stock Functions
        assert callable(fv.get_cn_stock_daily)
        assert callable(fv.get_cn_stock_quote)
        assert callable(fv.list_cn_stock_symbols)
        assert callable(fv.search_cn_stock)

        # China Index Functions
        assert callable(fv.get_cn_index_daily)
        assert callable(fv.get_cn_index_quote)
        assert callable(fv.list_cn_major_indices)
        assert callable(fv.get_cn_index_constituents)
        assert callable(fv.get_cn_index_weights)

        # China Fund Functions
        assert callable(fv.get_cn_fund_nav)
        assert callable(fv.get_cn_fund_quote)
        assert callable(fv.list_cn_fund_symbols)
        assert callable(fv.search_cn_fund)
        assert callable(fv.get_cn_fund_info)

        # US Stock Functions
        assert callable(fv.get_us_stock_daily)
        assert callable(fv.get_us_stock_quote)
        assert callable(fv.get_us_stock_info)
        assert callable(fv.search_us_stock)

        # US/HK Index Functions
        assert callable(fv.get_us_index_daily)
        assert callable(fv.get_hk_index_daily)

        # Macro Functions
        assert callable(fv.get_cn_macro_gdp)
        assert callable(fv.get_cn_macro_cpi)
        assert callable(fv.get_cn_macro_ppi)
        assert callable(fv.get_cn_macro_pmi)
        assert callable(fv.get_cn_macro_money_supply)
        assert callable(fv.get_cn_macro_social_financing)

        # Config functions
        assert callable(fv.set_proxies)
        assert callable(fv.set_timeout)
        assert callable(fv.set_cache)
        assert callable(fv.get_source_health)
        assert callable(fv.set_source_priority)
        assert callable(fv.reset_source_circuit)

        # Valuation Functions
        assert callable(fv.get_index_pe)
        assert callable(fv.get_index_pb)
        assert callable(fv.get_all_a_pb)

        # Shenwan Industry Functions
        assert callable(fv.get_sw_index_daily)
        assert callable(fv.get_sw_index_realtime)
        assert callable(fv.get_sw_index_analysis)

        # Financial Data Functions
        assert callable(fv.get_cn_income_statement)
        assert callable(fv.get_cn_balance_sheet)
        assert callable(fv.get_cn_cash_flow)
        assert callable(fv.get_cn_performance_forecast)
        assert callable(fv.get_cn_dividend_history)

        # Money Flow Functions
        assert callable(fv.get_cn_stock_moneyflow)
        assert callable(fv.get_cn_stock_moneyflow_realtime)
        assert callable(fv.get_cn_industry_moneyflow)

        # Minute Data Functions
        assert callable(fv.get_cn_stock_minute)

        # Futures Functions
        assert callable(fv.list_cn_futures_symbols)
        assert callable(fv.get_cn_futures_daily)
        assert callable(fv.get_cn_futures_positions)

        # Convertible Bond Functions
        assert callable(fv.list_cn_convertible_symbols)
        assert callable(fv.get_cn_convertible_daily)
        assert callable(fv.get_cn_convertible_info)

        # Dragon Tiger List Functions
        assert callable(fv.get_cn_lhb_list)
        assert callable(fv.get_cn_lhb_detail)
        assert callable(fv.get_cn_lhb_institution)

        # Option Functions
        assert callable(fv.list_cn_option_contracts)
        assert callable(fv.get_cn_option_quote)
        assert callable(fv.get_cn_option_daily)

        # Shareholder Functions
        assert callable(fv.get_cn_top_shareholders)
        assert callable(fv.get_cn_stock_pledge)
        assert callable(fv.get_cn_stock_unlock_schedule)

        # ETF Functions
        assert callable(fv.get_cn_etf_share_change)
        assert callable(fv.get_cn_etf_premium_discount)

        # Forex Functions
        assert callable(fv.get_exchange_rate)
        assert callable(fv.get_exchange_rate_history)


class TestConfiguration:
    """Test configuration functions."""

    def test_set_timeout(self):
        """Test setting timeout."""
        fv.set_timeout(60)
        assert fv.config.http.timeout == 60
        fv.set_timeout(30)  # Reset

    def test_set_timeout_invalid(self):
        """Test setting invalid timeout."""
        with pytest.raises(fv.ConfigError):
            fv.set_timeout(0)

    def test_set_cache(self):
        """Test cache configuration."""
        fv.set_cache(enabled=True, ttl=600)
        assert fv.config.cache.enabled is True
        assert fv.config.cache.ttl == 600
        fv.set_cache(enabled=True, ttl=300)  # Reset

    def test_source_health(self):
        """Test getting source health."""
        health = fv.get_source_health()
        assert isinstance(health, dict)
        assert "cn_stock_daily" in health

    def test_set_proxies(self):
        """Test setting proxies."""
        fv.set_proxies({"http": "http://127.0.0.1:7890"})
        assert fv.config.http.proxies == {"http": "http://127.0.0.1:7890"}
        fv.set_proxies(None)  # Reset

    def test_set_proxies_empty(self):
        """Test setting empty proxies."""
        fv.set_proxies({})
        assert fv.config.http.proxies == {}
        fv.set_proxies(None)  # Reset

    def test_set_source_priority(self):
        """Test setting source priority."""
        fv.set_source_priority("cn_stock_daily", ["eastmoney", "sina"])
        fv.reset_source_circuit("cn_stock_daily", "eastmoney")  # Reset

    def test_reset_source_circuit(self):
        """Test resetting source circuit breaker."""
        fv.reset_source_circuit("cn_stock_daily", "eastmoney")

    def test_set_cache_invalid_ttl(self):
        """Test setting invalid cache TTL."""
        with pytest.raises(fv.ConfigError):
            fv.set_cache(enabled=True, ttl=-1)


class TestExceptions:
    """Test exception classes."""

    def test_finvista_error(self):
        """Test base exception."""
        with pytest.raises(FinVistaError):
            raise fv.FinVistaError("Test error")

    def test_validation_error(self):
        """Test validation error."""
        with pytest.raises(ValidationError):
            raise fv.ValidationError("Invalid value", param_name="test")

    def test_exception_hierarchy(self):
        """Test exception inheritance."""
        assert issubclass(fv.ValidationError, fv.FinVistaError)
        assert issubclass(fv.NetworkError, fv.FinVistaError)
        assert issubclass(fv.APIError, fv.FinVistaError)
        assert issubclass(fv.RateLimitError, fv.APIError)

    def test_config_error(self):
        """Test config error."""
        with pytest.raises(fv.ConfigError):
            raise fv.ConfigError("Config error")

    def test_data_error_hierarchy(self):
        """Test data error inheritance."""
        assert issubclass(fv.DataError, fv.FinVistaError)
        assert issubclass(fv.DataNotFoundError, fv.DataError)
        assert issubclass(fv.DataParsingError, fv.DataError)

    def test_symbol_not_found_error(self):
        """Test symbol not found error."""
        with pytest.raises(fv.SymbolNotFoundError):
            raise fv.SymbolNotFoundError("Symbol not found", symbol="TEST")

    def test_date_range_error(self):
        """Test date range error."""
        with pytest.raises(fv.DateRangeError):
            raise fv.DateRangeError("Invalid date range")

    def test_source_error_hierarchy(self):
        """Test source error inheritance."""
        assert issubclass(fv.SourceError, fv.FinVistaError)
        assert issubclass(fv.AllSourcesUnavailableError, fv.SourceError)
        assert issubclass(fv.AllSourcesFailedError, fv.SourceError)


class TestValidation:
    """Test input validation."""

    def test_invalid_symbol_format(self):
        """Test invalid symbol format."""
        with pytest.raises(ValidationError):
            fv.get_cn_stock_daily("invalid")

    def test_empty_symbol(self):
        """Test empty symbol."""
        with pytest.raises(ValidationError):
            fv.get_cn_stock_daily("")

    def test_invalid_adjust(self):
        """Test invalid adjust type."""
        with pytest.raises(ValidationError):
            fv.get_cn_stock_daily("000001", adjust="invalid")


class TestMajorIndices:
    """Test major indices listing."""

    def test_list_major_indices(self):
        """Test listing major indices."""
        df = fv.list_cn_major_indices()
        assert len(df) > 0
        assert "symbol" in df.columns
        assert "name" in df.columns


# Integration tests (require network)
class TestIntegration:
    """Integration tests that require network access."""

    @pytest.mark.integration
    def test_get_stock_daily(self):
        """Test fetching daily stock data."""
        df = fv.get_cn_stock_daily("000001", start_date="2024-01-01", end_date="2024-01-10")
        assert len(df) > 0
        assert "date" in df.columns
        assert "close" in df.columns
        assert "source" in df.attrs

    @pytest.mark.integration
    def test_list_stock_symbols(self):
        """Test listing stock symbols."""
        df = fv.list_cn_stock_symbols(market="main")
        assert len(df) > 0
        assert "symbol" in df.columns
        assert "name" in df.columns

    @pytest.mark.integration
    def test_get_stock_quote(self):
        """Test fetching real-time quotes."""
        df = fv.get_cn_stock_quote(["000001", "600519"])
        assert len(df) > 0
        assert "symbol" in df.columns
        assert "price" in df.columns

    @pytest.mark.integration
    def test_search_stock(self):
        """Test searching for stocks."""
        df = fv.search_cn_stock("银行")
        assert len(df) > 0
        assert "symbol" in df.columns
        assert "name" in df.columns

    @pytest.mark.integration
    def test_get_index_daily(self):
        """Test fetching index daily data."""
        df = fv.get_cn_index_daily("000001", start_date="2024-01-01", end_date="2024-01-10")
        assert len(df) > 0
        assert "date" in df.columns
        assert "close" in df.columns

    @pytest.mark.integration
    def test_get_fund_nav(self):
        """Test fetching fund NAV data."""
        # Use 110011 (易方达中小盘混合) - a popular fund
        df = fv.get_cn_fund_nav("110011", start_date="2024-01-01", end_date="2024-01-31")
        assert len(df) > 0
        assert "date" in df.columns
        assert "nav" in df.columns

    @pytest.mark.integration
    def test_list_fund_symbols(self):
        """Test listing fund symbols."""
        df = fv.list_cn_fund_symbols(fund_type="stock")
        assert len(df) > 0
        assert "symbol" in df.columns
        assert "name" in df.columns

    @pytest.mark.integration
    def test_get_us_stock_daily(self):
        """Test fetching US stock data."""
        df = fv.get_us_stock_daily("AAPL", start_date="2024-01-01", end_date="2024-01-10")
        assert len(df) > 0
        assert "date" in df.columns
        assert "close" in df.columns

    @pytest.mark.integration
    def test_get_macro_gdp(self):
        """Test fetching GDP data."""
        df = fv.get_cn_macro_gdp()
        assert len(df) > 0
        assert "date" in df.columns
        assert "gdp" in df.columns

    @pytest.mark.integration
    def test_get_macro_cpi(self):
        """Test fetching CPI data."""
        df = fv.get_cn_macro_cpi()
        assert len(df) > 0
        assert "date" in df.columns
        assert "cpi" in df.columns

    @pytest.mark.integration
    def test_get_index_quote(self):
        """Test fetching index real-time quotes."""
        df = fv.get_cn_index_quote(["000001", "399001"])
        assert len(df) > 0
        assert "symbol" in df.columns

    @pytest.mark.integration
    def test_get_fund_quote(self):
        """Test fetching fund real-time quotes."""
        df = fv.get_cn_fund_quote(["110011"])
        assert len(df) > 0

    @pytest.mark.integration
    def test_search_fund(self):
        """Test searching for funds."""
        df = fv.search_cn_fund("易方达")
        assert len(df) > 0
        assert "symbol" in df.columns
        assert "name" in df.columns

    @pytest.mark.integration
    def test_get_fund_info(self):
        """Test fetching fund info."""
        info = fv.get_cn_fund_info("110011")
        assert info is not None

    @pytest.mark.integration
    @pytest.mark.xfail(reason="US stock API may be unavailable in CI")
    def test_get_us_stock_quote(self):
        """Test fetching US stock quotes."""
        df = fv.get_us_stock_quote(["AAPL", "GOOGL"])
        assert len(df) > 0
        assert "symbol" in df.columns

    @pytest.mark.integration
    @pytest.mark.xfail(reason="Yahoo Finance API may require authentication")
    def test_get_us_stock_info(self):
        """Test fetching US stock info."""
        info = fv.get_us_stock_info("AAPL")
        assert info is not None

    @pytest.mark.integration
    @pytest.mark.xfail(reason="US stock API may be unavailable in CI")
    def test_search_us_stock(self):
        """Test searching for US stocks."""
        df = fv.search_us_stock("Apple")
        assert len(df) > 0
        assert "symbol" in df.columns

    @pytest.mark.integration
    @pytest.mark.xfail(reason="US index API may be unavailable in CI")
    def test_get_us_index_daily(self):
        """Test fetching US index daily data."""
        df = fv.get_us_index_daily("DJI", start_date="2024-01-01", end_date="2024-01-10")
        assert len(df) > 0
        assert "date" in df.columns
        assert "close" in df.columns

    @pytest.mark.integration
    def test_get_hk_index_daily(self):
        """Test fetching HK index daily data."""
        df = fv.get_hk_index_daily("HSI", start_date="2024-01-01", end_date="2024-01-10")
        assert len(df) > 0
        assert "date" in df.columns
        assert "close" in df.columns

    @pytest.mark.integration
    def test_get_macro_ppi(self):
        """Test fetching PPI data."""
        df = fv.get_cn_macro_ppi()
        assert len(df) > 0
        assert "date" in df.columns

    @pytest.mark.integration
    def test_get_macro_pmi(self):
        """Test fetching PMI data."""
        df = fv.get_cn_macro_pmi()
        assert len(df) > 0
        assert "date" in df.columns

    @pytest.mark.integration
    @pytest.mark.xfail(reason="Money supply data may be temporarily unavailable")
    def test_get_macro_money_supply(self):
        """Test fetching money supply data."""
        df = fv.get_cn_macro_money_supply()
        assert len(df) > 0
        assert "date" in df.columns

    @pytest.mark.integration
    @pytest.mark.xfail(reason="Social financing data may be temporarily unavailable")
    def test_get_macro_social_financing(self):
        """Test fetching social financing data."""
        df = fv.get_cn_macro_social_financing()
        assert len(df) > 0
        assert "date" in df.columns

    @pytest.mark.integration
    def test_get_index_pe(self):
        """Test fetching index PE ratio."""
        pytest.importorskip("py_mini_racer")
        df = fv.get_index_pe("000300")
        assert len(df) > 0
        assert "date" in df.columns

    @pytest.mark.integration
    def test_get_index_pb(self):
        """Test fetching index PB ratio."""
        pytest.importorskip("py_mini_racer")
        df = fv.get_index_pb("000300")
        assert len(df) > 0
        assert "date" in df.columns

    @pytest.mark.integration
    def test_get_sw_index_daily(self):
        """Test fetching Shenwan index daily data."""
        df = fv.get_sw_index_daily("801010")
        assert len(df) > 0
        # Column name may be Chinese '日期' or English 'date'
        assert "date" in df.columns or "日期" in df.columns

    @pytest.mark.integration
    def test_get_cn_income_statement(self):
        """Test fetching income statement."""
        df = fv.get_cn_income_statement("000001")
        assert len(df) > 0

    @pytest.mark.integration
    def test_get_cn_balance_sheet(self):
        """Test fetching balance sheet."""
        df = fv.get_cn_balance_sheet("000001")
        assert len(df) > 0

    @pytest.mark.integration
    def test_get_cn_cash_flow(self):
        """Test fetching cash flow statement."""
        df = fv.get_cn_cash_flow("000001")
        assert len(df) > 0

    @pytest.mark.integration
    def test_get_cn_stock_moneyflow(self):
        """Test fetching stock money flow."""
        df = fv.get_cn_stock_moneyflow("000001")
        assert len(df) > 0

    @pytest.mark.integration
    def test_list_cn_futures_symbols(self):
        """Test listing futures symbols."""
        df = fv.list_cn_futures_symbols()
        assert len(df) > 0
        assert "symbol" in df.columns

    @pytest.mark.integration
    def test_list_cn_convertible_symbols(self):
        """Test listing convertible bond symbols."""
        df = fv.list_cn_convertible_symbols()
        assert len(df) > 0
        assert "symbol" in df.columns

    @pytest.mark.integration
    def test_get_cn_lhb_list(self):
        """Test fetching dragon tiger list."""
        df = fv.get_cn_lhb_list("2024-01-02")
        assert isinstance(df, type(df))  # May be empty on non-trading days

    @pytest.mark.integration
    @pytest.mark.xfail(reason="Option contracts may be empty outside trading hours")
    def test_list_cn_option_contracts(self):
        """Test listing option contracts."""
        df = fv.list_cn_option_contracts()
        assert len(df) > 0

    @pytest.mark.integration
    @pytest.mark.xfail(reason="Shareholder data source may be unavailable")
    def test_get_cn_top_shareholders(self):
        """Test fetching top shareholders."""
        df = fv.get_cn_top_shareholders("000001")
        assert len(df) > 0

    @pytest.mark.integration
    def test_get_exchange_rate(self):
        """Test fetching exchange rate."""
        rate = fv.get_exchange_rate("USD", "CNY")
        assert rate is not None

    @pytest.mark.integration
    @pytest.mark.xfail(reason="Index constituents data source may be unavailable")
    def test_get_cn_index_constituents(self):
        """Test fetching index constituents."""
        df = fv.get_cn_index_constituents("000300")
        assert len(df) > 0
        assert "symbol" in df.columns
