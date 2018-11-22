import numpy as np
class Yin:  
    def __init__(self):
        return
    
    def diff(self,x,tau_max):
        """
        --------------------------------------
        DESCRIPTION:
        - Compute difference function of data x
        --------------------------------------            
        INPUT:        
        - x: audio data
        - tau_max: integration window size
        --------------------------------------
        OUTPUT:
        - return: difference function [np.array]
        --------------------------------------
        """
        x = np.array(x, np.float64)
        w = x.size
        tau_max = min(tau_max, w)
        x_cumsum = np.concatenate((np.array([0.]), (x * x).cumsum()))
        size = w + tau_max
        p2 = (size // 32).bit_length()
        nice_numbers = (16, 18, 20, 24, 25, 27, 30, 32)
        size_pad = min(x * 2 ** p2 for x in nice_numbers if x * 2 ** p2 >= size)
        fc = np.fft.rfft(x, size_pad)
        conv = np.fft.irfft(fc * fc.conjugate())[:tau_max]
        return x_cumsum[w:w - tau_max:-1] + x_cumsum[w] - x_cumsum[:tau_max] - 2 * conv

    def cmndf(self,df):
        """
        -------------------------------------------------------------
        DESCRIPTION:
        - Compute cumulative mean normalized difference function (CMND)
        -------------------------------------------------------------
        INPUT:
        - df : Difference function 
        -------------------------------------------------------------
        OUTPUT:
        - return : cumulative mean normalized difference function 
        -------------------------------------------------------------
        """
        cmndf = df[1:] * range(1, len(df)) / np.cumsum(df[1:]).astype(float) #scipy method
        return np.insert(cmndf, 0, 1)
    
    def get_pitch(self,cmdf, tau_min, tau_max, harmo_th=0.1):
        """
        ---------------------------------------------------------------------------------------------
        DESCRIPTION:
        - Estimates fundamental period of a frame based on CMND function 
        ---------------------------------------------------------------------------------------------
        INPUT:
        - cmdf: Cumulative Mean Normalized Difference function
        - tau_min: minimum period for speech
        - tau_max: maximum period for speech
        - harmo_th: harmonicity threshold to determine if it is necessary to compute pitch frequency
        ---------------------------------------------------------------------------------------------
        OUTPUT
        return: fundamental period if there are values under threshold, 0 otherwise
        """
        tau = tau_min
        while tau < tau_max:
            if cmdf[tau] < harmo_th:
                while tau + 1 < tau_max and cmdf[tau + 1] < cmdf[tau]:
                    tau += 1
                return tau
            tau += 1
        return 0    # if unvoiced
    
    def yin(self, sig, sr, w_len=512, w_step=256, f0_min=100, f0_max=500, harmo_thresh=0.1):
        """
        --------------------------------------------------------------------------------------------------------
        DESCRIPTION
        -Compute the Yin Algorithm. Return fundamental frequency and harmonic rate.
        --------------------------------------------------------------------------------------------------------
        INPUT
        -sig: Audio signal (list of float)
        -sr: sampling rate (int)
        -w_len: size of the analysis window (samples)
        -w_step: overlap samples between two consecutives windows (samples)
        -f0_min: Minimum fundamental frequency that can be detected (hertz)
        -f0_max: Maximum fundamental frequency that can be detected (hertz)
        -harmo_tresh: Threshold of detection
        --------------------------------------------------------------------------------------------------------
        OUTPUT
        -pitches: list of fundamental frequencies,
        -harmonic_rates: list of harmonic rate values for each fundamental frequency value (= confidence value)
        -argmins: minimums of the Cumulative Mean Normalized DifferenceFunction
        -times: list of time of each estimation
        --------------------------------------------------------------------------------------------------------
        """
        tau_min = int(sr / f0_max)
        tau_max = int(sr / f0_min)

        timeScale = range(0, len(sig) - w_len, w_step)  # time values for each analysis window
        times = [t/float(sr) for t in timeScale]
        frames = [sig[t:t + w_len] for t in timeScale]

        pitches = [0.0] * len(timeScale)
        harmonic_rates = [0.0] * len(timeScale)
        argmins = [0.0] * len(timeScale)

        for i, frame in enumerate(frames):

            #Compute YIN
            df = self.diff(frame, tau_max)
            cmdf = self.cmndf(df)
            p = self.get_pitch(cmdf, tau_min, tau_max, harmo_thresh)

            #Get results
            if np.argmin(cmdf)>tau_min:
                argmins[i] = float(sr / np.argmin(cmdf))
            if p != 0: # A pitch was found
                pitches[i] = float(sr / p)
                harmonic_rates[i] = cmdf[p]
            else: # No pitch, but we compute a value of the harmonic rate
                harmonic_rates[i] = min(cmdf)

        return pitches, harmonic_rates, argmins, times



    

