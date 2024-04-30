import json
import time
import traceback

from PySide6.QtCore import QThread, Signal

import Utils.DataUtils as Data
from Config.ArtifactLevelConfig import artifact_level_dict
from Moudles.GradeCalModule import cal_artifact_grade
from Utils import Constant
from Utils.FileUtils import FileOper


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
        try:
            self.appendOut.emit("<span style='color: rgb(86, 177, 110);'>组件加载中...</span>")

            time.sleep(1)

            # 获取文本编辑框的文本内容
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
        # 推荐列表
        commend_list = []
        # 潜力推荐强化
        commend_potential_list = []
        # 推荐强化
        commend_up_list = []
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
                progress_bar = f"<span style='color: rgb(114, 173, 51);'>[ {('█' * progress)}{fill_blank} ]</span>" \
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

                accord_list, equip_dict = get_accord_list(artifact_map, role_info)
                progress_bar += f"<span style='color: rgb(96, 135, 237);'>&nbsp;&nbsp;符合圣遗物数量：{len(accord_list)}</span>"
                self.replaceOut.emit(progress_bar)

                # 角色各部位评分字典 key：部位，value：[评分，索引]
                grade_dict = {}
                # 角色 100%的词条
                max_weight_entry = [key for key, value in role_info.items() if value == 100]
                # 不推荐词条
                min_weight_entry = [key for key, value in role_info.items() if value == 0]

                # 遍历筛选出的圣遗物 并打分
                for artifact_info in accord_list:
                    try:
                        level = artifact_info['level']
                        if level < 4:
                            weight_count = 0
                            # 满足两个100%权重副词条，则推荐潜力
                            for item in artifact_info['children_tag']:
                                if Data.tag_dict[item['name']] in max_weight_entry:
                                    weight_count += 1
                            if weight_count >= 2:
                                commend_potential_list.append({
                                    "index": artifact_info.get('index', 1),
                                    "role_name": role_info['role_name'],
                                    "slot": artifact_info['slot'],
                                    "grade": 0,
                                    "advice": "潜力，推荐强化",
                                    "artifact_info": artifact_info
                                })
                                continue
                        elif level < 20:
                            # 获取权重为0的词条强化level，如果合计 > 0，则跳过
                            fail_count = 0
                            for item in artifact_info['children_tag']:
                                tag_name = item['name']
                                tag_value = item['value']
                                # 小词条/无权重词条 加入计算
                                if (tag_name in ['攻击力', '防御力', '生命值'] and tag_value > 0) or \
                                        (tag_name in min_weight_entry):
                                    for level_item in artifact_level_dict[tag_name]:
                                        if level_item['min'] < tag_value < level_item['max']:
                                            fail_count += level_item['level']
                            if fail_count == 0:
                                commend_up_list.append({
                                    "index": artifact_info.get('index', 1),
                                    "role_name": role_info['role_name'],
                                    "slot": artifact_info['slot'],
                                    "grade": 0,
                                    "advice": "词条未歪，推荐强化",
                                    "artifact_info": artifact_info
                                })
                        # 满级才打分，
                        grade = cal_artifact_grade(role_info, artifact_info)
                        # 未超过自身装备，跳过
                        if grade < equip_dict.get('slot', 0.0):
                            continue
                        # 超过上一次记录
                        if grade > grade_dict.get(artifact_info['slot'][0], 0.0):
                            grade_dict[artifact_info['slot']] = [grade, artifact_info.get('index', 1), artifact_info]
                    except Exception as e:
                        traceback.print_exc()
                        print(f"圣遗物数据异常，{artifact_info}，异常信息：{e}")

                for slot, item in grade_dict.items():
                    commend_list.append({
                        "index": item[1],
                        "role_name": role_info['role_name'],
                        "slot": slot,
                        "grade": item[0],
                        "advice": "强力，更换装备",
                        "artifact_info": item[2]
                    })
                # time.sleep(2)

        self.appendOut.emit("<span style='color: rgb(86, 177, 110);'>数据分析完毕...</span>")

        # 输出分析结果
        self.appendOut.emit("<br>")
        self.appendOut.emit(
            "<span style='color: rgb(86, 177, 110);'>⋆˚｡✦⋆─────✦─────⋆✧⋆分析结果⋆✧⋆─────✦─────⋆˚｡✦⋆</span>")
        self.appendOut.emit(
            f"<span style='color: rgb(86, 177, 110);'>以下角色未配置推荐套装：</span>"
            f"<span style='color: white;'>{not_commend_roles}</span>")
        self.appendOut.emit(
            f"<span style='color: rgb(86, 177, 110);'>以下角色未配置主属性要求：</span>"
            f"<span style='color: white;'>{not_main_roles}</span>")

        # 推荐装备
        if len(commend_list) == 0:
            self.appendOut.emit(f"<span style='color: rgb(86, 177, 110);'>^_^无建议装备圣遗物，+20 可以全部清理</span>")
        for commend_info in commend_list:
            print(json.dumps(commend_info, ensure_ascii=False))
            self.appendOut.emit(
                f"<span style='color: rgb(86, 177, 110);'>建议角色：</span>"
                f"<span style='color: white;'>{commend_info['role_name'].ljust(5, ' ').replace(' ', 4 * '&nbsp;')}"
                f"&nbsp;&nbsp;|&nbsp;&nbsp;</span>"
                f"<span style='color: rgb(86, 177, 110);'>装备推荐索引：{commend_info['index']}&nbsp;&nbsp;|&nbsp;&nbsp;装备部位：</span>"
                f"<span style='color: rgb(96, 135, 237);'>{commend_info['slot']}&nbsp;&nbsp;|&nbsp;&nbsp;</span>"
                f"<span style='color: rgb(209, 89, 82);'>评分：{round(commend_info['grade'], 2)}</span>")

        # 未强化的潜力装备
        if len(commend_potential_list) == 0:
            self.appendOut.emit(f"<span style='color: rgb(86, 177, 110);'>^_^无潜力装备圣遗物，+0 可以全部清理</span>")
        for commend_info in commend_potential_list:
            self.appendOut.emit(
                f"<span style='color: rgb(86, 177, 110);'>建议角色：</span>"
                f"<span style='color: white;'>{commend_info['role_name'].ljust(5, ' ').replace(' ', 4 * '&nbsp;')}"
                f"&nbsp;&nbsp;|&nbsp;&nbsp;</span>"
                f"<span style='color: rgb(86, 177, 110);'>装备推荐索引：{commend_info['index']}&nbsp;&nbsp;|&nbsp;&nbsp;装备部位：</span>"
                f"<span style='color: rgb(96, 135, 237);'>{commend_info['slot']}&nbsp;&nbsp;|&nbsp;&nbsp;</span>"
                f"<span style='color: rgb(209, 89, 82);'>装备拥有潜力</span>")

        # 强化未满级/词条未歪
        if len(commend_up_list) == 0:
            self.appendOut.emit(f"<span style='color: rgb(86, 177, 110);'>^_^无潜力装备圣遗物，+0 可以全部清理</span>")
        for commend_info in commend_up_list:
            self.appendOut.emit(
                f"<span style='color: rgb(86, 177, 110);'>建议角色：</span>"
                f"<span style='color: white;'>{commend_info['role_name'].ljust(5, ' ').replace(' ', 4 * '&nbsp;')}"
                f"&nbsp;&nbsp;|&nbsp;&nbsp;</span>"
                f"<span style='color: rgb(86, 177, 110);'>装备推荐索引：{commend_info['index']}&nbsp;&nbsp;|&nbsp;&nbsp;装备部位：</span>"
                f"<span style='color: rgb(96, 135, 237);'>{commend_info['slot']}&nbsp;&nbsp;|&nbsp;&nbsp;</span>"
                f"<span style='color: rgb(209, 89, 82);'>装备词条未歪，推荐继续强化</span>")

        Data.settings.setValue("analysis_data", commend_list)


def get_accord_list(artifact_map, role_info):
    """
    清洗出符合推荐圣遗物数据
    :return 推荐圣遗物列表，角色已装备圣遗物字典
    """
    # 清洗出符合推荐套装的圣遗物
    accord_list = []
    # 已装备字典，key：部位，value：评分
    equip_dict = {}
    for name in role_info['commend_artifacts'].split(','):
        # 符合推荐套装 \ 符合主属性要求 \ 无人装备 \ 记录自身装备
        for artifact_info in artifact_map[name]:
            if artifact_info['equip_role'] == role_info['role_name']:
                equip_dict[artifact_info['slot']] = cal_artifact_grade(role_info, artifact_info)
                continue
            if check_main_attr(artifact_info, role_info) \
                    and len(artifact_info['equip_role']) == 0:
                accord_list.append(artifact_info)
    return accord_list, equip_dict


def check_main_attr(artifact_info, role_info):
    """
    检测圣遗物主属性是否符合要求
    :param artifact_info 圣遗物信息
    :param role_info 角色配置信息
    :return True：符合
    """
    main_attr = artifact_info['main_tag']['name']
    if artifact_info['slot'] == "理之冠":
        return main_attr == role_info['head_main']
    elif artifact_info['slot'] == "空之杯":
        return main_attr == role_info['cup_main']
    elif artifact_info['slot'] == "时之沙":
        return main_attr == role_info['sand_main']
    return True


if __name__ == '__main__':
    print(len('━'))

    print(len("测试测试"))
    print("来欧".ljust(5, '口').replace('口', '&nbsp;'))
    print(len("来欧司朗".ljust(5, '口').replace(' ', '&nbsp;')))
    # for index in range(30):
    #     print("[", ('█' * index).ljust(30), "]")
    # artifact_list = FileOper.load_config_file(f"/Users/zhouliangjun/Documents/temp/data/artifact_data.json")
    # print(len(artifact_list))
    # export_artifact_data(Data.get_excel_artifact_data(artifact_list, None))
