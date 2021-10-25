import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

TERMINAR = 0
NE = 1
ACTUALIZARCANVAS = 2

sg.theme("Light Blue 2")

lay = [
    [sg.Button("IK")],
    [sg.Canvas(key = "-CANVAS-")],
    [sg.Button("OK")]
]

ventana = sg.Window(title="Simulador de señales", layout=lay)



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
    elif(event == "IK"):
        cod = ACTUALIZARCANVAS
    return cod, pars

