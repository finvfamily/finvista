# 配置选项

FinVista 提供多种配置选项，用于自定义其运行行为。

## HTTP 代理配置

为所有请求设置代理：

```python
import finvista as fv

fv.set_proxies({
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890"
})
```

## 请求超时设置

设置请求超时时间（单位：秒）：

```python
fv.set_timeout(60)  # 60 seconds
```

## 缓存机制  

启用或禁用缓存机制：

```python
#启用缓存，TTL 为 5 分钟
fv.set_cache(enabled=True, ttl=300)

禁用缓存  
fv.set_cache(enabled=False)
```

## 数据源管理 

### 数据源健康状态检查  

```python
health = fv.get_source_health()
print(health)
```

输出： 
```python
{
    "cn_stock_daily": {
        "eastmoney": {"status": "healthy", "failures": 0, "avg_time": "0.5s"},
        "sina": {"status": "healthy", "failures": 0, "avg_time": "0.8s"},
        "tencent": {"status": "circuit_open", "failures": 5, "recover_at": "..."}
    }
}
```

### 断路器重置    

手动重置已触发断路器的数据源：

```python
fv.reset_source_circuit("cn_stock_daily", "sina")
```

### 数据源优先级设置 

自定义数据源的优先级顺序：   

```python
fv.set_source_priority("cn_stock_daily", ["sina", "eastmoney", "tencent"])
```

### 强制指定数据源 

在不启用故障转移的情况下使用指定的数据源:

```python
df = fv.get_cn_stock_daily("000001", source="eastmoney")
```

## 故障转移（Failover）配置 

配置断路器的行为参数： 

```python
#断路器开启前允许的失败次数
fv.config.failover.failure_threshold = 5

#断路器进入半开状态前的时间（单位：秒）
fv.config.failover.circuit_timeout = 60

#关闭断路器所需的成功次数 
fv.config.failover.success_threshold = 3
```

## 环境变量配置 

FinVista 同样支持通过环境变量进行配置：

```bash
# Set proxy
export FINVISTA_HTTP_PROXY="http://127.0.0.1:7890"

# Set timeout
export FINVISTA_TIMEOUT=60

# Enable debug logging
export FINVISTA_DEBUG=1
```

## 日志配置 

启用调试日志：

```python
import logging
logging.getLogger("finvista").setLevel(logging.DEBUG)
```
