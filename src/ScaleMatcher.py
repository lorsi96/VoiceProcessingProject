import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt

midi = []
for i in np.linspace(0, 12, 1000):
    midi.append(440*2**(i/12))


def caster(signal):
    def errfnc(f0):
        reference = [f0*2**(n/12) for n in range(-36, 48)]
        ret = []
        error = 0
        for element in signal:
            if element < 50:
                ret.append(0)
            else:
                ret.append(min(reference, key=lambda x: abs(x-element)))
                error += np.abs(ret[-1]-element)
        return error
    # optimal_ref = minimize(errfnc, 320, method='nelder-mead',
    #                       options={'xtol': .1, 'disp': True})['x']

    err = []
    for element in midi:
        err.append(errfnc(element))
    optimal_ref = midi[np.argmin(err)]
    # Final Adjustment
    reference = [float(optimal_ref)*2**(n/12) for n in range(-36, 48)]
    ret = []
    for element in signal:
        if element < 50:
            ret.append(0)
        else:
            ret.append(min(reference, key=lambda x: abs(x-element)))
    return np.array(ret), optimal_ref
