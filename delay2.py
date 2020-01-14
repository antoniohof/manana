import pyaudio
import wave
import time
from multiprocessing import Process

def record_audio(AUDIO_FILE):
    #Create audio stream    
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK,
                    input_device_index = 3)

    # begin recording
    print"* recording audio clip: ",AUDIO_FILE

    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK, exception_on_overflow = False)
        frames.append(data)

    #print"* done recording audio clip:", AUDIO_FILE

    #cleanup objects
    stream.stop_stream()
    stream.close()

    #save frames to audio clips
    print"* sending data to audio file:", AUDIO_FILE
    wf = wave.open(AUDIO_FILE , 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def play_audio(AUDIO_FILE):
    #open saved audio clip
    wf2 = wave.open(AUDIO_FILE , 'rb')

    #Introduce  playback delay


    #Define playback audio stream
    stream2 = p.open(format=p.get_format_from_width(wf2.getsampwidth()),
                channels=wf2.getnchannels(),
                rate=wf2.getframerate(),
                output=True,
                output_device_index = 3)

    data = wf2.readframes(CHUNK)
    print" *************************** playing back audio file:", AUDIO_FILE
    while data != '':        
        stream2.write(data)
        data = wf2.readframes(CHUNK)

    stream2.stop_stream()
    stream2.close()

    p.terminate()

if __name__=='__main__':

    CHUNK = 2048
    FORMAT = pyaudio.paInt16
    CHANNELS = 2               #stereo
    RATE = 44100
    RECORD_SECONDS = 30         #record chunks of 5 sec
    TOTAL_RECORD_NUMBER = 50    # total chunks to record and play

    x = 0

    while x < TOTAL_RECORD_NUMBER:

        #define audio file clip
        AUDIO_FILE = "recordings/audio{0}.wav".format(x)

        #initialize pyaudio
        p = pyaudio.PyAudio()        

        #Kick off record audio function process
        # p1 = Process(target = record_audio(AUDIO_FILE))
        # p1.start()

        #kick off play audio function process
        # p2 = Process(target = play_audio(AUDIO_FILE))        
        # p2.start()

        # p1.join()
        # p2.join()
        procs = []
        procs.append(Process(target=record_audio, args=(AUDIO_FILE,)))

                #define audio file clip
        if x > 0:
            AUDIO_FILE_TOPLAY = "recordings/audio{0}.wav".format(x - 1)
            procs.append(Process(target=play_audio, args=(AUDIO_FILE_TOPLAY,)))

        #     t1 = Process(target=test1, args=(q,))

        #increment record counter
        x += 1
        map(lambda x: x.start(), procs)
        map(lambda x: x.join(), procs)

