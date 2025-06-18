"""
OpenHands 异步工具模块
===================

技术栈：
- AsyncIO: Python异步编程框架，提供事件循环和协程支持
- ThreadPoolExecutor: 线程池执行器，用于在后台线程中运行同步代码
- Concurrent.futures: 并发执行框架，提供Future对象和执行器
- Typing: 类型注解支持，提供泛型和类型检查

功能说明：
本模块提供异步编程的核心工具函数，解决同步和异步代码之间的互操作问题：

1. **同步异步转换**: 在异步上下文中调用同步函数
2. **异步同步转换**: 在同步上下文中调用异步函数
3. **并发执行**: 并行执行多个协程并收集结果
4. **超时控制**: 为异步操作提供超时机制
5. **异常处理**: 统一的异常处理和聚合机制

核心特性：
- 线程池管理和资源复用
- 事件循环的正确管理和清理
- 超时控制和取消机制
- 多异常聚合和处理
- 类型安全的异步操作
"""

import asyncio
from concurrent import futures
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Coroutine, Iterable

# 全局配置常量
GENERAL_TIMEOUT: int = 15  # 默认超时时间（秒）
EXECUTOR = ThreadPoolExecutor()  # 全局线程池执行器，用于运行同步代码


async def call_sync_from_async(fn: Callable, *args, **kwargs):
    """
    在异步上下文中调用同步函数

    参数:
        fn: 要调用的同步函数
        *args: 位置参数
        **kwargs: 关键字参数

    返回:
        函数执行结果

    功能说明:
    使用默认的后台线程池执行器运行同步函数并等待结果。
    注意：由于同步代码的特性，此函数返回的Future不可取消。

    使用场景:
    - 在异步代码中调用阻塞的I/O操作
    - 调用CPU密集型的同步计算
    - 集成第三方同步库
    """
    loop = asyncio.get_event_loop()
    # 在线程池中执行同步函数，避免阻塞事件循环
    coro = loop.run_in_executor(None, lambda: fn(*args, **kwargs))
    result = await coro
    return result


def call_async_from_sync(
    corofn: Callable, timeout: float = GENERAL_TIMEOUT, *args, **kwargs
):
    """
    在同步上下文中调用异步函数

    参数:
        corofn: 要调用的协程函数
        timeout: 超时时间（秒）
        *args: 位置参数
        **kwargs: 关键字参数

    返回:
        协程执行结果

    功能说明:
    在后台线程池中创建新的事件循环来运行协程。
    这允许在同步代码中调用异步函数，但会创建额外的线程开销。

    使用场景:
    - 在同步框架中集成异步组件
    - 测试异步代码
    - 命令行工具中调用异步API
    """
    # 参数验证
    if corofn is None:
        raise ValueError('corofn is None')
    if not asyncio.iscoroutinefunction(corofn):
        raise ValueError('corofn is not a coroutine function')

    async def arun():
        """内部异步运行函数"""
        coro = corofn(*args, **kwargs)
        result = await coro
        return result

    def run():
        """在新线程中运行事件循环"""
        loop_for_thread = asyncio.new_event_loop()
        try:
            asyncio.set_event_loop(loop_for_thread)
            return asyncio.run(arun())
        finally:
            # 确保事件循环正确关闭，避免资源泄漏
            loop_for_thread.close()

    # 检查执行器是否已关闭
    if getattr(EXECUTOR, '_shutdown', False):
        result = run()
        return result

    # 在线程池中提交任务并等待结果
    future = EXECUTOR.submit(run)
    futures.wait([future], timeout=timeout or None)
    result = future.result()
    return result


async def call_coro_in_bg_thread(
    corofn: Callable, timeout: float = GENERAL_TIMEOUT, *args, **kwargs
):
    """
    在后台线程中运行协程

    参数:
        corofn: 协程函数
        timeout: 超时时间
        *args: 位置参数
        **kwargs: 关键字参数

    功能说明:
    这是一个便捷函数，结合了call_sync_from_async和call_async_from_sync，
    用于在当前异步上下文的后台线程中运行另一个协程。

    使用场景:
    - 避免协程之间的相互阻塞
    - 并行执行独立的异步任务
    - 隔离可能出错的异步操作
    """
    await call_sync_from_async(call_async_from_sync, corofn, timeout, *args, **kwargs)


async def wait_all(
    iterable: Iterable[Coroutine], timeout: int = GENERAL_TIMEOUT
) -> list:
    """
    并行等待所有协程完成

    参数:
        iterable: 协程的可迭代对象
        timeout: 超时时间（秒）

    返回:
        按原始顺序排列的结果列表

    异常处理:
        - 如果单个任务抛出异常，直接抛出该异常
        - 如果多个任务抛出异常，抛出包含所有异常的AsyncException
        - 如果超时，取消所有待处理任务并抛出TimeoutError

    功能说明:
    为每个协程创建任务并并行执行，提供统一的异常处理和超时控制。
    这比使用asyncio.gather更灵活，因为它提供了更好的异常聚合机制。

    使用场景:
    - 并行执行多个独立的异步操作
    - 批量处理异步任务
    - 需要收集所有结果的并发操作
    """
    # 为每个协程创建任务
    tasks = [asyncio.create_task(c) for c in iterable]
    if not tasks:
        return []

    # 等待所有任务完成或超时
    _, pending = await asyncio.wait(tasks, timeout=timeout)

    # 处理超时情况
    if pending:
        # 取消所有待处理的任务
        for task in pending:
            task.cancel()
        raise asyncio.TimeoutError()

    # 收集结果和异常
    results = []
    errors = []
    for task in tasks:
        try:
            results.append(task.result())
        except Exception as e:
            errors.append(e)

    # 处理异常
    if errors:
        if len(errors) == 1:
            raise errors[0]  # 单个异常直接抛出
        raise AsyncException(errors)  # 多个异常聚合抛出

    return [task.result() for task in tasks]


class AsyncException(Exception):
    """
    异步异常聚合类

    功能说明:
    用于聚合多个异步操作中产生的异常，提供统一的异常处理机制。
    当多个并行任务都失败时，这个类可以将所有异常信息组合在一起。

    属性:
        exceptions: 异常列表，包含所有收集到的异常

    使用场景:
    - 并行任务的异常聚合
    - 批量操作的错误报告
    - 需要了解所有失败原因的场景
    """

    def __init__(self, exceptions):
        """
        初始化异步异常聚合器

        参数:
            exceptions: 异常列表
        """
        self.exceptions = exceptions
        super().__init__(
            f'Multiple async exceptions occurred: {len(exceptions)} errors'
        )

    def __str__(self):
        """
        返回所有异常的字符串表示

        返回:
            包含所有异常信息的多行字符串
        """
        return '\n'.join(str(e) for e in self.exceptions)
