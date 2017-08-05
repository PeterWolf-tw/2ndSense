#!/usr/bin/env python
# -*- coding:utf-8 -*-

import numpy as np
import pyaudio
from PySide import QtCore
import pyqtgraph as pg
import time

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

def draw_waveform(all_frames):
    time.sleep(1) # Wait just one second
    pw = pg.plot(title="Waveform") # Window title
    pg.setConfigOptions(antialias=True) # Enable antialias for better resolution
    pw.win.resize(1300, 160) # Define window size
    pw.win.move(300 * 1920 / 1920, 850 * 1080 / 1080) # Define window position
    pw.showAxis('bottom', False) # Hide bottom axis
    while True: # Loop over the frames of the audio / data chunks
        data = ''.join(all_frames[-20:]) # Join last 20 frames of all frames
        data = np.fromstring(data, 'int16') # Binary string to numpy int16 data format
        #data2 = ''.join(thresh_frames[-20:]) # Join last 20 frames of thrsh frames
        #data2 = numpy.fromstring(data2, 'int16') # Binary string to numpy int16 data format
        pw.setMouseEnabled(x=False) # Disable mouse
        pw.setRange(yRange=[-10000,10000]) # Set Y range of graph
        pw.plot(data, clear=True, pen=pg.mkPen('w', width=0.5, style=QtCore.Qt.DotLine)) # Plot all frames with white pen
        #pw.plot(data2, pen=pg.mkPen('y', width=0.5, style=QtCore.Qt.DotLine)) # Plot thresh frames with yellow pen
        #text = pg.TextItem("Seconds : " + str(int(len(all_frames)/(RATE/CHUNK))), color=(255, 255, 255)) # Define seconds according to number of total frames as a text
        #pw.addItem(text) # Display seconds according to number of total frames
        #text.setPos(500, 0) # Set text position
        pg.QtGui.QApplication.processEvents()
        time.sleep(0.05) # Wait a few miliseconds

if __name__== "__main__":
    signal = QtCore.Signal(np.ndarray)
    mic = MicrophoneRecorder(signal)
    draw_waveform(signal)