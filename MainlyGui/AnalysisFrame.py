from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QMessageBox, QProgressDialog, QDialog, QVBoxLayout, QTextEdit, QHBoxLayout, QPushButton

from Strategy.AnalysisStrategy import AnalysisJob
from Strategy.ExcelStrategy import AnalysisExportJob
from Utils.CssUtils import BtnCss


class SubAnalysisWindow(QDialog):
    """
    数据分析-子窗口
    """

    def __init__(self):
        super().__init__()
        self.progress_dialog = None
        self.analysisJob = None
        self.is_job_running = False
        self.setWindowTitle("圣遗物分析")

        layout = QVBoxLayout()
        self.textEdit = QTextEdit()
        self.textEdit.setStyleSheet("background-color: rgb(20, 23, 40);")
        # self.textEdit.setHtml(log_content)
        self.textEdit.setFixedSize(1000, 400)
        # 设置为不可编辑
        self.textEdit.setReadOnly(True)
        layout.addWidget(self.textEdit)

        btnLayout = QHBoxLayout()
        self.analysisDialogBtn = QPushButton()
        self.analysisDialogBtn.setObjectName(u"analysisDialogBtn")
        self.analysisDialogBtn.clicked.connect(lambda: self.analysis_data())
        self.analysisDialogBtn.setText(QCoreApplication.translate("MainWindow", "分析", None))
        btnLayout.addWidget(self.analysisDialogBtn)

        self.exportDialogBtn = QPushButton()
        self.is_export = False
        self.exportDialogBtn.setObjectName(u"exportDialogBtn")
        self.exportDialogBtn.clicked.connect(lambda: self.export_analysis_data())
        self.exportDialogBtn.setText(QCoreApplication.translate("MainWindow", "导出", None))
        self.exportDialogBtn.setEnabled(True)
        btnLayout.addWidget(self.exportDialogBtn)
        layout.addLayout(btnLayout)
        # 解禁按钮
        BtnCss.blue(self.analysisDialogBtn)
        BtnCss.gray(self.exportDialogBtn)

        self.setLayout(layout)
        # 设置为模态对话框
        self.setModal(True)
        self.exec()

    def append_text(self, text):
        self.textEdit.append(text)

    def replace_text(self, new_line):
        # 获取当前HTML内容
        html_content = self.textEdit.toHtml()

        # 分割HTML内容为行
        lines = html_content.split('</p>')

        # 替换最后一行内容
        lines[-2] = new_line

        # 重新设置HTML内容
        new_html_content = '</p>'.join(lines)
        self.textEdit.setHtml(new_html_content)

    def analysis_data(self):
        if self.is_job_running:
            QMessageBox.information(self, '提示', '分析任务执行中，请勿重复执行任务', QMessageBox.Ok)
            return
        # 执行前，清空上一次的记录
        self.textEdit.clear()
        self.analysisJob = AnalysisJob()
        self.analysisJob.appendOut.connect(self.append_text)
        self.analysisJob.replaceOut.connect(self.replace_text)
        self.analysisJob.finishOut.connect(self.job_finish)
        self.analysisJob.start()
        self.is_job_running = True

    def job_finish(self):
        print("任务结束")
        self.is_job_running = False
        self.is_export = True
        BtnCss.green(self.exportDialogBtn)

    def export_analysis_data(self):
        """
        导出分析结果
        """
        if self.is_export:
            self.analysisJob = AnalysisExportJob()
            self.analysisJob.finishOut.connect(lambda: self.export_job_finish())
            self.analysisJob.start()
            # loading框
            self.progress_dialog = QProgressDialog(self)
            self.progress_dialog.setLabelText('开始导出数据，请稍等...')
            self.progress_dialog.setRange(0, 0)  # 设置为无限进度条（即不确定进度）
            self.progress_dialog.setModal(True)  # 设置为模态对话框，阻塞用户输入
            self.progress_dialog.setCancelButton(None)
            self.progress_dialog.exec()
            print("导出分析数据")
            return

    def export_job_finish(self):
        """
        导出任务结束
        """
        self.progress_dialog.close()
        QMessageBox.information(self, '提示', '数据导出完毕', QMessageBox.Ok)
