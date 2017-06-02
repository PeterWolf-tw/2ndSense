#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# FileName: orate.py
# Development starting date: 2016.10.20

# Developer: Peter. w (peter.w@droidtown.co)

# This Software/Scipt is protected by copyright and other
# intellectual property laws and treaties.
# Droidtown Linguistic Technology Co., Ltd. owns the copyright,
# and other intellectual property rights in the Software/Script.
# 卓騰語言科技有限公司 版權所有
# Copyright 2016 Droidtown Ling. Tech. Co., Ltd
# All Rights Reserved.


import copy
import logging
import math
import numpy
import os
import pylab as plt
import scipy.io.wavfile
import time


logging.basicConfig(level=logging.DEBUG)
mylog = logging.getLogger(__name__)

class VoiceSound:
    def __init__(self, wavFileName=None):
        self.lookupTableDICT = {"NONE":0, "SINE":1, "COSINE":2, "HAMMING":3, "HANN":4, "GAUSSIAN":5}
        if wavFileName == None:
            self.samplingRateFreq = 0
            self.wavSignalRawARY = None
            self.wavSignalNormalizedARY = None
            self.zcrLIST = []
            self.energyLIST = []

        else:
            self.wavFileOpener(wavFileName)

        return None

    def wavFileOpener(self, wavFileName, showPlot=False):
        '''
        input: *.wav format audio file.
        output: (self.samplingRateFreq, self.wavSignalRawARY).
        '''
        if os.path.isfile(wavFileName):
            pass
        else:
            raise FileNotFoundError

        (self.samplingRateFreq, self.wavSignalRawARY)= scipy.io.wavfile.read(wavFileName)

        # <Plotting>
        if showPlot == False:
            pass
        else:
            time = numpy.arange(0, len(self.wavSignalRawARY)) * (1.0 / self.samplingRateFreq)
            plt.plot(time, self.wavSignalRawARY)
            plt.title("Raw signal.")
            plt.xlabel("Time (sec.)")
            plt.ylabel("Amplitude")
            plt.show()
        # </Plotting>


        return (self.samplingRateFreq, self.wavSignalRawARY)

    def normalize(self, wavSignalARY, showPlot=False):
        '''
        input: wavSignalARY
        output: self.wavSignalNormalizedARY
        Normalize input wavSignalARY, save it in self.wavNormlizedARY and return.
        '''

        self.wavSignalNormalizedARY = wavSignalARY/max(wavSignalARY)

        # <myLog>
        mylog.info("self.wavSignalNormalizedARY:{0}".format(self.wavSignalNormalizedARY))
        # </myLog>

        # <Plotting>
        if showPlot == False:
            pass
        else:
            time = numpy.arange(0, len(self.wavSignalNormalizedARY)) * (1.0 / self.samplingRateFreq)
            plt.plot(time, self.wavSignalNormalizedARY)
            plt.title("Normalized signal.")
            plt.xlabel("Time (sec.)")
            plt.ylabel("Amplitude")
            plt.show()
        # </Plotting>

        return self.wavSignalNormalizedARY

    def zcrDetector(self, wavSignalARY, windowSize, overLappingRatio, showPlot=False):
        '''
        input: wavSignalARY
        output: self.zcrLIST
        Calculate ZCR distribution by the windowSize and store them into self.zcrLIST.
        '''
        windowSize = int(windowSize)
        dataLength = len(wavSignalARY)
        step = int(windowSize - (windowSize*overLappingRatio))
        frameNum = math.ceil(dataLength/step)
        self.zcrLIST = [] #numpy.zeros((frameNum, 1))

        for i in range(frameNum):
            curFrame = wavSignalARY[numpy.arange(i*step, min(i*step+windowSize, dataLength))]
            #To avoid DC bias, usually we need to perform mean subtraction on each frame
            #ref: http://neural.cs.nthu.edu.tw/jang/books/audiosignalprocessing/basicFeatureZeroCrossingRate.asp
            curFrame = curFrame - numpy.mean(curFrame) # zero-justified
            self.zcrLIST.append(sum(curFrame[0:-1]*curFrame[1::]<=0))

        self.zcrMotionMeanLIST = numpy.convolve(self.zcrLIST, numpy.ones((3,))/3, mode="full")[(3-1):]

        print("zcrMotionMean:", self.zcrMotionMeanLIST)
        print(len(self.zcrMotionMeanLIST))
        # <myLog>
        mylog.info("self.zcrLIST:{0}".format(self.zcrLIST))
        # </myLog>

        # <Plotting>
        if showPlot == False:
            pass
        else:
            time = numpy.arange(0, len(self.zcrLIST)) * (len(wavSignalARY)/len(self.zcrLIST) / self.samplingRateFreq)
            plt.plot(time, self.zcrLIST)
            plt.plot(time, self.zcrMotionMeanLIST, color="black")
            plt.title("ZCR>> window_size:{0}sec.".format(windowSize/self.samplingRateFreq))
            plt.xlabel("Time (sec.)")
            plt.ylabel("ZCR")
            plt.show()
        # </Plotting>
        return [x for x in zip(time, self.zcrLIST)]

    def energyDetector(self, wavSignalARY, windowSize, overLappingRatio, showPlot=False):
        '''
        input: wavSignalARY
        output: self.energyLIST
        Calculate energy distribution by the windowSize and store them into self.energyLIST.
        '''
        windowSize = int(windowSize)
        dataLength = len(wavSignalARY)
        step = int(windowSize - (windowSize*overLappingRatio))
        frameNum = math.ceil(dataLength/step)
        self.energyLIST = [] #numpy.zeros((frameNum, 1))
        for i in range(frameNum):
            curFrame = numpy.sum(numpy.absolute(wavSignalARY[numpy.arange(i*step, min(i*step+windowSize, dataLength))]))
            self.energyLIST.append(curFrame)

        # <myLog>
        mylog.info("self.energyLIST:{0}".format(self.energyLIST))
        # </myLog>

        # <Plotting>
        if showPlot == False:
            pass
        else:
            time = numpy.arange(0, len(self.energyLIST)) * (len(wavSignalARY)/len(self.energyLIST) / self.samplingRateFreq)
            plt.plot(time, self.energyLIST)
            plt.title("Energy>> window_size:{0}sec.".format(windowSize/self.samplingRateFreq))
            plt.xlabel("Time (sec.)")
            plt.ylabel("Energy")
            plt.show()
        # </Plotting>
        return self.energyLIST

    def _createLookupTable(self, size, WindowType=None):
        '''
        REF: http://homepage.univie.ac.at/christian.herbst//python/dsp_util_8py_source.html
        '''
        data = numpy.zeros(size)
        for i in range(size):
            xrel = float(i) / float(size)
            if WindowType == self.lookupTableDICT["NONE"]:
                tmp = 1
            elif WindowType == self.lookupTableDICT["SINE"]:
                tmp = math.sin (xrel * math.pi * 2)
            elif WindowType == self.lookupTableDICT["COSINE"]:
                tmp = math.cos (xrel * math.pi * 2)
            elif WindowType == self.lookupTableDICT["HAMMING"]:
                tmp = 0.54 - 0.46 * math.cos(2 * math.pi * xrel)
            elif WindowType == self.lookupTableDICT["HANN"]:
                tmp = 0.5 - 0.5 * math.cos(2 * math.pi * xrel)
            #elif type == LOOKUP_TABLE_GAUSSIAN:
            #   // y = exp(1) .^ ( - ((x-size./2).*pi ./ (size ./ 2)) .^ 2 ./ 2);
            #   tmp = pow((double)exp(1.0), (double)(( - pow ((double)(((FLOAT)x-table_size / 2.0) * math.pi / (table_size / 2.0)) , (double)2.0)) / 2.0));
            else:
                raise Exception('WindowType ' + str(WindowType) + ' not recognized')
            data[i] = tmp
        return data

    def _findArrayMaximum(self, wavSignalARY, offsetLeft = 0, offsetRight = -1, doInterpolate = True):
        '''
        REF: http://homepage.univie.ac.at/christian.herbst//python/dsp_util_8py_source.html
        ::offsetRight: If -1, the array size will be used
        ::doInterpolate: Increase accuracy by performing a parabolic interpolation
        '''
        #objType = type(data).__name__.strip()
        #if objType <> "ndarray":
            #raise Exception('data argument is no instance of numpy.array')
        size = len(wavSignalARY)
        if (size < 1):
            raise Exception('wavSignalARY array is empty')
        xOfMax = -1
        valMax = min(wavSignalARY)
        if offsetRight == -1:
            offsetRight = size
        for i in range(offsetLeft + 1, offsetRight - 1):
            if wavSignalARY[i] >= wavSignalARY[i-1] and wavSignalARY[i] >= wavSignalARY[i + 1]:
                if wavSignalARY[i] > valMax:
                    valMax = wavSignalARY[i]
                    xOfMax = i
        if doInterpolate:
            if xOfMax > 0 and xOfMax < size - 1:
                # use parabolic interpolation to increase accuracty of result
                alpha = wavSignalARY[xOfMax - 1]
                beta = wavSignalARY[xOfMax]
                gamma = wavSignalARY[xOfMax + 1]
                xTmp = (alpha - gamma) / (alpha - beta * 2 + gamma) / 2.0
                xOfMax = xTmp + xOfMax
                valMax = interpolateParabolic(alpha, beta, gamma, xTmp)
        return [xOfMax, valMax]

    def _f0Calculator(self, wavSignalARY, samplingRateFreq, Fmin = 50,Fmax = 3000, voicingThreshold = 0.3, applyWindow = False):
        startingTime = time.time()
        dataTmp = copy.deepcopy(wavSignalARY)

        # apply window
        if applyWindow:
            fftWindow = self._createLookupTable(len(dataTmp), LOOKUP_TABLE_HANN)
            dataTmp *= fftWindow

        # autocorrelation
        result = numpy.correlate(dataTmp, dataTmp, mode = "full")#, old_behavior = False)
        r = result[result.size//2:] / len(wavSignalARY)

        # find peak in AC
        try:
            xOfMax, valMax = self._findArrayMaximum(r, samplingRateFreq / Fmax, samplingRateFreq / Fmin)
            valMax /= max(r)
            f0 = samplingRateFreq / xOfMax
            print("Total Time: {0}".format(time.time()-startingTime))
            return f0
        except Exception as e:
            #print e
            print("Total Time: {0}".format(time.time()-startingTime))
            return 0


    def cycleF0Detector(self, wavSignalARY, samplingRateFreq, Fmin=50, Fmax=3000, numPeriods=5.0, voicingThreshold=0.3, applyWindow=False, showPlot=False):
        '''
        REF: http://homepage.univie.ac.at/christian.herbst//python/namespacedsp_util.html#a48180e63db3995a33905f865dbb55d75
        Estimates the time-varying fundamental frequency of a given signal in a
        way similar to `Praat's autocorrelation <http://www.fon.hum.uva.nl/praat/manual/Sound__To_Pitch__ac____.html>`_ function.
        However, unlike Praat, this function attempts to provide a cycle-by-cycle estimate (see the progressPeriods parameter documentation)

        input:
        output: A dictionary with two entries, both of which are numpy arrays.
                One contains the temporal steps of the measurents, and the other contains the estimated fundamental frequency at the
                respective step.
        '''

        numFrames = len(wavSignalARY)
        readSize = int(numPeriods * float(samplingRateFreq) / Fmin)
        step = 0
        numCycles = 0
        f0DICT = {"time":[], "f0":[]}
        #F0progressPeriods = progressPeriods
        while (step < numFrames):
            print("step:{}, numFrames:{}".format(step, numFrames))
            dataTmp = numpy.zeros(readSize)
            for i in range(readSize):
                idx = i + step - (readSize // 2)
                if idx >= 0 and idx < numFrames:
                    dataTmp[i] = wavSignalARY[idx]

            f0 = self._f0Calculator(dataTmp, samplingRateFreq, Fmin=Fmin, Fmax=Fmax, voicingThreshold=voicingThreshold, applyWindow=applyWindow)

            periodSize = 0
            if f0 > 0:
                periodSize = samplingRateFreq / f0
            t = (step + (periodSize / 2.0))/samplingRateFreq
            if f0 >= Fmin and f0 <= Fmax:
                f0DICT["time"].append(t)
                f0DICT["f0"].append(f0)
            else:
                # set F0 to zero if out of bounds
                f0DICT["time"].append(t)
                f0DICT["f0"].append(0)

            if periodSize > 10:
                step += periodSize * progressPeriods
            else:
                step += 10
        f0DICT["time"] = numpy.array(f0DICT["time"])
        f0DICT["f0"] = numpy.array(f0DICT["f0"])
        return f0DICT

    def f0Detector(self, wavSignalARY, samplingRateFreq, Fmin=50, Fmax=3000, showPlot=False):
        '''
        input:
        output: A dictionary with two entries, both of which are numpy arrays.
                One contains the temporal steps of the measurents, and the other contains the estimated fundamental frequency at the
                respective step.
        '''
        f0DICT = {}

        # <Plotting> TODO:
        if showPlot == False:
            pass
        else:
            time = f0DICT[""]
            plt.plot(time, self.energyLIST)
            plt.title("F0>> window_size:{0}sec.".format(numFrames/self.samplingRateFreq))
            plt.xlabel("Time (sec.)")
            plt.ylabel("F0")
            plt.show()
        # </Plotting>
        return f0DICT

    def formantDetector(self):
        formantLIST = []
        return formantLIST

    def syllableDetector(self):
        syllableTimeLIST = []
        return syllableTimeLIST

    def twMandarinASR(self):
        return None



class VoicePlot:
    def __init__(self, wavFileName=None):
        return None

    def waveformDrawer(self, signal):
        return None

    def mfccDrawer(self, signal):
        return None

    def f1f2Drawer(self, signal):
        return None


class InputError(Exception):
    def __init__(self):
        self.message = "Dude, I can't find any data!"
        return None
    def __str__(self):
        return self.message


if __name__== "__main__":

    startingTime = time.time()
    test = True
    if test == True:
        wavFileName = "./測試用連續錄音/News98 張大春泡新聞專訪 g0v 零時政府參與者 venev - 20140915_07.wav"
        vs = VoiceSound()
        vs.wavFileOpener(wavFileName)
        vs.normalize(vs.wavSignalRawARY, showPlot=True)
        #</ Window Size 設定說明>
        #vs.samplingRateFreq/4 是測試出來的數字設定。 以 取樣率/4 做為 window size 時，第一個音節的參考性較高。
        print("zcr:", vs.zcrDetector(vs.wavSignalNormalizedARY, vs.samplingRateFreq/400, 0.5, showPlot=True))
        #</ Window Size 設定說明>
        vs.energyDetector(vs.wavSignalNormalizedARY, vs.samplingRateFreq/400, 0.5, showPlot=True)
        print(vs.f0Detector(vs.wavSignalNormalizedARY, vs.samplingRateFreq))
        print("Total Time:{}".format(time.time() - startingTime))
