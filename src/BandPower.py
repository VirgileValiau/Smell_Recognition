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
    for i in range(len(EEG.columns)-2):
        s = np.array(EEG['Electrode ' + str(i+1)])
        #s = centering_and_normalize(s)
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
    beta  = bandWith(W,f_signal,12,30)
    gamma = bandWith(W,f_signal,30,48)
    
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
        
def energy(time,x):
    return intg.simps(np.abs(x)**2,time)

def get_BPEnergy(BPS,df):
    time=df['time']
    E_original_s = []
    BPEnergy = []
    for i,elec in enumerate(BPS):
        E_original_s.append(energy(time,df['Electrode '+str(i+1)]))#centering_and_normalize(df['Electrode '+str(i+1)])))
        E_elec = []
        for cut_s in elec:
            E_elec.append(energy(time,cut_s)/E_original_s[i])
        BPEnergy.append(E_elec)
    return np.array(BPEnergy)

def meanEnergy(BPEnergy):
    means=np.zeros(5)
    for i,wave in enumerate(BPEnergy.T):
        means[i] = np.mean(wave)
    return means

def varying_energy(x,time,nb_samples=10):
    if nb_samples>=len(time):
        print("nb_samples is too big, setting it to len(time)/2")
        nb_samples=len(time)//2
    step_time = np.max(time)/nb_samples
    i=1
    res=[]
    done=False
    step_size = len(time[time<step_time])
    while not done:
        sub_x = x[step_size*(i-1):step_size*i]
        sub_time = time[step_size*(i-1):step_size*i]
        res.append(energy(sub_time,sub_x))
        i += 1
        if step_time*i>np.max(time):
            done=True
    return res

def BP_varying_energy(BPS,df,nb_samples=20):
    time=df['time']
    BPVE=[]
    for elec_bps in BPS:
        elecVE=[]
        for wave in elec_bps:
            elecVE.append(varying_energy(wave,time,nb_samples=nb_samples))
        BPVE.append(elecVE)
    return np.array(BPVE)

def plot_bandPower_signal(BPS,df,electrode):
    time=df['time']
    fig, axs = plt.subplots(5, 1, constrained_layout=True,figsize=(10,8))
    fig.suptitle("Band Power signals for electrode " + str(electrode),fontsize=30)    
    for i,bandPower in enumerate(BPS[electrode-1]):
        axs[i].plot(time,bandPower)

def plot_raw_signal(df):
    time=np.array(df['time'])
    fig, axs = plt.subplots(len(df.columns)-2,1, constrained_layout=True,figsize=(10,8))
    fig.suptitle('Raw Signals',fontsize = 30)
    for i in range(len(df.columns)-2):
        s = df['Electrode '+str(i+1)]
        s = centering_and_normalize(s)
        axs[i].plot(time,s)
        
def plot_bandPower_energy(BPEnergy):
    fig, axs = plt.subplots(4, 2, constrained_layout=True,figsize=(10,10))
    fig.suptitle("Band Power Energy",fontsize=30)
    for i,E in enumerate(BPEnergy):
        axs[i//2][i%2].bar(range(5),height = E,tick_label=['delta','theta','alpha','beta','gamma'])
        axs[i//2][i%2].set_title('Electrode '+str(i+1))
    plt.show()
    
