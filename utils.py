# vim:ts=4:sts=4:sw=4:expandtab

import numpy as np
from itertools import cycle
from bisect import bisect

#-----------------------------------------------------------------------------#

def group(iterator, count):
    itr = iter(iterator)
    while True:
        yield [itr.next() for i in range(count)]

#-----------------------------------------------------------------------------#

def fft(signal, framerate):
    signal = np.fromstring(''.join(signal), dtype=np.int16)
    fourier = np.fft.fft(signal)/len(signal)
    freqs = np.fft.fftfreq(len(signal))
    freqs = map(lambda x: abs(x * framerate), freqs)
    fourier = map(np.abs, fourier)

    return dict(zip(freqs, fourier))

#-----------------------------------------------------------------------------#

def fft_amps(fft, *args):
    bandwidth = 0
    res = {}
    s = 0
    freqs = sorted(fft.keys())
    for arg in args:
        i = bisect(freqs, arg)
        res[arg] = np.sum([fft[x] for x in freqs[i-bandwidth:i+bandwidth+1]])

    return res

#-----------------------------------------------------------------------------#

def fft_dist(amps):
    s = sum(amps.values())
    res = amps

    for key in res.keys():
        res[key] = res[key]/s if s else 0

    return res

#-----------------------------------------------------------------------------#

def sine_wave(freq, amp, framerate):
    points = np.round(framerate/freq)
    tone = (amp*np.sin(np.r_[0:np.pi*2:np.pi*2/points])).astype(np.int16).tostring()
    
    return cycle(tone)
