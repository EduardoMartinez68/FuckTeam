from ursina import *

# Inicializar el motor Ursina
app = Ursina()
def draw_text(text):
    texto = Text(text=text, origin=(0, 0), x=-0.5, y=0.5, scale=2, background=True)

def mita_screen():
    ancho_ventana, alto_ventana = window.fullscreen_size

    # Texto que quieres mostrar
    texto = "¡Hola, Mundo!"

    # Calcular la posición para centrar el texto horizontal y verticalmente
    x = -ancho_ventana / 2 + ancho_ventana / 4
    y = alto_ventana / 2 - alto_ventana / 4
    return x,y

def draw_dialog(character,text):
    fontArial = "engine/font/NunitoSans_7pt_Condensed-Light.ttf" #SourceSans3-Light
    x,y=mita_screen() #.125,-.125-.125-.125
    print(x,y)
    size=1.125
    spaceY=-.125/3
    Text(text=character, origin=(.5, 0), x=x, y=y, scale=size, background=False,color=color.rgb(211, 0, 0),font=fontArial)
    Text(text=text, origin=(0, 0), x=x, y=y+spaceY, scale=size, background=False,font=fontArial)


draw_dialog('Billy','Hi, do you need a friend? my name is Billy')
# Ejecutar el bucle del motor Ursina para mostrar la ventana
app.run()