#
#  sound_delay.py
#

"""
Record sound and play it back after a delay.
"""

import multiprocessing as mp
import time

CHUNK = 4096
CHANNELS = 1
RATE = 44100
DELAY_SECONDS = 5
DELAY_SIZE = DELAY_SECONDS * RATE / (10 * CHUNK)


def record_to_file():
    import pyaudio
    import wave
     
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 2048
    FILE_TIME = 20
    WAVE_OUTPUT_FILENAME = "file.wav"
     
    audio = pyaudio.PyAudio()
     
    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK,
                    input_device_index= 3)
    print "recording..."
    frames = []
     
    for i in range(0, int(RATE / CHUNK * FILE_TIME)):
        data = stream.read(CHUNK)
        frames.append(data)
    print "finished recording"
     
     
    # stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()
     
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()


def feed_queue(q):
    import pyaudio
    import numpy

    FORMAT = pyaudio.paInt16
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK,
                    input_device_index = 3)

    while True:
        frame = []
        for i in xrange(10):
            frame.append(stream.read(CHUNK, exception_on_overflow = False))
        data_ar = numpy.fromstring(''.join(frame), 'int16')
        if q.full():
            q.get_nowait()
        q.put(data_ar)


queue = mp.Queue(maxsize=DELAY_SIZE)
p = mp.Process(target=feed_queue, args=(queue,))
p.start()

#Kick off record audio function process
recordProcess = mp.Process(target = record_to_file)
recordProcess.start()


# give some time to bufer
time.sleep(DELAY_SECONDS)

import pygame.mixer
pygame.mixer.init()
S = pygame.mixer.Sound
while True:
    d = queue.get()
    S(d).play()
