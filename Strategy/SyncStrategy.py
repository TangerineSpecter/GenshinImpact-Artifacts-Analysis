import os
import re

import cv2
from PySide6.QtCore import QThread, Signal

import Utils.Constant as Constant
import Utils.DataUtils as Data
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

        ocr = CnOcr()

        # 单个读取
        json_data = []
        total_count = len(image_files)
        # 圣遗物数据
        artifact_list = Data.settings.value("artifact_list")
        artifact_name = [item['name'] for item in artifact_list]
        for index in range(len(image_files)):
            filename = image_files[index]
            self.statusOut.emit(f"圣遗物数据解析进度：({index + 1}/{total_count})")
            if filename.endswith(".jpg"):
                data = {}
                image_path = os.path.join(image_folder, filename)
                ori_image = cv2.imread(image_path)
                gray_img = cv2.cvtColor(ori_image, cv2.COLOR_BGR2GRAY)
                image = cv2.bitwise_not(gray_img)

                # 词条1
                img = image[290:325, 20:250]
                # 词条2
                img1 = image[325:365, 20:250]
                # 词条3
                img2 = image[355:395, 20:250]
                # 词条4/套装
                img3 = image[385:425, 20:250]
                # 套装/未知
                img4 = image[425:455, 20:250]
                # 套装-子名称
                img5 = image[0:45, 20:250]
                # 部位
                img6 = image[55:85, 20:90]
                # 主属性
                img7 = image[120:150, 20:250]
                # 主属性值
                img8 = image[150:190, 20:200]
                # 装备角色
                img9 = image[660:690, 65:250]
                # 强化值
                img10 = image[250:290, 25:80]

                children_list = []
                info = ocr.ocr_for_single_line(img)
                children_data = match_text(info['text'])
                children_list.append({"name": children_data[0], "value": children_data[1]})

                info = ocr.ocr_for_single_line(img1)
                children_data = match_text(info['text'])
                children_list.append({"name": children_data[0], "value": children_data[1]})

                info = ocr.ocr_for_single_line(img2)
                children_data = match_text(info['text'])
                children_list.append({"name": children_data[0], "value": children_data[1]})

                info = ocr.ocr_for_single_line(img3)
                if match_text(info['text']):
                    data['main_name'] = info['text'].replace("：", "")
                else:
                    children_data = match_text(info['text'])
                    children_list.append({"name": children_data[0], "value": children_data[1]})
                data['children_tag'] = children_list
                info = ocr.ocr_for_single_line(img4)
                if data['main_name']:
                    text = info['text'].replace("：", "")
                    if text in artifact_name:
                        data['main_name'] = text
                info = ocr.ocr_for_single_line(img5)
                data['children_name'] = info['text']
                info = ocr.ocr_for_single_line(img6)
                data['type'] = info['text']

                main_data = {}
                info = ocr.ocr_for_single_line(img7)
                main_data['name'] = info['text']
                info = ocr.ocr_for_single_line(img8)
                main_data['value'] = info['text'].replace(",", "")
                data['main_tag'] = main_data
                info = ocr.ocr_for_single_line(img9)
                role_name = info['text'].replace("已装备", "")
                role_list = Data.settings.value("role_list")
                if role_name in role_list:
                    data['equip_role'] = role_name
                info = ocr.ocr_for_single_line(img10)
                number = int(re.search(r'(\d+(\.\d+)?)', info['text']).group(1))
                data['level'] = number
                print("数据,", data)
                json_data.append(data)


def match_text(text):
    """
    词条文字清洗
    :param text: 清洗文字
    :return: 属性词条，属性值
    """
    result1 = None
    result2 = None
    for entry in entry_list:
        if entry in text:
            result1 = entry
            result2 = float(re.search(r'(\d+(\.\d+)?)', text).group(1))
            break

    return result1, result2
