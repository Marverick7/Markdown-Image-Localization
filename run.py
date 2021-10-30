#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

from PyQt5.QtWidgets import *

from main import main_method
from ui.MainWindow import Ui_MainWindow
from ui.MessageBox import Ui_Dialog


class MsgWindow(Ui_Dialog, QDialog):
    def __init__(self):
        super(MsgWindow, self).__init__()
        self.setupUi(self)
        self.pushButton_ok.clicked.connect(self.close)
        self.pushButton_close.clicked.connect(self.close)
        self.pushButton_open_dir.clicked.connect(mainWindow.open_dir)


class MainWindow(Ui_MainWindow, QMainWindow):
    target_path = ""

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.toolButton_dir.clicked.connect(self.select_dir)
        self.toolButton_single_file.clicked.connect(self.select_single_file)
        self.pushButton.clicked.connect(self.submit)

    def select_dir(self):
        dirPath = QFileDialog.getExistingDirectory(self, "选择文件夹")
        # print(dirPath)
        self.comboBox.clear()
        self.comboBox.addItem(dirPath)

    def select_single_file(self):
        filePath, fileType = QFileDialog.getOpenFileName(self, "选择文件", "./", "*.md")
        self.comboBox.clear()
        self.comboBox.addItem(filePath)
        # print(filePath)

    def submit(self):
        self.target_path = self.comboBox.currentText()
        if self.target_path:
            # print(target_path)
            if main_method(self.target_path):
                msgWindow.label.setText("成功！")
                msgWindow.pushButton_close.hide()
                msgWindow.pushButton_open_dir.show()
            else:
                msgWindow.label.setText("失败！")
                msgWindow.pushButton_open_dir.hide()
                msgWindow.pushButton_close.show()
            msgWindow.show()

    def open_dir(self):
        dirPath = self.target_path.replace("/", "\\")
        os.system(f"explorer.exe {dirPath}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    msgWindow = MsgWindow()
    mainWindow.show()
    sys.exit(app.exec_())