import time

from PySide6.QtCore import QThread, Signal

import Utils.DataUtils as Data
from Utils import Constant
from Utils.FileUtils import FileOper


def check_main_attr(artifact_info, role_table_data):
    """
    检测圣遗物主属性是否符合要求
    :param artifact_info 圣遗物信息
    :param role_table_data 角色配置信息
    :return True：符合
    """
    main_attr = artifact_info['main_tag']['name']
    if artifact_info['slot'] == "理之冠":
        return main_attr == role_table_data['head_main']
    elif artifact_info['slot'] == "空之杯":
        return main_attr == role_table_data['cup_main']
    elif artifact_info['slot'] == "时之沙":
        return main_attr == role_table_data['sand_main']
    return True


class AnalysisJob(QThread):
    # 追加内容信号
    appendOut = Signal(str)
    # 替换内容信号
    replaceOut = Signal(str)
    # 结束信号
    finishOut = Signal()

    def __init__(self):
        super(AnalysisJob, self).__init__()

    def run(self):
        """
        分析数据
        """
        # TODO 分析打印待实现  ━ 605.3/605.3 kB 787.7 kB/s eta 0:00:00
        try:
            self.appendOut.emit("<span style='color: rgb(86, 177, 110);'>组件加载中...</span>")

            time.sleep(1)

            # 获取文本编辑框的文本内容
            self.appendOut.emit("<span style='color: rgb(86, 177, 110);'>开始分析...</span>")
            self.appendOut.emit("<span style='color: rgb(86, 177, 110);'>开始分析...</span>")

            self.analysis_artifact_data()
            self.appendOut.emit("<span style='color: rgb(86, 177, 110);'>分析完毕...</span>")
        except Exception as e:
            print(e)
            self.appendOut.emit("<span style='color: rgb(86, 177, 110);'>分析异常，终止</span>")
        self.finishOut.emit()

    def analysis_artifact_data(self):
        """
        分析圣遗物数据
        """
        # 初始化参数
        not_commend_roles = []  # 未配置推荐套装
        not_main_roles = []  # 未配置主属性要求

        config_dir = Data.settings.value("config_dir")
        # 圣遗物数据
        dir_path = FileOper.get_dir(f"{config_dir}/{Constant.data_dir}")
        artifact_list = FileOper.load_config_file(f"{dir_path}/artifact_data.json")
        self.appendOut.emit(
            f"<span style='color: rgb(86, 177, 110);'>加载背包圣遗物数据，数量：[ {len(artifact_list)} ]</span>")
        # 角色数据
        tableData = Data.settings.value("table_data", None)
        self.appendOut.emit(
            f"<span style='color: rgb(86, 177, 110);'>加载分析角色数据，数量：[ {int(len(tableData) / 12)} ]</span>")

        # 分析进度条
        total_count = int(len(tableData) / len(Data.table_heads))
        if total_count > 0:
            self.appendOut.emit("<span style='color: rgb(86, 177, 110);'>开始分析数据...</span>")

            # 判断是否有本地圣遗物数据
            if len(artifact_list) <= 0:
                self.appendOut.emit("<span style='color: rgb(86, 177, 110);'>无圣遗物数据，终止分析...</span>")
                return

            # 转换数据
            artifact_map = {}
            for item in artifact_list:
                key = item["main_name"]
                if key in artifact_map:
                    artifact_map[key].append(item)
                else:
                    artifact_map[key] = [item]

            for index in range(total_count):
                role_info = Data.table_data_2_obj(index, tableData)
                # 分析进度条 = 数字所占比例 * 20份
                progress = int((index + 1) / total_count * 20)
                # 构建进度条字符串
                fill_blank = '口' * (20 - progress)
                # progress_bar = f"<span style='color: rgb(114, 173, 51);'>[ {('━' * progress)}{fill_blank} ]</span>" \
                #                f"<span style='color: rgb(209, 89, 82);'>&nbsp;&nbsp;分析进度：{index + 1} / {total_count}</span>" \
                #                f"<span style='color: rgb(96, 135, 237);'>&nbsp;&nbsp;当前分析角色：{artifact_list[index]['main_name']} - {artifact_list[index]['children_name']}</span>"
                progress_bar = f"<span style='font-family: MiSans;color: rgb(114, 173, 51);'>[ {('█' * progress)}{fill_blank} ]</span>" \
                               f"<span style='color: rgb(209, 89, 82);'>&nbsp;&nbsp;分析进度：{index + 1} / {total_count}</span>" \
                               f"<span style='color: rgb(96, 135, 237);'>&nbsp;&nbsp;当前分析角色：{role_info['role_name']}</span>"
                self.replaceOut.emit(progress_bar)
                # 未设置推荐
                if len(role_info['commend_artifacts']) <= 0:
                    not_commend_roles.append(role_info['role_name'])
                    continue
                # 未设置属性要求
                if len(role_info['head_main']) <= 0 \
                        or len(role_info['cup_main']) <= 0 \
                        or len(role_info['sand_main']) <= 0:
                    not_main_roles.append(role_info['role_name'])
                    continue

                # TODO 按照推荐套装计算评分\计算主属性\跟当前装备套装比对
                # 清洗出符合推荐套装的圣遗物
                accord_list = []
                for name in role_info['commend_artifacts'].split(','):
                    # 符合推荐套装的圣遗物列表
                    commend_list = artifact_map[name]
                    # 主属性清洗
                    for artifact_info in commend_list:
                        if check_main_attr(artifact_info, role_info):
                            accord_list.append(artifact_info)
                progress_bar += f"<span style='color: rgb(96, 135, 237);'>&nbsp;&nbsp;符合圣遗物数量：{len(accord_list)}</span>"
                self.replaceOut.emit(progress_bar)
                # print(json.dumps(accord_list, ensure_ascii=False))
                time.sleep(0.1)

        self.appendOut.emit("<span style='color: rgb(86, 177, 110);'>数据分析完毕...</span>")

        # 输出分析结果
        self.appendOut.emit("<br>")
        self.appendOut.emit("<span style='color: rgb(86, 177, 110);'>=================分析结果=================</span>")
        self.appendOut.emit(
            f"<span style='color: rgb(86, 177, 110);'>以下角色未配置推荐套装：{not_commend_roles}</span>")
        self.appendOut.emit(
            f"<span style='color: rgb(86, 177, 110);'>以下角色未配置主属性要求：{not_main_roles}</span>")


if __name__ == '__main__':
    print(len('━'))
    # for index in range(30):
    #     print("[", ('█' * index).ljust(30), "]")
    # artifact_list = FileOper.load_config_file(f"/Users/zhouliangjun/Documents/temp/data/artifact_data.json")
    # print(len(artifact_list))
    # export_artifact_data(Data.get_excel_artifact_data(artifact_list, None))
