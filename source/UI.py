import PySimpleGUI as sg
from signalGen import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

TERMINAR = 0
NE = 1
ACTUALIZARCANVAS = 2
ACTUALIZARDROPDOWN = 3
COMENZAR = 4

CANTPLAT = 8

tamAtri = 9
cantAtri = 4

archDefault = "VP.txt"

sg.theme("Light Blue 2")


def crear_frame_plat(n):
    n = str(n)
    lay = [[sg.Text("t med rep[ms]:"), sg.InputText(key="A1"+n, size=tamAtri),
            sg.Text("t de inicio[ms]:"), sg.InputText(key="A2" + n, size=tamAtri),
            sg.Text("fp[hz]:"), sg.InputText(key="A3"+n, size=tamAtri),
            sg.Text("P[V^2]:"), sg.InputText(key="A4"+n, size=tamAtri)]]
    return sg.Frame("Plataforma "+n, layout=lay, key="P"+n)


plats = []
for i in range(1, CANTPLAT+1):
    plats.append([crear_frame_plat(i)])


lay = [
    [sg.Text("Número de plataformas:"), sg.DropDown(list(range(1, CANTPLAT+1)), default_value=8, enable_events=True, key="CantPlat", readonly=True)],
    [sg.Frame("Atributos", layout=plats), sg.Canvas(key="-CANVAS-", size=(600, 400))],
    [sg.Text("Tiempo de simulación[ms]:"), sg.InputText(size=(15, 1), key="Tsim"), sg.Text("Archivo: "), sg.InputText(key="NOMBREARCHIVO", size=(20, 1)), sg.Text("ms"), sg.Button("Comenzar"), sg.Text("Error: valores no válidos", key = "MSGERRORIP", visible= False, text_color="red")],
    [sg.Image("logoUNLP.png", size=(75, 75)), sg.Image("logoGrIDComD.png", size=(75, 75))]
]


ventana = sg.Window(title="Simulador de señales", layout=lay)

def check_inputs(values):
    cumple = True
    i = 1
    while(cumple and i <= values["CantPlat"]):
        j = 1
        while(cumple and j <= cantAtri):
            cumple = values["A"+str(j)+str(i)].isnumeric()
            j = j + 1
        i=i+1

    return cumple

def actualizar_plats(n):
    for i in range(1, n+1):
        ventana.Element("P"+str(i)).Update(visible=True)
    for i in range(n+1, CANTPLAT+1):
        ventana.Element("P"+str(i)).Update(visible=False)


def actualizar_canvas(fig):
    if ventana["-CANVAS-"].TKCanvas.children:
        for child in ventana["-CANVAS-"].TKCanvas.winfo_children():
            child.destroy()
    figure_canvas_agg = FigureCanvasTkAgg(fig, ventana["-CANVAS-"].TKCanvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg


def manejar_evento():
    cod = 1
    pars = None

    event, values = ventana.read()
    if event == sg.WIN_CLOSED:
        cod = TERMINAR
    if event == "CantPlat":
        cod = ACTUALIZARDROPDOWN
        pars = values["CantPlat"]
    elif event == "Comenzar":
        if (values["Tsim"].isnumeric() and values["NOMBREARCHIVO"] != "" and check_inputs(values)):
            cod = COMENZAR
            ventana.Element("MSGERRORIP").Update(visible=False)
            pars = values
        else:
            cod = NE
            ventana.Element("MSGERRORIP").Update(visible=True)
    return cod, pars

def cargarDefaults():
    try:
        archi= open(archDefault, mode="r")
        lineas = archi.readlines()
        print(len(lineas))
        archi.close()
        return True
    except IOError:
        return False

def escribir(archi, s):
    print(s)
    if s is None:
        s = ""
    archi.write(s+"\n")

def guardarDefaults(vals):
    archi = open(archDefault, "w")
    escribir(archi,vals["CantPlat"])
    for i in range(1, CANTPLAT + 1):
        for j in range(1, cantAtri + 1):
            escribir(archi, vals["A" + str(j) + str(i)])
    escribir(archi, vals["Tsim"])
    escribir(archi,vals["NOMBREARCHIVO"])
    archi.close()