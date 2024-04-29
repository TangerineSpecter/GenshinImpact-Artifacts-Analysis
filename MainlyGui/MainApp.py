# -*- coding: utf-8 -*-
import json
import os
import platform

from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect, QStringListModel, Qt)
from PySide6.QtGui import (QAction, QIcon, QCursor)
from PySide6.QtWidgets import (QGridLayout, QMenu, QFileDialog, QTableWidget, QListView, QGroupBox,
                               QMenuBar, QWidget, QMessageBox, QPushButton, QTextEdit, QLabel, QVBoxLayout,
                               QTableWidgetItem, QHeaderView, QAbstractItemView, QStatusBar, QDialog, QComboBox,
                               QStyledItemDelegate, QListWidget, QListWidgetItem, QToolTip, QHBoxLayout,
                               QProgressDialog)

from Strategy.AnalysisStrategy import AnalysisJob
from Strategy.ExcelStrategy import ExportJob, AnalysisExportJob

################################################################################
## Form generated from reading UI file 'StarRail.ui'
##
## Created by: Qt User 丢失的橘子 Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

if platform.system() == 'Windows':
    from Moudles.KeyboardModule import KeyboardModule
from Strategy.MainStrategy import Strategy
from Strategy.SyncStrategy import SyncJob
from Utils.CssUtils import (BtnCss)
from Utils.FileUtils import FileOper
import Config.SystemInfo as SystemInfo
from Config.RoleWeightConfig import role_weight_dict
from Config.SlotOptionConfig import attr_dict
import Config.LoggingConfig as Logging
import Config.UpdateLog as UpdateInfo
import Utils.DataUtils as Data
import Utils.Constant as Constant

# 系统信息
systemInfo = SystemInfo.base_info


class MainApp(object):

    def __init__(self, MainWindow):
        Logging.info("启动应用程序")
        # 初始化窗体基本信息
        MainWindow.setObjectName(u"MainWindow")
        MainWindow.setFixedSize(Constant.window_width, Constant.window_height)
        MainWindow.setWindowIcon(QIcon(Data.get_resource_path(Constant.icon)))
        MainWindow.setWindowTitle(
            QCoreApplication.translate("MainWindow", f"{systemInfo['title']} v{systemInfo['version']}", None))

        # 初始化布局
        self.__initLayout(MainWindow)

        # 初始化数据
        self.__initData()

        # 初始化菜单栏
        self.__initMenubar(MainWindow)

        # 初始化按钮部分
        self.__initButton()

        # 初始化说明部分
        self.__initLabel()

        # 初始化样式
        self.__initStyle()

        # 初始化提示
        self.__init_tips()

        if platform.system() == 'Windows':
            KeyboardModule(self.worker).bind_start_game()
            KeyboardModule(self.worker).bind_position()

        QMetaObject.connectSlotsByName(MainWindow)
        print("初始化窗口完毕")

    def __initButton(self):
        """
        初始化按钮
        """
        # 打开
        self.openFileBtn = QPushButton(self.centralWidget)
        self.openFileBtn.setObjectName(u"openFileBtn")
        self.openFileBtn.setGeometry(QRect(Constant.window_width - 110, 10, 80, 40))
        self.openFileBtn.clicked.connect(self.open_file)
        self.openFileBtn.setText(QCoreApplication.translate("MainWindow", "目录", None))

        # 启动
        self.startGameBtn = QPushButton(self.centralWidget)
        self.startGameBtn.setObjectName(u"startGameBtn")
        self.startGameBtn.setGeometry(QRect(Constant.window_width - 110, 80, 80, 40))
        self.startGameBtn.clicked.connect(lambda: self.worker.start())
        self.startGameBtn.setText(QCoreApplication.translate("MainWindow", "扫描", None))

        # 分析
        self.analysisBtn = QPushButton(self.centralWidget)
        self.analysisBtn.setObjectName(u"analysisBtn")
        self.analysisBtn.setGeometry(QRect(Constant.window_width - 110, 150, 80, 40))
        self.analysisBtn.clicked.connect(show_analysis)
        self.analysisBtn.setText(QCoreApplication.translate("MainWindow", "分析", None))

        # 导出
        self.exportBtn = QPushButton(self.centralWidget)
        self.exportBtn.setObjectName(u"exportBtn")
        self.exportBtn.setGeometry(QRect(Constant.window_width - 110, 220, 80, 40))
        self.exportBtn.clicked.connect(lambda: self.exportJob.start())
        self.exportBtn.setText(QCoreApplication.translate("MainWindow", "导出", None))

        # 同步
        self.syncBtn = QPushButton(self.centralWidget)
        self.syncBtn.setObjectName(u"syncBtn")
        self.syncBtn.setGeometry(QRect(Constant.window_width - 110, 290, 80, 40))
        self.syncBtn.clicked.connect(lambda: self.__syncData())
        self.syncBtn.setText(QCoreApplication.translate("MainWindow", "同步", None))

        # 添加内容按钮
        self.addItemBtn = QPushButton(self.groupBox)
        self.addItemBtn.setObjectName(u"addItemBtn")
        self.addItemBtn.setGeometry(QRect(180, 310, 80, 40))
        self.addItemBtn.clicked.connect(self.addListViewItem)
        self.addItemBtn.setText(QCoreApplication.translate("MainWindow", "添加", None))

        # 设置内容按钮
        # self.settingItemBtn = QPushButton(self.groupBox)
        # self.settingItemBtn.setObjectName(u"settingItemBtn")
        # self.settingItemBtn.setGeometry(QRect(290, 310, 80, 40))
        # self.settingItemBtn.clicked.connect(self.settingTableItem)
        # self.settingItemBtn.setText(QCoreApplication.translate("MainWindow", "设置", None))

        # 移除内容按钮
        self.removeItemBtn = QPushButton(self.groupBox)
        self.removeItemBtn.setObjectName(u"removeItemBtn")
        self.removeItemBtn.setGeometry(QRect(290, 310, 80, 40))
        self.removeItemBtn.clicked.connect(self.removeTableItem)
        self.removeItemBtn.setText(QCoreApplication.translate("MainWindow", "移除", None))

        # 导出按钮按钮
        self.exportItemBtn = QPushButton(self.groupBox)
        self.exportItemBtn.setObjectName(u"exportItemBtn")
        self.exportItemBtn.setGeometry(QRect(400, 310, 80, 40))
        self.exportItemBtn.clicked.connect(self.exportTableData)
        self.exportItemBtn.setText(QCoreApplication.translate("MainWindow", "导出数据", None))

        # 导入按钮按钮
        self.importItemBtn = QPushButton(self.groupBox)
        self.importItemBtn.setObjectName(u"importItemBtn")
        self.importItemBtn.setGeometry(QRect(510, 310, 80, 40))
        self.importItemBtn.clicked.connect(self.importTableData)
        self.importItemBtn.setText(QCoreApplication.translate("MainWindow", "导入数据", None))

    def __syncData(self):
        QMessageBox.information(self.centralWidget, '提示', '开始同步数据，请稍等...', QMessageBox.Ok)
        self.syncJob.start()

    def __initLabel(self):
        """
        初始化说明标签
        """
        # 列表选择
        self.selectListLabel = QLabel(self.groupBox)
        self.selectListLabel.setObjectName(u"selectListLabel")
        self.selectListLabel.setGeometry(QRect(20, 25, 58, 16))
        self.selectListLabel.setText(QCoreApplication.translate("MainWindow", "角色列表", None))

        # 运行表格
        self.runListLabel = QLabel(self.groupBox)
        self.runListLabel.setObjectName(u"runListLabel")
        self.runListLabel.setGeometry(QRect(180, 25, 320, 16))
        self.runListLabel.setText(
            QCoreApplication.translate("MainWindow", "角色分析配置(词条评分计算比例以及套装要求)", None))

        # 启动快捷键
        self.runKeyboardLabel = QLabel(self.groupBox)
        self.runKeyboardLabel.setObjectName(u"runKeyboardLabel")
        self.runKeyboardLabel.setGeometry(QRect(20, 310, 158, 16))
        # self.runKeyboardLabel.setStyleSheet("color: red;")
        # self.runKeyboardLabel.setText(
        #     QCoreApplication.translate("MainWindow", f"启动快捷键：{Constant.start_keyboard}", None))

        # 停止快捷键
        self.stopKeyboardLabel = QLabel(self.groupBox)
        self.stopKeyboardLabel.setObjectName(u"stopKeyboardLabel")
        self.stopKeyboardLabel.setGeometry(QRect(20, 330, 158, 16))
        # self.stopKeyboardLabel.setStyleSheet("color: red;")
        # self.stopKeyboardLabel.setText(
        #     QCoreApplication.translate("MainWindow", f"停止快捷键：{Constant.stop_keyboard}", None))

        # 注意事项
        self.textLabel = QLabel(self.centralWidget)
        self.textLabel.setObjectName(u"textLabel")
        self.textLabel.setGeometry(QRect(20, 432, 558, 16))
        self.textLabel.setStyleSheet("color: red;")
        self.textLabel.setText(
            QCoreApplication.translate("MainWindow",
                                       f"说明：扫描圣遗物请打开到背包圣遗物界面后执行。^_^", None))
        pass

    def __initLayout(self, MainWindow):
        """
        初始化布局
        """
        self.centralWidget = QWidget(MainWindow)
        self.centralWidget.setObjectName(u"centralWidget")
        self.gridLayout = QGridLayout(self.centralWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        MainWindow.setCentralWidget(self.centralWidget)

        # 路径框
        self.gamePathText = QTextEdit(self.centralWidget)
        self.gamePathText.setObjectName(u"gamePathText")
        self.gamePathText.setGeometry(QRect(10, 10, Constant.window_width - 140, 40))
        self.gamePathText.setReadOnly(True)
        self.gamePathText.setPlaceholderText(QCoreApplication.translate("MainWindow", "游戏启动路径", None))

        # 设置部分窗体
        self.groupBox = QGroupBox(self.centralWidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(20, 70, Constant.window_width - 140, 360))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", "设置", None))

        # 状态栏
        self.statusBar = QStatusBar(self.centralWidget)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.runStatusLabel = QLabel()
        self.setStatusText("待机")
        self.statusBar.addPermanentWidget(self.runStatusLabel)

    def __initMenubar(self, MainWindow):
        """
        初始化菜单栏
        """
        # 打开
        self.openAction = QAction(MainWindow)
        self.openAction.setObjectName(u"openAction")
        self.openAction.triggered.connect(self.open_file)
        self.openAction.setText(QCoreApplication.translate("MainWindow", "打开", None))

        # 关于
        self.aboutAction = QAction(MainWindow)
        self.aboutAction.setObjectName(u"aboutAction")
        self.aboutAction.triggered.connect(show_about_dialog)
        self.aboutAction.setText(QCoreApplication.translate("MainWindow", "关于", None))

        # 更新记录
        self.updateLogAction = QAction(MainWindow)
        self.updateLogAction.setObjectName(u"updateLogAction")
        self.updateLogAction.triggered.connect(show_update_log)
        self.updateLogAction.setText(QCoreApplication.translate("MainWindow", "更新记录", None))

        # 日志
        self.logAction = QAction(MainWindow)
        self.logAction.setObjectName(u"logAction")
        self.logAction.triggered.connect(show_log)
        self.logAction.setText(QCoreApplication.translate("MainWindow", "日志", None))

        # 下拉菜单
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 269, 37))
        # 菜单栏 1
        self.menu1 = QMenu(self.menubar)
        self.menu1.setObjectName(u"menu1")
        MainWindow.setMenuBar(self.menubar)
        # 菜单栏 2
        self.menu2 = QMenu(self.menubar)
        self.menu2.setObjectName(u"menu2")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menu1.menuAction())
        self.menubar.addAction(self.menu2.menuAction())
        # 绑定下拉
        self.menu1.addAction(self.openAction)
        self.menu1.addAction(self.aboutAction)
        self.menu1.setTitle(QCoreApplication.translate("MainWindow", "文件", None))
        self.menu2.addAction(self.logAction)
        self.menu2.addAction(self.updateLogAction)
        self.menu2.setTitle(QCoreApplication.translate("MainWindow", "帮助", None))

    def __initStyle(self):
        """
        样式设置
        """
        BtnCss.blue(self.openFileBtn)
        BtnCss.blue(self.addItemBtn)
        BtnCss.orange(self.importItemBtn)
        BtnCss.green(self.exportItemBtn)
        BtnCss.red(self.removeItemBtn)
        BtnCss.blue(self.startGameBtn)
        BtnCss.purple(self.analysisBtn)
        BtnCss.green(self.exportBtn)
        BtnCss.white(self.syncBtn)
        # icon设置
        self.addItemBtn.setIcon(QIcon(Data.get_resource_path("Resource/icon/add.png")))
        # self.settingItemBtn.setIcon(QIcon(Data.get_resource_path("Resource/icon/setting.png")))
        self.removeItemBtn.setIcon(QIcon(Data.get_resource_path("Resource/icon/remove.png")))
        self.openFileBtn.setIcon(QIcon(Data.get_resource_path("Resource/icon/file.png")))
        self.analysisBtn.setIcon(QIcon(Data.get_resource_path("Resource/icon/log.png")))
        self.startGameBtn.setIcon(QIcon(Data.get_resource_path("Resource/icon/start.png")))
        self.exportBtn.setIcon(QIcon(Data.get_resource_path("Resource/icon/export.png")))
        self.syncBtn.setIcon(QIcon(Data.get_resource_path("Resource/icon/sync.png")))

    def __init_tips(self):
        """
        初始化提示
        """
        self.openFileBtn.setToolTip("选择数据存放目录")
        self.startGameBtn.setToolTip("执行背包圣遗物扫描")
        self.addItemBtn.setToolTip("添加列表需要执行的任务")
        # self.settingItemBtn.setToolTip("修改选中任务内容以及次数")
        self.removeItemBtn.setToolTip("对选中任务进行移除")
        self.analysisBtn.setToolTip("进行圣遗物推荐分析")

    def open_file(self):
        """
        打开游戏文件
        """
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.Directory)
        # file_dialog.setNameFilter("Executable Files (*.exe)")

        if file_dialog.exec():
            file_path = file_dialog.selectedFiles()[0]
            self.gamePathText.setText(file_path)
            # 保存设置
            Data.settings.setValue("config_dir", file_path)

    def addTableItem(self, data, columnCount=12, rowCount=1):
        """
        添加表格数据
        :param data: 数据
        :param columnCount: 列数
        :param rowCount: 行数
        """
        # 根据上一次行数进行计算
        start_row_count = self.tableWidget.rowCount()
        for rowIndex in range(rowCount):
            self.tableWidget.insertRow(self.tableWidget.rowCount())
            for columnIndex in range(columnCount):
                item = QTableWidgetItem(data[rowIndex * columnCount + columnIndex])
                # 设置数据居中
                item.setTextAlignment(Qt.AlignCenter)
                # 拼接到上一次行数后面
                self.tableWidget.setItem(start_row_count + rowIndex, columnIndex, item)
        self.__refreshTableCache()

    def updateTableItem(self, data, columnCount=3, rowCount=1):
        """
        更新表格数据
        :param data: 数据
        :param columnCount: 列数
        :param rowCount: 行数
        """
        for columnIndex in range(columnCount):
            item = QTableWidgetItem(str(data[columnIndex]))
            # 设置数据居中
            item.setTextAlignment(Qt.AlignCenter)
            # 拼接到上一次行数后面
            self.tableWidget.setItem(rowCount, columnIndex, item)
        self.__refreshTableCache()

    def clear_table_data(self):
        """
        清空表格数据
        """
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)
        self.__refreshTableCache()
        print("清空数据")

    def addListViewItem(self):
        """
        添加list数据到table
        :return:
        """
        select_data_list = self.listView.selectedIndexes()
        if not select_data_list:
            QMessageBox.information(self.centralWidget, '提示', '未选中数据', QMessageBox.Ok)
            return

        select_data = select_data_list[0].data()
        tableData = self.tableData
        if tableData and select_data in tableData:
            QMessageBox.information(self.centralWidget, '提示', '角色已存在', QMessageBox.Ok)
            return
        # # 初始化表格数据
        add_data = [select_data, "--", "--", "--", "--", '0', '0', '0', '0', '0', '0', '0']
        weight_data = role_weight_dict.get(select_data, None)
        if weight_data:
            add_data[5] = str(weight_data['attack'])
            add_data[6] = str(weight_data['defense'])
            add_data[7] = str(weight_data['health'])
            add_data[8] = str(weight_data['critical_rate'])
            add_data[9] = str(weight_data['critical_damage'])
            add_data[10] = str(weight_data['elemental_mastery'])
            add_data[11] = str(weight_data['energy_recharge'])
        self.addTableItem(add_data)

    def removeTableItem(self):
        """
        移除表格数据
        :return:
        """
        select_item = self.tableWidget.selectedItems()
        if not select_item:
            QMessageBox.information(self.centralWidget, '提示', '未选中数据', QMessageBox.Ok)
            return

        msgBox = QMessageBox()
        msgBox.setText('确定要移除数据吗？')
        msgBox.setWindowTitle('确认')
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        # 获取按钮对象并设置自定义文本
        yes_button = msgBox.button(QMessageBox.Yes)
        yes_button.setText('确定')
        no_button = msgBox.button(QMessageBox.No)
        no_button.setText('取消')
        reply = msgBox.exec_()
        if reply == QMessageBox.Yes:
            self.tableWidget.removeRow(select_item[0].row())
            self.__refreshTableCache()

    def exportTableData(self):
        """
        导出表格数据
        """
        folder_path = QFileDialog.getExistingDirectory(self.tableWidget, "选择文件夹", options=QFileDialog.ShowDirsOnly)

        if folder_path:
            default_filename = "genshin-impact-data.json"  # 默认文件名
            file_path = os.path.join(folder_path, default_filename)
            # 在这里可以进行保存文件的操作，例如写入数据到文件
            with open(file_path, 'w') as file:
                file.write(json.dumps(Data.table_data_2_list(self.tableData), indent=4, ensure_ascii=False))
            QMessageBox.information(self.centralWidget, '提示', '导出数据完毕', QMessageBox.Ok)

    def importTableData(self):
        """
        导入表格数据
        """
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Executable Files (*.json)")

        if file_dialog.exec():
            file_path = file_dialog.selectedFiles()[0]
            json_list_str = FileOper.load_file(file_path)
            self.clear_table_data()
            for json_data in json.loads(json_list_str):
                self.addTableItem(Data.obj_2_table_data(json_data))
            QMessageBox.information(self.centralWidget, '提示', '导入数据完毕', QMessageBox.Ok)

    def __refreshTableCache(self):
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
                    return
                all_data.append(item.text())

        Data.settings.setValue("table_data", all_data)
        self.tableData = all_data

    def setStatusText(self, text):
        self.runStatusLabel.setText(f"当前状态：{text}")

    def showMsg(self, text):
        QMessageBox.information(self.centralWidget, '提示', text, QMessageBox.Ok)
        return

    def refreshData(self):
        """
        刷新窗口数据
        """
        role_list = Data.settings.value("role_list")
        if role_list:
            model = QStringListModel()
            model.setStringList(role_list)
            self.listView.setModel(model)

    def __initData(self):
        """
        初始化面板数据部分
        """
        # 列表选项框
        self.listView = QListView(self.groupBox)
        self.listView.setObjectName(u"listView")
        self.listView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.listView.setGeometry(QRect(15, 50, 141, 240))
        role_list = Data.settings.value("role_list")
        if role_list:
            model = QStringListModel()
            model.setStringList(role_list)
            self.listView.setModel(model)

        # 执行表格
        self.tableWidget = QTableWidget(self.groupBox)
        self.tableWidget.setObjectName(u"tableView")
        self.tableWidget.setGeometry(QRect(180, 50, Constant.window_width - 340, 240))
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
        # 悬停显示
        # self.tableWidget.itemEntered.connect(self.showTableToolTip)
        # 点击显示
        self.tableWidget.cellClicked.connect(self.showTableToolTip)

        # 数据
        self.tableData = Data.settings.value("table_data", None)
        self.tableWidget.setColumnCount(len(Data.table_heads))
        self.tableWidget.setHorizontalHeaderLabels(Data.table_heads)
        # 双击编辑单元格
        self.tableWidget.setEditTriggers(QTableWidget.DoubleClicked)

        # 设置单元格下拉框
        delegate = ComboBoxDelegate()
        self.tableWidget.setItemDelegateForColumn(1, delegate)
        self.tableWidget.setItemDelegateForColumn(2, delegate)
        self.tableWidget.setItemDelegateForColumn(3, delegate)
        self.tableWidget.setItemDelegateForColumn(4, delegate)
        if self.tableData is not None:
            self.addTableItem(self.tableData, rowCount=(len(self.tableData) // len(Data.table_heads)))
        # 数据变动监听
        self.tableWidget.itemChanged.connect(self.__refreshTableCache)

        # 加载设置
        self.config_dir = Data.settings.value("config_dir", None)
        if self.config_dir is not None:
            self.gamePathText.setText(self.config_dir)

        # 线程创建
        self.worker = Strategy()
        self.worker.sinOut.connect(self.showMsg)
        # 同步任务
        self.syncJob = SyncJob()
        self.syncJob.statusOut.connect(self.setStatusText)
        self.syncJob.refreshOut.connect(self.refreshData)
        # 导出任务
        self.exportJob = ExportJob()
        self.exportJob.statusOut.connect(self.setStatusText)

    def showTableToolTip(self, item):
        if item is not None:
            # 获取鼠标当前的全局位置
            globalPos = QCursor.pos()
            # 将全局坐标转换为表格部件的本地坐标
            localPos = self.tableWidget.viewport().mapFromGlobal(globalPos)
            # 使用本地坐标获取单元格项
            itemAtPos = self.tableWidget.itemAt(localPos)
            if itemAtPos is not None:
                styledText = "<html><body style='background-color: #409EFF; color: black; font-size: 12px;'>" + itemAtPos.text() + "</body></html>"
                QToolTip.showText(globalPos, styledText)


class MultiSelectionDialog(QDialog):
    """
    套装设置选择框
    """

    def __init__(self, options, selected, parent=None):
        """
        :param options 默认选项
        :param selected 选中选项
        """
        super().__init__(parent)
        self.listWidget = QListWidget(self)
        for option in options:
            item = QListWidgetItem(option)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Checked if option in selected else Qt.Unchecked)
            self.listWidget.addItem(item)

        self.okButton = QPushButton("保存", self)
        self.okButton.clicked.connect(self.accept)

        layout = QVBoxLayout(self)
        layout.addWidget(self.listWidget)
        layout.addWidget(self.okButton)

    def selectedItems(self):
        return [self.listWidget.item(i).text() for i in range(self.listWidget.count()) if
                self.listWidget.item(i).checkState() == Qt.Checked]


class ComboBoxDelegate(QStyledItemDelegate):
    """
    初始化编辑框为下拉框
    """

    def createEditor(self, parent, option, index):
        column_index = index.column()
        # 主词条绑定
        if column_index in [2, 3, 4]:
            combo = QComboBox(parent)
            for item in attr_dict[column_index]:
                combo.addItem(item)
            return combo
        elif column_index in [1]:
            # 套装绑定
            artifact_list = Data.settings.value("artifact_list")
            if artifact_list is None:
                artifact_list = ['--']
            else:
                artifact_list = [item['name'] for item in artifact_list]
            dialog = MultiSelectionDialog(artifact_list, index.data().split(","), parent)
            if dialog.exec():
                selected_items = dialog.selectedItems()
                items_str = ",".join(selected_items)
                # 获取单元格的模型
                model = index.model()
                # 获取单元格的模型
                model.setData(index, items_str)
        return None


class AboutDialog(QMessageBox):
    def __init__(self, parent=None):
        super(AboutDialog, self).__init__(parent)
        self.setWindowTitle("关于")
        self.setText(f"版本号：{systemInfo['version']}\n"
                     f"作者：{systemInfo['author']}\n"
                     f"Bug反馈邮箱：{systemInfo['email']}")
        self.exec()


# 关于对话框
def show_about_dialog():
    AboutDialog()


def show_log():
    """
    打开日志
    """
    sub_window = SubLogWindow()
    # 设置为模态对话框
    sub_window.setModal(True)
    sub_window.exec()


def show_analysis():
    """
    打开分析界面
    """
    sub_window = SubAnalysisWindow()
    # 设置为模态对话框
    sub_window.setModal(True)
    sub_window.exec()


class SubLogWindow(QDialog):

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


class SubAnalysisWindow(QDialog):

    def __init__(self):
        super().__init__()
        self.progress_dialog = QProgressDialog(self)
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
        btnLayout.addWidget(self.exportDialogBtn)
        layout.addLayout(btnLayout)
        # 解禁按钮
        self.exportDialogBtn.setEnabled(True)
        BtnCss.blue(self.analysisDialogBtn)
        BtnCss.gray(self.exportDialogBtn)

        self.setLayout(layout)

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
            self.progress_dialog.setLabelText('开始同步数据，请稍等...')
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


def show_update_log():
    """
    更新记录
    """
    sub_window = SubUpdateWindow()
    # 设置为模态对话框
    sub_window.setModal(True)
    sub_window.exec()


class SubUpdateWindow(QDialog):
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
