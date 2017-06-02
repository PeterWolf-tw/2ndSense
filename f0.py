#!/usr/bin/env python3
# -*- coding:utf-8 -*-


from pylab import*
from scipy.io import wavfile
import numpy

sampFreq, snd = wavfile.read('440_sine.wav')
snd = snd / (2.**15)
s1 = snd[:,0] 
n = len(s1) 
p = fft(s1) # take the fourier transform 
nUniquePts = int(ceil((n+1)/2.0))
p = p[0:nUniquePts]
p = abs(p)
p = p / float(n) # scale by the number of points so that
                 # the magnitude does not depend on the length 
                 # of the signal or on its sampling frequency  
p = p**2  # square it to get the power 

# multiply by two (see technical document for details)
# odd nfft excludes Nyquist point
if n % 2 > 0: # we've got odd number of points fft
    p[1:len(p)] = p[1:len(p)] * 2
else:
    p[1:len(p) -1] = p[1:len(p) - 1] * 2 # we've got even number of points fft

freqArray = arange(0, nUniquePts, 1.0) * (sampFreq / n);

i = 0
for f in freqArray/1000:
    if f < 0.7:
        i = i+1

m = mean(10*log10(p)[:i])
print(m)

maxFreq = max(10*log10(p)[:i])
print(maxFreq)

f0 = freqArray[numpy.where(10*log10(p)[:i] == maxFreq)]
print(f0)

plot(freqArray/1000, 10*log10(p), color='k')
plot(freqArray/1000, [m]*len(p), color='r')
xlabel('Frequency (kHz)')
ylabel('Power (dB)')
plt.show()

