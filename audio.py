import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pyaudio
import numpy as np
import signal
from itertools import count

plt.style.use('fivethirtyeight')

# USE THIS FILE TO RECORD YOUR OWN AUDIO

# TODO: figure out noise reduction, fft stuff, use the oop way, make it look cool
# TODO: # https://github.com/CoreyMSchafer/code_snippets/blob/master/Python/Matplotlib/09-LiveData/snippets.txt 
# use this to for example instead of cla() 


# # to ensure the script finishes even if a keyboard interrupt is done
# def signal_handler(signal, frame):
#     global interrupted
#     interrupted = True
# interrupeted = False
# signal.signal(signal.SIGINT, signal_handler)

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

p=pyaudio.PyAudio() # start the PyAudio Class

for i in range(0, p.get_device_count()):
    dic = p.get_device_info_by_index(i)
    if 'microphone' in dic['name'].lower():
        INDEX = i
        CHANNELS = dic['maxInputChannels']
        RATE = int(dic['defaultSampleRate'])
        print('Using {} as the input device'.format(dic['name']))

if INDEX is None:
    print('USING DEFAULT DEVICE')

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

print('recording...')

def init():
    ax.set_xlim(left=MIN_X, right=MAX_X)
    ax.set_ylim(bottom=MIN_X, top=MAX_X)
    ax.set_zlim(MIN_Y, MAX_Y)
    # fig.set_facecolor('black')

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

ani = FuncAnimation(fig, animation, interval=10, init_func=init)

fig.tight_layout()
plt.show()

stream.stop_stream()
stream.close()
p.terminate()

print('finished recording')