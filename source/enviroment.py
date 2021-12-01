import numpy as np

c = 300000000

def doppler(f,v, tita):
    return (f*v*np.cos(tita)/c)


def pel(A):
    print("Llegué")
    return A/(np.random.uniform(1, 3.98107170553))