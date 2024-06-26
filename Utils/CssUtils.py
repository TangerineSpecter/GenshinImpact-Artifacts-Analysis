class BtnCss:

    @staticmethod
    def white(btnObj):
        """蓝色按钮样式
        :param btnObj 按钮对象
        """
        btnObj.setStyleSheet(
            """
            QPushButton {
                background-color: white;
                border: 1px solid #dcdfe6;
                color: #606266;
                padding: 5px 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #ecf5ff;
                border: 1px solid #c6e2ff;
            }
            """
        )

    @staticmethod
    def blue(btnObj):
        """蓝色按钮样式
        :param btnObj 按钮对象
        """
        btnObj.setStyleSheet(
            """
            QPushButton {
                background-color: #409EFF;
                border: 1px solid #409EFF;
                color: white;
                padding: 5px 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #66b1ff;
                border: 1px solid #66b1ff;
            }
            """
        )

    @staticmethod
    def orange(btnObj):
        """橙色按钮样式
        :param btnObj 按钮对象
        """
        btnObj.setStyleSheet(
            """
            QPushButton {
                background-color: #ff7f00;
                border: 1px solid #ff7f00;
                color: white;
                padding: 5px 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #ffa64d;
                border: 1px solid #ffa64d;
            }
            """
        )

    @staticmethod
    def red(btnObj):
        """红色按钮样式
        :param btnObj 按钮对象
        """
        btnObj.setStyleSheet(
            """
            QPushButton {
                background-color: #f56c6c;
                border: 1px solid #f56c6c;
                color: white;
                padding: 5px 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #d1616a;
                border: 1px solid #d1616a;
            }
            """
        )

    @staticmethod
    def purple(btnObj):
        """紫色按钮样式
        :param btnObj 按钮对象
        """
        btnObj.setStyleSheet(
            """
            QPushButton {
                background-color: #7d54de;
                border: 1px solid #7d54de;
                color: white;
                padding: 5px 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #A488E8;
                border: 1px solid #A488E8;
            }
            """
        )

    @staticmethod
    def green(btnObj):
        """紫色按钮样式
        :param btnObj 按钮对象
        """
        btnObj.setStyleSheet(
            """
            QPushButton {
                background-color: #279947;
                border: 1px solid #279947;
                color: white;
                padding: 5px 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2CAD50;
                border: 1px solid #2CAD50;
            }
            """
        )

    @staticmethod
    def gray(btnObj):
        """灰色按钮样式
        :param btnObj 按钮对象
        """
        btnObj.setStyleSheet(
            """
            QPushButton {
                background-color: #909399;
                border: 1px solid #909399;
                color: white;
                padding: 5px 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #c8c9cc;
                border: 1px solid #c8c9cc;
            }
            """
        )

    @staticmethod
    def light_orange(btnObj):
        """浅橙色按钮样式
        :param btnObj 按钮对象
        """
        btnObj.setStyleSheet(
            """
            QPushButton {
                background-color: #e6a23c;
                border: 1px solid #e6a23c;
                color: white;
                padding: 5px 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #f3d19e;
                border: 1px solid #f3d19e;
            }
            """
        )