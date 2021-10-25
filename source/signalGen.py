import numpy as np
import scipy.signal as sig
import scipy.sparse as sparse
import matplotlib.pyplot as plt
from random import randrange

fs = 44100

hdr = np.concatenate((np.array(np.ones(15, dtype=int)),
                      np.array([0, 0, 0, 1, 0, 1, 1, 1], dtype=int),
                      np.array([1], dtype=int)
))

def num_a_bin(num):
    b = bin(num)[2:]
    vec = np.array([], dtype=int)
    for i in b:
        vec = np.append(vec, np.array([int(i)], dtype=int))
    return vec

def generar_msg():
    msg = hdr
    id
    return msg
"""
fig = plt.figure()
f = np.arange(0, fs-1/fs, 1/fs)
ax = fig.add_subplot(111)
line1 = ax.plot(f, f)

def fig_blanca():
    return fig

def sig_prueba():
    line1.set_ydata(f, 2 * np.sin(2 * np.pi * f))
    return fig
"""