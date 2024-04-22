import pyautogui
from PIL import ImageGrab
import Utils.DataUtils as Data
import cv2
import numpy as np
from Utils.Constant import artifact_dir

# 获取屏幕分辨率
screen_width, screen_height = pyautogui.size()


def cv(index):
    """
    识别圣遗物图片
    :param index: 圣遗物索引
    :return 是否可继续扫描，True：继续
    """
    # 装备信息，截取左上角和右下角坐标
    window_position = Data.settings.value("window_position")
    print(window_position)
    screen_region = ImageGrab.grab(bbox=(window_position['x'] + 1095,
                                         window_position['y'] + 130,
                                         window_position['x'] + 1510,
                                         window_position['y'] + 830))
    artifact_img = cv2.cvtColor(np.array(screen_region), cv2.COLOR_RGB2BGR)
    color = artifact_img[25, 330]
    # print("颜色", color)
    ## bgr颜色 金色： 50 105 188，紫色：224  86 161，蓝色：203 127  81
    if np.array_equal(color, np.array([50, 105, 188])):
        # 存储到本地数据
        config_dir = Data.settings.value("config_dir")
        cv2.imwrite(f"{config_dir}/{artifact_dir}/artifact-{index}.jpg", artifact_img)
        return True
    print("非金色")
    return False
