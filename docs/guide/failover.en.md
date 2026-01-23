# Multi-Source Failover

FinVista's core feature is automatic failover between multiple data sources.

## How It Works

```
┌─────────────────────────────────────────────────────────────┐
│                      User Request                           │
│         fv.get_cn_stock_daily("000001")                     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Source Manager                            │
│  1. Get available sources (exclude circuit-broken)          │
│  2. Try sources by priority                                 │
│  3. Return on success / try next on failure                 │
└─────────────────────────────────────────────────────────────┘
           │              │              │
           ▼              ▼              ▼
    ┌──────────┐   ┌──────────┐   ┌──────────┐
    │ EastMoney│   │   Sina   │   │ Tencent  │
    │priority=0│   │priority=1│   │priority=2│
    │ [HEALTHY]│   │ [HEALTHY]│   │ [CIRCUIT]│
    └──────────┘   └──────────┘   └──────────┘
```

## Circuit Breaker Pattern

The circuit breaker prevents cascading failures:

```
                    Success
     ┌────────────────────────────────────┐
     │                                    │
     ▼                                    │
┌─────────┐  5 consecutive    ┌────────────────┐
│ CLOSED  │  failures         │     OPEN       │
│ (Normal)│ ─────────────────►│ (Reject calls) │
└─────────┘                   └────────────────┘
     ▲                               │
     │ 3 consecutive                 │ After 60s
     │ successes                     ▼
┌─────────┐                   ┌────────────────┐
│ CLOSED  │ ◄──────────────── │   HALF-OPEN    │
│         │    Success        │ (Test one call)│
└─────────┘                   └────────────────┘
                                     │
                                     │ Failure
                                     ▼
                              Back to OPEN
```

### States

| State | Description | Behavior |
|-------|-------------|----------|
| CLOSED | Normal operation | All requests pass through |
| OPEN | Circuit tripped | All requests rejected immediately |
| HALF-OPEN | Testing recovery | Allow one test request |

### Configuration

```python
import finvista as fv

# Failures before circuit opens
fv.config.failover.failure_threshold = 5

# Seconds before testing recovery
fv.config.failover.circuit_timeout = 60

# Successes needed to close circuit
fv.config.failover.success_threshold = 3
```

## Monitoring Source Health

```python
health = fv.get_source_health()

# Example output
{
    "cn_stock_daily": {
        "eastmoney": {
            "status": "healthy",
            "consecutive_failures": 0,
            "total_requests": 150,
            "success_rate": 0.99,
            "avg_response_time": 0.45
        },
        "sina": {
            "status": "circuit_open",
            "consecutive_failures": 5,
            "circuit_opened_at": "2024-01-15T10:30:00",
            "recover_at": "2024-01-15T10:31:00"
        }
    }
}
```

## Manual Controls

### Reset Circuit Breaker

```python
# Reset specific source
fv.reset_source_circuit("cn_stock_daily", "sina")
```

### Change Priority

```python
# Make Sina the primary source
fv.set_source_priority("cn_stock_daily", ["sina", "eastmoney", "tencent"])
```

### Force Specific Source

```python
# Bypass failover, use only EastMoney
df = fv.get_cn_stock_daily("000001", source="eastmoney")
```

## Check Which Source Was Used

```python
df = fv.get_cn_stock_daily("000001")
print(f"Data from: {df.attrs.get('source')}")  # e.g., "eastmoney"
```

## Error Handling

When all sources fail:

```python
from finvista.exceptions import AllSourcesFailedError

try:
    df = fv.get_cn_stock_daily("000001")
except AllSourcesFailedError as e:
    print(f"All sources failed: {e}")
    print(f"Last error: {e.last_error}")
```

## Best Practices

1. **Don't disable failover** - It's there for reliability
2. **Monitor source health** - Check periodically in production
3. **Use caching** - Reduces load on data sources
4. **Handle errors gracefully** - Catch `AllSourcesFailedError`
