
import numpy as np
from pylsl import StreamInlet, resolve_stream
import matplotlib.pyplot as plt


def getStream():
    print('looking for streams...')
    streams = resolve_stream()
    print('got it')
    return StreamInlet(streams[0])


inlet = getStream()
run = True

while run:
    print('1')
    print(inlet.pull_sample())
    print('2')