# 股票价格监控系统

## 项目简介
这是一个基于Python的股票价格监控系统，可以实时追踪股票价格变动并在达到设定的波动阈值时发出警报提醒。

## 主要功能
- 实时监控多支股票价格
- 计算并显示每支股票的收益率和盈亏情况
- 价格波动超过阈值时发出声音警报
- 支持添加和管理股票持仓信息
- 自动保存持仓数据
- 完整的日志记录功能

## 系统要求
- Python 3.6+
- Windows系统（因使用winsound模块）

## 依赖包安装
```bash
pip install tushare
```

## 配置说明
在运行程序前，需要创建`config.json`配置文件，包含以下内容：
```json
{
    "tushare_token": "你的Tushare Token",
    "alert_threshold": 0.05,
    "monitor_interval": 10,
    "max_workers": 5,
    "max_retries": 3,
    "timeout": 5,
    "positions_file": "positions.json",
    "log_file": "stock_monitor.log"
}
```

### 配置参数说明
- `tushare_token`: Tushare API的访问令牌
- `alert_threshold`: 价格波动警报阈值（默认0.05，即5%）
- `monitor_interval`: 监控间隔时间（秒）
- `max_workers`: 最大线程数
- `max_retries`: API调用失败重试次数
- `timeout`: API调用超时时间（秒）
- `positions_file`: 持仓信息保存文件路径
- `log_file`: 日志文件路径

## 使用方法
1. 运行程序：`python Stock_price_monitoring.py`

2. 主菜单选项：
   - 1: 添加股票持仓
   - 2: 开始监控
   - 3: 退出程序

3. 添加股票时需要输入：
   - 股票代码（以6、0或3开头）
   - 买入价格
   - 持仓数量



## 注意事项
1. 确保已正确配置Tushare Token
2. 股票代码格式必须正确（6/0/3开头）
3. 程序运行时会自动创建日志文件
4. 持仓信息会自动保存到JSON文件中

## 日志说明
程序会自动记录以下类型的日志：
- 系统启动和初始化信息
- 股票价格监控记录
- 警报触发信息
- 错误和异常信息



