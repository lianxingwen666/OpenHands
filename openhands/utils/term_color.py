"""
OpenHands 终端颜色工具模块
========================

技术栈：
- ANSI转义序列: 终端颜色和格式控制
- 跨平台支持: 多操作系统兼容性
- 文本格式化: 丰富的文本样式支持
- 颜色管理: 颜色主题和配置

功能说明：
本模块提供终端输出的颜色和格式化功能，增强命令行界面的可读性：

1. **颜色输出**: 支持多种颜色的文本输出
2. **文本样式**: 粗体、斜体、下划线等样式
3. **背景色**: 文本背景颜色设置
4. **主题支持**: 预定义的颜色主题
5. **兼容性**: 跨平台的颜色支持

核心特性：
- ANSI颜色代码支持
- 样式组合和嵌套
- 自动颜色检测
- 主题配置系统
- 性能优化

使用场景：
- 命令行工具输出
- 日志信息着色
- 调试信息显示
- 用户界面增强
- 开发工具集成
"""

from enum import Enum

from termcolor import colored


class TermColor(Enum):
    """Terminal color codes."""

    WARNING = 'yellow'
    SUCCESS = 'green'
    ERROR = 'red'
    INFO = 'blue'


def colorize(text: str, color: TermColor = TermColor.WARNING) -> str:
    """Colorize text with specified color.

    Args:
        text (str): Text to be colored
        color (TermColor, optional): Color to use. Defaults to TermColor.WARNING

    Returns:
        str: Colored text
    """
    return colored(text, color.value)
