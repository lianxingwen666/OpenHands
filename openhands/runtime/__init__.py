"""
OpenHands Runtime 模块初始化文件
=================================

技术栈：
- Python 3.12+ 作为主要编程语言
- 工厂模式用于Runtime实例创建
- 多种运行时环境支持（Docker、E2B、Modal等）

功能说明：
本文件是OpenHands运行时系统的入口点，负责：
1. 导入所有可用的Runtime实现类
2. 提供Runtime类型到具体实现的映射
3. 提供动态Runtime类获取功能

支持的运行时类型：
- Docker: 本地Docker容器运行时（默认）
- E2B: 云端代码执行环境
- Remote: 远程运行时环境
- Modal: Modal云计算平台
- Runloop: Runloop云端运行环境
- Local: 本地直接执行（无容器隔离）
- Daytona: Daytona开发环境
- CLI: 命令行界面运行时
"""

from openhands.runtime.base import Runtime  # Runtime基类，定义所有运行时的接口
from openhands.runtime.impl.cli.cli_runtime import CLIRuntime  # CLI运行时实现
from openhands.runtime.impl.daytona.daytona_runtime import (
    DaytonaRuntime,  # Daytona运行时实现
)
from openhands.runtime.impl.docker.docker_runtime import (  # Docker运行时实现（默认）
    DockerRuntime,
)
from openhands.runtime.impl.e2b.e2b_runtime import E2BRuntime  # E2B云端运行时实现
from openhands.runtime.impl.local.local_runtime import LocalRuntime  # 本地运行时实现
from openhands.runtime.impl.modal.modal_runtime import (
    ModalRuntime,  # Modal云计算运行时实现
)
from openhands.runtime.impl.remote.remote_runtime import RemoteRuntime  # 远程运行时实现
from openhands.runtime.impl.runloop.runloop_runtime import (
    RunloopRuntime,  # Runloop运行时实现
)
from openhands.utils.import_utils import get_impl  # 动态导入工具

# mypy: disable-error-code="type-abstract"
# 默认运行时类映射表 - 使用工厂模式管理不同的Runtime实现
_DEFAULT_RUNTIME_CLASSES: dict[str, type[Runtime]] = {
    'eventstream': DockerRuntime,  # 事件流模式（使用Docker）
    'docker': DockerRuntime,  # Docker容器运行时（推荐用于开发和生产）
    'e2b': E2BRuntime,  # E2B云端执行环境（适合云端部署）
    'remote': RemoteRuntime,  # 远程运行时（适合分布式部署）
    'modal': ModalRuntime,  # Modal云计算平台（适合大规模计算）
    'runloop': RunloopRuntime,  # Runloop云端环境（适合CI/CD）
    'local': LocalRuntime,  # 本地直接执行（开发测试用，无隔离）
    'daytona': DaytonaRuntime,  # Daytona开发环境（适合团队开发）
    'cli': CLIRuntime,  # 命令行界面运行时（适合脚本化使用）
}


def get_runtime_cls(name: str) -> type[Runtime]:
    """
    获取Runtime类的工厂方法

    参数:
        name: Runtime类型名称（如 'docker', 'e2b' 等）

    返回:
        对应的Runtime类

    功能说明:
    1. 如果name是预定义的运行时名称，直接返回对应的类
    2. 否则尝试将name解析为Runtime的子类并返回
    3. 如果都失败则抛出ValueError异常

    使用工厂模式，支持：
    - 预定义的Runtime类型
    - 自定义Runtime实现的动态加载
    """
    if name in _DEFAULT_RUNTIME_CLASSES:
        return _DEFAULT_RUNTIME_CLASSES[name]
    try:
        # 尝试动态导入自定义Runtime实现
        return get_impl(Runtime, name)
    except Exception as e:
        known_keys = _DEFAULT_RUNTIME_CLASSES.keys()
        raise ValueError(
            f'Runtime {name} not supported, known are: {known_keys}'
        ) from e


# 模块公开接口 - 定义可以被外部导入的类和函数
__all__ = [
    'Runtime',  # Runtime基类
    'E2BRuntime',  # E2B云端运行时
    'RemoteRuntime',  # 远程运行时
    'ModalRuntime',  # Modal云计算运行时
    'RunloopRuntime',  # Runloop运行时
    'DockerRuntime',  # Docker运行时（默认）
    'DaytonaRuntime',  # Daytona运行时
    'CLIRuntime',  # CLI运行时
    'get_runtime_cls',  # Runtime类获取工厂方法
]
