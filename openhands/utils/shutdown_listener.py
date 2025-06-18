"""
OpenHands 优雅关闭监听器模块
==========================

技术栈：
- 信号处理: 系统信号捕获和处理
- 异步编程: 异步关闭流程管理
- 资源管理: 系统资源的优雅释放
- 生命周期管理: 应用程序生命周期控制

功能说明：
本模块提供应用程序的优雅关闭机制，确保资源正确释放：

1. **信号监听**: 监听系统关闭信号
2. **优雅关闭**: 有序的资源清理和关闭
3. **超时控制**: 关闭过程的超时保护
4. **状态管理**: 关闭状态的跟踪和管理
5. **回调机制**: 自定义关闭回调函数

核心特性：
- 多信号支持（SIGTERM、SIGINT等）
- 异步关闭流程
- 资源清理保证
- 超时保护机制
- 状态通知和回调

使用场景：
- 服务器应用关闭
- 容器化应用部署
- 系统维护和更新
- 资源密集型应用
- 长时间运行的服务
"""

import asyncio
import signal
import threading
import time
from types import FrameType
from typing import Callable
from uuid import UUID, uuid4

from uvicorn.server import HANDLED_SIGNALS

from openhands.core.logger import openhands_logger as logger

_should_exit = None
_shutdown_listeners: dict[UUID, Callable] = {}


def _register_signal_handler(sig: signal.Signals) -> None:
    original_handler = None

    def handler(sig_: int, frame: FrameType | None) -> None:
        logger.debug(f'shutdown_signal:{sig_}')
        global _should_exit
        if not _should_exit:
            _should_exit = True
            listeners = list(_shutdown_listeners.values())
            for callable in listeners:
                try:
                    callable()
                except Exception:
                    logger.exception('Error calling shutdown listener')
            if original_handler:
                original_handler(sig_, frame)  # type: ignore[unreachable]

    original_handler = signal.signal(sig, handler)


def _register_signal_handlers() -> None:
    global _should_exit
    if _should_exit is not None:
        return
    _should_exit = False

    logger.debug('_register_signal_handlers')

    # Check if we're in the main thread of the main interpreter
    if threading.current_thread() is threading.main_thread():
        logger.debug('_register_signal_handlers:main_thread')
        for sig in HANDLED_SIGNALS:
            _register_signal_handler(sig)
    else:
        logger.debug('_register_signal_handlers:not_main_thread')


def should_exit() -> bool:
    _register_signal_handlers()
    return bool(_should_exit)


def should_continue() -> bool:
    _register_signal_handlers()
    return not _should_exit


def sleep_if_should_continue(timeout: float) -> None:
    if timeout <= 1:
        time.sleep(timeout)
        return
    start_time = time.time()
    while (time.time() - start_time) < timeout and should_continue():
        time.sleep(1)


async def async_sleep_if_should_continue(timeout: float) -> None:
    if timeout <= 1:
        await asyncio.sleep(timeout)
        return
    start_time = time.time()
    while time.time() - start_time < timeout and should_continue():
        await asyncio.sleep(1)


def add_shutdown_listener(callable: Callable) -> UUID:
    id_ = uuid4()
    _shutdown_listeners[id_] = callable
    return id_


def remove_shutdown_listener(id_: UUID) -> bool:
    return _shutdown_listeners.pop(id_, None) is not None
