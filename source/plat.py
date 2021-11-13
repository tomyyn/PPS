from signalGen import *

class Platform:
    def __init__(self, tmed, ti, fp, Pm, ts):
        self.fp = fp
        self.A = np.sqrt(2*Pm)
        self.tiempos = []
        self.id = randrange(cantID)
        auxt= int(ti)
        ts = int(ts)
        tmed = int(tmed)
        while(auxt < ts):
            self.tiempos.append(auxt)
            auxt= auxt + tmed
        self.avanzar()

    def avanzar(self):
        if (self.tiempos):
            self.next = self.tiempos.pop(0)
        else:
            self.next = -1

    def simular(self):
        msg = generar_msg(self.id, 1)
        msg = msg_a_pulso(msg)
        desp = self.next/1000
        t = np.arange(desp, tpor + msg.shape[0] / fs + desp, 1 / fs)
        #Acá deberían calcularse los efectos del ambiente
        sim = msg = pulso_a_senal(msg, self.fp, t, self.A)

        return sim

    def proximo(self, lim):
        if(self.next == -1 or self.next > lim):
            return None, -1
        else:
            sim = self.simular()
            aux = self.next
            self.avanzar()
            return sim, aux