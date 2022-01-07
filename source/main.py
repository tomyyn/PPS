"""
Programa principal, encargado de llevar a cabo las acciones correspondientes a los distintos eventos de la interfaz.
"""

from UI import *
from plat import *
from simulador import *

cod = NE
#Mientras no se cierre la ventana
while cod != TERMINAR:
    #Obtener acción a realizar
    cod, pars = manejar_evento()
    #Actualizar número de plataformas en pantalla
    if cod == ACTUALIZARDROPDOWN:
        actualizar_plats(pars)
    #Realizar simulación
    elif cod == COMENZAR:
        #Inicializar plataformas
        plataformas = []
        for i in range(int(pars["CantPlat"])):
            plataformas.append(Platform(int(pars["A1"+str(i+1)]), int(pars["A2"+str(i+1)]), int(pars["A3"+str(i+1)]), float(pars["A4"+str(i+1)]), pars["A5"+str(i+1)], pars["A6"+str(i+1)]))
        #Simular
        dep = simular(plataformas, int(pars["Tsim"]), pars["NOMBREARCHIVO"]+".wav")
        #Mostrar DEP en pantalla
        actualizar_canvas(actualizarFig(dep[0], dep[1]))
        #Guardar parámetros
        guardarDefaults(pars)
    #Cargar parámetros de la simulación anterior
    elif cod == CARGAR:
        cargarDefaults()

