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

# Common timeout message that can be used across different timeout scenarios
TIMEOUT_MESSAGE_TEMPLATE = (
    "You may wait longer to see additional output by sending empty command '', "
    'send other commands to interact with the current process, '
    'send keys to interrupt/kill the command, '
    'or use the timeout parameter in execute_bash for future commands.'
)
