"""
OpenHands 浏览器Base64图像处理工具
===============================

技术栈：
- Base64编码: 图像数据编码/解码
- PIL (Pillow): Python图像处理库
- NumPy: 数值计算和数组处理
- BytesIO: 内存中的字节流处理

功能说明：
提供图像与Base64编码之间的转换功能，用于：
1. 浏览器截图的编码传输
2. 图像数据的网络传输
3. 前端显示图像数据
4. 图像格式标准化处理
"""

import base64  # 标准库Base64编码
import io  # 输入输出流处理

import numpy as np  # 数值计算库，处理图像数组
from PIL import Image  # Python图像处理库


def image_to_png_base64_url(
    image: np.ndarray | Image.Image, add_data_prefix: bool = False
) -> str:
    """
    将图像转换为Base64编码的PNG格式URL

    参数:
        image: NumPy数组或PIL图像对象
        add_data_prefix: 是否添加data:image/png;base64,前缀

    返回:
        Base64编码的图像字符串

    功能说明:
    1. 支持NumPy数组和PIL图像的输入
    2. 自动处理RGBA/LA模式转换为RGB
    3. 生成标准PNG格式的Base64编码
    4. 可选择是否添加data URL前缀
    """
    # 如果输入是NumPy数组，转换为PIL图像
    if isinstance(image, np.ndarray):
        image = Image.fromarray(image)

    # 处理透明通道，转换为RGB模式（PNG兼容性）
    if image.mode in ('RGBA', 'LA'):
        image = image.convert('RGB')

    # 使用内存缓冲区保存PNG格式图像
    buffered = io.BytesIO()
    image.save(buffered, format='PNG')

    # 编码为Base64字符串
    image_base64 = base64.b64encode(buffered.getvalue()).decode()

    # 根据需要添加data URL前缀
    return (
        f'data:image/png;base64,{image_base64}'
        if add_data_prefix
        else f'{image_base64}'
    )


def png_base64_url_to_image(png_base64_url: str) -> Image.Image:
    """
    将Base64编码的PNG图像URL转换为PIL图像对象

    参数:
        png_base64_url: Base64编码的图像字符串（可包含data URL前缀）

    返回:
        PIL图像对象

    功能说明:
    1. 自动处理data URL前缀的移除
    2. Base64解码为二进制数据
    3. 使用PIL加载图像对象
    4. 支持标准Base64和data URL两种格式
    """
    # 分离data URL前缀和Base64数据
    splited = png_base64_url.split(',')
    if len(splited) == 2:
        base64_data = splited[1]  # 移除data:image/png;base64,前缀
    else:
        base64_data = png_base64_url  # 纯Base64数据

    # 解码Base64数据并创建PIL图像对象
    return Image.open(io.BytesIO(base64.b64decode(base64_data)))
