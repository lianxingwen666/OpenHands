"""
OpenHands 工具函数模块
================

技术栈：
- 系统编程
- 工具函数
- 辅助功能

功能说明：
提供系统级工具函数和辅助功能
"""

import io
import logging
from contextlib import asynccontextmanager


@asynccontextmanager
async def capture_logs(logger_name, level=logging.ERROR):
    logger = logging.getLogger(logger_name)

    # Store original handlers and level
    original_handlers = logger.handlers[:]
    original_level = logger.level

    # Set up capture
    log_capture = io.StringIO()
    handler = logging.StreamHandler(log_capture)
    handler.setLevel(level)

    logger.handlers = [handler]
    logger.setLevel(level)

    try:
        yield log_capture
    finally:
        # Restore original configuration
        logger.handlers = original_handlers
        logger.setLevel(original_level)
