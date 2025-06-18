"""
OpenHands 浏览器模块初始化文件
============================

技术栈：
- Playwright: 现代浏览器自动化框架
- Selenium: 备用浏览器驱动（兼容性支持）
- Base64编码: 图像和文件处理
- 异步编程: 支持高性能浏览器操作

功能说明：
浏览器模块提供Web自动化功能，包括：
1. 网页浏览和交互
2. 截图和页面内容提取
3. 表单填写和点击操作
4. JavaScript执行和DOM操作
"""

from openhands.runtime.browser.utils import browse  # 主要的浏览器操作函数

__all__ = ['browse']  # 模块公开接口
