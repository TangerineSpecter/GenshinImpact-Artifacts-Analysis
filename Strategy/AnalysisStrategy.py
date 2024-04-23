import time

from PySide6.QtCore import QThread, Signal


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
        # TODO 分析打印待实现
        # self.textEdit.setHtml("<span style='color: rgb(86, 177, 110);'>组件加载中...</span> ")
        self.appendOut.emit("<span style='color: rgb(86, 177, 110);'>组件加载中...</span>")

        time.sleep(1)

        # 获取文本编辑框的文本内容
        self.appendOut.emit("<span style='color: rgb(86, 177, 110);'>开始分析...</span>")
        self.appendOut.emit("<span style='color: rgb(86, 177, 110);'>开始分析...</span>")
        total_count = 30
        for count in range(total_count):
            # 计算当前数字在总数中的比例
            progress = count / total_count
            # 计算对应的count值
            index = int(progress * 30) + 1
            # 构建进度条字符串
            fill_blank = '&nbsp;' * (120 - (4 * index))
            progress_bar = f"<span style='color: rgb(114, 173, 51);'>[ {('█' * index)}{fill_blank} ]</span>" \
                           f"<span style='color: rgb(209, 89, 82);'>&nbsp;&nbsp;分析进度：{count + 1} / {total_count}</span>"
            self.replaceOut.emit(progress_bar)
            time.sleep(1)

        # text = self.textEdit.toHtml()
        # self.textEdit.append("<span style='color: rgb(86, 177, 110);'>0</span> " + text)
        # #       ━ 605.3/605.3 kB 787.7 kB/s eta 0:00:00
        # for count in range(10):
        #     time.sleep(1)
        #     existing_html = self.textEdit.toHtml()
        #     print(existing_html)
        #     # 找到现有html头部内容
        #     index = existing_html.find("<p>")
        #     new_html = f"<span style='color: rgb(86, 177, 110);'>{count}</span> " + existing_html[index:]
        #     self.textEdit.setHtml(new_html)

        # 获取最后一行的内容
        # lines = text.split("\n")
        # 替换最新一行
        # lines[0] = str(time.time())
        # 重新设置文本编辑框的内容
        # self.textEdit.setPlainText("\n".join(lines))
        # self.textEdit.setHtml("")
        self.finishOut.emit()


if __name__ == '__main__':
    # print(len('━'))
    for index in range(30):
        print("[", ('█' * index).ljust(30), "]")
