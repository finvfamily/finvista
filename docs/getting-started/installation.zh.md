# 安装指南

## 系统要求

- Python >= 3.10
- pip（Python 包管理器）

## 基本安装

使用 pip 安装 FinVista：

```bash
pip install finvista
```

## 可选依赖

### 完整安装

安装所有可选依赖：

```bash
pip install finvista[full]
```

这将包含以下内容： 

-   `curl-cffi` —— 更强大的 HTTP 客户端，支持浏览器伪装
-   `openpyxl` —— Excel 文件支持
-   `xlrd`—— 旧版 Excel 文件支持

### 异步支持 

用于支持 async/await 功能：

```bash
pip install finvista[async]
```

### 缓存支持  

用于 Redis 或基于磁盘的缓存支持：

```bash
pip install finvista[cache]
```

### 开发环境

用于开发与测试：  

```bash
pip install finvista[dev]
```

## 验证安装 

```python
import finvista as fv

#检查已安装的版本 
print(fv.__version__)

#快速测试  
df = fv.get_cn_stock_quote(["000001"])
print(df)
```

## 升级    

```bash
pip install --upgrade finvista
```

## 卸载 

```bash
pip uninstall finvista
```