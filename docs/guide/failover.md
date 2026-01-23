# 故障转移机制

FinVista 的核心特性之一是多数据源自动故障转移。

## 工作原理

当主数据源失败时，FinVista 会自动尝试备用数据源：

```
主数据源 (东方财富) → 失败
    ↓
备用数据源 1 (新浪) → 失败
    ↓
备用数据源 2 (腾讯) → 成功 ✓
```

## 熔断器模式

为防止故障蔓延，FinVista 实现了熔断器模式：

```
健康状态 → 连续 5 次失败 → 熔断（60秒）
    ↑                            ↓
    └── 连续 3 次成功 ← 半开状态
```

### 状态说明

| 状态 | 说明 |
|------|------|
| 健康 (Healthy) | 数据源正常工作 |
| 半开 (Half-Open) | 熔断恢复期，尝试请求 |
| 熔断 (Circuit Open) | 数据源暂时不可用，跳过 |

## 配置熔断器

```python
import finvista as fv

# 失败阈值（触发熔断的失败次数）
fv.config.failover.failure_threshold = 5

# 熔断时间（秒）
fv.config.failover.circuit_timeout = 60

# 恢复阈值（关闭熔断的成功次数）
fv.config.failover.success_threshold = 3
```

## 检查数据源健康状态

```python
health = fv.get_source_health()
print(health)
```

输出示例：

```python
{
    "cn_stock_daily": {
        "eastmoney": {
            "status": "healthy",
            "failures": 0,
            "avg_time": "0.5s"
        },
        "sina": {
            "status": "healthy",
            "failures": 0,
            "avg_time": "0.8s"
        },
        "tencent": {
            "status": "circuit_open",
            "failures": 5,
            "recover_at": "2024-01-15 10:31:00"
        }
    }
}
```

## 手动重置熔断器

```python
# 重置特定数据源的熔断器
fv.reset_source_circuit("cn_stock_daily", "tencent")
```

## 自定义数据源优先级

```python
# 设置数据源优先级（按顺序尝试）
fv.set_source_priority("cn_stock_daily", ["sina", "eastmoney", "tencent"])
```

## 强制使用特定数据源

```python
# 不使用故障转移，强制使用东方财富
df = fv.get_cn_stock_daily("000001", source="eastmoney")
```

## 查看实际使用的数据源

```python
df = fv.get_cn_stock_daily("000001")
print(f"数据来源: {df.attrs.get('source')}")
```

## 数据源列表

### A 股日线

| 优先级 | 数据源 | 说明 |
|--------|--------|------|
| 1 | eastmoney | 东方财富，数据全面 |
| 2 | sina | 新浪财经，稳定可靠 |
| 3 | tencent | 腾讯财经，作为备用 |

### A 股实时行情

| 优先级 | 数据源 | 说明 |
|--------|--------|------|
| 1 | sina | 新浪财经，速度快 |
| 2 | tencent | 腾讯财经 |
| 3 | eastmoney | 东方财富 |

### 基金数据

| 优先级 | 数据源 | 说明 |
|--------|--------|------|
| 1 | tiantian | 天天基金，数据权威 |

### 美股数据

| 优先级 | 数据源 | 说明 |
|--------|--------|------|
| 1 | yahoo | Yahoo Finance |

## 最佳实践

### 1. 监控数据源健康

```python
# 定期检查数据源状态
import schedule

def check_health():
    health = fv.get_source_health()
    for data_type, sources in health.items():
        for source, status in sources.items():
            if status['status'] != 'healthy':
                print(f"警告: {data_type}/{source} 状态异常")

schedule.every(5).minutes.do(check_health)
```

### 2. 异常处理

```python
from finvista import AllSourcesFailedError

try:
    df = fv.get_cn_stock_daily("000001")
except AllSourcesFailedError:
    print("所有数据源都失败了，请稍后重试")
```

### 3. 生产环境建议

- 设置合理的超时时间
- 启用缓存减少请求
- 配置代理提高稳定性
- 监控数据源健康状态
