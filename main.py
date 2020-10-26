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
from lxml import etree
import time


class MainWindow(QMainWindow, Ui_BrowserWindow):
    signal_1 = pyqtSignal(str)

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("自定义浏览器（http://www.github.com/geniustesda）")
        self.resize(1300, 800)
        self.last_url = "https://www.github.com/geniustesda"
        self.history_list = []
        self.html_cache = []
        self.current_index = 0
        self.custom_ui()

    def custom_ui(self):
        self.current_url('https://leetcode-cn.com/problemset/all')
        self.GoAddress.clicked.connect(self.go_address)
        self.webView.loadFinished.connect(self.load_page_finish)
        self.LastPage.clicked.connect(lambda: self.change_page("L"))
        self.NextPage.clicked.connect(lambda: self.change_page("N"))
        self.ReloadAddress.clicked.connect(self.reload_page)
        self.AddressLine.returnPressed.connect(self.go_address)

    def current_url(self, url, recode=True, html_page=None):
        # if html_page:
        #     self.webView.setHtml(html_page)
        #     return
        self.webView.load(QUrl(url))
        if recode:
            self.history_list.append(url)
            self.current_index += 1

    def reload_page(self):
        print(self.last_url)
        self.current_url(url=self.last_url, recode=False)

    def go_address(self):
        url = self.AddressLine.text()
        if url == self.last_url:
            return
        if not url.startswith('https://'):
            url = "https://" + url
        self.current_url(url)

    def change_page(self, action):
        if action == "L":
            self.current_index -= 1
            if self.current_index <= 0:
                self.current_index = 0
        elif action == "N":
            self.current_index += 1
            if self.current_index >= len(self.history_list):
                self.current_index = len(self.history_list) - 1
        # self.current_url(url="", html_page=self.html_cache[self.current_index],
        #                  recode=False)
        self.current_url(url=self.history_list[self.current_index],
                         recode=False)

    def load_page_finish(self):
        print(self.history_list)
        url = self.webView.url().toString()
        self.last_url = url
        self.AddressLine.setText(url)
        self.webView.page().toHtml(lambda c: self.analyse_page(c))
        # self.webView.page().toPlainText(lambda x: self.analyse_page(x))

    def analyse_page(self, html):
        dom = etree.HTML(html)
        self.html_cache.append(html)
        http_list = [_ for _ in dom.xpath("//@href") if _.startswith('http')]
        # if http_list:
        #     print(http_list)
        #     self.current_url(http_list[0])


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
