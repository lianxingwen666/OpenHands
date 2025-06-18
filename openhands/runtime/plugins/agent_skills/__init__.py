"""
OpenHands Agent_Skills 模块初始化文件
==============================

技术栈：
- Python 模块系统
- 组件导入管理

功能说明：
agent_skills模块的初始化和接口定义
"""

from dataclasses import dataclass

from openhands.events.action import Action
from openhands.events.observation import Observation
from openhands.runtime.plugins.agent_skills import agentskills
from openhands.runtime.plugins.requirement import Plugin, PluginRequirement


@dataclass
class AgentSkillsRequirement(PluginRequirement):
    name: str = 'agent_skills'
    documentation: str = agentskills.DOCUMENTATION


class AgentSkillsPlugin(Plugin):
    name: str = 'agent_skills'

    async def initialize(self, username: str) -> None:
        """Initialize the plugin."""
        pass

    async def run(self, action: Action) -> Observation:
        """Run the plugin for a given action."""
        raise NotImplementedError('AgentSkillsPlugin does not support run method')
