import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pyaudio
import numpy as np
import signal
from itertools import count
import wave

plt.style.use('fivethirtyeight')

# USE THIS FILE TO RECORD YOUR OWN AUDIO

# CONSTANTS:
MAX_Y = 20000
MIN_Y = -20000

MAX_X = 4096
MIN_X = 0

CHUNK = 4 * 1024 # number of data points to read at a time
RATE = None # time resolution of the recording device (Hz)
FORMAT = pyaudio.paInt16 # audio format
INDEX = None # input device index
CHANNELS = None # number of input channels for input device
FILENAME = 'practice.wav' # name of file created when you want to classify your own audio recorded by your microphone

p=pyaudio.PyAudio() # start the PyAudio Class

# find the laptop microphone or any other external microphone
for i in range(0, p.get_device_count()):
    dic = p.get_device_info_by_index(i)
    if 'microphone' in dic['name'].lower():
        INDEX = i
        CHANNELS = dic['maxInputChannels']
        RATE = int(dic['defaultSampleRate'])
        print('Using {} as the input device'.format(dic['name']))

if INDEX is None:
    print('USING DEFAULT DEVICE')

# open pyAudio stream
stream = p.open(
    format=FORMAT, 
    channels = CHANNELS, 
    rate=RATE, 
    input=True, 
    output=True, 
    frames_per_buffer=CHUNK, 
    input_device_index=INDEX
)

fig = plt.figure()
ax = plt.axes(projection='3d')

# just to ensure that the microphone is properly recording
print('recording...')

frames = []

# create the animation
def init():
    ax.set_xlim(left=MIN_X, right=MAX_X)
    ax.set_ylim(bottom=MIN_X, top=MAX_X)
    ax.set_zlim(MIN_Y, MAX_Y)
    # fig.set_facecolor('black')

# update every 10 miliseconds
def update():
    ax.set_xlim(left=MIN_X, right=MAX_X)
    ax.set_ylim(bottom=MIN_X, top=MAX_X)
    ax.set_zlim(MIN_Y, MAX_Y)
    # ax.set_title('Waveform')
    ax.grid(True)
    ax.tick_params(bottom=True, top=True)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    # ax.set_axis_off()
    fig.set_facecolor('black')
    data = stream.read(CHUNK)
    frames.append(data)

# create the matplotlib animation
def animation(i):
    data = stream.read(CHUNK, exception_on_overflow=False)
    unpacked = np.frombuffer(data, dtype=np.int16)
    x_vals = np.arange(start=0, stop=len(unpacked), dtype=np.int16)
    y_vals = np.arange(start=0, stop=len(unpacked), dtype=np.int16)
    num = np.max(unpacked)
    num2 = np.min(unpacked)
    print(num, num2)
    ax.cla()
    update()
    ax.plot(x_vals, y_vals, unpacked)

# Initialize function
ani = FuncAnimation(fig, animation, interval=10, init_func=init)


fig.tight_layout()
plt.show()

stream.stop_stream()
stream.close()
p.terminate()

# record your own audio
wavFile = wave.open(FILENAME, 'wb')
wavFile.setnchannels(CHANNELS)
wavFile.setsampwidth(p.get_sample_size(FORMAT))
wavFile.setframerate(RATE)
wavFile.writeframes(b''.join(frames))
wavFile.close()

print('finished recording')