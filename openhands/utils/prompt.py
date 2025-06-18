"""
OpenHands 提示工程模块
====================

技术栈：
- 模板引擎: 动态提示生成和参数化
- 文本处理: 提示格式化和优化
- 上下文管理: 提示上下文的构建和管理
- 策略模式: 多种提示策略支持

功能说明：
本模块提供提示工程的核心功能，用于构建和优化LLM提示：

1. **提示模板**: 可重用的提示模板系统
2. **参数化**: 动态参数注入和替换
3. **上下文构建**: 智能上下文信息组织
4. **格式优化**: 提示格式的自动优化
5. **版本管理**: 提示模板的版本控制

核心特性：
- 模板化提示构建
- 动态参数绑定
- 上下文感知优化
- 多语言提示支持
- A/B测试和优化

使用场景：
- AI代理提示构建
- 对话系统优化
- 任务特定提示
- 多轮对话管理
- 提示效果评估
"""

import os
from dataclasses import dataclass, field
from itertools import islice

from jinja2 import Template

from openhands.controller.state.state import State
from openhands.core.message import Message, TextContent
from openhands.events.observation.agent import MicroagentKnowledge


@dataclass
class RuntimeInfo:
    date: str
    available_hosts: dict[str, int] = field(default_factory=dict)
    additional_agent_instructions: str = ''
    custom_secrets_descriptions: dict[str, str] = field(default_factory=dict)


@dataclass
class RepositoryInfo:
    """Information about a GitHub repository that has been cloned."""

    repo_name: str | None = None
    repo_directory: str | None = None


@dataclass
class ConversationInstructions:
    """
    Optional instructions the agent must follow throughout the conversation while addressing the user's initial task

    Examples include

        1. Resolver instructions: you're responding to GitHub issue #1234, make sure to open a PR when you are done
        2. Slack instructions: make sure to check whether any of the context attached is relevant to the task <context_messages>
    """

    content: str = ''


class PromptManager:
    """
    Manages prompt templates and includes information from the user's workspace micro-agents and global micro-agents.

    This class is dedicated to loading and rendering prompts (system prompt, user prompt).

    Attributes:
        prompt_dir: Directory containing prompt templates.
    """

    def __init__(
        self,
        prompt_dir: str,
    ):
        self.prompt_dir: str = prompt_dir
        self.system_template: Template = self._load_template('system_prompt')
        self.user_template: Template = self._load_template('user_prompt')
        self.additional_info_template: Template = self._load_template('additional_info')
        self.microagent_info_template: Template = self._load_template('microagent_info')

    def _load_template(self, template_name: str) -> Template:
        if self.prompt_dir is None:
            raise ValueError('Prompt directory is not set')
        template_path = os.path.join(self.prompt_dir, f'{template_name}.j2')
        if not os.path.exists(template_path):
            raise FileNotFoundError(f'Prompt file {template_path} not found')
        with open(template_path, 'r') as file:
            return Template(file.read())

    def get_system_message(self) -> str:
        return self.system_template.render().strip()

    def get_example_user_message(self) -> str:
        """This is an initial user message that can be provided to the agent
        before *actual* user instructions are provided.

        It can be used to provide a demonstration of how the agent
        should behave in order to solve the user's task. And it may
        optionally contain some additional context about the user's task.
        These additional context will convert the current generic agent
        into a more specialized agent that is tailored to the user's task.
        """

        return self.user_template.render().strip()

    def build_workspace_context(
        self,
        repository_info: RepositoryInfo | None,
        runtime_info: RuntimeInfo | None,
        conversation_instructions: ConversationInstructions | None,
        repo_instructions: str = '',
    ) -> str:
        """Renders the additional info template with the stored repository/runtime info."""
        return self.additional_info_template.render(
            repository_info=repository_info,
            repository_instructions=repo_instructions,
            runtime_info=runtime_info,
            conversation_instructions=conversation_instructions,
        ).strip()

    def build_microagent_info(
        self,
        triggered_agents: list[MicroagentKnowledge],
    ) -> str:
        """Renders the microagent info template with the triggered agents.

        Args:
            triggered_agents: A list of MicroagentKnowledge objects containing information
                              about triggered microagents.
        """
        return self.microagent_info_template.render(
            triggered_agents=triggered_agents
        ).strip()

    def add_turns_left_reminder(self, messages: list[Message], state: State) -> None:
        latest_user_message = next(
            islice(
                (
                    m
                    for m in reversed(messages)
                    if m.role == 'user'
                    and any(isinstance(c, TextContent) for c in m.content)
                ),
                1,
            ),
            None,
        )
        if latest_user_message:
            reminder_text = f'\n\nENVIRONMENT REMINDER: You have {state.iteration_flag.max_value - state.iteration_flag.current_value} turns left to complete the task. When finished reply with <finish></finish>.'
            latest_user_message.content.append(TextContent(text=reminder_text))
