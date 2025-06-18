"""
OpenHands Plugins 插件
====================

技术栈：
- 插件架构
- 动态加载
- 扩展机制

功能说明：
plugins功能的插件实现，提供可扩展的功能模块
"""

from abc import abstractmethod
from dataclasses import dataclass

from openhands.events.action import Action
from openhands.events.observation import Observation


class Plugin:
    """Base class for a plugin.

    This will be initialized by the runtime client, which will run inside docker.
    """

    name: str

    @abstractmethod
    async def initialize(self, username: str) -> None:
        """Initialize the plugin."""
        pass

    @abstractmethod
    async def run(self, action: Action) -> Observation:
        """Run the plugin for a given action."""
        pass


@dataclass
class PluginRequirement:
    """Requirement for a plugin."""

    name: str
