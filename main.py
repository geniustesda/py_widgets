#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@Create date: 2020/10/23
@Author: tesda
"""
from PyQt5.QtWidgets import QMainWindow, QApplication, QLineEdit, QWidget, QFileDialog, QMessageBox
from PyQt5.QtCore import QUrl, pyqtSignal
from PyQt5 import QtGui

from browser_window import Ui_BrowserWindow
from Qrcode_widget import Ui_Qrcode
from PageAnalyse_widget import Ui_PageAnalyse
from lxml import etree
import qrcode
import time

QR_img_name = "qr_tmp.png"


class ShowQrcodeWidget(QWidget, Ui_Qrcode):
    control_signal = pyqtSignal(str)

    def __init__(self):
        super(ShowQrcodeWidget, self).__init__()
        self.setupUi(self)
        self.control_signal.connect(lambda c: self.show_qrcode_text(c))
        self.control_signal.connect(self.qrcode_gen)
        self.QrcodeAddressText.textChanged.connect(lambda: self.qrcode_gen(self.QrcodeAddressText.text()))

    def show_qrcode_text(self, content):
        self.QrcodeAddressText.setText(content)

    def save_qrcode(self):
        img_path, _ = QFileDialog.getSaveFileName(self, 'Save qrcode', '', filter='Qrcode path(*.png)')
        if not img_path:
            return
        self.img.save(img_path)
        QMessageBox.about(self, "Info", "Success save the qrcode!")

    def qrcode_gen(self, content):
        # print(content)
        qr = qrcode.QRCode(version=5,
                           error_correction=qrcode.constants.ERROR_CORRECT_H,
                           box_size=8, border=4)
        qr.add_data(content)
        qr.make(fit=True)
        self.img = qr.make_image()
        self.img.save(QR_img_name)
        self.show_qrcode_image()

    def show_qrcode_image(self):
        pixmap_image = QtGui.QPixmap(QR_img_name)
        resize_pixmap = pixmap_image.scaled(300, 300)
        self.QrcodeShow.setPixmap(resize_pixmap)


class PageAnalyseWidget(QWidget, Ui_PageAnalyse):
    def __init__(self):
        super(PageAnalyseWidget, self).__init__()
        self.setupUi(self)


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
        self.qrcode = True
        self.custom_ui()

    def custom_ui(self):
        self.current_url('https://leetcode-cn.com/problemset/all')
        self.GoAddress.clicked.connect(self.go_address)
        self.webView.loadFinished.connect(self.load_page_finish)
        self.LastPage.clicked.connect(lambda: self.change_page("L"))
        self.NextPage.clicked.connect(lambda: self.change_page("N"))
        self.ReloadAddress.clicked.connect(self.reload_page)
        self.AddressLine.returnPressed.connect(self.go_address)
        self.QrCode.clicked.connect(self.show_qrcode)

        self.qrcode_widget = ShowQrcodeWidget()
        self.qrcode_x = int(desktop.width() / 2 + 1300 * 1 / 2)
        self.qrcode_y = int(desktop.height() / 2 - 800 / 2)
        self.qrcode_widget.move(self.qrcode_x, self.qrcode_y)

        self.page_analyse_widget = PageAnalyseWidget()
        self.page_analyse_widget.show()

    def show_qrcode(self):
        if self.qrcode:
            self.qrcode_widget.show()
        else:
            self.qrcode_widget.hide()
        self.qrcode = 1 - self.qrcode

    def moveEvent(self, a0: QtGui.QMoveEvent) -> None:
        pos = a0.pos()
        c_x = pos.x()
        c_y = pos.y()
        # if not self.qrcode_widget.isHidden():
        self.qrcode_x = c_x + 1300
        self.qrcode_y = c_y - 30
        self.qrcode_widget.move(self.qrcode_x, self.qrcode_y)
        self.page_analyse_widget.move(self.qrcode_x, self.qrcode_y+365)

    def current_url(self, url, recode=True, html_page=None):
        # if html_page:
        #     self.webView.setHtml(html_page)
        #     return
        self.webView.load(QUrl(url))
        if recode:
            self.history_list.append(url)
            self.current_index += 1

    def reload_page(self):
        # print(self.last_url)
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
        # print(self.history_list)
        url = self.webView.url().toString()
        self.last_url = url
        self.AddressLine.setText(url)
        self.webView.page().toHtml(lambda c: self.analyse_page(c))
        # self.webView.page().toPlainText(lambda x: self.analyse_page(x))
        self.qrcode_widget.control_signal.emit(self.last_url)

    def analyse_page(self, html):
        dom = etree.HTML(html)
        self.html_cache.append(html)
        http_list = [_ for _ in dom.xpath("//@href") if _.startswith('http')]
        # if http_list:
        #     print(http_list)
        #     self.current_url(http_list[0])

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        sys.exit(0)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    desktop = app.desktop()
    win = MainWindow()
    # win = ShowQrcode()
    # win = PageAnalyseWidget()
    center_x = int(desktop.width() * 1 / 2 - win.width() / 2)
    center_y = int(desktop.height() * 1 / 2 - win.height() / 2)
    win.move(center_x, center_y)
    win.show()
    sys.exit(app.exec_())
