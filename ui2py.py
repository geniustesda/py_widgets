#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@Create date: 2020/10/23
@Author: tesda
"""
import os
import re
import time
import pathlib
import subprocess

ui_dir = pathlib.Path('./ui')

for ui_file in ui_dir.glob("*.ui"):
    ui_name = ui_file.name.rsplit('.')[0]
    ui_abs_path = ui_file.absolute()
    subprocess.Popen(['pyuic5', '-o', f"{ui_name}.py", f"./ui/{ui_file.name}"])

time.sleep(2)  # waite for the *py file to be generated

# Modify syntax
py_dir = pathlib.Path('.')
for _ in py_dir.glob('*window.py'):
    print(_.absolute())
    file_path = str(_.absolute())
    # os.system(f"chmod 777 {file_path}")
    with open(file_path, 'r')as fp:
        content = fp.read()
    re_con0 = re.sub(r"from PyQt5 import QtWebKitWidgets",
                     "\nfrom PyQt5.QtWebEngineWidgets import QWebEngineView", content)
    re_con = re.sub(r"QtWebKitWidgets.QWebView", "QWebEngineView", re_con0)
    with open(file_path, 'w+', encoding='utf-8')as fp:
        fp.write(re_con)

if __name__ == '__main__':
    pass
