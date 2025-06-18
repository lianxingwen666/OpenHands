"""
OpenHands Runtime 构建器基类
==========================

技术栈：
- 构建器模式: 复杂对象的分步构建
- 抽象工厂模式: 支持多种构建策略
- Docker API: 容器镜像构建
- 异步构建: 非阻塞的构建过程

功能说明：
Runtime构建器基类定义了构建接口：
1. 镜像构建的抽象流程
2. 依赖安装和环境配置
3. 构建过程的监控和日志
4. 错误处理和回滚机制
"""

import abc


class RuntimeBuilder(abc.ABC):
    @abc.abstractmethod
    def build(
        self,
        path: str,
        tags: list[str],
        platform: str | None = None,
        extra_build_args: list[str] | None = None,
    ) -> str:
        """Build the runtime image.

        Args:
            path (str): The path to the runtime image's build directory.
            tags (list[str]): The tags to apply to the runtime image (e.g., ["repo:my-repo", "sha:my-sha"]).
            platform (str, optional): The target platform for the build. Defaults to None.
            extra_build_args (list[str], optional): Additional build arguments to pass to the builder. Defaults to None.

        Returns:
            str: The name:tag of the runtime image after build (e.g., "repo:sha").
                This can be different from the tags input if the builder chooses to mutate the tags (e.g., adding a
                registry prefix). This should be used for subsequent use (e.g., `docker run`).

        Raises:
            AgentRuntimeBuildError: If the build failed.
        """
        pass

    @abc.abstractmethod
    def image_exists(self, image_name: str, pull_from_repo: bool = True) -> bool:
        """Check if the runtime image exists.

        Args:
            image_name (str): The name of the runtime image (e.g., "repo:sha").
            pull_from_repo (bool): Whether to pull from the remote repo if the image not present locally

        Returns:
            bool: Whether the runtime image exists.
        """
        pass
