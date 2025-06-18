"""
OpenHands File_Ops 模块初始化文件
==========================

技术栈：
- Python 模块系统
- 组件导入管理

功能说明：
file_ops模块的初始化和接口定义
"""

from openhands.runtime.plugins.agent_skills.file_ops import file_ops
from openhands.runtime.plugins.agent_skills.utils.dependency import import_functions

import_functions(
    module=file_ops, function_names=file_ops.__all__, target_globals=globals()
)
__all__ = file_ops.__all__
