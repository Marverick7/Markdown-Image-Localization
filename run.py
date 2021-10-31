#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

from PyQt5.QtWidgets import *

from main import main_method
from ui.MainWindow import Ui_MainWindow


class MainWindow(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.pushButton_dir.clicked.connect(self.select_dir)
        self.pushButton_file.clicked.connect(self.select_file)
        self.pushButton_clear.clicked.connect(self.clear)
        self.pushButton_run.clicked.connect(self.submit)

    def clear(self):
        self.listWidget.clear()

    def select_dir(self):
        self.listWidget.clear()
        dirPath = QFileDialog.getExistingDirectory(self, "选择文件夹")
        # print(dirPath)
        self.listWidget.addItem(dirPath)

    def select_file(self):
        self.listWidget.clear()
        filePath, fileType = QFileDialog.getOpenFileNames(self, "选择文件", "./", "*.md")
        self.listWidget.addItems(filePath)

    def submit(self):
        target_path = []
        for i in range(self.listWidget.count()):
            target_path.append(self.listWidget.item(i).text())
        flag = self.checkBox_backup.isChecked()
        if target_path:
            total, success, fail = main_method(target_path, flag)
            if success != 0:
                QMessageBox.information(self, "提示", f"共{total}个文件，处理{success}个，无需处理{fail}个", QMessageBox.Ok)
            else:
                QMessageBox.information(self, "提示", "没有需要处理的文件", QMessageBox.Ok)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
