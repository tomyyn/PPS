from signalGen import *
from scipy.io.wavfile import write

extra = fs

def tiempo_a_ind(t):
    t = t/1000

    return int(t * fs)

def simular(plats, tiempo, name = "test.wav"):
    msgt=np.zeros(int(extra + fs * (tiempo/1000)))
    for i in plats:
        msg, aux = i.proximo(tiempo)
        while (aux != -1):
            print(aux)
            desp = tiempo_a_ind(aux)
            msgt[desp:desp+msg.shape[0]] =msgt[desp:desp+msg.shape[0]]+ msg
            msg, aux = i.proximo(tiempo)

    msgt = np.int16(msgt/np.max(np.abs(msgt)) * 32767)
    write(name, 44100, msgt)

    return np.asarray(sig.welch(msgt, fs, return_onesided=False))