#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# FileName: 2ndSense.py
# Development starting date: 2016.10.20

# Developer: Peter. w (peter.w@droidtown.co)

# This Software/Scipt is protected by copyright and other
# intellectual property laws and treaties.
# Droidtown Linguistic Technology Co., Ltd. owns the copyright,
# and other intellectual property rights in the Software/Script.
# 卓騰語言科技有限公司 版權所有
# Copyright 2016 Droidtown Ling. Tech. Co., Ltd
# All Rights Reserved.

import os
import sys

from PySide import QtCore
from PySide import QtGui

from urllib.parse import urlparse

class TableWidgetItem(QtGui.QTableWidgetItem):
    '''
    在原始 QTableWidgetItem 類別下, 新增表格 item 用來排序的數值型態。
    '''
    def __init__(self, text, sortKey):
        QtGui.QTableWidgetItem.__init__(self, text, QtGui.QTableWidgetItem.UserType)
        self.sortKey = sortKey

    #Qt uses a simple < check for sorting items, override this to use the sortKey
    def __lt__(self, other):
        return self.sortKey < other.sortKey



class DropZoneLabel(QtGui.QLabel):
    def __init__(self):
        super(DropZoneLabel, self).__init__()

        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
        print("dragging enter")
        if e.mimeData().hasUrls:
            e.accept()
        else:
            e.ignore()
        #if e.mimeData().hasFormat('text/plain'):
            #e.accept()
        #else:
            #e.ignore()

    def dropEvent(self, e):
        print("dropping at", e.mimeData())
        if e.mimeData().hasUrls:
            fileLIST = []
            for url in e.mimeData().urls():
                path = url.toLocalFile()
                if os.path.isfile(path):
                    fileLIST.append(path)
            print(fileLIST)
            return fileLIST
        else:
            return None

class FileListTable(QtGui.QTableWidget):
    def __init__(self):
        super(FileListTable, self).__init__()
        self.fileLIST = []
        self.setAcceptDrops(True)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setVisible(False)

    def dragEnterEvent(self, e):
        print("fileLIST dragging enter")
        if e.mimeData().hasUrls:
            e.accept()
        else:
            e.ignore()
        #if e.mimeData().hasFormat('text/plain'):
            #e.accept()
        #else:
            #e.ignore()

    def dragMoveEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        print("fileLIST dropping at", e.mimeData())
        if e.mimeData().hasUrls:
            for url in e.mimeData().urls():
                path = url.toLocalFile()
                if os.path.isfile(path):
                    self.fileLIST.append([path])
            self.fileListSetter(self.fileLIST)
        else:
            return None

    def fileListSetter(self, fileLIST):
        print("fileLIST:", fileLIST)
        self.insertRow(len(fileLIST))
        self.setRowCount(len(self.fileLIST))
        self.setColumnCount(len(self.fileLIST[0]))
        self.setSortingEnabled(False)
        for i, row in enumerate(sorted(fileLIST)):
            for j, col in enumerate(row):
                item = TableWidgetItem(col, col)
                self.setItem(i, j, item)
        self.setSortingEnabled(True)
        self.resizeColumnsToContents()
        #for f in fileLIST:
            #self.setItem(0, 0, f)




class MainWindow(QtGui.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.dropZoneWidth = 120
        self.dropZoneHeight = self.dropZoneWidth
        self.fileListWidth = self.dropZoneWidth
        self.initUI()

    def initUI(self):
        extHBox = QtGui.QHBoxLayout()
        extLeftFrame = QtGui.QFrame()
        extRightFrame = QtGui.QFrame()
        leftVBox = QtGui.QVBoxLayout(extLeftFrame)
        rightVBox = QtGui.QVBoxLayout(extRightFrame)
        extLeftFrame.setMaximumWidth(self.dropZoneWidth+10)

        upperLeftFrame = QtGui.QFrame()
        upperLeftFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        upperLeftFrame.setFixedSize(self.dropZoneWidth, self.dropZoneHeight)

        lowerLeftFrame = QtGui.QFrame()
        lowerLeftFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        lowerLeftFrame.setFixedWidth(self.fileListWidth)
        lowerLeftFrame.setMinimumWidth(self.dropZoneWidth)

        upperRightFrame = QtGui.QFrame()
        upperRightFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        upperRightFrame.setFixedHeight(self.dropZoneHeight*2.5)

        lowerRightFrame = QtGui.QFrame()
        lowerRightFrame.setFrameShape(QtGui.QFrame.StyledPanel)

        upperLeftVBox = QtGui.QVBoxLayout(upperLeftFrame)
        lowerLeftVBox = QtGui.QVBoxLayout(lowerLeftFrame)
        upperRightVBox = QtGui.QVBoxLayout(upperRightFrame)
        lowerRightVBox = QtGui.QVBoxLayout(lowerRightFrame)

        upperLeftVBox.setSpacing(0)
        upperLeftVBox.setContentsMargins(0, 0, 0, 0)
        lowerLeftVBox.setContentsMargins(0, 0, 0, 0)

        # <內容>
        upperLeftLabel = DropZoneLabel() #QtGui.QLabel(upperLeftFrame)
        upperLeftLabel.setText(">Drop Zone<")
        upperLeftLabel.setAlignment(QtCore.Qt.AlignCenter)
        upperLeftLabel.setFixedSize(self.dropZoneWidth, self.dropZoneHeight)
        upperLeftVBox.addWidget(upperLeftLabel)

        lowerLeftLable = QtGui.QLabel()
        lowerLeftLable.setText("File List:")
        lowerLeftVBox.addWidget(lowerLeftLable)
        #lowerLeftTable = QtGui.QTableWidget(lowerLeftFrame)
        lowerLeftTable = FileListTable() #QtGui.QTableWidget(lowerLeftFrame)
        #lowerLeftTable.setItem()
        lowerLeftVBox.addWidget(lowerLeftTable)

        upperRightButton = QtGui.QPushButton(upperRightFrame)
        upperRightButton.setText("RIGHT TOP")
        upperRightVBox.addWidget(upperRightButton)

        lowerRightButton = QtGui.QPushButton(lowerRightFrame)
        lowerRightButton.setText("RIGHT Lower")
        lowerRightVBox.addWidget(lowerRightButton)
        # </內容>

        upperLeftFrame.setLayout(upperLeftVBox)
        lowerLeftFrame.setLayout(lowerLeftVBox)
        upperRightFrame.setLayout(upperRightVBox)
        lowerRightFrame.setLayout(lowerRightVBox)

        leftVBox.addWidget(upperLeftFrame)
        leftVBox.addWidget(lowerLeftFrame)
        rightVBox.addWidget(upperRightFrame)
        rightVBox.addWidget(lowerRightFrame)

        extHBox.addWidget(extLeftFrame)
        extHBox.addWidget(extRightFrame)
        self.setLayout(extHBox)

        #screenSize = QtGui.QDesktopWidget().screenGeometry()

        #self.setGeometry(screenSize)
        self.setFixedSize(1046, 550)
        #self.setAcceptDrops(True)
        extRightFrame.setAcceptDrops(False)


        self.show()

        return None

    #def dragEnterEvent(self, e):
        #print("dragging enter")
        #if e.mimeData().hasUrls:
            #e.accept()
        #else:
            #e.ignore()

    def dragMoveEvent(self, e):
        print("dragging move")
        if e.mimeData().hasUrls:
            e.accept()
        else:
            e.ignore()

    #def dropEvent(self, e):
        #print("dropping at", e.mimeData())
        ##print((10, 10) < e.pos())
        ##if (10, 10) < e.pos() < (self.dropZoneWidth, self.dropZoneHeight):
            ##print("Inside drop zone")
        #if e.mimeData().hasUrls:
            #print(e.mimeData().urls())
        #return None


def main():
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())

if __name__== "__main__":
    main()