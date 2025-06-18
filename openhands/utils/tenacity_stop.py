"""
OpenHands 重试停止条件模块
========================

技术栈：
- Tenacity: Python重试库，提供灵活的重试机制
- 策略模式: 多种停止条件策略
- 时间管理: 基于时间的重试控制
- 条件判断: 复杂的停止条件逻辑

功能说明：
本模块定义重试操作的停止条件，控制何时停止重试：

1. **停止策略**: 多种重试停止策略
2. **条件组合**: 复杂停止条件的组合
3. **时间控制**: 基于时间的停止条件
4. **次数限制**: 基于次数的停止条件
5. **自定义条件**: 支持自定义停止逻辑

核心特性：
- 灵活的停止条件配置
- 策略组合和嵌套
- 动态条件评估
- 性能优化
- 详细的重试统计

使用场景：
- 网络请求重试
- 数据库连接重试
- 外部服务调用
- 文件操作重试
- 系统恢复机制
"""

from tenacity import RetryCallState
from tenacity.stop import stop_base

from openhands.utils.shutdown_listener import should_exit


class stop_if_should_exit(stop_base):
    """Stop if the should_exit flag is set."""

    def __call__(self, retry_state: 'RetryCallState') -> bool:
        return bool(should_exit())
