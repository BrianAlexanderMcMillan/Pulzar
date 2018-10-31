import sounddevice as sd
from numpy import linalg as LA
import numpy as np

duration = 5  # seconds
global i

i = 0

def print_sound(indata, outdata, frames, time, status):
    global i
    volume_norm = np.linalg.norm(indata)*10
    i += 1
    print ("Volume: ", i, ", ", int(volume_norm), ", ",int(frames))


with sd.Stream(callback=print_sound):
     sd.sleep(duration * 1000)


