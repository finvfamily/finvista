# Configuration API

## HTTP Settings

### set_proxies

Set HTTP proxy for all requests.

```python
fv.set_proxies(proxies: dict) -> None
```

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| `proxies` | dict | Proxy configuration |

**Example:**

```python
fv.set_proxies({
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890"
})
```

---

### set_timeout

Set request timeout.

```python
fv.set_timeout(seconds: int) -> None
```

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| `seconds` | int | Timeout in seconds |

**Example:**

```python
fv.set_timeout(60)
```

---

## Caching

### set_cache

Configure caching behavior.

```python
fv.set_cache(enabled: bool = True, ttl: int = 300) -> None
```

**Parameters:**

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `enabled` | bool | True | Enable/disable caching |
| `ttl` | int | 300 | Cache TTL in seconds |

**Example:**

```python
# Enable with 5-minute TTL
fv.set_cache(enabled=True, ttl=300)

# Disable caching
fv.set_cache(enabled=False)
```

---

## Data Source Management

### get_source_health

Get health status of all data sources.

```python
fv.get_source_health() -> dict
```

**Returns:** Dict with source health information

**Example:**

```python
health = fv.get_source_health()
print(health)
# {
#     "cn_stock_daily": {
#         "eastmoney": {"status": "healthy", "failures": 0},
#         "sina": {"status": "circuit_open", "failures": 5}
#     }
# }
```

---

### reset_source_circuit

Reset circuit breaker for a specific source.

```python
fv.reset_source_circuit(data_type: str, source_name: str) -> None
```

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| `data_type` | str | Data type (e.g., "cn_stock_daily") |
| `source_name` | str | Source name (e.g., "eastmoney") |

**Example:**

```python
fv.reset_source_circuit("cn_stock_daily", "sina")
```

---

### set_source_priority

Set priority order for data sources.

```python
fv.set_source_priority(data_type: str, sources: list[str]) -> None
```

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| `data_type` | str | Data type |
| `sources` | list | Source names in priority order |

**Example:**

```python
# Make Sina the primary source
fv.set_source_priority("cn_stock_daily", ["sina", "eastmoney", "tencent"])
```

---

## Failover Configuration

Access via `fv.config.failover`:

```python
# Failures before circuit opens
fv.config.failover.failure_threshold = 5

# Seconds before circuit half-opens
fv.config.failover.circuit_timeout = 60

# Successes needed to close circuit
fv.config.failover.success_threshold = 3
```

---

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FINVISTA_HTTP_PROXY` | HTTP proxy URL | None |
| `FINVISTA_TIMEOUT` | Request timeout (seconds) | 30 |
| `FINVISTA_DEBUG` | Enable debug logging | 0 |
