from PySide6.QtCore import QThread, Signal

import Utils.Constant as Constant
import Utils.DataUtils as Data
from Utils.FileUtils import FileOper


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

        self.statusOut.emit("开始同步背包圣遗物数据")
        self.statusOut.emit("数据同步完成")
        self.refreshOut.emit()
