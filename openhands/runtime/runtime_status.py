"""
OpenHands Runtime 状态管理模块
============================

技术栈：
- Python Enum 枚举类型
- 状态机模式用于Runtime生命周期管理
- 国际化支持（i18n）的状态消息

功能说明：
定义Runtime运行时的各种状态，用于：
1. 跟踪Runtime的生命周期
2. 向用户显示当前运行状态
3. 支持前端状态展示和国际化
"""

from enum import Enum


class RuntimeStatus(Enum):
    """
    Runtime运行时状态枚举类

    使用状态机模式管理Runtime的生命周期，每个状态包含：
    - value: 状态标识符（用于国际化和前端显示）
    - message: 默认英文消息（用于日志和调试）

    状态转换流程：
    STOPPED -> BUILDING_RUNTIME -> STARTING_RUNTIME -> RUNTIME_STARTED
    -> SETTING_UP_WORKSPACE -> SETTING_UP_GIT_HOOKS -> READY
    """

    def __init__(self, value: str, message: str):
        """
        初始化Runtime状态

        参数:
            value: 状态值，用于前端国际化（格式：STATUS$状态名）
            message: 状态描述消息
        """
        self._value_ = value
        self.message = message

    # Runtime生命周期状态定义
    STOPPED = 'STATUS$STOPPED', 'Stopped'  # 已停止状态
    BUILDING_RUNTIME = (
        'STATUS$BUILDING_RUNTIME',
        'Building runtime...',
    )  # 构建运行时环境
    STARTING_RUNTIME = 'STATUS$STARTING_RUNTIME', 'Starting runtime...'  # 启动运行时
    RUNTIME_STARTED = 'STATUS$RUNTIME_STARTED', 'Runtime started...'  # 运行时已启动
    SETTING_UP_WORKSPACE = (
        'STATUS$SETTING_UP_WORKSPACE',
        'Setting up workspace...',
    )  # 设置工作空间
    SETTING_UP_GIT_HOOKS = (
        'STATUS$SETTING_UP_GIT_HOOKS',
        'Setting up git hooks...',
    )  # 设置Git钩子
    READY = 'STATUS$READY', 'Ready...'  # 就绪状态，可以接受任务
