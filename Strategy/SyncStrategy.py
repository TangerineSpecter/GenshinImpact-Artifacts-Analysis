import decimal
import json
import os
import re

import cv2
from PySide6.QtCore import QThread, Signal

import Utils.Constant as Constant
import Utils.DataUtils as Data
from Config.OcrCoordinateConfig import entry_position_dict
from Utils.FileUtils import FileOper

unknown_list = set()
"""未知字段"""


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
            FileOper.save_json_file(f"{config_dir}/{Constant.conf_dir}", "role-data.json", role_list)
            FileOper.save_json_file(f"{config_dir}/{Constant.conf_dir}", "artifact-data.json", artifact_list)
            self.statusOut.emit("本地配置文件同步完成")

        self.analysis_artifact_data()
        self.statusOut.emit("数据同步完成")
        if unknown_list:
            self.statusOut.emit(f"存在错误识别文字：{unknown_list}")
        self.refreshOut.emit()

    def analysis_artifact_data(self):
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
                data = {'index': re.findall(r'\d+', filename)[0]}
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
                # print(json.dumps(data, ensure_ascii=False))
        dir_path = FileOper.get_dir(f"{config_dir}/{Constant.data_dir}")
        with open(f"{dir_path}/artifact_data.json", "w", encoding='utf-8') as file:
            json.dump(json_data, file, ensure_ascii=False)

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
    # 获取正则表达式
    pattern = position_info.get('pattern', None)
    # 获取映射列表
    mapper_data = Data.settings.value("mapper_table_data")
    mapper_dict = {}
    column_count = len(Data.mapper_table_heads)
    if mapper_data:
        for index in range(int(len(mapper_data) / column_count)):
            mapper_dict[mapper_data[index * column_count + 1]] = mapper_data[index * column_count]

    # 数据加工
    for entry in Data.entry_list:
        if entry in text and pattern is not None:
            pattern_result = re.search(pattern, text)
            if pattern_result is None:
                return entry
            # 处理正则数据
            attr_value = pattern_result.group(1)
            if "%" in text:
                attr_value = decimal.Decimal(pattern_result.group(1)) / decimal.Decimal(100)
            return entry, str(attr_value)

    # 替换处理
    replace = position_info.get('replace', None)
    if replace:
        text = text.replace(replace, "")

    # 上方无法匹配，则说明为无法识别词条(非套装)，采用映射方式
    mapper = position_info.get('mapper', None)
    if mapper and text not in Data.artifact_name_list:
        # 使用正则表达式去掉符号和数字
        entry = re.sub(r'[^\w\s]|\d', '', text)
        # 映射转换
        if mapper_dict.get(entry) is not None:
            entry = mapper_dict.get(entry)
            if entry in Data.entry_list:
                attr_value = re.findall(r"\+(.*)", text)[0]
                if "%" in attr_value:
                    attr_value = decimal.Decimal(attr_value.replace("%", "")) / decimal.Decimal(100)
                return entry, str(attr_value)
            elif entry in Data.artifact_name_list:
                return entry
        else:
            # 对于三词条可能会识别到无需处理的字符串，比如："(*) 件套攻击力提高", -1
            # 套装主词条目前仅用空字符串作为处理判断，所以这里设置为空
            entry = ""
            unknown_list.add(entry)
            print("未识别：", text)
            return entry
        return entry, -1

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
    # json1 = {}
    # data1 = match_text('攻击力+20%', entry_position_dict['children_tag_1'])
    # print(len(data1))
    # json1['test'] = data1
    # print(json1)
    # print(re.search("", "测试").group(1))
    ori_image = cv2.imread("../test/artifact-319.jpg")
    gray_img = cv2.cvtColor(ori_image, cv2.COLOR_BGR2GRAY)
    # adjusted_img = cv2.convertScaleAbs(gray_img, alpha=1.2, beta=30)
    # 对调整后的图像进行反色处理
    image = cv2.bitwise_not(gray_img)

    position_info = entry_position_dict["main_name"]
    img = image[position_info['left_top'][1]:position_info['right_bottom'][1],
          position_info['left_top'][0]:position_info['right_bottom'][0]]
    # cv2.imshow("title", img)
    # cv2.waitKey(0)
    from cnocr import CnOcr

    ocr = CnOcr()
    info = ocr.ocr_for_single_line(img)
    print(info)
    print("结果：", match_text(info['text'], position_info))

    # mapper_data = Data.settings.value("mapper_table_data")
    # print(mapper_data)
    # mapper_dict = {}
    # column_count = len(Data.mapper_table_heads)
    #
    # print(match_text('·攻击办+11.1%', entry_position_dict['children_tag_1']))
    # print(match_text('·测试+11.1%', entry_position_dict['children_tag_1']))

    # SyncJob().analysis_artifact_data()
