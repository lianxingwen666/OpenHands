"""
OpenHands Runtime Builder 模块初始化文件
=====================================

技术栈：
- Docker API: 容器镜像构建和管理
- 构建器模式: 用于创建复杂的Runtime环境
- 抽象工厂模式: 支持多种Runtime构建策略
- 异步构建: 支持非阻塞的镜像构建过程

功能说明：
Runtime Builder模块负责：
1. 构建自定义的Runtime Docker镜像
2. 管理依赖安装和环境配置
3. 支持多种构建策略和优化
4. 提供构建过程的监控和日志
"""

from openhands.runtime.builder.base import RuntimeBuilder  # Runtime构建器基类
from openhands.runtime.builder.docker import DockerRuntimeBuilder  # Docker构建器实现

__all__ = ['RuntimeBuilder', 'DockerRuntimeBuilder']  # 模块公开接口
