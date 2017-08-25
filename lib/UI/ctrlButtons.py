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

from PySide import QtCore
from PySide import QtGui

class DropZoneFrame(QtGui.QFrame):
#class DropZoneFrame(QtGui.QWidget):
    def __init__(self):
        cwd = os.getcwd()+"/app/"
        super(DropZoneFrame, self).__init__()
        self.setToolTip("Drag & Drop files to add to the 'File list' below!")
        self.setAcceptDrops(True)
        self.setContentsMargins(0, 0, 6, 6)
        self.setFrameShape(QtGui.QFrame.StyledPanel)
        self.iconSize = 32
        self.buttonSize = 36

        self.playButton = QtGui.QPushButton()
        self.playButton.setToolTip("Play")
        self.playButton.setIcon(QtGui.QIcon(cwd+"resources/img/media_playback_start.png"))
        self.playButton.setIconSize(QtCore.QSize(self.iconSize, self.iconSize))
        self.playButton.setFixedSize(self.buttonSize, self.buttonSize)

        self.recordButton = QtGui.QPushButton()
        self.recordButton.setToolTip("Record")
        self.recordButton.setIcon(QtGui.QIcon(cwd+"resources/img/media_record.png"))
        self.recordButton.setIconSize(QtCore.QSize(self.iconSize, self.iconSize))
        self.recordButton.setFixedSize(self.buttonSize, self.buttonSize)

        self.stopButton = QtGui.QPushButton()
        self.stopButton.setToolTip("Stop")
        self.stopButton.setIcon(QtGui.QIcon(cwd+"resources/img/media_playback_stop.png"))
        self.stopButton.setIconSize(QtCore.QSize(self.iconSize, self.iconSize))
        self.stopButton.setFixedSize(self.buttonSize, self.buttonSize)

        self.terminalButton = QtGui.QPushButton()
        self.terminalButton.setToolTip("Terminal")
        self.terminalButton.setIcon(QtGui.QIcon(cwd+"resources/img/terminal.png"))
        self.terminalButton.setIconSize(QtCore.QSize(self.iconSize, self.iconSize))
        self.terminalButton.setFixedSize(self.buttonSize, self.buttonSize)

        self.settingButton = QtGui.QPushButton()
        self.settingButton.setToolTip("Setting")
        self.settingButton.setIcon(QtGui.QIcon(cwd+"resources/img/Gear Filled-50.png"))
        self.settingButton.setIconSize(QtCore.QSize(self.iconSize, self.iconSize))
        self.settingButton.setFixedSize(self.buttonSize, self.buttonSize)

        self.app3dButton = QtGui.QPushButton()
        self.app3dButton.setToolTip("3D")
        self.app3dButton.setIcon(QtGui.QIcon(cwd+"resources/img/applications-3d.png"))
        self.app3dButton.setIconSize(QtCore.QSize(self.iconSize, self.iconSize))
        self.app3dButton.setFixedSize(self.buttonSize, self.buttonSize)

        self.spectrogramButton = QtGui.QPushButton()
        self.spectrogramButton.setToolTip("Spectrogram")
        self.spectrogramButton.setIcon(QtGui.QIcon(cwd+"resources/img/Frequency-50.png"))
        self.spectrogramButton.setIconSize(QtCore.QSize(self.iconSize, self.iconSize))
        self.spectrogramButton.setFixedSize(self.buttonSize, self.buttonSize)

        self.defaultViewButton = QtGui.QPushButton()
        self.defaultViewButton.setToolTip("Default View")
        self.defaultViewButton.setIcon(QtGui.QIcon(cwd+"resources/img/Settings Backup Restore Filled-50.png"))
        self.defaultViewButton.setIconSize(QtCore.QSize(self.iconSize, self.iconSize))
        self.defaultViewButton.setFixedSize(self.buttonSize, self.buttonSize)

        self.saveButton = QtGui.QPushButton()
        self.saveButton.setToolTip("Save All")
        self.saveButton.setIcon(QtGui.QIcon(cwd+"resources/img/smart_media_unmount.png"))
        self.saveButton.setIconSize(QtCore.QSize(self.iconSize, self.iconSize))
        self.saveButton.setFixedSize(self.buttonSize, self.buttonSize)

        buttonGridLayout = QtGui.QGridLayout(self)
        buttonGridLayout.addWidget(self.playButton, 0, 0)
        buttonGridLayout.addWidget(self.recordButton, 0, 1)
        buttonGridLayout.addWidget(self.stopButton, 0, 2)
        buttonGridLayout.addWidget(self.terminalButton, 1, 0)
        buttonGridLayout.addWidget(self.settingButton, 1, 1)
        buttonGridLayout.addWidget(self.app3dButton, 1, 2)
        buttonGridLayout.addWidget(self.spectrogramButton, 2, 0)
        buttonGridLayout.addWidget(self.defaultViewButton, 2, 1)
        buttonGridLayout.addWidget(self.saveButton, 2, 2)


        #self.setLayout(buttonGridLayout)


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