import numpy as np
from scipy import signal as sg
import matplotlib.pyplot as plt
import EnergyUtils as eu
import Yin as yn
import MidiConvert


def most_common(lst):
    return max(set(lst), key=lst.count)


def find_notes(signal):
    holi = np.abs(np.diff(signal**2, 10))
    deriv = np.abs(np.diff(holi))
    deriv /= np.max(np.abs(deriv))
    deriv = np.convolve(deriv, [1]*300, 'same')
    haa = 0
    a = []
    arr = []
    plt.plot(deriv)
    plt.show()
    while haa != 10:
        arr = np.random.rand(6, 1).reshape(-1)
        print(arr)
        a = sg.find_peaks(deriv, arr[0], threshold=arr[1],
                          prominence=[arr[2]], width=[arr[3]], distance=6000)
        haa = len(a[0])
        print(haa)
    print(a[0])
    print(arr)
    plt.plot(deriv)
    for element in a[0]:
        plt.plot(element, deriv[element], 'o')
    plt.show()


def find_notes3(signal):
    holi = np.abs(np.diff(signal**2, 3))
    deriv = np.abs(np.diff(holi))
    deriv /= np.max(np.abs(deriv))
    haa = 0
    a = []
    arr = [0.14312914, 0.06851706, 0.12012904,
           0.16185419, 0.61722255, 0.97487688]
    a = sg.find_peaks(deriv, arr[0], threshold=arr[1],
                      prominence=[arr[2]], width=[arr[3]], distance=4800*2.5)
    plt.plot(deriv)
    for element in a[0]:
        plt.plot(element, deriv[element], 'o')
    plt.show()


# [0.14312914, 0.06851706, 0.12012904, 0.16185419, 0.61722255, 0.97487688]


def find_notes2(signal):
    holi = np.abs(np.diff(signal**2, 10))
    deriv = np.abs(np.diff(holi))
    deriv = np.convolve(deriv, [1]*2000, 'same')
    deriv /= np.max(np.abs(deriv))
    return (deriv > .2).astype(int)


def get_events(signal, window=1500):
    a = find_notes2(signal)
    plt.plot(a)
    plt.show()
    a = np.diff(a)
    arr = []
    for ind in range(0, len(a), window):
        arr.append(np.round(np.sum(a[ind:ind+window])))
    ret = [{
        'duration': 0,
        'pitch': 0
    }]
    last_ev = 0
    time = 0
    pc = yn.Yin()
    ans = pc.yin(signal, 48000, 2048, 1024, 100, 2000, .2)[0]
    plt.plot(ans)
    plt.show()
    for ind, element in enumerate(arr):
        try:
            if(arr[ind] > 0 and (np.abs(arr[ind-1]) != 1)):
                estim = pc.yin2(signal[int(48000*last_ev):int(48000*time)])
                print(estim)
                ret[-1]['duration'] = time - last_ev
                ret.append({
                    'duration': 0,
                    'pitch': int(round(12*np.log2(estim/440) + 69)) if estim > 0 else 0
                })
                last_ev = time
            if(arr[ind] < 0 and (np.abs(arr[ind-1]) != 1)):
                ret[-1]['duration'] = time - last_ev
                ret.append({
                    'duration': 0,
                    'pitch': 0
                })
                last_ev = time
            time = 1500/48000 * ind
        except:
            time = 1500/48000 * ind
    MidiConvert.to_midi2(ret[:-1])
    print(ret)


# find_notes2(np.load('./Audios/LastAudio.npy'))
get_events(np.load('./Audios/LastAudio.npy'))
