"""
OpenHands 搜索工具模块
====================

技术栈：
- 搜索算法: 多种搜索策略和算法
- 文本索引: 高效的文本搜索和索引
- 相似度计算: 语义相似度和匹配算法
- 数据结构: 优化的搜索数据结构

功能说明：
本模块提供各种搜索功能，支持代码、文档、对话等内容的搜索：

1. **全文搜索**: 高效的全文搜索功能
2. **语义搜索**: 基于语义的智能搜索
3. **模糊匹配**: 容错的模糊搜索
4. **排序算法**: 搜索结果的智能排序
5. **过滤机制**: 多维度的搜索过滤

核心特性：
- 多种搜索算法支持
- 实时索引更新
- 相关性评分
- 搜索结果聚合
- 性能优化和缓存

使用场景：
- 代码库搜索
- 文档检索
- 对话历史搜索
- 知识库查询
- 智能推荐系统
"""

import base64
from typing import AsyncIterator, Callable


def offset_to_page_id(offset: int, has_next: bool) -> str | None:
    if not has_next:
        return None
    next_page_id = base64.b64encode(str(offset).encode()).decode()
    return next_page_id


def page_id_to_offset(page_id: str | None) -> int:
    if not page_id:
        return 0
    offset = int(base64.b64decode(page_id).decode())
    return offset


async def iterate(fn: Callable, **kwargs) -> AsyncIterator:
    """Iterate over paged result sets. Assumes that the results sets contain an array of result objects, and a next_page_id"""
    kwargs = {**kwargs}
    kwargs['page_id'] = None
    while True:
        result_set = await fn(**kwargs)
        for result in result_set.results:
            yield result
        if result_set.next_page_id is None:
            return
        kwargs['page_id'] = result_set.next_page_id
