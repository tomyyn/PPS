"""
Motor de la simulación.
"""

from signalGen import *
from scipy.io.wavfile import write
import scipy.signal as sig
extra = fs


"""
tiempo_a_ind: convierte un instante de tiempo en un índice del vector de la simulación.
Entradas:
    -t: instante de tiempo
Salidas:
    -Índice del vector de simulación
"""
def tiempo_a_ind(t):
    t = t/1000

    return int(t * fs)


"""
simular: realiza la simulación de todas las plataformas y guardarla en un archivo .wav.
Parámetros:
    -plats: plataformas a simular
    -tiempo: duración de la simulación[ms]
    -name: nombre del archivo de salida
Salidas:
    -DEP de la simulación
"""
def simular(plats, tiempo, name="test.wav"):
    #Crear vector para la simulación
    msgt=np.zeros(int(extra + fs * (tiempo/1000)))
    #Para cada plataforma obtener simulaciones de transmisiones hasta que estas excedan el tiempo de la simulación e
    #insertarlas en el vector de la simulación
    for i in plats:
        msg, aux = i.proximo(tiempo)
        while aux != -1:
            desp = tiempo_a_ind(aux)
            msgt[desp:desp+msg.shape[0]] = msgt[desp:desp+msg.shape[0]] + msg
            msg, aux = i.proximo(tiempo)

    #Normalizar el vector de la simulación y guardarlo en un archivo .wav
    msgt = np.int16(msgt/np.max(np.abs(msgt)) * 32767)
    write(name, 44100, msgt)

    #Obtener y devolver DEP de la simulación
    return np.asarray(sig.welch(msgt, fs, return_onesided=True))
