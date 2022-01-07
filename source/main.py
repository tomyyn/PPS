from UI import *
from plat import *
from simulador import *

cod = NE
while cod != TERMINAR:
    cod, pars = manejar_evento()
    if cod == ACTUALIZARDROPDOWN:
        actualizar_plats(pars)
    elif cod == COMENZAR:
        plataformas = []
        for i in range(int(pars["CantPlat"])):
            plataformas.append(Platform(int(pars["A1"+str(i+1)]), int(pars["A2"+str(i+1)]), int(pars["A3"+str(i+1)]), float(pars["A4"+str(i+1)]), pars["A5"+str(i+1)], pars["A6"+str(i+1)]))
        dep = simular(plataformas, int(pars["Tsim"]), pars["NOMBREARCHIVO"]+".wav")
        actualizar_canvas(actualizarFig(dep[0], dep[1]))
        guardarDefaults(pars)
    elif cod == CARGAR:
        cargarDefaults()

