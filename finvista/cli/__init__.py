"""
FinVista Command Line Interface.

Usage:
    finvista quote <symbols>...
    finvista history <symbol> [--start=<date>] [--end=<date>]
    finvista search <keyword>
    finvista health
"""

from finvista.cli.main import main, cli_entry

__all__ = ["main", "cli_entry"]
