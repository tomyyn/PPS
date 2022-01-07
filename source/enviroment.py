"""
Efectos ambientales.
"""

import numpy as np
from signalGen import fs
from random import randrange

tmaxDop = 60*15
#Cantidad de perfiles de Doppler
perfDop = 1

#Perfiles
tim = -1 * (np.arange(0, tmaxDop-1/fs, 1 / fs) - tmaxDop/2)

#Crear lista con los perfiles
perfs =[]
perfs.append(tim)


"""
par_doppler: entrega los parámetros de Doppler al azar para una plataforma.
Salidas:
    -Número de perfil de Doppler
    -Posición de inicio dentro del perfil mencionado
"""
def par_doppler():
    per = randrange(perfDop)
    i0 = randrange(np.size(perfs[per]))
    return per, i0


"""
doppler: refleja el efecto Doppler en la frecuencia de una transmisión.
Parámetros:
    -fp: frecuencia de portadora de la transmisión
    -t: vector de tiempo de la transmisión
    -i0: posición de comienzo de la plataforma
    -perfil: perfil de Doppler de la plataforma
Salidas:
    -Vector de frecuencia de la portadora a través del tiempo
"""
def doppler(fp, t, i0=0, perfil=0):
    ilim = np.size(perfs[perfil])
    t = (t * fs).astype(int) + i0
    t = (t+i0) % ilim #Se utiliza % ya que el perfil se repite
    return perfs[perfil][t]+fp

"""
pel: refleja la pérdida de potencia en el espacio libre en una transmisión.
Parámetros:
    -A: amplitud de la señal transmitida
Salidas:
    -Amplitud dividida por un número aleatorio entre 0 y 3.98107170553 (con distribución uniforme), lo cual indica en 
    potencia una degradación de entre 0 y 12 dbw
"""
def pel(A):
    return A/(np.random.uniform(1, 3.98107170553))
