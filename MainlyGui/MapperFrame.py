from PySide6.QtCore import QRect, QCoreApplication
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QPushButton, QLineEdit, QLabel, QComboBox, QVBoxLayout, QDialog, QTableWidget, \
    QHeaderView, QHBoxLayout, QTableWidgetItem, QMessageBox

import Utils.DataUtils as Data
from Utils.CssUtils import BtnCss


class SubMapperWindow(QDialog):
    """
    映射配置-子窗口
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("识别映射配置")
        self.setFixedSize(300, 400)

        layout = QVBoxLayout()
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setObjectName(u"mapperTableView")
        self.tableWidget.setGeometry(QRect(180, 50, 300, 240))
        # 禁止编辑单元格
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
        # 单元格自适应
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        # 最后一列铺满
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 选中整行
        self.tableWidget.setSelectionBehavior(QTableWidget.SelectRows)
        self.tableWidget.setSelectionMode(QTableWidget.SingleSelection)
        self.tableWidget.setMouseTracking(True)
        self.tableData = Data.settings.value("mapper_table_data", None)

        # 数据
        column_count = len(Data.mapper_table_heads)
        self.tableWidget.setColumnCount(column_count)
        self.tableWidget.setHorizontalHeaderLabels(Data.mapper_table_heads)
        layout.addWidget(self.tableWidget)
        if self.tableData is not None:
            self.addTableItem(self.tableData, rowCount=(len(self.tableData) // column_count))

        # 区域
        # self.groupBox = QGroupBox(self)
        # self.groupBox.setObjectName(u"groupBox")
        # self.groupBox.setFixedHeight(50)
        # layout.addWidget(self.groupBox)

        # 按钮
        btnLayout = QHBoxLayout()
        self.addItemDialogBtn = QPushButton()
        self.addItemDialogBtn.setObjectName(u"addItemDialogBtn")
        self.addItemDialogBtn.setGeometry(QRect(15, 5, 80, 40))
        self.addItemDialogBtn.clicked.connect(lambda: self.addTableItem())
        self.addItemDialogBtn.setText(QCoreApplication.translate("MainWindow", "添加", None))
        btnLayout.addWidget(self.addItemDialogBtn)

        self.removeItemDialogBtn = QPushButton()
        self.removeItemDialogBtn.setObjectName(u"removeItemDialogBtn")
        self.removeItemDialogBtn.setGeometry(QRect(160, 5, 80, 40))
        self.removeItemDialogBtn.clicked.connect(lambda: self.removeTableItem())
        self.removeItemDialogBtn.setText(QCoreApplication.translate("MainWindow", "移除", None))
        btnLayout.addWidget(self.removeItemDialogBtn)

        BtnCss.blue(self.addItemDialogBtn)
        BtnCss.red(self.removeItemDialogBtn)

        layout.addLayout(btnLayout)
        self.setLayout(layout)
        self.setModal(True)
        self.exec()

    def addTableItem(self, data=None, rowCount=1):
        """
        添加表格数据
        :param data 数据
        :param rowCount 添加数据行数
        """
        # 无数据则弹窗填入
        if data is None:
            form_dialog = FormDialog()
            form_dialog.exec_()
            data = form_dialog.submitData

        if not data:
            # 未输入则终止后续执行
            return

        # 根据上一次行数进行计算
        start_row_count = self.tableWidget.rowCount()
        for rowIndex in range(rowCount):
            self.tableWidget.insertRow(self.tableWidget.rowCount())
            for columnIndex in range(len(Data.mapper_table_heads)):
                item = QTableWidgetItem(data[rowIndex * len(Data.mapper_table_heads) + columnIndex])
                # 设置数据居中
                item.setTextAlignment(Qt.AlignCenter)
                # 拼接到上一次行数后面
                self.tableWidget.setItem(start_row_count + rowIndex, columnIndex, item)

    def removeTableItem(self):
        """
        移除表格数据
        :return:
        """
        select_item = self.tableWidget.selectedItems()
        if not select_item:
            QMessageBox.information(self, '提示', '未选中数据', QMessageBox.Ok)
            return

        self.tableWidget.removeRow(select_item[0].row())

    def refreshTableCache(self):
        """
        刷新表格缓存数据
        """
        # 获取表格的行数和列数
        rows = self.tableWidget.rowCount()
        cols = self.tableWidget.columnCount()
        # 创建一个空列表来存储所有数据
        all_data = []

        # 遍历表格的每一行和每一列，获取单元格数据
        for row in range(rows):
            for col in range(cols):
                item = self.tableWidget.item(row, col)
                if item is None:
                    continue
                all_data.append(item.text())

        Data.settings.setValue("mapper_table_data", all_data)


class FormDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.submitData = []
        self.setWindowTitle("添加识别映射")

        layout = QVBoxLayout()

        label = QLabel("属性：")
        self.combobox = QComboBox()
        self.combobox.addItems(Data.entry_list)

        layout.addWidget(label)
        layout.addWidget(self.combobox)

        label = QLabel("映射文本：")
        self.text_input = QLineEdit()

        layout.addWidget(label)
        layout.addWidget(self.text_input)

        # 添加提交按钮
        submit_button = QPushButton("提交")
        submit_button.clicked.connect(self.submit_form)
        layout.addWidget(submit_button)

        self.setLayout(layout)

        BtnCss.blue(submit_button)

    def submit_form(self):
        selected_item = self.combobox.currentText()
        text_input_value = self.text_input.text()
        self.submitData = [selected_item, text_input_value]
        self.close()
