import numpy as np

c = 300000000

def doppler(f,v, tita):
    return (f*v*np.cos(tita)/c)

def pel(d, fp):
    return (4 * np.pi * d * fp/c)