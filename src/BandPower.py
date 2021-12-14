import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.fftpack import rfft, irfft, fftfreq
from scipy import integrate as intg


def toBandPower(EEG):
    """from an eeg dataFrame, decompose the signal into 5 frequency bands:
        delta (0.1,4)Hz, theta(4,8), alpha(8,12), beta(12,30), gamma(30,100)

    Args:
        EEG (DataFrame): dataframe containing the signals from the 8 electrodes and the time.
    """
    
    time = EEG['time']
    Signal = []
    for i in range(8):
        s = np.array(EEG['Electrode ' + str(i+1)])
        s = centering_and_normalize(s)
        Signal.append(s)
    
    #res = np.zeros((len(Signal),5,len(Signal[0])))
    res = []
    for s in Signal:
        res.append(decomposition(s,time))
    return np.array(res)

def decomposition(x,time):
    W = fftfreq(x.size, d=time[1]-time[0])
    f_signal = rfft(x)

    delta = bandWith(W,f_signal,0.1,4)
    theta = bandWith(W,f_signal,4,8)
    alpha = bandWith(W,f_signal,8,12)
    beta = bandWith(W,f_signal,12,30)
    gamma = bandWith(W,f_signal,30,100)
    
    return [delta,theta,alpha,beta,gamma]
    
def bandWith(W,f_signal,f1,f2):
    cut_f = f_signal.copy()
    cut_f[(W<f1)] = 0
    cut_f[(W>f2)] = 0
    return irfft(cut_f)

def centering_and_normalize(s):
    s = s-np.mean(s) # On centre le signal
    s = s/np.linalg.norm(s) # On normalise le signal 
    return s

def plot(time,BPS):
    for i,bp in enumerate(BPS):
        for j,cut_s in enumerate(bp):
            plt.subplot(5,1,j+1)
            plt.plot(time,cut_s)
        plt.show()
        
def energie(time,x):
    return intg.simps(np.abs(x)**2,time)

def get_BPEnergy(BPS,df):
    time=df['time']
    E_original_s = []
    BPEnergy = []
    for i,elec in enumerate(BPS):
        E_original_s.append(energie(time,centering_and_normalize(df['Electrode '+str(i+1)])))
        E_elec = []
        for cut_s in elec:
            E_elec.append(energie(time,cut_s)/E_original_s[i])
        BPEnergy.append(E_elec)
    return np.array(BPEnergy)

def meanEnergy(BPEnergy):
    means=np.zeros(5)
    for i,wave in enumerate(BPEnergy.T):
        means[i] = np.mean(wave)
    return means

def plot_bandPower_energy(BPEnergy):
    fig, axs = plt.subplots(4, 2, constrained_layout=True,figsize=(10,10))
    fig.suptitle("Band Power Energy",fontsize=30)
    for i,E in enumerate(BPEnergy):
        axs[i//2][i%2].bar(range(5),height = E,tick_label=['delta','theta','alpha','beta','gamma'])
        axs[i//2][i%2].set_title('Electrode '+str(i+1))
    plt.show()
    
def plot_raw_signal(df):
    time=np.array(df['time'])

    fig, axs = plt.subplots(8,1, constrained_layout=True,figsize=(10,8))
    fig.suptitle('Raw Signals',fontsize = 30)
    for i in range(8):
        s = df['Electrode '+str(i+1)]
        s = centering_and_normalize(s)
        axs[i].plot(time,s)
