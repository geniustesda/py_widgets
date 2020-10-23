#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@Create date: 2020/10/23
@Author: tesda
"""
from PyQt5.QtWidgets import QMainWindow, QApplication, QLineEdit
from PyQt5.QtCore import QUrl, pyqtSignal
from PyQt5 import QtGui
from browser_window import Ui_BrowserWindow


class CustomLineEdit(QLineEdit):
    def mouseMoveEvent(self, a0: QtGui.QMouseEvent) -> None:
        pass


class MainWindow(QMainWindow, Ui_BrowserWindow):
    signal_1 = pyqtSignal(str)

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("自定义浏览器")
        self.resize(1300, 800)
        self.last_url = "https://www.github.com/geniustesda"
        self.custom_ui()

    def custom_ui(self):
        self.current_url('https://leetcode-cn.com/problemset/all')
        self.pushButton.clicked.connect(self.go_address)
        self.pushButton_2.clicked.connect(lambda: self.current_url(self.last_url))
        self.lineEdit.returnPressed.connect(self.go_address)

    def current_url(self, url):
        self.webView.load(QUrl(url))
        self.lineEdit.setText(url)
        self.last_url = url

    def go_address(self):
        url = self.lineEdit.text()
        if not url.startswith('https://'):
            url = "https://" + url
        self.current_url(url)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    win = MainWindow()
    desktop = app.desktop()
    center_x = int(desktop.width() * 1 / 2 - win.width() / 2)
    center_y = int(desktop.height() * 1 / 2 - win.height() / 2)
    win.move(center_x, center_y)
    win.show()
    sys.exit(app.exec_())
