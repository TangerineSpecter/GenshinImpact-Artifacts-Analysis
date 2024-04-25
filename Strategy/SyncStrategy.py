import os
import re

import cv2
from PySide6.QtCore import QThread, Signal

import Utils.Constant as Constant
import Utils.DataUtils as Data
from Config.OcrCoordinateConfig import entry_position_dict
from Utils.FileUtils import FileOper

entry_list = ["防御力", "暴击率", "暴击伤害", "生命值", "攻击力", "元素精通",
              "元素充能效率", "岩元素伤害加成", "水元素伤害加成", "草元素伤害加成",
              "物理元素伤害加成", "雷元素伤害加成", "火元素伤害加成", "风元素伤害加成"]
'''词条列表'''


class SyncJob(QThread):
    # 状态通知信号
    statusOut = Signal(str)
    # 刷新数据信号
    refreshOut = Signal()

    def __init__(self):
        super(SyncJob, self).__init__()
        self.ocr = None

    def run(self):
        """
        同步数据
        """
        self.statusOut.emit("角色数据同步中...")
        role_list = Data.get_role_list()
        if role_list:
            name_list = [item['name'] for item in role_list]
            Data.settings.setValue("role_list", name_list)
        self.statusOut.emit("角色数据同步完成")

        self.statusOut.emit("圣遗物数据同步中...")
        artifact_list = Data.get_artifact_list()
        if artifact_list:
            Data.settings.setValue("artifact_list", artifact_list)
        self.statusOut.emit("圣遗物数据同步完成")

        config_dir = Data.settings.value("config_dir")
        if config_dir:
            FileOper.save_file(f"{config_dir}/{Constant.conf_dir}", "role-data.json", role_list)
            FileOper.save_file(f"{config_dir}/{Constant.conf_dir}", "artifact-data.json", artifact_list)
            self.statusOut.emit("本地配置文件同步完成")

        self.analysis_artifact_data()
        self.statusOut.emit("数据同步完成")
        self.refreshOut.emit()

    def analysis_artifact_data(self):
        # TODO 数据入库
        self.statusOut.emit("准备同步背包圣遗物数据，请稍等...")
        # 图像文件夹路径
        config_dir = Data.settings.value("config_dir")
        image_folder = FileOper.get_dir(f"{config_dir}/{Constant.artifact_dir}")

        # 获取图像文件列表
        image_files = os.listdir(image_folder)
        from cnocr import CnOcr
        self.ocr = CnOcr()

        # 单个读取
        json_data = []
        total_count = len(image_files)
        for index in range(total_count):
            filename = image_files[index]
            self.statusOut.emit(f"圣遗物数据解析进度：({index + 1}/{total_count})")
            if filename.endswith(".jpg"):
                data = {}
                # 读取圣遗物图片
                image_path = os.path.join(image_folder, filename)
                ori_image = cv2.imread(image_path)
                gray_img = cv2.cvtColor(ori_image, cv2.COLOR_BGR2GRAY)
                image = cv2.bitwise_not(gray_img)

                # 根据配置字典遍历识别
                for entry in entry_position_dict.keys():
                    text = self.get_ocr_text(image, entry)
                    data[entry] = text

                # 调整数据格式后插入
                json_data.append(Data.cvdata_2_json_data(data))

    def get_ocr_text(self, image, key):
        """
        识别图片上指定坐标的文字
        :param image 识别的图片
        :param key 坐标配置key
        """
        position_info = entry_position_dict[key]
        img = image[position_info['left_top'][1]:position_info['right_bottom'][1],
              position_info['left_top'][0]:position_info['right_bottom'][0]]
        info = self.ocr.ocr_for_single_line(img)
        return match_text(info['text'], position_info)


def match_text(text, position_info):
    """
    词条文字清洗(子词条返回两个，否则返回原本清洗)
    :param text: 清洗文字
    :param position_info 坐标配置
    :return: 清洗文本/属性词条，None/属性值
    """
    pattern = position_info.get('pattern', None)

    for entry in entry_list:
        if entry in text:
            return entry, str(re.search(pattern, text).group(1))

    # 替换处理
    replace = position_info.get('replace', None)
    if replace:
        text = text.replace(replace, "")

    # 正则处理
    if pattern:
        re_result = re.search(pattern, text)
        if re_result:
            text = re_result.group(1)

    # 检测处理(无法匹配处理为空)
    check_data = position_info.get('check_data', None)
    if check_data:
        cache_list = Data.settings.value(check_data)
        for item in cache_list:
            if isinstance(item, str) and item in text:
                return item
            elif isinstance(item, dict) and item['name'] in text:
                return item['name']
        text = ""
    return text


if __name__ == '__main__':
    json = {}
    data1 = match_text('攻击力+20%', entry_position_dict['children_tag_1'])
    print(len(data1))
    json['test'] = data1
    print(json)
