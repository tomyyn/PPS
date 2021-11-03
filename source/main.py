"""from UI import *"""
import numpy as np

from signalGen import *
from enviroment import *
"""
msg = generar_msg(3, 1)

msg = (msg_a_pulso(msg))
msg = pulso_a_senal(msg, 10000)

print(msg.shape[0])

dep = np.asarray(sig.welch(msg, fs, return_onesided=False))
plt.plot(dep[0], dep[1])
plt.show()

cod = NE
while cod != 0:
    cod, pars = manejar_evento()
    print("Pasó algo" + str(cod))
    if cod == ACTUALIZARDROPDOWN:
        actualizar_plats(pars)
        actualizar_canvas(fig_blanca())
"""
print(pel(384000000, 8400000000))