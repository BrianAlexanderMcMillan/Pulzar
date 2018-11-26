import sounddevice as sd
from numpy import linalg as LA
import numpy as np

SampleRate = 44100  # Hertz
SamplingDuration = 0.1  # seconds
TriggerValue = 200
TriggerActive = False

for i in range(50):
    indata = sd.rec(int(SampleRate * SamplingDuration), samplerate=SampleRate,
                channels=2, blocking=True)

    Volume = np.linalg.norm(indata)*10
    if Volume > TriggerValue:
        TriggerActive = True
    else:
        TriggerActive = False

    print ("Volume ", int(Volume), ", ", TriggerActive)


