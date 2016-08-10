# vim:ts=4:sts=4:sw=4:expandtab

import pulseaudio as pa
import numpy as np
import bitstring as bs
from itertools import islice
from utils import group, fft, fft_dist, fft_amps, sine_wave
from parser import Parser

#-----------------------------------------------------------------------------#

ZERO_FREQ = 880
ONE_FREQ = 2600

#-----------------------------------------------------------------------------#

class Receiver(object):
    
    def __init__(self, addr, bps, framerate):
        self.addr = addr
        self.framerate = framerate
        self.framewidth = framerate / bps
        self.bps = bps

        self.recorder = pa.simple.open(
            direction=pa.STREAM_RECORD,
            format=pa.SAMPLE_S16LE,
            rate=framerate,
            channels=1)
        self.input_buffer = []

    def record(self, frames_count):
        self.input_buffer = []                    # clear buffer
        cnt = int(frames_count * self.framewidth) # how many points to read

        while len(self.input_buffer) < cnt:
            self.input_buffer += self.recorder.read(min(100, cnt-len(self.input_buffer)))

    def synchronize(self, tries=20):
        diff = 1                   # amplitude ratio difference

        while diff > 0.05 and tries > 0:
            self.record(0.3)       # move window by 0.3 of frame width
            self.record(1)         # record one frame

            # compute fft and signal distribution along frequencies
            _fft = fft(self.input_buffer, self.framerate)
            amps = fft_amps(_fft, ZERO_FREQ, ONE_FREQ)
            dist = fft_dist(amps)

            # we try to minimize amplitude of the lesser signal in the window
            diff = min(dist.values())
            # limit how many windows we can test
            tries -= 1

        return (diff <= 0.05)            

    def record_string(self, n=65536, z=8):
        inp = bs.BitArray()        # input bit array
        trailing_zeros = 0

        min_ = 10000

        while (len(inp) < n) and (trailing_zeros < z):  # read at most n bytes or z zeros
            self.record(1)                              # record one frame

            # compute fft and signal distribution along frequencies
            _fft = fft(self.input_buffer, self.framerate)
            amps = fft_amps(_fft, ZERO_FREQ, ONE_FREQ)

            if amps[ZERO_FREQ] < 1000 and amps[ONE_FREQ] < 1000:
                break

            dist = fft_dist(amps)
            min_ = min(min_, max(dist.values()))

            if dist[ZERO_FREQ] > dist[ONE_FREQ]:
                inp.append('0b0')
                trailing_zeros += 1
            else:
                inp.append('0b1')
                trailing_zeros = 0

        print min_
        return inp

    def listen(self, addr):
        while True:
            self.record(1)                                # record one frame
            _fft = fft(self.input_buffer, self.framerate) # compute fft
            amps = fft_amps(_fft, ZERO_FREQ, ONE_FREQ)

            if amps[ZERO_FREQ] > 1000 or amps[ONE_FREQ] > 1000:
                if not self.synchronize():
                    continue
                
                string = self.record_string()
                if not string:
                    continue

                print "------BINARY INPUT START-------"
                print string.bin
                print "------BINARY INPUT END-------"

                (src_addr, dest_addr, msg) = Parser.decode(string)

                if dest_addr == self.addr and msg is not None:
                    return (src_addr, msg)

#-----------------------------------------------------------------------------#

class Transmitter(object):

    def __init__(self, addr, bps, framerate, amp):
        self.addr = addr
        self.framerate = framerate
        self.framewidth = framerate / bps
        self.bps = bps
        self.amp = amp

        self.one_sine = list(
            islice(
                sine_wave(ONE_FREQ, self.amp, self.framerate),
                self.framewidth))
        self.zero_sine = list(
            islice(
                sine_wave(ZERO_FREQ, self.amp, self.framerate),
                self.framewidth))
        
        self.player = pa.simple.open(
            direction=pa.STREAM_PLAYBACK,
            format=pa.SAMPLE_S16LE,
            rate=framerate,
            channels=1)
        self.output_buffer = []

    def play(self):
        self.player.write(''.join(self.output_buffer))
        
    def write_bit(self, bit):
        self.output_buffer += (self.zero_sine if bit == 0 else self.one_sine)

    def play_bitarray(self, msg):
        self.output_buffer = []
        for i in msg:
            self.write_bit(i)
        self.play()

    def send_message(self, msg_addr, msg):
        out = bs.BitArray()
        out.append(bs.BitArray('0b10') * 32)
        out.append(bs.BitArray('0b0')  * 5)
        out.append(Parser.encode(self.addr, msg_addr, bs.BitArray(bytes=msg)))
        out.append(bs.BitArray('0b0')  * 16)

        print "------BINARY OUTPUT START-------"
        print out.bin
        print "------BINARY OUTPUT END-------"

        self.play_bitarray(out)
