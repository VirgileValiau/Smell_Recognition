from tkinter import *
from tkinter import ttk
import numpy as np
from pylsl import StreamInlet, resolve_stream
import matplotlib.pyplot as plt
import pandas as pd
import os
import time


def getStream():
    print('looking for streams...')
    streams = resolve_stream()
    print('got it')
    return StreamInlet(streams[0])

class Acquisition:
    
    def __init__(self,root,Smells,auto_Stop = True,acqui_time=2):
        
        self.acqui_time = acqui_time
        
        data_PATH = '../Smell_Recognition/DATA/'
        self.save_dir = self.create_new_dir(data_PATH)
        
        self.selected = StringVar()
        self.selected.set(Smells[0])
        
        self.recording = BooleanVar()
        self.recording.set(False)
        
        self.recording_txt = StringVar()
        self.recording_txt.set("'Start Acquisition' to start acquire!")
        
        self.recording_smell = StringVar()
        self.recording_smell.set("Nothing")
        
        
        root.title("Acquisition EEG")
        
        mainframe = ttk.Frame(root,padding="15 15 15 15")
        mainframe.grid(column=0, row=0, sticky=(N,W,E,S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        
        
        ttk.Label(mainframe,text="Smells :",borderwidth=2, relief="solid", padding="10 5 10 5").grid(column=1,row=1,sticky=S)
        
        smells_selection = ttk.Frame(mainframe,padding = "10 10 10 10")
        smells_selection.grid(column=1, row=2, sticky=(N,W,E,S))
        
        mainframe.grid(column=0, row=0, sticky=(N,W,E,S))
        
        ttk.Label(mainframe,textvariable = self.selected, padding="10 5 10 5",font=("Arial",20)).grid(column=1,row=3,sticky=S)
        
        for s in Smells:
            i=Smells.index(s)
            ttk.Radiobutton(smells_selection, text=str(i+1)+". "+s, variable = self.selected, value = s).grid(column=i%4, row=i//4, sticky=W)
        
        StartAndStop = ttk.Frame(mainframe,padding = "10 10 10 10")
        StartAndStop.grid(column=1,row=4,sticky=S)
        
        if not auto_Stop:
            ttk.Button(StartAndStop,text="Start Acquisition",command=self.start).grid(column=1,row=1,padx = 20)
            ttk.Button(StartAndStop,text="Stop Acquisition",command=self.stop).grid(column=2,row=1,padx = 20)
        else:
            ttk.Button(StartAndStop,text="Start Acquisition",command=self.start_and_stop).grid(column = 1,row=1,sticky = E)
            
            
        ttk.Label(mainframe,textvariable=self.recording_txt, padding="10 5 10 5",font=("Arial",15)).grid(column=1,row=5,sticky=S)

        
        
    def start(self):
        self.inlet = getStream()
        if (self.recording.get()):
            return
        print("Acquisition Started !")
        self.recording_txt.set("Recording " + self.selected.get())
        self.recording.set(True)
        sample,self.t0 = self.inlet.pull_sample()
        self.Signals = []
        self.timeStamps = []
        self.recording_smell.set(self.selected.get())
    
    def start_and_stop(self):
        self.start()
        t = self.t0
        while (t - self.t0) < self.acqui_time :
            signal,t = self.inlet.pull_sample()
            t += self.inlet.time_correction()
            self.addSignal(signal[:8])
            self.addTimeStamp(t-self.t0)
        self.stop()
    
    def stop(self):
        
        self.recording_txt.set("Acquisition done")
        self.recording.set(False)
        
        self.Signals = np.array(self.Signals)
        
        self.create_file()
        
        self.plot(self.Signals,self.timeStamps)
        
        self.recording_smell.set("Nothing")
        print("Acquisition stopped !")
        
    def create_file(self):
        col =["time"] + ["Electrode " + str(i+1) for i in range(len(self.Signals.T))]
        
        df = pd.DataFrame(np.c_[self.timeStamps,self.Signals],columns = col)
    
        df.to_csv(self.save_dir + self.recording_smell.get() + '.csv')  
    
    def create_new_dir(self,path):
        exist = True
        i=0
        while(exist and i<100):
            if not os.path.isdir(path + 'subject_' + str(i)):
                os.makedirs(path + 'subject_' + str(i))
                exist = False
            i +=1
        return path + 'subject_' + str(i-1) + '/'
    
    def plot(self,signals,time):
        plt.figure()
        for i,s in enumerate(signals.T) :
            plt.plot(time,label="Electrode n°" + str(i+1))
            plt.legend()
            plt.show()

        
    def addSignal(self,s):
        self.Signals.append(s)
    
    def addTimeStamp(self,t):
        self.timeStamps.append(t)
            
def pull_sample_or_not(acqui):
    if acqui.recording.get():
        signal,t = acqui.inlet.pull_sample()
        acqui.addSignal(signal[:8])
        acqui.addTimeStamp(t-acqui.t0)
    root.after(1,lambda: pull_sample_or_not(acqui))



odors = ["smell " + str(i+1) for i in range(12)]
root=Tk()
acqui = Acquisition(root,odors,auto_Stop=True,acqui_time = 10)
root.after(1, lambda: pull_sample_or_not(acqui))
root.mainloop()
