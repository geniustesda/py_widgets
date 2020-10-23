#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@Create date: 2020/10/23
@Author: tesda
"""
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import QtCore
from browser_window import Ui_BrowserWindow


class MainWindow(QMainWindow, Ui_BrowserWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("自定义浏览器")

    def custom_ui(self):
        pass


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    win = MainWindow()
    desktop = app.desktop()
    center_x = int(desktop.width()*1/2 - win.width()/2)
    center_y = int(desktop.height()*1/2 - win.height()/2)
    win.move(center_x, center_y)
    win.show()
    sys.exit(app.exec_())
