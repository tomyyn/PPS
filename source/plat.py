from signalGen import *
from enviroment import *


class Platform:
    def __init__(self, tmed, ti, fp, Pm, IPEL, IED):
        self.fp = fp
        self.A = np.sqrt(2*Pm)
        self.id = randrange(cantID)
        self.IPEL = IPEL
        self.IED = IED
        self.tmed = tmed
        if self.IED:
            self.perf, self.i0d = par_doppler()
        self.next = ti

    def simular(self):
        msg = generar_msg(self.id, N=randrange(1, 9))
        msg = msg_a_pulso(msg)
        if self.IPEL:
            As = pel(self.A)
        else:
            As = self.A
        desp = self.next/1000
        t = np.arange(desp, tpor + msg.shape[0] / fs + desp, 1 / fs)
        if t.shape[0] % 2 == 1:
            t = np.delete(t, -1)

        if self.IED:
            fps = doppler(self.fp, t, self.i0d, self.perf)
        else:
            fps = self.fp
        sim = pulso_a_senal(msg, fps, t, As)

        return sim

    def proximo(self, lim):
        if self.next > lim:
            return None, -1
        else:
            sim = self.simular()
            aux = self.next
            self.next = self.next + self.tmed
            return sim, aux
