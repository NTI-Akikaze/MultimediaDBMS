import librosa
import numpy as np
from wavefile import WaveFile
import pickle

def normalize(vector):
    with open('normalize.obj', 'rb') as input:
        min_arr = pickle.load(input)
        max_arr = pickle.load(input)
        vector = np.array(vector)
    return (vector-min_arr) / (max_arr-min_arr)

def average_energy(arr):
    return np.average(arr*arr)

def createWaveFileFromPath(path):
    x,sr = librosa.load(path)
    # chroma_stft = librosa.feature.chroma_stft(x,sr)
    ave_energy = average_energy(x);
    rms = librosa.feature.rms(x)
    spec_cent = librosa.feature.spectral_centroid(x,sr)
    spec_bw = librosa.feature.spectral_bandwidth(x,sr)
    rolloff = librosa.feature.spectral_rolloff(x,sr)
    zcr = librosa.feature.zero_crossing_rate(x)
    # feature_vector = [np.mean(chroma_stft), np.mean(rms), np.mean(spec_cent), np.mean(spec_bw), np.mean(rolloff), np.mean(zcr)]
    feature_vector = [ave_energy, np.mean(rms), np.mean(spec_cent), np.mean(spec_bw), np.mean(rolloff), np.mean(zcr)]
    
    # mfcc = librosa.feature.mfcc(x,sr)
    # for e in mfcc:
        # feature_vector.append(np.mean(e))
    feature_vector = normalize(feature_vector)
    
    obj = WaveFile(feature_vector, path)
    return obj   
    
