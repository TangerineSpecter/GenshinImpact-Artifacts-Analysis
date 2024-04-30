from PySide6.QtWidgets import QMessageBox

from Config.SystemInfo import system_info


class AboutDialog(QMessageBox):
    """
    关于信息-子窗口
    """

    def __init__(self, parent=None):
        super(AboutDialog, self).__init__(parent)
        self.setWindowTitle("关于")
        self.setText(f"版本号：{system_info['version']}\n"
                     f"作者：{system_info['author']}\n"
                     f"Bug反馈邮箱：{system_info['email']}")
        self.exec()
