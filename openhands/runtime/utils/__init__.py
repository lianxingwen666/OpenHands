"""
OpenHands Runtime 工具函数模块
===========================

技术栈：
- 系统编程: 底层系统操作和资源管理
- 网络编程: TCP端口管理和网络工具
- 文件I/O: 高效的文件操作和处理
- 进程管理: 子进程创建和管理
- 日志系统: 结构化日志记录和流处理
- 内存管理: 内存监控和优化

功能说明：
工具模块提供Runtime系统所需的各种底层工具函数：

1. **系统工具** - 端口查找、系统信息获取
2. **文件工具** - 文件操作、编辑、查看
3. **命令工具** - Bash命令执行和管理
4. **网络工具** - HTTP请求、连接管理
5. **日志工具** - 日志捕获、流处理
6. **监控工具** - 系统资源监控
7. **构建工具** - Runtime环境构建
"""

from openhands.runtime.utils.system import (
    display_number_matrix,  # 数字矩阵显示工具（用于调试和可视化）
    find_available_tcp_port,  # 查找可用TCP端口的工具函数
)

# 模块公开接口 - 常用的系统工具函数
__all__ = ['display_number_matrix', 'find_available_tcp_port']
