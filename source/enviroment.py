import numpy as np
from signalGen import fs
from random import randrange
c = 300000000

tmaxDop = 60*15
perfDop = 1

tim = -1 * (np.arange(0, tmaxDop-1/fs, 1 / fs) - tmaxDop/2)

perfs = np.array([tim])


def par_doppler():
    per = randrange(perfDop)
    i0 = randrange(np.size(perfs[per]))
    return per, i0


def doppler(fp, t, i0=0, perfil=0):
    ilim = np.size(perfs[perfil])
    t = (t * fs).astype(int) + i0
    t = (t+i0) % ilim
    print(t)
    return perfs[perfil][t]+fp


def pel(A):
    print("Llegué")
    return A/(np.random.uniform(1, 3.98107170553))