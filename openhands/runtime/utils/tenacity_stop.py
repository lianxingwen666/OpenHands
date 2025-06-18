"""
OpenHands 工具函数模块
================

技术栈：
- 系统编程
- 工具函数
- 辅助功能

功能说明：
提供系统级工具函数和辅助功能
"""

from tenacity import RetryCallState
from tenacity.stop import stop_base

from openhands.utils.shutdown_listener import should_exit


class stop_if_should_exit(stop_base):
    """Stop if the should_exit flag is set."""

    def __call__(self, retry_state: 'RetryCallState') -> bool:
        return should_exit()
