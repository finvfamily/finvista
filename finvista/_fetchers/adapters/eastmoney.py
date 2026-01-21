"""
East Money (东方财富) data adapter.

This module provides data fetching from East Money, one of the most
popular financial data sources in China.
"""

from __future__ import annotations

import logging
import re
from datetime import date, datetime
from typing import Any

import pandas as pd

from finvista._core.exceptions import DataNotFoundError, DataParsingError
from finvista._fetchers.adapters.base import BaseAdapter

logger = logging.getLogger(__name__)


class EastMoneyAdapter(BaseAdapter):
    """
    Adapter for East Money (东方财富) data source.

    This adapter provides access to:
    - A-share stock data (daily, real-time quotes)
    - Fund data
    - Index data
    - Basic financial information

    Example:
        >>> adapter = EastMoneyAdapter()
        >>> df = adapter.fetch_stock_daily("000001", start_date="2024-01-01")
    """

    name = "eastmoney"
    base_url = "https://push2his.eastmoney.com"

    # Market code mapping
    MARKET_CODES = {
        "sh": "1",  # Shanghai
        "sz": "0",  # Shenzhen
        "bj": "0",  # Beijing (uses Shenzhen code)
    }

    # Adjust type mapping
    ADJUST_MAP = {
        "none": "0",
        "qfq": "1",  # Forward adjust
        "hfq": "2",  # Backward adjust
    }

    def is_available(self) -> bool:
        """Check if East Money API is available."""
        try:
            self._get_json(
                "https://push2.eastmoney.com/api/qt/clist/get",
                params={"pn": 1, "pz": 1, "fs": "m:0+t:6"},
            )
            return True
        except Exception:
            return False

    def _get_market_code(self, symbol: str) -> str:
        """
        Get market code for a symbol.

        Args:
            symbol: Stock symbol (e.g., '000001', '600519').

        Returns:
            Market code ('0' for Shenzhen, '1' for Shanghai).
        """
        if symbol.startswith(("6", "9")):
            return "1"  # Shanghai
        elif symbol.startswith(("0", "2", "3")):
            return "0"  # Shenzhen
        elif symbol.startswith(("4", "8")):
            return "0"  # Beijing/New Third Board
        return "0"

    def _get_secid(self, symbol: str) -> str:
        """
        Get secid for a symbol.

        Args:
            symbol: Stock symbol.

        Returns:
            Security ID in format 'market.symbol'.
        """
        market = self._get_market_code(symbol)
        return f"{market}.{symbol}"

    def fetch_stock_daily(
        self,
        symbol: str,
        start_date: str | date | None = None,
        end_date: str | date | None = None,
        adjust: str = "none",
        **kwargs: Any,
    ) -> pd.DataFrame:
        """
        Fetch daily stock data.

        Args:
            symbol: Stock symbol (e.g., '000001').
            start_date: Start date (YYYY-MM-DD or date object).
            end_date: End date (YYYY-MM-DD or date object).
            adjust: Adjustment type ('none', 'qfq', 'hfq').

        Returns:
            DataFrame with columns: date, open, high, low, close, volume,
            amount, change, change_pct, turnover.

        Raises:
            DataNotFoundError: When no data is found.
            DataParsingError: When data cannot be parsed.
        """
        # Format dates
        if start_date is None:
            start_date = "19900101"
        elif isinstance(start_date, (date, datetime)):
            start_date = start_date.strftime("%Y%m%d")
        else:
            start_date = start_date.replace("-", "")

        if end_date is None:
            end_date = datetime.now().strftime("%Y%m%d")
        elif isinstance(end_date, (date, datetime)):
            end_date = end_date.strftime("%Y%m%d")
        else:
            end_date = end_date.replace("-", "")

        secid = self._get_secid(symbol)
        fqt = self.ADJUST_MAP.get(adjust, "0")

        params = {
            "secid": secid,
            "fields1": "f1,f2,f3,f4,f5,f6",
            "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61",
            "klt": "101",  # Daily
            "fqt": fqt,
            "beg": start_date,
            "end": end_date,
        }

        data = self._get_json(
            "https://push2his.eastmoney.com/api/qt/stock/kline/get",
            params=params,
        )

        if not data.get("data") or not data["data"].get("klines"):
            raise DataNotFoundError(
                f"No data found for symbol {symbol}",
                query_params={"symbol": symbol, "start_date": start_date, "end_date": end_date},
            )

        klines = data["data"]["klines"]
        records = []

        for line in klines:
            parts = line.split(",")
            if len(parts) >= 11:
                records.append(
                    {
                        "date": parts[0],
                        "open": float(parts[1]),
                        "close": float(parts[2]),
                        "high": float(parts[3]),
                        "low": float(parts[4]),
                        "volume": int(float(parts[5])),
                        "amount": float(parts[6]),
                        "amplitude": float(parts[7]) if parts[7] != "-" else None,
                        "change_pct": float(parts[8]) if parts[8] != "-" else None,
                        "change": float(parts[9]) if parts[9] != "-" else None,
                        "turnover": float(parts[10]) if parts[10] != "-" else None,
                    }
                )

        df = pd.DataFrame(records)
        df["date"] = pd.to_datetime(df["date"]).dt.date

        return df

    def fetch_stock_quote(
        self,
        symbols: list[str] | str,
        **kwargs: Any,
    ) -> pd.DataFrame:
        """
        Fetch real-time stock quotes.

        Args:
            symbols: Single symbol or list of symbols.

        Returns:
            DataFrame with real-time quote data.
        """
        if isinstance(symbols, str):
            symbols = [symbols]

        secids = [self._get_secid(s) for s in symbols]
        secids_str = ",".join(secids)

        params = {
            "secids": secids_str,
            "fields": "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18",
        }

        data = self._get_json(
            "https://push2.eastmoney.com/api/qt/ulist/get",
            params=params,
        )

        if not data.get("data") or not data["data"].get("diff"):
            raise DataNotFoundError(f"No quote data found for symbols: {symbols}")

        records = []
        for item in data["data"]["diff"]:
            records.append(
                {
                    "symbol": item.get("f12", ""),
                    "name": item.get("f14", ""),
                    "price": item.get("f2", 0) / 100 if item.get("f2") else None,
                    "change": item.get("f4", 0) / 100 if item.get("f4") else None,
                    "change_pct": item.get("f3", 0) / 100 if item.get("f3") else None,
                    "open": item.get("f17", 0) / 100 if item.get("f17") else None,
                    "high": item.get("f15", 0) / 100 if item.get("f15") else None,
                    "low": item.get("f16", 0) / 100 if item.get("f16") else None,
                    "pre_close": item.get("f18", 0) / 100 if item.get("f18") else None,
                    "volume": item.get("f5", 0),
                    "amount": item.get("f6", 0),
                }
            )

        return pd.DataFrame(records)

    def fetch_stock_list(
        self,
        market: str = "all",
        **kwargs: Any,
    ) -> pd.DataFrame:
        """
        Fetch list of all A-share stocks.

        Args:
            market: Market filter ('all', 'sh', 'sz', 'bj').

        Returns:
            DataFrame with stock information.
        """
        # Market filter string
        market_filter = {
            "all": "m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23",
            "sh": "m:1+t:2,m:1+t:23",
            "sz": "m:0+t:6,m:0+t:80",
            "main": "m:0+t:6,m:1+t:2",
            "gem": "m:0+t:80",  # ChiNext
            "star": "m:1+t:23",  # STAR Market
        }.get(market, "m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23")

        params = {
            "pn": 1,
            "pz": 10000,
            "fs": market_filter,
            "fields": "f1,f2,f3,f4,f12,f13,f14",
        }

        data = self._get_json(
            "https://push2.eastmoney.com/api/qt/clist/get",
            params=params,
        )

        if not data.get("data") or not data["data"].get("diff"):
            return pd.DataFrame()

        # diff can be a dict with numeric keys or a list
        diff_data = data["data"]["diff"]
        if isinstance(diff_data, dict):
            items = diff_data.values()
        else:
            items = diff_data

        records = []
        for item in items:
            market_code = item.get("f13", 0)
            records.append(
                {
                    "symbol": item.get("f12", ""),
                    "name": item.get("f14", ""),
                    "market": "sh" if market_code == 1 else "sz",
                    "price": item.get("f2", 0) / 100 if item.get("f2") else None,
                    "change_pct": item.get("f3", 0) / 100 if item.get("f3") else None,
                }
            )

        df = pd.DataFrame(records)
        df = df[df["symbol"].str.len() == 6]  # Filter valid symbols

        return df

    def fetch_index_daily(
        self,
        symbol: str,
        start_date: str | date | None = None,
        end_date: str | date | None = None,
        **kwargs: Any,
    ) -> pd.DataFrame:
        """
        Fetch daily index data.

        Args:
            symbol: Index symbol (e.g., '000001' for SSE Composite).
            start_date: Start date.
            end_date: End date.

        Returns:
            DataFrame with index daily data.
        """
        # Index market codes are different
        if symbol.startswith("0"):
            secid = f"1.{symbol}"  # Shanghai index
        elif symbol.startswith("3"):
            secid = f"0.{symbol}"  # Shenzhen index
        else:
            secid = f"1.{symbol}"

        # Format dates
        if start_date is None:
            start_date = "19900101"
        elif isinstance(start_date, (date, datetime)):
            start_date = start_date.strftime("%Y%m%d")
        else:
            start_date = start_date.replace("-", "")

        if end_date is None:
            end_date = datetime.now().strftime("%Y%m%d")
        elif isinstance(end_date, (date, datetime)):
            end_date = end_date.strftime("%Y%m%d")
        else:
            end_date = end_date.replace("-", "")

        params = {
            "secid": secid,
            "fields1": "f1,f2,f3,f4,f5,f6",
            "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61",
            "klt": "101",
            "fqt": "1",
            "beg": start_date,
            "end": end_date,
        }

        data = self._get_json(
            "https://push2his.eastmoney.com/api/qt/stock/kline/get",
            params=params,
        )

        if not data.get("data") or not data["data"].get("klines"):
            raise DataNotFoundError(f"No index data found for {symbol}")

        klines = data["data"]["klines"]
        records = []

        for line in klines:
            parts = line.split(",")
            if len(parts) >= 7:
                records.append(
                    {
                        "date": parts[0],
                        "open": float(parts[1]),
                        "close": float(parts[2]),
                        "high": float(parts[3]),
                        "low": float(parts[4]),
                        "volume": int(float(parts[5])),
                        "amount": float(parts[6]),
                    }
                )

        df = pd.DataFrame(records)
        df["date"] = pd.to_datetime(df["date"]).dt.date

        return df


# Global adapter instance
eastmoney_adapter = EastMoneyAdapter()
