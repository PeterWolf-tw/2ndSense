#!/usr/bin/env python
# -*- coding:utf-8 -*-
# FileName: wavTools.py

import numpy
import wave
import struct

class WavGear:
    def __init__(self):
        self.wavFileName = None
        self.frameNumber = None
        self.channelNumber = None
        self.wavDataDICT = {"signal"           : None,
                            "normalizedSignal" : None,
                            "samplingRate"     : None,
                            "width"            : None, # in bytes. 1->8 bits, 2->16 bits
                            "env"              : None,
                            }


    def wavReader(self, wavFileName):
        self.wavFileName = wavFileName

        self.wavFileObj = wave.open(self.wavFileName, "r")
        self.frameNumber = self.wavFileObj.getnframes()
        self.wavDataDICT["signal"] = numpy.fromstring(self.wavFileObj.readframes(self.frameNumber), "Int16")/32767.0
        self.wavDataDICT["normalizedSignal"] = self._signalNormalizer(self.wavDataDICT["signal"])
        self.wavDataDICT["samplingRate"] = self.wavFileObj.getframerate()
        self.wavDataDICT["width"] = self.wavFileObj.getsampwidth()
        self.wavFileObj.close()
        if self.wavDataDICT["width"] == 2:
            self.wavDataDICT["env"] = "pcm16"
        elif self.wavDataDICT["width"] == 1:
            self.wavDataDICT["env"] = "pcm8"
        else:
            self.wavDataDICT["env"] = "Unknown. (Only 8bit or 16bit audio are supported."

        return self.wavDataDICT

    def _signalNormalizer(self, signalARY, ceilling=0.95):
        avg = numpy.mean(signalARY)
        wavSignalARY = signalARY - avg
        normalizedSignalARY = numpy.int16(wavSignalARY/numpy.max(numpy.abs(wavSignalARY)*1.0)*32767*ceilling)
        return normalizedSignalARY

    def wavwrite(self):
        print("--SndFreqTools wavwrite starts --")
        self.wavFile.setparams((1, 2, 44100, len(self.signal), "NONE", "not compressed"))
        data = []
        for i in self.signal:
            data.append(struct.pack('h', i*32768))
        self.wavFile.writeframes("".join(data))
        fileSize = round((len(self.signal)*2+44)/1024.0, 2)
        self.wavFile.close()
        print("--SndFreqTools wavwrite ends --")

        return fileSize