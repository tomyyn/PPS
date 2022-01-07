"""
Generación de mensajes, pulsos y señales
"""

import numpy as np
import scipy.sparse as sparse
from random import randrange
from math import cos
from math import sin
from math import ceil

#Frecuencia de muestreo
fs = 44100
#Bps de la transmisión
bps = 400
#Muestras por bit
mpb = fs/bps

#Alfa de la transmisión
alfa = 1.1
a = cos(alfa)
b = sin(alfa)

#Tiempo de transmisión de solo la portadora
tpor = 0.16
npor = ceil(tpor * fs)

#Número posible de IDs de plataformas
cantID = 1048576

#Escalera de valores
escalera = np.array([0, 0, 0, 0,
                     0, 0, 0, 1,
                     0, 0, 1, 0,
                     0, 0, 1, 1,
                     0, 1, 0, 0,
                     0, 1, 0, 1,
                     0, 1, 1, 0,
                     0, 1, 1, 1], dtype=int)

#Forma de pulso Manchester
pulsoManchester = np.concatenate((np.ones(int(mpb/2), dtype=int), -(np.ones(int(mpb/2), dtype=int))))

#Valores constantes en la cabecera del mensaje
hdr = np.concatenate((np.array(np.ones(15, dtype=int)),
                      np.array([0, 0, 0, 1, 0, 1, 1, 1], dtype=int),
                      np.array([1], dtype=int)))

"""
num_a_bin: obtiene la representación en binario en forma de vector de un número.
Parámetros:
    -num: número a convertir
    -size: tamaño mínimo del vector
Salidas:
    -Vector con la representación binaria
"""
def num_a_bin(num, size=None):
    #Convertir número a binario en forma de string y remover sus dos primeros caracteres (0b)
    b = bin(num)[2:]
    #Agregar cada caracter a un vector
    vec = np.array([], dtype=int)
    for i in b:
        vec = np.append(vec, np.array([int(i)], dtype=int))
    #Si se especificó un tamaño mínimo, rellenar con ceros a la izquierda
    if size is None:
        vec = np.append(np.zeros(size - vec.shape[0], dtype=int), vec)

    return vec


"""
xor: realiza el XOR bit a bit entre dos vectores que se asumen solo poseen 1s y 0s como valores.
Parámetros:
    -B1: vector 1
    -B2: vector 2
Salidas:
    -Vector con el XOR bit a bit de los vectores
"""
def xor(B1, B2):
    res = np.array([], dtype=int)
    for i in range(8):
        if B1[i] == B2[i]:
            res = np.append(res, 0)
        else:
            res = np.append(res, 1)
    return res


"""
cks: obtiene el CRC de 8 bits de un mensaje.
Parámetros:
    -msg: mensaje del cual calcular el CRC
Salidas:
    -Vector de 8 bits con el CRC del mensaje
"""
def CRC(msg):
    #Realizar el xor de todos los bytes del mensaje
    N = int(msg.shape[0]/8)
    res = msg[0:8]
    for i in range(1, N):
        res = xor(res, msg[8*i:8*(i+1)])
    return res


"""
generar_msg: genera un mensaje a transmitir.
Parámetros:
    -pID: ID de la plataforma transmisora
    -N: tamaño del campo de datos del mensaje (en paquetes de 32 bits)
Salida:
    -Vector con los bits del mensaje
"""
def generar_msg(pID = randrange(cantID), N = randrange(1,9)):
    #Generar campo de datos agregando escaleras hasta que tenga la longitud deseada
    msg = np.array([])
    for i in range(N):
        msg = np.append(msg, escalera)
    #Convertir N y pID a vectores con su representación binaria
    N = num_a_bin(N,4)
    pID = num_a_bin(pID, 20)
    #Obtener el mensaje concatenando los campos fijos de la cabecera, N, pID, el campo de datos y finalmente calculando
    #y agregando el CRC
    msg = np.concatenate((hdr, N, pID, msg))
    return np.concatenate((msg, CRC(msg)))


"""
msg_a_pulso: convierte un mensaje a una secuencia de pulsos Manchester correspondiente.
Parámetros:
    -msg: mensaje a convertir a pulsos
Salidas:
    -vector con los pulsos
"""
def msg_a_pulso(msg):
    #Convertir los 0s y 1s del mensaje a -1s y 1s
    msg = (msg * 2)-1
    #Obtener los pulsos y devolverlos
    return sparse.kron(msg, pulsoManchester).toarray()[0]


"""
pulso_a_senal: convierte una secuencia de pulsos en una señal correspondiente a su transmisión.
Parámetros:
    -msg: secuencia de pulsos
    -fp: frecuencia de portadora (o vector con esta a través del tiempo)
    -t: vector de tiempo de la transmisión
    -A: amplitud de la señal
Salidas:
    -Vector con la señal
"""
def pulso_a_senal(msg, fp, t, A=1):
    #Diferenciar si la frecuencia de portadora es un escalar o un vector
    if np.size(fp) > 1:
        #Solo portadora
        portadora = A * np.cos(2 * np.pi * fp*t)
        #Mensaje
        portadora[npor:] = a * portadora[npor:] + msg * A * b * np.sin(2 * np.pi * (fp[npor:])*t[npor:])
    else:
        #Solo portadora
        portadora = A * np.cos(2 * np.pi * fp * t)
        #Mensaje
        portadora[npor:] = a * portadora[npor:] + msg * A * b * np.sin(2 * np.pi * fp *t[npor:])

    return portadora



