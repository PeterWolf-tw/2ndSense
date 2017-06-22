#!/usr/bin/env python
# -*- coding:utf-8 -*-
# FileName: plotZone.py

# Developer: Peter. w (peter.w@droidtown.co)
# This Software/Scipt is protected by copyright and other
# intellectual property laws and treaties.
# Droidtown Linguistic Technology Co., Ltd. owns the copyright,
# and other intellectual property rights in the Software/Script.
# 卓騰語言科技有限公司 版權所有
# Copyright 2016 Droidtown Ling. Tech. Co., Ltd
# All Rights Reserved.

import importlib
import inspect
import os
import pyaudio
from PySide import QtCore
from PySide import QtGui
import pyqtgraph as pqg
import sys
import numpy as np

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
        data = self.stream.read(CHUNKSZ)
        y = np.fromstring(data, 'int16')
        self.signal.emit(y)

    def close(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()


class CustomViewBox(pqg.ViewBox):
    def __init__(self, *args, **kwds):
        pqg.ViewBox.__init__(self, *args, **kwds)
        self.setMouseMode(self.RectMode)

    ## reimplement right-click to zoom out
    def mouseClickEvent(self, ev):
        if ev.button() == QtCore.Qt.RightButton:
            self.autoRange()

    def mouseDragEvent(self, ev):
        if ev.button() == QtCore.Qt.RightButton:
            ev.ignore()
        else:
            pqg.ViewBox.mouseDragEvent(self, ev)

class WaveformGraph(pqg.PlotWidget):
    def __init__(self):
        super(WaveformGraph, self).__init__()
        cvb = CustomViewBox()
        self.ViewBox = cvb
        self.setYRange(-1, 1, padding=0.05)
        self.setLimits(yMin=-1, yMax=1, xMin=0)
        pqg.setConfigOptions(antialias=True)
        #self.setMouseE
        self.data = []
        self.setLabel('left', 'amp')
        self.setLabel('bottom', 'Time', units='Sec.')
        return None

    def plotter(data):
        p = self.PlotItem.plot(data)

    #def wheelEvent(self, axis=None):
        ## 1. Pass on the wheelevent to the superclass, such
        ##    that the standard zoomoperation can be executed.
        #pqg.PlotWidget.wheelEvent(ev,axis)


class SpectrogramWidget(pqg.PlotWidget):
    read_collected = QtCore.Signal(np.ndarray)
    def __init__(self):
        super(SpectrogramWidget, self).__init__()
        cvb = CustomViewBox()
        self.ViewBox=cvb
        self.setYRange(0, 10000)
        self.setLimits(yMin=0)

        self.img = pqg.ImageItem()
        self.addItem(self.img)
        self.FS = 44100 #Hz
        self.CHUNKSZ = 1024 #samples
        self.img_array = np.zeros((1000, self.CHUNKSZ/2+1))

        # bipolar colormap

        pos = np.array([0., 1., 0.5, 0.25, 0.75])
        color = np.array([[0,255,255,255], [255,255,0,255], [0,0,0,255], (0, 0, 255, 255), (255, 0, 0, 255)], dtype=np.ubyte)
        cmap = pqg.ColorMap(pos, color)
        lut = cmap.getLookupTable(0.0, 1.0, 256)

        self.img.setLookupTable(lut)
        self.img.setLevels([-50,40])

        freq = np.arange((self.CHUNKSZ/2)+1)/(float(self.CHUNKSZ)/self.FS)
        yscale = 1.0/(self.img_array.shape[1]/freq[-1])
        self.img.scale((1./self.FS)*self.CHUNKSZ, yscale)

        self.setLabel('left', 'Frequency', units='Hz')
        self.setLabel('bottom', 'Time', units='Sec.')

        self.win = np.hanning(self.CHUNKSZ)
        self.show()

    def update(self, chunk):
        # normalized, windowed frequencies in data chunk

        spec = np.fft.rfft(chunk*self.win) / self.CHUNKSZ
        # get magnitude

        psd = abs(spec)
        # convert to dB scale

        psd = 20 * np.log10(psd)

        # roll down one and replace leading edge with new data

        self.img_array = np.roll(self.img_array, -1, 0)
        self.img_array[-1:] = psd

        self.img.setImage(self.img_array, autoLevels=False)

class ComboWidget(QtGui.QWidget):
    def __init__(self):
        super(ComboWidget, self).__init__()
        self.FS = 44100
        self.CHUNKSZ = 1024
        #<嚐試使用自動載入按鈕>
        try:
            moduleLIST = [m for m in os.listdir("./toolbox") if m.endswith("Tools.py")]
        except:
            moduleLIST = []

        toolDICT = {}

        for m in moduleLIST:
            module = importlib.import_module("toolbox."+m.replace(".py", ""))
            for name, obj in inspect.getmembers(module, inspect.isclass):
                toolDICT[name] = [f for f in obj.__dict__.keys() if f.startswith("_") == False]
                print("toolDICT:", toolDICT, "toolbox."+m.replace(".py", ".")+toolDICT[name][0])
                mObj = importlib.import_module("toolbox."+m.replace(".py", ""))
                mFuncLIST = [f for f in inspect.getmembers(mObj) if inspect.ismodule(f[1])]
                print("functions:", mFuncLIST)
        toolLIST = [m[:-3].upper().replace("TOOLS", " tools") for m in moduleLIST]
        toolCombobox = pqg.ComboBox(items=toolLIST)


        #</嚐試使用自動載入按鈕>


        self.hBox = QtGui.QHBoxLayout()

        self.vBox = QtGui.QVBoxLayout()
        waveformZone = WaveformGraph()
        self.spectrogramZone = SpectrogramWidget()
        self.setContentsMargins(-10, -10, -10, -5)

        waveformZone.setXLink(self.spectrogramZone)

        self.vBox.addWidget(waveformZone)
        self.vBox.addWidget(self.spectrogramZone)

        self.gBox = QtGui.QGridLayout()
        self.gBox.setAlignment(QtCore.Qt.Alignment(QtCore.Qt.AlignTop))
        self.gBox.addWidget(QtGui.QLabel("Toolbox"))
        self.gBox.addWidget(toolCombobox)

        self.hBox.addLayout(self.vBox)
        self.hBox.addLayout(self.gBox)

        self.setLayout(self.hBox)

        return None