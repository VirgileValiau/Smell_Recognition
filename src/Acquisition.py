from tkinter import *
from tkinter import ttk
import numpy as np
from pylsl import StreamInlet, resolve_stream

Smells = ["Smell 1","Smell 2","Smell 3","Smell 4",
          "Smell 5","Smell 6","Smell 7","Smell 8",
          "Smell 9","Smell 10","Smell 11","Smell 12"]

def getStream():
    print('looking for streams...')
    streams = resolve_stream()
    print('got it')
    return StreamInlet(streams[0])

class Acquisition:
    
    def __init__(self,root):
        
        root.title("Acquisition EEG")
        
        mainframe = ttk.Frame(root,padding="15 15 15 15")
        mainframe.grid(column=0, row=0, sticky=(N,W,E,S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        
        self.selected=Smells[0]
        ttk.Label(mainframe,text="Smells :",borderwidth=2, relief="solid", padding="10 5 10 5").grid(column=1,row=1,sticky=S)
        
        smells_selection = ttk.Frame(mainframe,padding = "10 10 10 10")
        smells_selection.grid(column=1, row=2, sticky=(N,W,E,S))
        
        mainframe.grid(column=0, row=0, sticky=(N,W,E,S))
        
        ttk.Label(mainframe,textvariable =self.selected, padding="10 5 10 5",font=("Arial",20)).grid(column=1,row=3,sticky=S)
        
        for s in Smells:
            i=Smells.index(s)
            ttk.Radiobutton(smells_selection, text=str(i+1)+". "+s, variable = self.selected, value = s).grid(column=i%4, row=i//4, sticky=W)
        
        StartAndStop = ttk.Frame(mainframe,padding = "10 10 10 10")
        StartAndStop.grid(column=1,row=4,sticky=(N,W,E,S))
        
        ttk.Button(StartAndStop,text="Start Acquisition",command=self.start).grid(column=1,row=1,padx = 30)
        ttk.Button(StartAndStop,text="Stop Acquisition",command=self.stop).grid(column=2,row=1,padx = 30)
        
        
    def start(self):
        print("Acquisition Started !")
    
    def stop(self):
        print("Acquisition Stopped !")
        
root=Tk()
Acquisition(root)
root.mainloop()