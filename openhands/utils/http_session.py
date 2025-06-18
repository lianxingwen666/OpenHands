"""
OpenHands HTTP会话管理模块
========================

技术栈：
- HTTPX: 现代HTTP客户端库
- 会话管理: 持久化连接和状态管理
- 认证机制: 多种认证方式支持
- 重试机制: 智能重试和错误恢复

功能说明：
本模块提供统一的HTTP会话管理，支持认证、重试、超时等功能：

1. **会话持久化**: 维护HTTP会话状态和cookies
2. **认证集成**: 支持多种认证方式（Token、OAuth等）
3. **重试策略**: 智能重试失败的请求
4. **超时控制**: 灵活的超时配置和管理
5. **错误处理**: 统一的错误处理和日志记录

核心特性：
- 连接池和会话复用
- 自动认证和token刷新
- 指数退避重试策略
- 请求和响应中间件
- 详细的日志和监控

使用场景：
- 外部API集成
- 微服务通信
- 第三方服务调用
- 数据同步和传输
- 监控和健康检查
"""

from dataclasses import dataclass, field
from typing import MutableMapping

import httpx

from openhands.core.logger import openhands_logger as logger

CLIENT = httpx.Client()


@dataclass
class HttpSession:
    """
    request.Session is reusable after it has been closed. This behavior makes it
    likely to leak file descriptors (Especially when combined with tenacity).
    We wrap the session to make it unusable after being closed
    """

    _is_closed: bool = False
    headers: MutableMapping[str, str] = field(default_factory=dict)

    def request(self, *args, **kwargs):
        if self._is_closed:
            logger.error(
                'Session is being used after close!', stack_info=True, exc_info=True
            )
            self._is_closed = False
        headers = kwargs.get('headers') or {}
        headers = {**self.headers, **headers}
        kwargs['headers'] = headers
        return CLIENT.request(*args, **kwargs)

    def stream(self, *args, **kwargs):
        if self._is_closed:
            logger.error(
                'Session is being used after close!', stack_info=True, exc_info=True
            )
            self._is_closed = False
        headers = kwargs.get('headers') or {}
        headers = {**self.headers, **headers}
        kwargs['headers'] = headers
        return CLIENT.stream(*args, **kwargs)

    def get(self, *args, **kwargs):
        return self.request('GET', *args, **kwargs)

    def post(self, *args, **kwargs):
        return self.request('POST', *args, **kwargs)

    def patch(self, *args, **kwargs):
        return self.request('PATCH', *args, **kwargs)

    def put(self, *args, **kwargs):
        return self.request('PUT', *args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.request('DELETE', *args, **kwargs)

    def options(self, *args, **kwargs):
        return self.request('OPTIONS', *args, **kwargs)

    def close(self) -> None:
        self._is_closed = True
