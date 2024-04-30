from PySide6.QtWidgets import QVBoxLayout, QTextEdit, QDialog

import Config.UpdateLog as UpdateInfo


class SubUpdateWindow(QDialog):
    """
    更新记录-子窗口
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("更新记录")

        layout = QVBoxLayout()
        self.textEdit = QTextEdit()
        update_log = UpdateInfo.update_log
        dialog_content = []
        for info in update_log:
            c = f"<h3 style='text-align: center;'>更新版本：{info['version']}</h3>" \
                f"<ul>"
            for text in info['content']:
                c += f"<li>{text}</li>"
            c += "</ul>"
            dialog_content.append(c)
        self.textEdit.setHtml("<br>".join(dialog_content))
        self.textEdit.setFixedSize(500, 600)
        # 设置为不可编辑
        self.textEdit.setReadOnly(True)
        layout.addWidget(self.textEdit)

        self.setLayout(layout)
        self.setModal(True)
        self.exec()
