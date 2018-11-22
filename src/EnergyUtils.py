import numpy as np

def shorttime_energy(signal, window, step_size):
    short_time_energy = []
    squared_signal = signal**2
    squared_window = window**2
    for i in range(0, len(signal), step_size):
        squared_signal_segment = squared_signal[i:i+len(window)]
        squared_signal_window_convolution = np.convolve(squared_signal_segment, squared_window, 'full')
        short_time_energy.append(np.sum(squared_signal_window_convolution))
    return np.ndarray.flatten(np.array(short_time_energy))


def binary_voice_detector(signal, fs=48000, th=0.02, custom_params=None):
    # Error Validation
    window = np.hamming(int(fs*20e-3))
    step_size = int(len(window))
    # Main function
    norm_signal = signal / np.max(np.abs(signal))
    shte = shorttime_energy(norm_signal, window, step_size)
    shte /= np.max(np.abs(shte))
    detection = []
    for estimation in shte:
            detection.extend([int(estimation > th)]*len(window))
    return detection


        




    


    
