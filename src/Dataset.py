import numpy as np
from BandPower import *
import glob

def make_img_from_bpve(BPVE,wave):
    ve = BPVE[:,wave,:]
    Grid = np.array([[0, 1, 0],
            [2, 3, 4],
            [6, 5, 8],
            [0, 7, 0]])
    
    IMGS = np.zeros((len(ve[0]),len(Grid),len(Grid[0])))
    for i in range(8):
        x,y = np.where(Grid==i+1)
        IMGS[:,x[0],y[0]] = ve[i][:]
    return IMGS

def make_videos(data,nb_samples):
    PowerSpectrum = toBandPower(data)
    BPVE = BP_varying_energy(PowerSpectrum,data,nb_samples)
    nb_elec,nb_waves,nb_samples = BPVE.shape
    VIDEOS = []
    for wave in range(nb_waves):
        IMGS = make_img_from_bpve(BPVE,wave)
        VIDEOS.append(IMGS)
    return VIDEOS

def make_simple_image(data,nb_samples):
    PowerSpectrum = toBandPower(data)
    VE = BP_varying_energy(PowerSpectrum,data,nb_samples)
    nb_elec,nb_waves,nb_samples = VE.shape
    img = np.zeros((nb_elec*nb_waves,nb_samples))
    for i in range(nb_elec):
        for j in range(nb_waves):
            img[i+j*nb_elec] = VE[i][j]
    return img

def create_img_dataset(DATA,nb_samples,dir_name):
    IMGS=[]
    labels = []
    for dir in glob.glob(DATA+'/*'):
        label = 0
        for file in glob.glob(dir+'/*'):
            data = pd.read_csv(file)
            img = make_simple_image(data,nb_samples)
            IMGS.append(img.reshape(-1))
            labels.append(label)
            label += 1
    return np.array(IMGS),np.array(labels)

def create_video_dataset(DATA):
    return ...