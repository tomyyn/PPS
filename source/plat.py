"""
Clase utilizada para representar una plataforma.
"""

from signalGen import *
from enviroment import *


class Platform:
    """
    Constructor: instancia una plataforma e inicializa sus valores.
    Parámetros:
        -tmed: tiempo medio de repetición[ms]
        -ti: tiempo de inicio[ms]
        -fp: frecuencia de portadora[hz]
        -Pm: potencia media[V^2]
        -IPEL: incluir pérdida en el espacio libre
        -IED: incluir efecto Doppler
    """
    def __init__(self, tmed, ti, fp, Pm, IPEL, IED):
        self.fp = fp                #Frecuencia de portadora[hz]
        self.A = np.sqrt(2*Pm)      #Amplitud[V]
        self.id = randrange(cantID) #Id de la plataforma
        self.IPEL = IPEL            #Incluir pérdida en el espacio libre
        self.IED = IED              #Incluir efecto Doppler
        self.tmed = tmed            #Tiempo medio de repetición[ms]
        #Si se incluye el efecto Doppler, obtener pérfil de Doppler y lugar de comienzo
        if self.IED:
            self.perf, self.i0d = par_doppler()
        self.next = ti              #Tiempo de inicio de la próxima simulación[ms]

    """
    simular: realiza la simulación de una tramsmisión de la plataforma.
    Salidas:
        -simulación de la transmisión en formato de vector
    """
    def simular(self):
        #Obtener secuencia de bits a enviar
        msg = generar_msg(self.id, N=randrange(1, 9))

        #Convertir secuencia de bits a pulsos
        msg = msg_a_pulso(msg)

        #Si se incluye PEL, incluirla en la amplitud
        if self.IPEL:
            As = pel(self.A)
        else:
            As = self.A

        #Gemerar vector de tiempo
        desp = self.next/1000
        t = np.arange(desp, tpor + msg.shape[0] / fs + desp, 1 / fs)
        # Si el número de elementos es impar, quitar el último para evitar errores
        if t.shape[0] % 2 == 1:
            t = np.delete(t, -1)

        #Si se incluye ED, incluirlo en la frecuencia de portadora
        if self.IED:
            fps = doppler(self.fp, t, self.i0d, self.perf)
        else:
            fps = self.fp

        #Convertir pulso a señal
        sim = pulso_a_senal(msg, fps, t, As)

        return sim

    """
    proximo: obtiene la siguiente simulación de la plataforma, siempre y cuando esta no exceda el tiempo máximo.
    Parámetros:
        -lim: límite de tiempo[ms]
    Salidas:
        -simulación de la transmisión en formato de vector
        -tiempo de inicio de la transmisión simulada[ms], -1 si esta no se puede realizar
    """
    def proximo(self, lim):
        #Si el inicio de la siguiente simulación excede el tiempo máximo, indicar que no se pudo realizar
        if self.next > lim:
            return None, -1
        #Si se pudo realizar, obtener la simulación y actualizar el tiempo de inicio de la próxima simulación
        else:
            sim = self.simular()
            aux = self.next
            self.next = self.next + self.tmed
            return sim, aux
