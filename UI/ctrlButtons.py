#!/usr/bin/env python
# -*- coding:utf-8 -*-
# FileName:ctrlButtons.py

# Developer: Peter. w (peter.w@droidtown.co)
# This Software/Scipt is protected by copyright and other
# intellectual property laws and treaties.
# Droidtown Linguistic Technology Co., Ltd. owns the copyright,
# and other intellectual property rights in the Software/Script.
# 卓騰語言科技有限公司 版權所有
# Copyright 2017 Droidtown Ling. Tech. Co., Ltd
# All Rights Reserved.

import os

from PySide import QtGui

class DropZoneLabel(QtGui.QLabel):
    def __init__(self):
        super(DropZoneLabel, self).__init__()
        self.setToolTip("Drag & Drop files to add to the 'File list' below!")
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
        print("dragging enter")
        if e.mimeData().hasUrls:
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        print("dropping at", e.mimeData())
        if e.mimeData().hasUrls:
            fileLIST = []
            fileDICT = {}
            for url in e.mimeData().urls():
                path = url.toLocalFile()
                if os.path.isfile(path):
                    fileLIST.append(path)
            print(fileLIST)

            return fileLIST
        else:
            return None