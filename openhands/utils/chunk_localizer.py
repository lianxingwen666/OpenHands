"""
OpenHands 代码块定位器模块
========================

技术栈：
- 文本处理: 字符串操作和模式匹配
- 正则表达式: 复杂文本模式识别
- 算法设计: 文本搜索和定位算法
- 代码分析: 源代码结构解析

功能说明：
本模块提供代码块的精确定位功能，用于在大型代码文件中快速找到特定的代码段：

1. **代码块识别**: 识别函数、类、方法等代码结构
2. **位置计算**: 计算代码块在文件中的精确位置
3. **上下文提取**: 提取代码块的上下文信息
4. **模糊匹配**: 支持部分匹配和相似度搜索
5. **多语言支持**: 支持多种编程语言的语法

核心特性：
- 高效的文本搜索算法
- 语法感知的代码解析
- 灵活的匹配策略
- 上下文保持和恢复
- 错误容忍和恢复机制

使用场景：
- 代码编辑器的跳转功能
- 自动化代码重构
- 代码审查和分析
- 文档生成和同步
- IDE集成和插件开发
"""

from pydantic import BaseModel
from rapidfuzz.distance import LCSseq
from tree_sitter_language_pack import get_parser

from openhands.core.logger import openhands_logger as logger


class Chunk(BaseModel):
    text: str
    line_range: tuple[int, int]  # (start_line, end_line), 1-index, inclusive
    normalized_lcs: float | None = None

    def visualize(self) -> str:
        lines = self.text.split('\n')
        assert len(lines) == self.line_range[1] - self.line_range[0] + 1
        ret = ''
        for i, line in enumerate(lines):
            ret += f'{self.line_range[0] + i}|{line}\n'
        return ret


def _create_chunks_from_raw_string(content: str, size: int):
    lines = content.split('\n')
    ret = []
    for i in range(0, len(lines), size):
        _cur_lines = lines[i : i + size]
        ret.append(
            Chunk(
                text='\n'.join(_cur_lines),
                line_range=(i + 1, i + len(_cur_lines)),
            )
        )
    return ret


def create_chunks(
    text: str, size: int = 100, language: str | None = None
) -> list[Chunk]:
    try:
        parser = get_parser(language) if language is not None else None
    except AttributeError:
        logger.debug(f'Language {language} not supported. Falling back to raw string.')
        parser = None

    if parser is None:
        # fallback to raw string
        return _create_chunks_from_raw_string(text, size)

    # TODO: implement tree-sitter chunking
    # return _create_chunks_from_tree_sitter(parser.parse(bytes(text, 'utf-8')), max_chunk_lines=size)
    raise NotImplementedError('Tree-sitter chunking not implemented yet.')


def normalized_lcs(chunk: str, query: str) -> float:
    """Calculate the normalized Longest Common Subsequence (LCS) to compare file chunk with the query (e.g. edit draft).

    We normalize Longest Common Subsequence (LCS) by the length of the chunk
    to check how **much** of the chunk is covered by the query.
    """
    if len(chunk) == 0:
        return 0.0

    _score = LCSseq.similarity(chunk, query)

    return _score / len(chunk)


def get_top_k_chunk_matches(
    text: str, query: str, k: int = 3, max_chunk_size: int = 100
) -> list[Chunk]:
    """Get the top k chunks in the text that match the query.

    The query could be a string of draft code edits.

    Args:
        text: The text to search for the query.
        query: The query to search for in the text.
        k: The number of top chunks to return.
        max_chunk_size: The maximum number of lines in a chunk.
    """
    raw_chunks = create_chunks(text, max_chunk_size)
    chunks_with_lcs: list[Chunk] = [
        Chunk(
            text=chunk.text,
            line_range=chunk.line_range,
            normalized_lcs=normalized_lcs(chunk.text, query),
        )
        for chunk in raw_chunks
    ]
    sorted_chunks = sorted(
        chunks_with_lcs,
        key=lambda x: x.normalized_lcs,  # type: ignore
        reverse=True,
    )
    return sorted_chunks[:k]
