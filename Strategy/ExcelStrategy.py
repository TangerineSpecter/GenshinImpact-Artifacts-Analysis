from PySide6.QtCore import QThread, Signal

import Utils.DataUtils as Data
from Utils import Constant
from Utils.ExcelUtils import export_artifact_data
from Utils.FileUtils import FileOper


class ExportJob(QThread):
    # 状态通知信号
    statusOut = Signal(str)

    def __init__(self):
        super(ExportJob, self).__init__()

    def run(self):
        """
        导出excel数据
        """
        try:
            # 处理数据
            config_dir = Data.settings.value("config_dir")
            artifact_list = FileOper.load_config_file(f"{config_dir}/{Constant.data_dir}/artifact_data.json")
            self.statusOut.emit("Excel数据导出写入中，请稍等...")
            export_artifact_data(Data.get_excel_artifact_data(artifact_list))
            self.statusOut.emit("Excel数据导出完毕")
        except Exception as e:
            self.statusOut.emit("导出数据不存在或者存在异常")
