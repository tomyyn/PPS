from UI import *
from signalGen import *
"""
msg = generar_msg(3, 1)

msg = (msg_a_pulso(msg))
msg = pulso_a_senal(msg, 10000)

print(msg.shape[0])

dep = np.asarray(sig.welch(msg, fs, return_onesided=False))
plt.plot(dep[0], dep[1])
plt.show()
"""

cod = NE
while(cod != 0):
    cod, pars = manejar_evento()
    print("Pasó algo")
    if(cod == ACTUALIZARDROPDOWN):
        actualizar_plats(pars)