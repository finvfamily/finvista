# 配置 API

## 代理设置

### set_proxies

设置 HTTP 代理。

```python
fv.set_proxies(proxies: dict) -> None
```

**参数：**

| 名称 | 类型 | 说明 |
|------|------|------|
| `proxies` | dict | 代理配置字典 |

**示例：**

```python
import finvista as fv

fv.set_proxies({
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890"
})
```

---

## 超时设置

### set_timeout

设置请求超时时间。

```python
fv.set_timeout(timeout: int) -> None
```

**参数：**

| 名称 | 类型 | 说明 |
|------|------|------|
| `timeout` | int | 超时时间（秒） |

**示例：**

```python
fv.set_timeout(60)  # 60 秒超时
```

---

## 缓存设置

### set_cache

配置缓存。

```python
fv.set_cache(enabled: bool = True, ttl: int = 300) -> None
```

**参数：**

| 名称 | 类型 | 说明 |
|------|------|------|
| `enabled` | bool | 是否启用缓存 |
| `ttl` | int | 缓存过期时间（秒） |

**示例：**

```python
# 启用缓存，5 分钟过期
fv.set_cache(enabled=True, ttl=300)

# 禁用缓存
fv.set_cache(enabled=False)
```

---

## 数据源健康

### get_source_health

获取数据源健康状态。

```python
fv.get_source_health() -> dict
```

**返回：** 各数据源的健康状态字典。

**示例：**

```python
health = fv.get_source_health()
print(health)
```

**输出：**

```python
{
    "cn_stock_daily": {
        "eastmoney": {"status": "healthy", "failures": 0, "avg_time": "0.5s"},
        "sina": {"status": "healthy", "failures": 0, "avg_time": "0.8s"},
        "tencent": {"status": "circuit_open", "failures": 5}
    }
}
```

---

## 熔断器重置

### reset_source_circuit

重置数据源熔断器。

```python
fv.reset_source_circuit(data_type: str, source: str) -> None
```

**参数：**

| 名称 | 类型 | 说明 |
|------|------|------|
| `data_type` | str | 数据类型（如 "cn_stock_daily"） |
| `source` | str | 数据源名称（如 "sina"） |

**示例：**

```python
fv.reset_source_circuit("cn_stock_daily", "tencent")
```

---

## 数据源优先级

### set_source_priority

设置数据源优先级。

```python
fv.set_source_priority(data_type: str, sources: list[str]) -> None
```

**参数：**

| 名称 | 类型 | 说明 |
|------|------|------|
| `data_type` | str | 数据类型 |
| `sources` | list | 数据源列表（按优先级排序） |

**示例：**

```python
# 优先使用新浪，然后是东方财富、腾讯
fv.set_source_priority("cn_stock_daily", ["sina", "eastmoney", "tencent"])
```

---

## 配置对象

### config

访问配置对象直接修改设置。

```python
fv.config
```

**可配置项：**

```python
# 故障转移配置
fv.config.failover.failure_threshold = 5   # 失败阈值
fv.config.failover.circuit_timeout = 60    # 熔断时间（秒）
fv.config.failover.success_threshold = 3   # 恢复阈值

# 请求配置
fv.config.request.timeout = 30             # 请求超时
fv.config.request.retry_count = 3          # 重试次数

# 缓存配置
fv.config.cache.enabled = True             # 启用缓存
fv.config.cache.ttl = 300                  # 缓存过期时间
```

---

## 环境变量

FinVista 支持通过环境变量配置：

| 环境变量 | 说明 |
|----------|------|
| `FINVISTA_HTTP_PROXY` | HTTP 代理地址 |
| `FINVISTA_HTTPS_PROXY` | HTTPS 代理地址 |
| `FINVISTA_TIMEOUT` | 请求超时（秒） |
| `FINVISTA_DEBUG` | 启用调试日志（1/0） |
| `FINVISTA_CACHE_ENABLED` | 启用缓存（1/0） |
| `FINVISTA_CACHE_TTL` | 缓存过期时间（秒） |

**示例：**

```bash
export FINVISTA_HTTP_PROXY="http://127.0.0.1:7890"
export FINVISTA_TIMEOUT=60
export FINVISTA_DEBUG=1
```

---

## 日志配置

启用调试日志：

```python
import logging
logging.getLogger("finvista").setLevel(logging.DEBUG)
```

**日志级别：**

| 级别 | 说明 |
|------|------|
| DEBUG | 详细调试信息 |
| INFO | 一般信息 |
| WARNING | 警告信息 |
| ERROR | 错误信息 |

---

## 使用示例

### 生产环境配置

```python
import finvista as fv

# 设置代理
fv.set_proxies({
    "http": "http://proxy.company.com:8080",
    "https": "http://proxy.company.com:8080"
})

# 设置较长超时
fv.set_timeout(120)

# 启用缓存
fv.set_cache(enabled=True, ttl=600)

# 配置故障转移
fv.config.failover.failure_threshold = 3
fv.config.failover.circuit_timeout = 30
```

### 监控数据源

```python
import schedule
import time

def check_health():
    health = fv.get_source_health()
    for data_type, sources in health.items():
        for source, status in sources.items():
            if status['status'] != 'healthy':
                print(f"警告: {data_type}/{source} 异常")
                # 可发送告警

schedule.every(5).minutes.do(check_health)

while True:
    schedule.run_pending()
    time.sleep(1)
```
