import sounddevice as sd
from numpy import linalg as LA
import numpy as np

samplerate = 44100  # Hertz
duration = 0.3  # seconds
filename = 'output.wav'

for i in range(50):
    indata = sd.rec(int(samplerate * duration), samplerate=samplerate,
                channels=2, blocking=True)

    volume_norm = np.linalg.norm(indata)*10

    print ("Volume ", int(volume_norm))


