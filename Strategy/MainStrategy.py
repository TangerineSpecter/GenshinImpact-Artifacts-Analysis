import os
import time

import psutil
import pyautogui
from PySide6.QtCore import QThread, Signal

import Config.LoggingConfig as Logging
import Utils.Constant as Constant
import Utils.DataUtils as Data
import platform

if platform.system() == 'Windows':
    import win32gui
    import win32process
import Utils.ImageUtils as ImageUtils


class Strategy(QThread):
    sinOut = Signal(str)
    statusOut = Signal(str)

    def __init__(self):
        super(Strategy, self).__init__()
        # 执行行数，每次主策略调度初始化
        self.row_index = 0
        self.tableData = []
        self.config_dir = None

    def run(self):
        self.__init_data()
        self.run_game()

    def __init_data(self):
        """
        重载数据，避免线程初始化之后数据未刷新
        """
        # 重置
        self.tableData.clear()
        self.config_dir = Data.settings.value("config_dir", None)
        data = Data.settings.value("table_data", None)
        # for i in range(0, len(data), 3):
        #     obj = {
        #         "main_name": data[i],
        #         "process_name": data[i + 1],
        #         "count": data[i + 2]
        #     }
        #     self.tableData.append(obj)

    def stop(self):
        Logging.warn("终止脚本运行")
        self.statusOut.emit("手动停止脚本")
        self.terminate()

    def run_game(self):
        try:
            self.statusOut.emit("开始检测游戏运行状态")
            Logging.info("开始检测游戏运行状态")
            if check_process_exists():
                Logging.info("游戏已运行，执行下一步")
                self.__init_window()
            else:
                self.sinOut.emit("游戏未运行")
                self.statusOut.emit("脚本运行结束")
                Logging.info("游戏未运行，终止")
                return
        except Exception as e:
            Logging.error(f"脚本运行异常，异常信息：{e}")

        Logging.info("脚本运行结束")
        self.sinOut.emit("脚本运行结束")
        self.statusOut.emit("脚本运行结束")

    def __run_table_data(self):
        """
        执行表格数据
        """
        for index in range(len(self.tableData)):
            # 设置当前读取列索引
            Logging.info(f"开始执行第{index}行数据")
            self.row_index = index
            self.__init_window()

    def __init_window(self):
        """
        初始化界面
        :return:
        """
        # 获取目标进程的窗口句柄
        hwnd = win32gui.FindWindow(None, "原神")

        # 获取窗口所属的进程ID
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        print("进程ID", pid)

        # 如果当前活动窗口非目标串钩，将进程窗口切换到前台
        if win32gui.GetForegroundWindow() != hwnd:
            win32gui.SetForegroundWindow(hwnd)
            left, top, right, bottom = win32gui.GetWindowRect(hwnd)
            window_position = {
                "x": left,
                "y": top,
                "w": right - left,
                "h": bottom - top
            }
            Data.settings.setValue("window_position", window_position)
            print("窗口位置：左边距：{}，上边距：{}，宽度：{}，高度：{}".format(left, top, right - left, bottom - top))
        # 检测是否设置目录以及文件夹创建
        config_dir = Data.settings.value("config_dir")
        if config_dir is None:
            self.sinOut.emit("未设置数据目录")
            return

        folder_path = f"{config_dir}/{Constant.artifact_dir}"
        # 确保目标文件夹存在，如果不存在则创建它
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # 开始识别
        start = time.time()
        total_count = 0
        # 一页40个，按照最大50页执行扫描
        for page in range(50):
            # 5行
            for rowIndex in range(5):
                imgIndex = (page * 40) + rowIndex * 8 + 1
                # print(imgIndex)
                pyautogui.moveTo((left, top), duration=0.1)
                pyautogui.moveRel((150, (rowIndex + 1) * 140 + 90), duration=0.1)
                pyautogui.click()
                # 截取屏幕特定区域
                result = ImageUtils.cv(imgIndex)
                if not result:
                    return
                total_count = imgIndex
                # 平移7次
                for index in range(1, 8):
                    itemIndex = imgIndex + index
                    # print(itemIndex)

                    pyautogui.moveRel((120, 0), duration=0.1)
                    pyautogui.click()
                    result = ImageUtils.cv(itemIndex)
                    if not result:
                        return
                    total_count = itemIndex
            # 拖动到下一页
            pyautogui.moveTo((left + 1000, top + 770), duration=0.1)
            pyautogui.mouseDown(button='left')
            pyautogui.moveRel(0, -811, duration=0.5)
            # 等待一下 避免拖动惯性
            time.sleep(0.5)
            pyautogui.mouseUp(button='left')
        print(f"执行完毕，扫描总数：{total_count}，耗时：{time.time() - start}")

        # 策略分发
        # dis = DistributeStrategy()
        # context = Context(dis, self.statusOut)
        # result = context.execute_strategy(self.tableData[self.row_index])

        # if not result:
        #     Logging.error("策略执行失败，跳过此次执行")
        #     return


def check_process_exists():
    """
    检测进程是否存在
    :return: True:存在
    """
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == Constant.app_name:
            return True
    return False
