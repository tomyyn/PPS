import numpy as np
import scipy.sparse as sparse
import matplotlib.pyplot as plt
from random import randrange
from math import cos
from math import sin
from math import ceil


fs = 44100
bps = 400
mpb = fs/bps

alfa = 1.1
a = cos(alfa)
b = sin(alfa)

tpor = 0.16
npor = ceil(tpor * fs)

cantID = 1048576


escalera = np.array([0, 0, 0, 0,
                     0, 0, 0, 1,
                     0, 0, 1, 0,
                     0, 0, 1, 1,
                     0, 1, 0, 0,
                     0, 1, 0, 1,
                     0, 1, 1, 0,
                     0, 1, 1, 1], dtype=int)

pulsoManchester = np.concatenate((np.ones(int(mpb/2), dtype=int), -(np.ones(int(mpb/2), dtype=int))))

hdr = np.concatenate((np.array(np.ones(15, dtype=int)),
                      np.array([0, 0, 0, 1, 0, 1, 1, 1], dtype=int),
                      np.array([1], dtype=int)))


def num_a_bin(num, size=-1):
    b = bin(num)[2:]
    vec = np.array([], dtype=int)
    for i in b:
        vec = np.append(vec, np.array([int(i)], dtype=int))

    if size != -1:
        vec = np.append(np.zeros(size - vec.shape[0], dtype=int), vec)

    return vec


def xor(B1, B2):
    res = np.array([], dtype=int)
    for i in range(8):
        if B1[i] == B2[i]:
            res = np.append(res, 0)
        else:
            res = np.append(res, 1)
    return res


def cks(msg):
    N = int(msg.shape[0]/8)
    res = msg[0:8]
    for i in range(1, N):
        res = xor(res, msg[8*i:8*(i+1)])
    return res


def generar_msg(pID = randrange(cantID), N = randrange(1,9)):
    msg = np.array([])
    for i in range(N):
        msg = np.append(msg, escalera)

    N = num_a_bin(N,4)
    pID = num_a_bin(pID, 20)

    msg = np.concatenate((hdr, N, pID, msg))
    return np.concatenate((msg, cks(msg)))


def msg_a_pulso(msg):
    msg = (msg * 2)-1
    return sparse.kron(msg, pulsoManchester).toarray()[0]


def pulso_a_senal(msg, fp, t, A=1):
    if np.size(fp) > 1:
        portadora = A * np.cos(2 * np.pi * fp*t)
        portadora[npor:] = a * portadora[npor:] + msg * A * b * np.sin(2 * np.pi * (fp[npor:])*t[npor:])
    else:
        portadora = A * np.cos(2 * np.pi * fp * t)
        portadora[npor:] = a * portadora[npor:] + msg * A * b * np.sin(2 * np.pi * fp *t[npor:])

    return portadora


def actualizarFig(x, y):
    fig = plt.figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(x, y)
    return fig
