from PySide6.QtWidgets import QDialog, QVBoxLayout, QTextEdit

from Utils.FileUtils import FileOper


class SubLogWindow(QDialog):
    """
    日志记录-子窗口
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("查看日志")

        layout = QVBoxLayout()
        self.textEdit = QTextEdit()
        self.textEdit.setStyleSheet("background-color: rgb(20, 23, 40);")
        log_content = FileOper.load_log_file("app.log")
        self.textEdit.setHtml(log_content)
        self.textEdit.setFixedSize(1000, 400)
        # 设置为不可编辑
        self.textEdit.setReadOnly(True)
        layout.addWidget(self.textEdit)
        self.setLayout(layout)
        self.setModal(True)
        self.exec()
