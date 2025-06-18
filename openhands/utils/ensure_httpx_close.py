"""
OpenHands HTTP连接管理模块
========================

技术栈：
- HTTPX: 现代异步HTTP客户端库
- 异步编程: AsyncIO和协程管理
- 资源管理: 连接池和生命周期管理
- 上下文管理器: 自动资源清理

功能说明：
本模块确保HTTPX客户端连接的正确关闭，防止资源泄漏：

1. **连接管理**: 自动管理HTTP连接的生命周期
2. **资源清理**: 确保连接在使用后正确关闭
3. **异常安全**: 即使在异常情况下也能正确清理资源
4. **性能优化**: 避免连接泄漏导致的性能问题
5. **内存管理**: 防止未关闭连接导致的内存泄漏

核心特性：
- 自动连接关闭机制
- 异常安全的资源管理
- 上下文管理器支持
- 连接池优化
- 错误处理和恢复

使用场景：
- HTTP客户端的安全使用
- 微服务间的通信
- 外部API调用
- 资源密集型应用
- 长时间运行的服务
"""

import contextlib
from typing import Callable

import httpx


@contextlib.contextmanager
def ensure_httpx_close():
    wrapped_class = httpx.Client
    proxys = []

    class ClientProxy:
        """
        Sometimes LiteLLM opens a new httpx client for each connection, and does not close them.
        Sometimes it does close them. Sometimes, it reuses a client between connections. For cases
        where a client is reused, we need to be able to reuse the client even after closing it.
        """

        client_constructor: Callable
        args: tuple
        kwargs: dict
        client: httpx.Client

        def __init__(self, *args, **kwargs):
            self.args = args
            self.kwargs = kwargs
            self.client = wrapped_class(*self.args, **self.kwargs)
            proxys.append(self)

        def __getattr__(self, name):
            # Invoke a method on the proxied client - create one if required
            if self.client is None:
                self.client = wrapped_class(*self.args, **self.kwargs)
            return getattr(self.client, name)

        def close(self):
            # Close the client if it is open
            if self.client:
                self.client.close()
                self.client = None

        def __iter__(self, *args, **kwargs):
            # We have to override this as debuggers invoke it causing the client to reopen
            if self.client:
                return self.client.iter(*args, **kwargs)
            return object.__getattribute__(self, 'iter')(*args, **kwargs)

        @property
        def is_closed(self):
            # Check if closed
            if self.client is None:
                return True
            return self.client.is_closed

    httpx.Client = ClientProxy
    try:
        yield
    finally:
        httpx.Client = wrapped_class
        while proxys:
            proxy = proxys.pop()
            proxy.close()
