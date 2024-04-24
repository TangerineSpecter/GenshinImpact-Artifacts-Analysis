"""
数据处理工具类
"""
import json
import os
import re
import sys
from urllib.parse import urlparse

import pyautogui
import requests
from PySide6.QtCore import QSettings
from bs4 import BeautifulSoup

import Config.LoggingConfig as Logging
import Utils.Constant as Constant

# 创建 QSettings 对象，将 parent 参数设置为 None
settings = QSettings("TangerineSpecter", "GenshinImpact", parent=None)

# 角色数据url
ROLE_DATA_URL = "https://api-static.mihoyo.com/common/blackboard/ys_obc/v1/home/content/list?app_sn=ys_obc&channel_id=189";
ARTIFACT_DATA_URL = "https://wiki.biligame.com/ys/圣遗物一览"

# 获取屏幕分辨率
screen_width, screen_height = pyautogui.size()

# 默认点间隔
duration = 0.1


def get_resource_path(file_path):
    """
    获取
    :param file_path: 文件路径
    :return: 路径
    """
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, file_path)
    return file_path


def get_desc(pattern, text):
    """
    正则处理数据
    :param pattern 正则表达式
    :param text 需要处理的文本数据
    """
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    else:
        return None


def get_file_name_from_url(url):
    """
    提取出url中文件名部分
    """
    parsed_url = urlparse(url)
    file_name = os.path.basename(parsed_url.path)
    return file_name


def download_file_to_local(url, file_path):
    """
    下载文件到本地（使用下载文件名作为本地文件名）
    :param url 下载地址
    :param file_path 文件保存目录（只需要配置目录下的目标文件夹）
    """
    config_dir = settings.value("config_dir")
    if not config_dir:
        print("未配置本地文件目录")
        return

    if not url:
        print("下载地址不存在")
        return

    file_name = get_file_name_from_url(url)
    # 组装后目标文件路径
    target_dir = f"{config_dir}/{file_path}"
    # 本地文件路径
    local_file = f"{target_dir}/{file_name}"
    if os.path.exists(local_file):
        # print("下载文件本地已存在")
        return

    # 确保目标文件夹存在，如果不存在则创建它
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    r = requests.get(url, stream=True)
    with open(local_file, 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)


def get_role_list():
    """
    获取原神角色数据列表
    :return 角色数据
    """
    result = []
    try:
        # 发起HTTP GET请求获取JSON数据
        response = requests.get(ROLE_DATA_URL)
        jsonData = response.text

        # 解析JSON数据
        data = json.loads(jsonData)
        roleList = data["data"]["list"][0]["children"][0]["list"]
        for role in roleList:
            name = role['title']
            if "预告" in name:
                continue
            ext_json = role['ext']
            icon = role['icon']
            # 设置元素、地区、武器信息
            element = get_desc(r"\"元素/(.*?)\\\"", ext_json)
            region = get_desc(r"\"地区/(.*?)\\\"", ext_json)
            arms = get_desc(r"\"武器/(.*?)\\\"", ext_json)
            # 下载文件到本地
            download_file_to_local(icon, Constant.img_dir)

            result.append({
                "name": name,
                "element": element,
                "region": region,
                "arms": arms,
                "icon": icon
            })
    except Exception as e:
        Logging.error(f"同步角色数据异常，异常信息：{e.__cause__}")
    return result


def get_artifact_list():
    """
        获取原神圣遗物数据列表
        :return 圣遗物数据
        """
    response = requests.get(ARTIFACT_DATA_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    result = []
    try:
        for info in soup.find_all(class_="g"):
            name = info.find(class_="L").get_text()
            icon = info.find("img")['src'] if info.find("img") is not None else ""
            download_file_to_local(icon, Constant.img_dir)
            # 图标可能为空
            result.append({
                "name": name,
                "icon": icon
            })
    except Exception as e:
        Logging.error(f"同步圣遗物数据异常，异常信息：{e.__cause__}")
    return result


def get_excel_artifact_data(artifact_list):
    """
    将json数据转换为excel导出格式
    """
    result = []
    for item in artifact_list:
        data = {
            "main_name": item['main_name'],
            "children_name": item['children_name'],
            "slot": item['slot'],
            "equip_role": item['equip_role'],
            "main_tag_name": item['main_tag']['name'],
            "main_tag_value": item['main_tag']['value']
        }
        children_tags = item['children_tag']
        for index in range(len(children_tags)):
            data[f'children_tag_name_{index + 1}'] = children_tags[index]['name']
            data[f'children_tag_value_{index + 1}'] = children_tags[index]['value']
        result.append(data)
    return result
