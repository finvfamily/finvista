# 数据接口踩坑后，我用AI辅助写了个开源库

> 前几篇文章用到了一个叫 finvista 的库来获取数据，有读者问这是什么。今天就聊聊这个库的来龙去脉——一个被数据接口折腾到崩溃后，用 AI 辅助开发的开源项目。

先说背景：我不是专业程序员，本职工作是做量化研究的。写代码是为了实现策略，不是为了写代码本身。

但就是数据这一环，让我踩了无数坑。

---

## 一、踩坑经历

### 1.1 数据源的不稳定

2024年某天，我正在跑一个实盘策略，突然发现程序报错了。

排查后发现：**东方财富的接口挂了**。

不是我的问题，是他们的服务器出了故障。那天挂了整整8个小时，我的策略完全停摆。

这种事不是第一次了：
- 新浪财经接口时不时返回空数据
- 腾讯的接口突然改了返回格式
- 某些免费接口直接下线

### 1.2 现有方案的问题

我试过市面上的几个库：

**Tushare**
- 要积分，免费额度很快用完
- 高级数据要付费

**AKShare**
- 免费，数据全
- 但单一数据源，挂了就没辙
- 接口变动频繁

**自己直接调API**
- 灵活，但要写很多适配代码
- 每个数据源格式都不一样
- 维护成本高

### 1.3 最痛的一次

有一次我的策略连续三天没有正常执行，原因是：

1. 东方财富接口挂了（第一天）
2. 我手动切换到新浪，但新浪被限流了（第二天）
3. 切换到腾讯，发现腾讯的数据格式变了，解析报错（第三天）

三天时间，策略错过了好几个信号。事后算了一下，少赚了大概2%。

**这件事让我下定决心：必须做一个多数据源自动切换的方案。**

---

## 二、设计思路

### 2.1 核心需求

1. **多数据源**：不能只依赖一个源
2. **自动切换**：主数据源挂了，自动用备用源，用户无感知
3. **熔断保护**：某个源连续失败，暂时不再尝试，避免拖慢整体速度
4. **统一接口**：不管用哪个源，返回格式一致
5. **简单易用**：一行代码获取数据，不想写复杂配置

### 2.2 架构设计

```
用户调用
   │
   ▼
┌─────────────────┐
│  统一API层      │  fv.get_cn_stock_daily("000001")
└─────────────────┘
         │
         ▼
┌─────────────────┐
│  数据源管理器   │  选择可用数据源，处理故障转移
└─────────────────┘
         │
    ┌────┼────┐
    ▼    ▼    ▼
┌─────┐┌─────┐┌─────┐
│东财 ││新浪 ││腾讯 │  各数据源适配器
└─────┘└─────┘└─────┘
```

### 2.3 熔断器设计

借鉴了微服务架构中的熔断器模式：

```
正常状态(CLOSED)
     │
     │ 连续失败5次
     ▼
熔断状态(OPEN) ──60秒后──▶ 半开状态(HALF_OPEN)
     ▲                              │
     │                              │ 尝试一次
     │    失败                      ▼
     └──────────────────────── 成功则恢复
```

- **CLOSED**：正常使用该数据源
- **OPEN**：暂停使用，直接跳过
- **HALF_OPEN**：试探性地尝试一次，成功则恢复

---

## 三、AI 辅助开发

### 3.1 为什么用 AI

说实话，这个项目如果纯手写，我可能需要几个月。

但我用 AI（主要是 Claude）辅助开发，大大提高了效率：

**AI 擅长的部分**：
- 生成重复性代码（各数据源的适配器结构类似）
- 写单元测试
- 生成文档和注释
- 代码重构和优化建议
- 快速实现标准模式（如熔断器）

**我负责的部分**：
- 整体架构设计
- 核心逻辑决策
- 实际测试和调试
- 接口设计（怎么用起来顺手）

### 3.2 AI 辅助的实际例子

**例子1：生成数据源适配器**

我写好了东方财富的适配器后，让 AI 参考这个结构，生成新浪和腾讯的适配器。

```
我："参考 eastmoney.py 的结构，帮我写一个 sina.py，
    用于从新浪财经获取股票日线数据。API地址是xxx，返回格式是xxx。"

AI：生成了完整的 sina.py，包括请求、解析、异常处理

我：测试、微调、合并
```

本来可能要写半天的代码，20分钟搞定。

**例子2：实现熔断器**

```
我："帮我实现一个熔断器类，要求：
    - 连续失败N次后进入熔断状态
    - 熔断T秒后进入半开状态
    - 半开状态下成功M次后恢复
    - 要线程安全"

AI：生成了完整的 CircuitBreaker 类

我：review代码、补充边界情况、添加日志
```

**例子3：写测试用例**

```
我："给 source_manager.py 写单元测试，覆盖以下场景：
    - 主数据源正常
    - 主数据源失败，切换到备用
    - 所有数据源都失败
    - 熔断器触发和恢复"

AI：生成了完整的测试文件

我：运行测试、修复发现的bug
```

### 3.3 效率提升

粗略估算：

| 模块 | 纯手写预估 | AI辅助实际 | 节省 |
|------|------------|------------|------|
| 数据源适配器（4个） | 16小时 | 4小时 | 75% |
| 熔断器 | 4小时 | 1小时 | 75% |
| 单元测试 | 8小时 | 2小时 | 75% |
| 文档 | 4小时 | 1小时 | 75% |
| **合计** | **32小时** | **8小时** | **75%** |

当然，AI 生成的代码不能直接用，需要 review 和调整。但它确实帮我跳过了大量"体力活"。

### 3.4 AI 辅助的局限

也有 AI 做不好的地方：

- **架构决策**：该用什么设计模式、模块怎么划分，还是得自己想
- **业务逻辑**：金融数据的特殊处理（复权、停牌等），AI 不一定懂
- **调试**：遇到诡异的 bug，还是得自己排查
- **接口设计**：怎么设计才好用，需要自己的使用经验

**AI 是工具，不是替代品。它放大了我的效率，但核心的思考和决策还是我自己做的。**

---

## 四、FinVista 功能介绍

说了这么多背景，介绍一下这个库的功能。

### 4.1 安装

```bash
pip install finvista
```

### 4.2 基本用法

```python
import finvista as fv

# A股日线数据
df = fv.get_cn_stock_daily("000001", start_date="2024-01-01")

# 实时行情
df = fv.get_cn_stock_quote(["000001", "600519"])

# 美股数据
df = fv.get_us_stock_daily("AAPL", start_date="2024-01-01")

# 基金净值
df = fv.get_cn_fund_nav("110011")

# 指数数据
df = fv.get_cn_index_daily("000300")  # 沪深300

# 宏观数据
df = fv.get_cn_macro_gdp()
df = fv.get_cn_macro_cpi()
```

### 4.3 多数据源故障转移

这是核心功能：

```python
# 正常使用，自动选择最优数据源
df = fv.get_cn_stock_daily("000001")

# 查看实际用了哪个数据源
print(df.attrs.get('source'))  # 可能是 'eastmoney', 'sina', 或 'tencent'

# 查看各数据源健康状态
health = fv.get_source_health()
print(health)
# {
#   "cn_stock_daily": {
#     "eastmoney": {"status": "healthy", "failures": 0},
#     "sina": {"status": "healthy", "failures": 0},
#     "tencent": {"status": "circuit_open", "failures": 5}
#   }
# }
```

如果你不想用自动切换，也可以指定数据源：

```python
# 强制使用新浪
df = fv.get_cn_stock_daily("000001", source="sina")
```

### 4.4 数据源映射

| 数据类型 | 主数据源 | 备用数据源 |
|----------|----------|------------|
| A股日线 | 东方财富 | 新浪、腾讯 |
| A股实时 | 新浪 | 腾讯、东方财富 |
| 指数 | 东方财富 | 新浪 |
| 基金 | 天天基金 | - |
| 美股 | Yahoo Finance | - |
| 宏观数据 | 东方财富 | - |

### 4.5 配置

```python
# 设置代理（如果需要）
fv.set_proxies({"http": "http://127.0.0.1:7890"})

# 设置超时
fv.set_timeout(60)

# 启用缓存
fv.set_cache(enabled=True, ttl=300)  # 缓存5分钟

# 手动重置熔断器
fv.reset_source_circuit("cn_stock_daily", "sina")
```

### 4.6 命令行工具

也提供了 CLI，方便快速查询：

```bash
# 查行情
finvista quote 000001 600519

# 导出历史数据
finvista history 000001 --start 2024-01-01 --format csv

# 查看数据源状态
finvista health
```

---

## 五、技术细节

### 5.1 数据源管理器

```python
class SourceManager:
    """数据源管理器"""

    def fetch_with_fallback(self, data_type, **kwargs):
        """带故障转移的数据获取"""

        # 获取该数据类型的所有可用数据源（排除熔断的）
        sources = self.get_available_sources(data_type)

        if not sources:
            raise AllSourcesUnavailableError(f"No available sources for {data_type}")

        last_error = None

        # 按优先级依次尝试
        for source in sources:
            try:
                data = source.fetch(**kwargs)
                self.record_success(data_type, source.name)
                return data, source.name

            except Exception as e:
                self.record_failure(data_type, source.name, e)
                last_error = e
                continue  # 尝试下一个数据源

        raise AllSourcesFailedError(f"All sources failed for {data_type}", last_error)
```

### 5.2 熔断器实现

```python
class CircuitBreaker:
    """熔断器"""

    def __init__(self, failure_threshold=5, timeout=60, success_threshold=3):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.success_threshold = success_threshold

        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None

    def is_available(self):
        """检查是否可用"""
        if self.state == CircuitState.CLOSED:
            return True

        if self.state == CircuitState.OPEN:
            # 检查是否超时，可以进入半开状态
            if time.time() - self.last_failure_time > self.timeout:
                self.state = CircuitState.HALF_OPEN
                return True
            return False

        if self.state == CircuitState.HALF_OPEN:
            return True

        return False

    def record_success(self):
        """记录成功"""
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.success_threshold:
                self.state = CircuitState.CLOSED
                self.failure_count = 0
                self.success_count = 0
        else:
            self.failure_count = 0

    def record_failure(self):
        """记录失败"""
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.state == CircuitState.HALF_OPEN:
            self.state = CircuitState.OPEN
            self.success_count = 0

        elif self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
```

### 5.3 统一数据格式

不管用哪个数据源，返回的 DataFrame 格式是一致的：

```python
# 日线数据统一格式
columns = ['date', 'open', 'high', 'low', 'close', 'volume', 'amount']

# 实时行情统一格式
columns = ['symbol', 'name', 'price', 'change', 'change_pct', 'open', 'high', 'low', 'volume', 'amount']
```

每个数据源适配器负责把原始数据转换成统一格式。

---

## 六、开源与贡献

### 6.1 项目地址

- **GitHub**: https://github.com/finvfamily/finvista
- **PyPI**: https://pypi.org/project/finvista/
- **文档**: https://finvfamily.github.io/finvista/

### 6.2 欢迎贡献

项目还在早期，有很多可以完善的地方：

**Good First Issues**（新手友好）：
- 添加港股市场支持
- 添加更多宏观经济指标
- 中文文档翻译

**进阶任务**：
- 异步API支持
- 更多数据源适配器
- Redis缓存支持

如果你在使用过程中发现 bug，或者有功能建议，欢迎提 Issue。

如果你愿意贡献代码，更是感激不尽。

### 6.3 为什么开源

几个原因：

1. **回馈社区**：我自己也用了很多开源工具，应该回馈一下
2. **共同维护**：一个人维护多个数据源太累，希望有人一起
3. **倒逼质量**：开源出来，代码质量会被迫提高
4. **交流学习**：希望认识更多做量化的朋友

---

## 七、写在最后

这个项目从一个"被数据接口折腾到崩溃"的痛点出发，到现在开源发布，大概花了两个月时间（业余时间断断续续做的）。

几点感想：

**1. 痛点驱动**

最好的项目往往来自真实的痛点。不是"我想做个什么"，而是"我必须解决这个问题"。

**2. AI 改变了开发方式**

以前觉得"造轮子"很可怕，要写很多代码。现在有 AI 辅助，重复性工作大大减少，个人开发者也能做出相对完整的项目。

**3. 开源是一种选择**

可以自己用，也可以开源出来。开源意味着更多责任，但也有更多收获。

**4. 完成比完美重要**

这个库还有很多不完善的地方，但先发布出来，边用边改，比追求完美但永远不发布要好。

---

如果你也在做量化，也被数据问题困扰过，欢迎试试这个库。

有问题欢迎 GitHub Issue 或评论区讨论。

```bash
pip install finvista
```

---

*下一篇预告：《2025年我的量化策略复盘：真实收益与教训》*
