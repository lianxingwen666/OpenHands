"""
OpenHands Runtime 实现模块
========================

技术栈：
- 抽象工厂模式: 统一管理不同Runtime实现
- 策略模式: 支持多种执行策略
- 适配器模式: 适配不同的云平台API
- HTTP客户端: 与远程服务通信
- 容器技术: Docker、E2B等容器化方案

功能说明：
本模块包含OpenHands支持的所有Runtime实现：

1. **ActionExecutionClient** - 基础执行客户端，其他Runtime的基类
2. **DockerRuntime** - 本地Docker容器运行时（默认推荐）
3. **LocalRuntime** - 本地直接执行（开发测试用）
4. **E2BRuntime** - E2B云端执行环境
5. **RemoteRuntime** - 远程分布式执行
6. **ModalRuntime** - Modal云计算平台
7. **RunloopRuntime** - Runloop云端环境
8. **DaytonaRuntime** - Daytona开发环境
9. **CLIRuntime** - 命令行界面运行时

每种Runtime都针对不同的使用场景进行了优化。
"""

from openhands.runtime.impl.action_execution.action_execution_client import (
    ActionExecutionClient,  # 基础Action执行客户端，所有Runtime的抽象基类
)
from openhands.runtime.impl.cli import CLIRuntime  # CLI命令行运行时
from openhands.runtime.impl.daytona.daytona_runtime import (
    DaytonaRuntime,  # Daytona开发环境
)
from openhands.runtime.impl.docker.docker_runtime import (
    DockerRuntime,  # Docker容器运行时（默认）
)
from openhands.runtime.impl.e2b.e2b_runtime import E2BRuntime  # E2B云端运行时
from openhands.runtime.impl.local.local_runtime import (
    LocalRuntime,  # 本地直接执行运行时
)
from openhands.runtime.impl.modal.modal_runtime import ModalRuntime  # Modal云计算运行时
from openhands.runtime.impl.remote.remote_runtime import (
    RemoteRuntime,  # 远程分布式运行时
)
from openhands.runtime.impl.runloop.runloop_runtime import (
    RunloopRuntime,  # Runloop云端运行时
)

# 模块公开接口 - 所有可用的Runtime实现
__all__ = [
    'ActionExecutionClient',  # 基础执行客户端
    'CLIRuntime',  # CLI运行时
    'DaytonaRuntime',  # Daytona运行时
    'DockerRuntime',  # Docker运行时（推荐）
    'E2BRuntime',  # E2B云端运行时
    'LocalRuntime',  # 本地运行时
    'ModalRuntime',  # Modal运行时
    'RemoteRuntime',  # 远程运行时
    'RunloopRuntime',  # Runloop运行时
]
