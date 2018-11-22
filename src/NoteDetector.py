import numpy as np
from scipy import signal as sg
import matplotlib.pyplot as plt
import EnergyUtils as eu


def find_notes(signal):
    window = np.hamming(int(48000*20e-3))
    holi = np.abs(np.diff(eu.shorttime_energy(
        signal, window, len(window)), n=1))
    deriv = np.abs(np.diff(holi))
    deriv /= np.max(np.abs(deriv))
    a = sg.find_peaks(deriv, 0.2, distance=4800*5)
    print(a[0])
    plt.plot(deriv)
    for element in a[0]:
        plt.plot(element, deriv[element], 'o')
    plt.show()


find_notes(np.load('./Audios/Himno.npy'))
