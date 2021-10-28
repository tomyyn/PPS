import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

TERMINAR = 0
NE = 1
ACTUALIZARCANVAS = 2
ACTUALIZARDROPDOWN = 3

CANTPLAT = 8

tamAtri = 10

sg.theme("Light Blue 2")

def crear_frame_plat(n):
    n=str(n)
    lay=[[sg.Text("Atributo 1:"), sg.InputText(key="A1"+n, size=tamAtri)]]
    return sg.Frame("Plataforma"+n, layout=lay, key="P"+n)

plats = []
for i in range(1,CANTPLAT+1):
    plats.append([crear_frame_plat(i)])

lay = [
    [sg.Button("IK")],
    [sg.Text("Número de plataformas:"), sg.DropDown(list(range(1,CANTPLAT+1)), default_value=1, enable_events=True, key="CantPlat", readonly=True)],
    plats,
    [sg.Canvas(key = "-CANVAS-")],
    [sg.Button("OK")]
]

ventana = sg.Window(title="Simulador de señales", layout=lay)

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
    if(event == sg.WIN_CLOSED):
        cod = TERMINAR
    if(event == "CantPlat"):
        cod = ACTUALIZARDROPDOWN
        pars = values["CantPlat"]
    elif(event == "IK"):
        cod = ACTUALIZARCANVAS
    return cod, pars

