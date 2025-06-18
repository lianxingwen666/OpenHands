"""
OpenHands 动态导入工具模块
========================

技术栈：
- Importlib: Python标准库动态导入模块，支持运行时模块加载
- Functools.lru_cache: 最近最少使用缓存装饰器，提供函数结果缓存
- Typing.TypeVar: 泛型类型变量，支持类型安全的泛型编程
- 反射机制: 运行时类型检查和验证

功能说明：
本模块提供OpenHands的核心扩展机制，支持运行时实现替换和动态类加载：

1. **动态导入**: 通过完全限定名动态导入Python对象
2. **实现替换**: 支持基类实现的运行时替换
3. **类型安全**: 确保导入的实现符合基类接口
4. **缓存优化**: 避免重复导入相同的类
5. **扩展机制**: 为应用程序提供自定义实现的能力

核心特性：
- 完全限定名解析和导入
- 继承关系验证和类型检查
- LRU缓存提高性能
- 支持插件架构和依赖注入
- 运行时配置和实现切换

使用场景：
- 服务器组件的自定义实现
- 存储后端的可插拔架构
- 第三方服务集成
- 测试环境的模拟实现
- 多租户系统的差异化配置
"""

import importlib
from functools import lru_cache
from typing import TypeVar

# 泛型类型变量，用于类型安全的实现替换
T = TypeVar('T')


def import_from(qual_name: str):
    """
    通过完全限定名动态导入Python对象

    参数:
        qual_name: 完全限定名，格式为 'module.submodule.name'
                  例如: 'openhands.server.user_auth.UserAuth'

    返回:
        导入的对象（类、函数或变量）

    功能说明:
    这是一个通用的动态导入工具函数，可以导入任何Python值（类、函数、变量）。
    它通过解析完全限定名来定位和导入指定的对象。

    实现原理:
    1. 将完全限定名按'.'分割
    2. 提取模块名（除最后一部分外的所有部分）
    3. 使用importlib导入模块
    4. 通过getattr获取模块中的指定属性

    使用场景:
    - 配置驱动的组件加载
    - 插件系统的动态加载
    - 工厂模式的实现
    - 依赖注入容器

    示例:
        >>> UserAuth = import_from('openhands.server.user_auth.UserAuth')
        >>> auth = UserAuth()
        >>> func = import_from('mymodule.utils.helper_function')
        >>> result = func()
    """
    # 解析完全限定名
    parts = qual_name.split('.')
    module_name = '.'.join(parts[:-1])  # 模块路径
    object_name = parts[-1]  # 对象名称

    # 动态导入模块
    module = importlib.import_module(module_name)

    # 获取模块中的指定对象
    result = getattr(module, object_name)
    return result


@lru_cache()
def get_impl(cls: type[T], impl_name: str | None) -> type[T]:
    """
    导入并验证基类的命名实现

    参数:
        cls: 定义接口的基类
        impl_name: 实现类的完全限定名，或None使用基类
                  例如: 'openhands.server.conversation_manager.StandaloneConversationManager'

    返回:
        实现类，保证是cls的子类

    功能说明:
    这是OpenHands的核心扩展机制，允许运行时替换实现。它使应用程序能够
    通过提供自己的基类实现来自定义行为。

    类型安全保证:
    函数通过验证导入的类是基类的子类来确保类型安全，如果不符合继承关系
    将抛出AssertionError。

    缓存机制:
    使用@lru_cache装饰器缓存结果，避免重复导入相同的类，提高性能。

    常见用例:
    - 服务器组件 (ConversationManager, UserAuth等)
    - 存储实现 (ConversationStore, SettingsStore等)
    - 服务集成 (GitHub, GitLab, Bitbucket服务)
    - 监控和日志组件
    - 认证和授权系统

    扩展模式:
    1. 定义基类接口（抽象方法和属性）
    2. 提供默认实现
    3. 应用程序创建自定义实现（继承基类）
    4. 通过配置指定自定义实现

    示例:
        >>> # 使用默认实现
        >>> ConversationManager = get_impl(ConversationManager, None)
        >>> # 使用自定义实现
        >>> CustomManager = get_impl(ConversationManager, 'myapp.CustomConversationManager')
        >>> # 在配置中指定
        >>> server_config.conversation_manager_class = 'myapp.ClusteredConversationManager'
        >>> Manager = get_impl(ConversationManager, server_config.conversation_manager_class)
    """
    # 如果没有指定实现名称，返回基类本身
    if impl_name is None:
        return cls

    # 动态导入指定的实现类
    impl_class = import_from(impl_name)

    # 验证类型安全：确保实现类是基类的子类
    assert cls == impl_class or issubclass(impl_class, cls), (
        f'Implementation {impl_name} must be a subclass of {cls.__name__}'
    )

    return impl_class
