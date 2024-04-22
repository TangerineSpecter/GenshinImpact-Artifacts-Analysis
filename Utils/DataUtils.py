"""
数据处理工具类
"""

import os
import sys

import pyautogui
from PySide6.QtCore import QSettings

# 创建 QSettings 对象，将 parent 参数设置为 None
settings = QSettings("TangerineSpecter", "GenshinImpact", parent=None)

# 获取屏幕分辨率
screen_width, screen_height = pyautogui.size()

# 默认点间隔
duration = 0.1


def getResourcePath(file_path):
    """
    获取
    :param file_path: 文件路径
    :return: 路径
    """
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, file_path)
    return file_path
