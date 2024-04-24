import time

from PySide6.QtCore import QThread, Signal

import Utils.DataUtils as Data
from Utils import Constant
from Utils.FileUtils import FileOper
from Utils.ExcelUtils import export_artifact_data


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
        except Exception as e:
            self.appendOut.emit("<span style='color: rgb(86, 177, 110);'>分析异常，终止</span>")
        self.finishOut.emit()

    def analysis_artifact_data(self):
        """
        分析圣遗物数据
        """
        config_dir = Data.settings.value("config_dir")
        dir_path = FileOper.get_dir(f"{config_dir}/{Constant.data_dir}")
        artifact_list = FileOper.load_config_file(f"{dir_path}/artifact_data.json")
        self.appendOut.emit("<span style='color: rgb(86, 177, 110);'>组件加载中...</span>")
        # 分析进度条
        total_count = len(artifact_list)
        for index in range(total_count):
            # 分析进度条 = 数字所占比例 * 50份
            progress = int(index / total_count * 50) + 1
            # 构建进度条字符串
            fill_blank = '&nbsp;' * (100 - (2 * progress))
            progress_bar = f"<span style='color: rgb(114, 173, 51);'>[ {('━' * progress)}{fill_blank} ]</span>" \
                           f"<span style='color: rgb(209, 89, 82);'>&nbsp;&nbsp;分析进度：{index + 1} / {total_count}</span>" \
                           f"<span style='color: rgb(96, 135, 237);'>&nbsp;&nbsp;当前数据：{artifact_list[index]['children_name']}</span>"
            self.replaceOut.emit(progress_bar)
            time.sleep(0.1)


if __name__ == '__main__':
    print(len('━'))
    # for index in range(30):
    #     print("[", ('█' * index).ljust(30), "]")
    artifact_list = FileOper.load_config_file(f"/Users/zhouliangjun/Documents/temp/data/artifact_data.json")
    print(len(artifact_list))
    export_artifact_data(Data.get_excel_artifact_data(artifact_list))
