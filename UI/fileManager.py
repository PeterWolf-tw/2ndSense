#!/usr/bin/env python
# -*- coding:utf-8 -*-
# FileName: fileManager.py

# Developer: Peter. w (peter.w@droidtown.co)
# This Software/Scipt is protected by copyright and other
# intellectual property laws and treaties.
# Droidtown Linguistic Technology Co., Ltd. owns the copyright,
# and other intellectual property rights in the Software/Script.
# 卓騰語言科技有限公司 版權所有
# Copyright 2012 Droidtown Ling. Tech. Co., Ltd
# All Rights Reserved.

import os

from PySide import QtGui
from PySide import QtCore


#class TableWidgetItem(QtGui.QTableWidgetItem):
    #'''
    #在原始 QTableWidgetItem 類別下, 新增表格 item 用來排序的數值型態。
    #'''
    #def __init__(self, text, sortKey):
        #QtGui.QTableWidgetItem.__init__(self, text, QtGui.QTableWidgetItem.UserType)
        #self.sortKey = sortKey

    ##Qt uses a simple < check for sorting items, override this to use the sortKey
    #def __lt__(self, other):
        #return self.sortKey < other.sortKey

#class FileListQTableWidget(QtGui.QTableWidget):
    #def __init__(self):
        #super(FileListQTableWidget, self).__init__()
        #self.fileLIST = []
        #self.fileDICT = {}
        #self.toolTip = "Drag&Drop files here!"
        #self.currentHoverLIST = [0, 0]
        #self.setAcceptDrops(True)
        #self.verticalHeader().setVisible(False)
        #self.horizontalHeader().setVisible(False)
        #self.setShowGrid(False)
        #self.doubleClicked.connect(self.filePick)

    #def dragEnterEvent(self, e):
        #print("fileLIST dragging enter")
        #if e.mimeData().hasUrls:
            #e.accept()
        #else:
            #e.ignore()
        ##if e.mimeData().hasFormat('text/plain'):
            ##e.accept()
        ##else:
            ##e.ignore()

    #def dragMoveEvent(self, e):
        #e.accept()

    #def dropEvent(self, e):
        #print("fileLIST dropping at", e.mimeData())
        #if e.mimeData().hasUrls:
            #for url in e.mimeData().urls():
                #path = url.toLocalFile()
                #if os.path.isfile(path):
                    #self.fileDICT[str(len(self.fileLIST)+1)] = {"fullPath": path, "fileObj":None} #filePath 用於讀取檔案； fileObj 用於記錄該檔案是否已開啟。若已實體化並開啟，就不會是 None
                    #self.fileLIST.append([str(len(self.fileLIST)+1), os.path.basename(path)])
            #self.fileListSetter(self.fileLIST)
        #else:
            #return None

    #def fileListSetter(self, fileLIST):
        #print("fileLIST:", fileLIST)
        #self.insertRow(len(fileLIST))
        #self.setRowCount(len(self.fileLIST))
        #self.setColumnCount(len(self.fileLIST[0]))
        #self.setSortingEnabled(False)
        #for i, row in enumerate(sorted(fileLIST)):
            #for j, col in enumerate(row):
                #item = TableWidgetItem(col, col)
                #item.setToolTip(self.fileDICT[str(i+1)]["fullPath"])
                #self.setItem(i, j, item)
        #self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        #self.setSortingEnabled(True)
        #self.hideColumn(0) #隱藏 self.fileDICT 的 key 值
        #self.resizeColumnsToContents()
        #return None

    #def filePick(self, event):
        #print("clicked!")
        #return None

    #def rowHover(self, row, column):
        #currentItem  = self.item(row, column)
        #previousItem = self.item(self.currentHoverLIST[0], self.currentHoverLIST[1])
        #if self.currentHoverLIST == [row, column]:
            #pass
        #else:
            #currentItem.showhint


class FileListQListWidget(QtGui.QListWidget):
    def __init__(self):
        super(FileListQListWidget, self).__init__()
        self.fileLIST = []
        self.fileDICT = {}
        self.toolTip = "Drag&Drop files here!"
        self.currentHoverLIST = [0, 0]
        self.setAcceptDrops(True)
        self.clicked.connect(self.filePick)

    def dragEnterEvent(self, e):
        print("fileLIST dragging enter")
        if e.mimeData().hasUrls:
            e.accept()
        else:
            e.ignore()
        return None

    def dragMoveEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        print("fileLIST dropping at", e.mimeData())
        if e.mimeData().hasUrls:
            for url in e.mimeData().urls():
                path = url.toLocalFile()
                if os.path.isfile(path):
                    self.fileDICT[len(self.fileLIST)] = {"fullPath": path, "fileObj":None} #filePath 用於讀取檔案； fileObj 用於記錄該檔案是否已開啟。若已實體化並開啟，就不會是 None
                    self.fileLIST.append(os.path.basename(path))
            self.fileListSetter(self.fileLIST)
        else:
            return None

    def fileListSetter(self, fileLIST):
        print("fileLIST:", fileLIST)

        self.clear()
        for i in range(0, len(fileLIST)):
            newItem = QtGui.QListWidgetItem(fileLIST[i])
            newItem.setData(QtCore.Qt.ToolTipRole, self.fileDICT[i]["fullPath"])
            self.addItem(newItem)

        return None

    def filePick(self):
        print(self.selectedIndexes()[0].row())
        index = self.selectedIndexes()[0].row()
        #id_us = str(self.fileLIST.index(self.model().data(index))+1)
        print("file clicked", index)
        print("file path:", self.fileDICT[index]["fullPath"])
        return None


    def rowHover(self, row, column):
        currentItem  = self.item(row, column)
        print("currentItem:", currentItem)
        previousItem = self.item(self.currentHoverLIST[0], self.currentHoverLIST[1])
        if self.currentHoverLIST == [row, column]:
            pass
        else:
            currentItem.showhint