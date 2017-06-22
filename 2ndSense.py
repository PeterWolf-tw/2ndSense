#!/usr/bin/env python
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
import pyaudio
from PySide import QtCore
from PySide import QtGui
import pyqtgraph as pqg
from UI.fileManager import FileListQListWidget
from UI.ctrlButtons import DropZoneFrame
from UI.plotZone import ComboWidget
import numpy as np
#from UI import plotZone

class MicrophoneRecorder():
    def __init__(self, signal):
        self.FS = 44100
        self.CHUNKSZ = 1024
        self.signal = signal
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16,
                                  channels=1,
                                  rate=self.FS,
                                  input=True,
                                  frames_per_buffer=self.CHUNKSZ)

    def read(self):
        data = self.stream.read(self.CHUNKSZ)
        y = np.fromstring(data, 'int16')
        self.signal.emit(y)

    def close(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

class MainWindow(QtGui.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.dropZoneWidth = 142
        self.dropZoneHeight = self.dropZoneWidth
        self.fileListWidth = self.dropZoneWidth
        self.initUI()

    def initUI(self):
        extHBox = QtGui.QHBoxLayout()
        extLeftFrame = QtGui.QFrame()
        extRightFrame = QtGui.QFrame()
        leftVBox = QtGui.QVBoxLayout(extLeftFrame)
        rightVBox = QtGui.QVBoxLayout(extRightFrame)
        extLeftFrame.setMaximumWidth(self.dropZoneWidth+5)

        upperLeftFrame = DropZoneFrame()
        upperLeftFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        upperLeftFrame.setFixedSize(self.dropZoneWidth, self.dropZoneHeight)

        lowerLeftFrame = QtGui.QFrame()
        lowerLeftFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        lowerLeftFrame.setFixedWidth(self.fileListWidth)
        lowerLeftFrame.setMinimumWidth(self.dropZoneWidth-5)

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

        lowerLeftLable = QtGui.QLabel()
        lowerLeftLable.setText("File List:")
        lowerLeftVBox.addWidget(lowerLeftLable)
        lowerLeftTable = FileListQListWidget()
        lowerLeftVBox.addWidget(lowerLeftTable)

        self.comboZone = ComboWidget()
        upperRightVBox.addWidget(self.comboZone)

        lowerRightButton = QtGui.QPushButton(lowerRightFrame)
        lowerRightButton.setText("RIGHT Lower")
        lowerRightVBox.addWidget(lowerRightButton)


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

        #extRightFrame.setAcceptDrops(False)

        self.show()



        return None

    def dragMoveEvent(self, e):
        print("dragging move")
        if e.mimeData().hasUrls:
            e.accept()
        else:
            e.ignore()



def main():
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()

    #<給筑安期末炫炮呈現使用，實際開發時需移除>
    spz = window.comboZone.spectrogramZone
    spz.read_collected.connect(spz.update)
    mic = MicrophoneRecorder(spz.read_collected)
    interval = 44100/1024
    t = pqg.QtCore.QTimer()
    t.timeout.connect(mic.read)
    t.start(1000/interval) #QTimer takes ms
    #</給筑安期末炫炮呈現使用，實際開發時需移除>


    sys.exit(app.exec_())

if __name__== "__main__":
    main()