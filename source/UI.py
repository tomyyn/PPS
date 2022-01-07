"""
Interfaz de usuario
"""

import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#Órdenes para el programa principal
TERMINAR = 0            #Salir del programa
NE = 1                  #No realizar nada
ACTUALIZARDROPDOWN = 2  #Actualizar número de plataformas en pantalla
COMENZAR = 3            #Simular
CARGAR = 4              #Cargar parámetros de simulación anterior

#Número máximo de plataformas
CANTPLAT = 8

#Tamaño de campo de entrada para atributos
tamAtri = 9
#Cantidad de atributos por plataforma
cantAtri = 6

#Archivo donde se encuentran los parámetros de la última simulación
archDefault = "VP.txt"

#Tema de la interfaz
sg.theme("Light Blue 2")


"""
crear_frame_plat: crea un frame en el cual se encuentran los campos de entrada para los atributos de una plataforma.
Parámetros:
    -n: número de plataforma dentro de la interfaz
Salidas:
    -frame
"""
def crear_frame_plat(n):
    n = str(n)
    lay = [[sg.Text("t med rep[ms]:"), sg.InputText(key="A1"+n, size=tamAtri),
            sg.Text("t de inicio[ms]:"), sg.InputText(key="A2" + n, size=tamAtri),
            sg.Text("fp[hz]:"), sg.InputText(key="A3"+n, size=tamAtri),
            sg.Text("P[V^2]:"), sg.InputText(key="A4"+n, size=tamAtri),
            sg.Checkbox("PEL", enable_events=False, key="A5"+n),
            sg.Checkbox("ED", enable_events=False, key="A6"+n)]]
    return sg.Frame("Plataforma "+n, layout=lay, key="P"+n)


#Crear los frames para todas las plataformas
plats = []
for i in range(1, CANTPLAT+1):
    plats.append([crear_frame_plat(i)])


"""
Colocar todos los componentes en la interfaz, cada línea representa:
    -Menú de cantidad de plataformas y botón de cargar última simulación.
    -Campos de entrada para los atributos de las plataformas y canvas para mostrar la DEP.
    -Campos para el tiempo de simulación y el nombre del archivo de salida, botón de simulación.
    -Logos.
"""
lay = [
    [sg.Text("Número de plataformas:"), sg.DropDown(list(range(1, CANTPLAT+1)), default_value=8, enable_events=True, key="CantPlat", readonly=True), sg.Button("Cargar última simulacion"), sg.Text("Error al cargar simulación", key = "MSGERRORLOAD", visible= False, text_color="red")],
    [sg.Frame("Atributos", layout=plats), sg.Canvas(key="-CANVAS-", size=(600, 400))],
    [sg.Text("Tiempo de simulación[ms]:"), sg.InputText(size=(15, 1), key="Tsim"), sg.Text("Archivo: "), sg.InputText(key="NOMBREARCHIVO", size=(20, 1)), sg.Text(".wav"), sg.Button("Comenzar"), sg.Text("Error: valores no válidos", key = "MSGERRORIP", visible= False, text_color="red")],
    [sg.Image("logoUNLP.png", size=(75, 75)), sg.Image("logoGrIDComD.png", size=(75, 75))]
]


#Crear ventana
ventana = sg.Window(title="Simulador de señales", layout=lay)

"""
check_inputs: chequea que todos los valores ingresados como parámetros de las plataformas 
sean correctos antes de comenzar la simulación. Este chequeo consta de verificar que los campos contengan números
Parámetros:
    -values: diccionario que contiene los valores ingresados
Salidas:
    -True si los parámetros son válidos, y False en caso contrario
"""
def check_inputs(values):
    cumple = True
    i = 1
    while(cumple and i <= values["CantPlat"]):
        j = 1
        while(cumple and j <= cantAtri-2): #No se chequean campos que constan de checkboxes ya que siempre son válidos
            cumple = values["A"+str(j)+str(i)].isnumeric()
            j = j + 1
        i=i+1

    return cumple


"""
actualizar_plats: actualiza el número de plataformas mostradas en pantalla.
Parámetros:
    -n: número de plataformas a mostrar
"""
def actualizar_plats(n):
    for i in range(1, n+1):
        ventana.Element("P"+str(i)).Update(visible=True)
    for i in range(n+1, CANTPLAT+1):
        ventana.Element("P"+str(i)).Update(visible=False)


"""
actualizar_canvas: actualiza la figura mostrada en el canvas de la interfaz.
Parámetros:
    -fig: figura a colocar en el canvas
"""
def actualizar_canvas(fig):
    if ventana["-CANVAS-"].TKCanvas.children:
        for child in ventana["-CANVAS-"].TKCanvas.winfo_children():
            child.destroy()
    figure_canvas_agg = FigureCanvasTkAgg(fig, ventana["-CANVAS-"].TKCanvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)


"""
manejar_evento: lee eventos de la interfaz y los convierte en órdenes para el programa principal.
Salidas:
    -código de la acción a realizar
    -parámetros
"""
def manejar_evento():
    cod = NE
    pars = None
    #Leer evento de la ventana
    event, values = ventana.read()
    #Si se cierra la ventana indicar que se termine el programa
    if event == sg.WIN_CLOSED:
        cod = TERMINAR
    #Si se actualiza el menú dropdown indicar que se actualice el número de plataformas mostradas en pantalla
    elif event == "CantPlat":
        cod = ACTUALIZARDROPDOWN
        pars = values["CantPlat"]
    #Si se presiona el botón de simular, chequear que los parámetros sean correctos e indicar que realice la simulación,
    #caso contrario indicar que no se haga nada
    elif event == "Comenzar":
        if values["Tsim"].isnumeric() and values["NOMBREARCHIVO"] != "" and check_inputs(values):
            cod = COMENZAR
            ventana.Element("MSGERRORIP").Update(visible=False)
            pars = values
        else:
            ventana.Element("MSGERRORIP").Update(visible=True)
    #Si se presiona el botón de cargar última simulación, indicar que se carguen sus parámetros a la interfaz
    elif event == "Cargar última simulacion":
        cod = CARGAR

    return cod, pars


"""
cargarDefaults: carga a la interfaz los parámetros de la última simulación.
Salidas: 
    -True si la carga fue exitosa y False en caso contrario
"""
def cargarDefaults():
    try:
        #Cargar valores del archivo y convertirlo a un vector de strings
        archi= open(archDefault, mode="r")
        lineas = archi.readlines()
        #Si no hay valores suficientes, devolver False e indicar en pantalla que no hubo éxito
        if len(lineas) < 51:
            ventana.Element("MSGERRORLOAD").Update(visible=True)
            return False

        for i in range(len(lineas)):
            lineas[i] = lineas[i][0:-1]

        #Cargar valores en los campos de la interfaz
        p = int(lineas[0])
        ventana.Element("CantPlat").Update(value=p)
        actualizar_plats(p)
        k = 1
        for i in range(1, CANTPLAT + 1):
            for j in range(1, cantAtri + 1 - 2):
                ventana.Element("A" + str(j) + str(i)).Update(value=lineas[k])
                k=k+1
            ventana.Element("A5"+str(i)).Update(value=lineas[k] == "True")
            k = k + 1
            ventana.Element("A6"+str(i)).Update(value=lineas[k] == "True")
            k = k + 1
        ventana.Element("Tsim").Update(value=lineas[k])
        k=k+1
        ventana.Element("NOMBREARCHIVO").Update(value=lineas[k])
        k = k + 1
        archi.close()
        ventana.Element("MSGERRORLOAD").Update(visible=False)
        return True
    #Si se genera alguna excepción, devolver False e indicar en pantalla que no hubo éxito
    except:
        ventana.Element("MSGERRORLOAD").Update(visible=True)
        return False


"""
escribir: escribe una línea en un archivo de texto.
Parámetros:
    -archi: archivo en el cual escribir
    -s: string a escribir en el archivo
"""
def escribir(archi, s):
    #Si s es nulo, convertirlo en un string vacío
    if s is None:
        s = ""
    #Escribir s y un fin de línea en archi
    archi.write(s+"\n")


"""
guardarDefaults: escribe los parámetros de la interfaz en un archivo de texto.
Parámetros:
    -vals: valores a escribir
"""
def guardarDefaults(vals):
    archi = open(archDefault, "w")
    escribir(archi, str(vals["CantPlat"]))
    for i in range(1, CANTPLAT + 1):
        for j in range(1, cantAtri + 1-2):
            escribir(archi, vals["A" + str(j) + str(i)])
        escribir(archi, str(vals["A5"+str(i)]))
        escribir(archi, str(vals["A6"+str(i)]))
    escribir(archi, vals["Tsim"])
    escribir(archi, vals["NOMBREARCHIVO"])
    archi.close()
