# Configuration

FinVista provides various configuration options to customize its behavior.

## HTTP Proxy

Set proxy for all requests:

```python
import finvista as fv

fv.set_proxies({
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890"
})
```

## Request Timeout

Set request timeout (in seconds):

```python
fv.set_timeout(60)  # 60 seconds
```

## Caching

Enable or disable caching:

```python
# Enable caching with 5-minute TTL
fv.set_cache(enabled=True, ttl=300)

# Disable caching
fv.set_cache(enabled=False)
```

## Data Source Control

### Check Source Health

```python
health = fv.get_source_health()
print(health)
```

Output:
```python
{
    "cn_stock_daily": {
        "eastmoney": {"status": "healthy", "failures": 0, "avg_time": "0.5s"},
        "sina": {"status": "healthy", "failures": 0, "avg_time": "0.8s"},
        "tencent": {"status": "circuit_open", "failures": 5, "recover_at": "..."}
    }
}
```

### Reset Circuit Breaker

Manually reset a source that has been circuit-broken:

```python
fv.reset_source_circuit("cn_stock_daily", "sina")
```

### Set Source Priority

Customize the order of data sources:

```python
fv.set_source_priority("cn_stock_daily", ["sina", "eastmoney", "tencent"])
```

### Force Specific Source

Use a specific source without failover:

```python
df = fv.get_cn_stock_daily("000001", source="eastmoney")
```

## Failover Configuration

Configure circuit breaker behavior:

```python
# Number of failures before circuit opens
fv.config.failover.failure_threshold = 5

# Time (seconds) before circuit half-opens
fv.config.failover.circuit_timeout = 60

# Number of successes needed to close circuit
fv.config.failover.success_threshold = 3
```

## Environment Variables

FinVista also supports environment variables:

```bash
# Set proxy
export FINVISTA_HTTP_PROXY="http://127.0.0.1:7890"

# Set timeout
export FINVISTA_TIMEOUT=60

# Enable debug logging
export FINVISTA_DEBUG=1
```

## Logging

Enable debug logging:

```python
import logging
logging.getLogger("finvista").setLevel(logging.DEBUG)
```
