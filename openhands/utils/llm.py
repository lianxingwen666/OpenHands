"""
OpenHands 大语言模型工具模块
==========================

技术栈：
- LLM集成: 多种大语言模型API支持
- 异步处理: 高并发的模型调用
- 提示工程: 智能提示构建和优化
- 缓存机制: 响应缓存和性能优化

功能说明：
本模块提供大语言模型的统一接口和工具函数：

1. **模型抽象**: 统一的LLM调用接口
2. **提示管理**: 提示模板和参数化
3. **响应处理**: 结果解析和格式化
4. **性能优化**: 缓存和批处理支持
5. **错误处理**: 模型调用的异常处理

核心特性：
- 多模型支持和切换
- 智能提示构建
- 流式响应处理
- 成本控制和监控
- 质量评估和优化

使用场景：
- AI代理的核心推理
- 自然语言处理任务
- 代码生成和分析
- 对话系统构建
- 智能助手功能
"""

import warnings

import httpx

with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    import litellm

from openhands.core.config import LLMConfig, OpenHandsConfig
from openhands.core.logger import openhands_logger as logger
from openhands.llm import bedrock


def get_supported_llm_models(config: OpenHandsConfig) -> list[str]:
    """Get all models supported by LiteLLM.

    This function combines models from litellm and Bedrock, removing any
    error-prone Bedrock models.

    Returns:
        list[str]: A sorted list of unique model names.
    """
    litellm_model_list = litellm.model_list + list(litellm.model_cost.keys())
    litellm_model_list_without_bedrock = bedrock.remove_error_modelId(
        litellm_model_list
    )
    # TODO: for bedrock, this is using the default config
    llm_config: LLMConfig = config.get_llm_config()
    bedrock_model_list = []
    if (
        llm_config.aws_region_name
        and llm_config.aws_access_key_id
        and llm_config.aws_secret_access_key
    ):
        bedrock_model_list = bedrock.list_foundation_models(
            llm_config.aws_region_name,
            llm_config.aws_access_key_id.get_secret_value(),
            llm_config.aws_secret_access_key.get_secret_value(),
        )
    model_list = litellm_model_list_without_bedrock + bedrock_model_list
    for llm_config in config.llms.values():
        ollama_base_url = llm_config.ollama_base_url
        if llm_config.model.startswith('ollama'):
            if not ollama_base_url:
                ollama_base_url = llm_config.base_url
        if ollama_base_url:
            ollama_url = ollama_base_url.strip('/') + '/api/tags'
            try:
                ollama_models_list = httpx.get(ollama_url, timeout=3).json()['models']  # noqa: ASYNC100
                for model in ollama_models_list:
                    model_list.append('ollama/' + model['name'])
                break
            except httpx.HTTPError as e:
                logger.error(f'Error getting OLLAMA models: {e}')

    return list(sorted(set(model_list)))
