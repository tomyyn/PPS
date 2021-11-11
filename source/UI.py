import PySimpleGUI as sg
from signalGen import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

TERMINAR = 0
NE = 1
ACTUALIZARCANVAS = 2
ACTUALIZARDROPDOWN = 3
COMENZAR = 4

CANTPLAT = 8

tamAtri = 10
cantAtri = 3

sg.theme("Light Blue 2")


def crear_frame_plat(n):
    n = str(n)
    lay = [[sg.Text("t medio de repetición:"), sg.InputText(key="A1"+n, size=tamAtri), sg.Text("ms"),
            sg.Text("fs:"), sg.InputText(key="A2"+n, size=tamAtri), sg.Text("hz"),
            sg.Text("P:"), sg.InputText(key="A3"+n, size=tamAtri), sg.Text("V^2"),]]
    return sg.Frame("Plataforma "+n, layout=lay, key="P"+n)


plats = []
for i in range(1, CANTPLAT+1):
    plats.append([crear_frame_plat(i)])


lay = [
    [sg.Text("Número de plataformas:"), sg.DropDown(list(range(1,CANTPLAT+1)), default_value=8, enable_events=True, key="CantPlat", readonly=True)],
    [sg.Frame("Atributos", layout=plats), sg.Canvas(key="-CANVAS-",size=(600, 400))],
    [sg.Text("Tiempo de simulación:"), sg.InputText(size=(15, 1), key="Tsim"), sg.Text("ms"),sg.Text("Archivo: "), sg.InputText(key="NOMBREARCHIVO", size=(20,1)) , sg.Button("Comenzar"), sg.Text("Error: valores no válidos", key = "MSGERRORIP", visible= False, text_color="red")],
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

