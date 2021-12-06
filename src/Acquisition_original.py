import tkinter
import numpy as np
from pylsl import StreamInlet, resolve_stream
import matplotlib.pyplot as plt
import keyboard


def getStream():
    print('looking for streams...')
    streams = resolve_stream()
    print('got it')
    return StreamInlet(streams[0])



inlet = getStream()
signal_sampling=500

registration = False
run = True
n_iter = 0

'''
m = tkinter.Tk()
m.title("random page")
m.geometry('720x420')
tkinter.Label(m, text="Experiment Begin", fg="red", font=('Helvetica 28')).pack(pady=150)
m.mainloop()
'''
while run:
    
    if n_iter%signal_sampling == 0 and registration:
        Signal_unit ,t = inlet.pull_sample()
        Signals.append(Signal_unit)
        time.append(t-t0)
      
    if keyboard.is_pressed("enter") and not registration:
        registration = True
        Signal_unit,t0 = inlet.pull_sample()
        Signals = []
        time = []
        print('registration started')
                
    if keyboard.is_pressed("esc") and registration:
        registration = False
        run = False
        print('registration ended')
        
                   
time = np.array(time)

Signals = np.array(Signals)

print(time)


np.savetxt('../Smell_Recognition/DATA/trials/try.txt', np.c_[time,Signals], delimiter=' ')

#for s in Signals.T:
#    plt.plot(time,s)
#    plt.show()