from UI import *
from scipy.io.wavfile import write
import numpy as np
from signalGen import *
from enviroment import *
from plat import *

msg = generar_msg(3, 1)
"""
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
plataformas = []
cod = NE
while cod != 0:
    cod, pars = manejar_evento()
    print("Pasó algo" + str(cod))
    if cod == ACTUALIZARDROPDOWN:
        actualizar_plats(pars)
        actualizar_canvas(fig_blanca())
    if (cod == COMENZAR):
            for i in range (int(pars["CantPlat"])):
                plataformas.append(Platform(int(pars["A1"+str(i+1)]), int(pars["A2"+str(i+1)]), int(pars["A3"+str(i+1)]), int(pars["A4"+str(i+1)]), pars["Tsim"]))
            for i in plataformas:
                print(i.tiempos)
                while(i.proximo(1000000) != -1):
                    print("a")
""""""