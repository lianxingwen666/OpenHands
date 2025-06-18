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

from types import ModuleType


def import_functions(
    module: ModuleType, function_names: list[str], target_globals: dict[str, object]
) -> None:
    for name in function_names:
        if hasattr(module, name):
            target_globals[name] = getattr(module, name)
        else:
            raise ValueError(f'Function {name} not found in {module.__name__}')
