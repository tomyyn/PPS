from UI import *
from scipy.io.wavfile import write
import numpy as np
from signalGen import *
from enviroment import *
from plat import *
from simulador import *
"""
msg = generar_msg(3, 1)

msg = msg_a_pulso(msg)
msg = pulso_a_senal(msg, 8000, 1)

print(msg.shape[0])

dep = np.asarray(sig.welch(msg, fs, return_onesided=False))
plt.plot(dep[0], dep[1])
plt.show()

scaled = np.int16(msg/np.max(np.abs(msg)) * 32767)
write('test.wav', 44100, scaled)
"""
"""
print(xor(np.array([1, 1, 1, 1, 0, 0, 0, 0]), np.array([0, 1, 1, 1, 0, 0, 0, 0])))
print(msg[0:8])
print(msg)
"""



cod = NE
while cod != 0:
    cod, pars = manejar_evento()
    print("Pasó algo" + str(cod))
    if cod == ACTUALIZARDROPDOWN:
        actualizar_plats(pars)
    if (cod == COMENZAR):
            plataformas = []
            for i in range (int(pars["CantPlat"])):
                plataformas.append(Platform(int(pars["A1"+str(i+1)]), int(pars["A2"+str(i+1)]), int(pars["A3"+str(i+1)]), int(pars["A4"+str(i+1)]), pars["Tsim"]))
            dep = simular(plataformas, int(pars["Tsim"]), pars["NOMBREARCHIVO"]+".wav")
            actualizar_canvas(actualizarFig(dep[0], dep[1]))
"""
z = np.zeros(fs*10)
p = Platform(1000, 500, 5000, 4, 5000)
q = Platform(800, 600, 10000, 1, 5000)
plataformas = []
plataformas.append(p)
plataformas.append(q)
simular(plataformas, 5000, "hola.wav")
"""
"""
msgt = np.array(())
msg, aux = p.proximo(1000)
while(aux != -1):
    msgt = np.concatenate((msgt, msg))
    msg, aux = p.proximo(1000)
"""
#scaled = np.int16(msgt/np.max(np.abs(msgt)) * 32767)
#write('test.wav', 44100, scaled)

#dep = np.asarray(sig.welch(msg, fs, return_onesided=False))
#plt.plot(dep[0], dep[1])
#plt.show()

