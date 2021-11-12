class Platform:
    def __init__(self, tmed, ti, fp, Pm, ts):
        self.fp = fp
        self.P = Pm
        self.tiempos = []
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

    def proximo(self, lim):
        if(self.next == -1 or self.next > lim):
            return -1
        else:
            """Obtener simulación"""
            self.avanzar()
            return 1