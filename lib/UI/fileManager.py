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


import logging
import os

from PySide import QtGui
from PySide import QtCore

from ..toolbox import wavTools

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


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
                    # <檢查是否列表中已有該檔案>
                    if path in [self.fileDICT[k]["fullPath"] for k in self.fileDICT.keys()]:
                        pass
                    else:
                        self.fileDICT[len(self.fileLIST)] = {"fullPath": path, "fileObj":None} #filePath 用於讀取檔案； fileObj 用於記錄該檔案是否已開啟。若已實體化並開啟，就不會是 None
                        self.fileLIST.append(os.path.basename(path))
                        logger.debug(self.fileDICT)
                    # </檢查是否列表中已有該檔案>
                else:
                    pass
            self.fileListSetter(self.fileLIST)
        else:
            return None

    def fileListSetter(self, fileLIST):
        print("fileLISTSetter:", fileLIST)
        self.clear()
        for i in range(0, len(fileLIST)):
            newItem = QtGui.QListWidgetItem(fileLIST[i])
            newItem.setData(QtCore.Qt.ToolTipRole, self.fileDICT[i]["fullPath"])
            logger.debug(self.fileDICT[i]["fullPath"])
            self.addItem(newItem)

        return None

    def filePick(self):
        print(self.selectedIndexes()[0].row())
        index = self.selectedIndexes()[0].row()
        #id_us = str(self.fileLIST.index(self.model().data(index))+1)
        print("file clicked", index)
        print("file path:", self.fileDICT[index]["fullPath"])
        if self.fileDICT[index]["fullPath"].endswith(".wav"):
            wg = wavTools.WavGear()
            wg.wavReader(self.fileDICT[index]["fullPath"])
        return None


    def rowHover(self, row, column):
        currentItem  = self.item(row, column)
        print("currentItem:", currentItem)
        previousItem = self.item(self.currentHoverLIST[0], self.currentHoverLIST[1])
        if self.currentHoverLIST == [row, column]:
            pass
        else:
            currentItem.showhint

