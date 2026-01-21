# Changelog

All notable changes to FinVista will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1] - 2025-01-21

### Added
- GitHub Actions workflow for automated testing
- GitHub Actions workflow for PyPI publishing
- Trusted publishing support (OIDC)

### Changed
- Updated GitHub repository URLs

## [0.1.0] - 2025-01-21

### Added
- Initial release
- Multi-source failover architecture
- Circuit breaker pattern implementation
- Built-in LRU caching
- Token bucket rate limiting

#### China Market
- A-share daily historical data
- A-share real-time quotes
- Stock list and search
- Index daily data and quotes
- Fund NAV history and quotes
- Fund information and search

#### US Market
- Stock daily historical data
- Real-time quotes
- Company information
- Stock search

#### Macroeconomic Data
- China GDP, CPI, PPI, PMI
- Money supply (M0, M1, M2)
- Social financing

#### Data Sources
- East Money (东方财富)
- Sina Finance (新浪财经)
- Tencent Finance (腾讯财经)
- Tiantian Fund (天天基金)
- Yahoo Finance

#### CLI
- `quote` - Real-time quotes
- `history` - Historical data
- `search` - Stock search
- `health` - Source health check
- `macro` - Macroeconomic data

---

## Upcoming

### Planned Features
- Hong Kong market support
- Forex data
- Cryptocurrency data
- Async API support
- Redis caching support
- More macroeconomic indicators

---

[0.1.1]: https://github.com/finvfamily/finvista/releases/tag/v0.1.1
[0.1.0]: https://github.com/finvfamily/finvista/releases/tag/v0.1.0
