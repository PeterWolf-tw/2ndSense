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

import PySide
import pyqtgraph as pqg

class waveformGraph(pqg.PlotWidget):
    def __init__(self):
        super(waveformGraph, self).__init__()
        self.setYRange(-1, 1, padding=0.05)
        #self.wheelEvent(self, ev, y)
        self.data = []
        return None

    def plotter(data):
        p = self.PlotItem.plot(data)


    def wheelEvent(self, ev, axis=None):
        # 1. Pass on the wheelevent to the superclass, such
        #    that the standard zoomoperation can be executed.
        pqg.PlotWidget.wheelEvent(ev,axis)