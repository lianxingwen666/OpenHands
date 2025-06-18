"""
OpenHands Runtime 插件系统
========================

技术栈：
- 插件架构模式: 可扩展的模块化设计
- 依赖注入: 动态加载和管理插件
- 抽象工厂模式: 统一的插件创建接口
- 策略模式: 不同插件的不同实现策略

功能说明：
插件系统为OpenHands Runtime提供可扩展的功能模块：

1. **Jupyter插件** - 提供交互式Python环境和notebook支持
2. **AgentSkills插件** - 提供AI代理的核心技能集合
3. **VSCode插件** - 提供代码编辑器集成和扩展支持

插件特性：
- 动态加载和卸载
- 依赖管理和版本控制
- 配置管理和环境隔离
- 错误处理和恢复机制
"""

# 插件依赖和实现导入
from openhands.runtime.plugins.agent_skills import (
    AgentSkillsPlugin,  # Agent技能插件实现
    AgentSkillsRequirement,  # Agent技能插件依赖
)
from openhands.runtime.plugins.jupyter import (  # Jupyter插件
    JupyterPlugin,
    JupyterRequirement,
)
from openhands.runtime.plugins.requirement import Plugin, PluginRequirement  # 插件基类
from openhands.runtime.plugins.vscode import (  # VSCode插件
    VSCodePlugin,
    VSCodeRequirement,
)

# 模块公开接口
__all__ = [
    'Plugin',  # 插件基类
    'PluginRequirement',  # 插件依赖基类
    'AgentSkillsRequirement',  # Agent技能依赖
    'AgentSkillsPlugin',  # Agent技能插件
    'JupyterRequirement',  # Jupyter依赖
    'JupyterPlugin',  # Jupyter插件
    'VSCodeRequirement',  # VSCode依赖
    'VSCodePlugin',  # VSCode插件
]

# 所有可用插件的注册表 - 使用工厂模式管理插件实例
ALL_PLUGINS = {
    'jupyter': JupyterPlugin,  # Jupyter交互式环境插件
    'agent_skills': AgentSkillsPlugin,  # AI代理技能集合插件
    'vscode': VSCodePlugin,  # VSCode编辑器集成插件
}
