# # -*- coding: utf-8 -*-
""""
Trasformar Codigo XML a KML usando XPath
@author: Luis Antonio Fernandez Suarez
"""

from typing import Text
import xml.etree.ElementTree as ET

# Variable Global file
file = open("arbolFamiliar.svg", "w") # Abre y borra automaticamente el contenido del archivo

# Variable global y final que nos indica el tamaño de cada fila en el arbol
ROW_HEIGHT = 100

# Variable global y final que nos indica el tamaño de cada caja de familiar en el arbol
BOX_HEIGHT = 80
BOX_WIDTH = 200

# Variable Global que nos indica en que fila estamos trabajando,
# cada vez que añadamos un familiar, esta variable aumentara en uno.
current_row = 1

# Variable Global que nos indica si un familiar es l raiz del arbol
# pasará a ser negativa en la primera iteraccion de xml_2_svg(archivo_XML)
root = True

def write_in_file(line):
    """ Funcion que escribe la linea en el archivo y agrega un salto de linea"""
    file.write(line)
    file.write("\n")


def xml_2_svg(archivo_XML):
    """
    Función xml_2_svg(archivo_XML):
    Transforma el contenido de un archivo XML basado
    en el XML Schema arbolGenealogico en un documento SVG

    Author: Luis Antonio Fernandez Suarez
    """
    try:
        arbol = ET.parse(archivo_XML)
    except IOError:
        print("No se encuentra el archivo ", archivo_XML)
        exit()

    except ET.ET.ParseError:
        print("Error procesando el archivo XML ", archivo_XML)
        exit()
    
    raiz = arbol.getroot() # Raiz del documento
    write_in_file_svg_head()

    familiar_raiz = raiz.find("familiar[1]")
    
    # Coordenadas de origen situadas fuera del area visible que permiten crear la raiz del 
    # documento en el punto inicial (10,10)
    x = -190
    y = 10

    draw_box_for_familiar(familiar_raiz,x,y)
    write_in_file("</svg>")


def draw_box_for_familiar(familiar,x_origen,y_origen):
    """
    Dibuja el contenido del elemento familiar en una caja
    cuyas coordenadas dependeran de la caja de origen (x_origen,y_origen) y de la fila actual
    """
    global current_row # Para indicarle a la funcion que current_row hace referencia a la variable global 
    global root # Para indicarle a la funcion que root hace referencia a la variable global 

    x = x_origen + 200
    
    if root is True: # if state que sirve para crear el nodo raiz en las coordenadas (10,10)
        y = 10
    else:
        y = current_row * ROW_HEIGHT

    box = '<rect x="{0}" y="{1}" width="{2}" height="{3}" style="fill:white;stroke:black;stroke-width:1" />'.format(
        str(x), str(y), str(BOX_WIDTH), str(BOX_HEIGHT)
    )
    write_in_file(box) # Incluye  la caja creada para este familiar

    write_familiar_data(familiar, x, y) # Incluye los datos personales

    if root is False: # La raiz no tiene ningun path de origen
        draw_path(x_origen, x,y_origen, y) # dibujar la union entre esta caja y su caja padre (x_origen, y_origen)
    else:
        root = False # Despues de pasar este if-statement por primera vez dejamos de estar en la raiz

    current_row = current_row + 1 # IMPORTANTE: Incrementa la fila para que el siguiente familiar se pinte en la linea siguiente

    for parent in familiar.findall("./familiar"):
        draw_box_for_familiar(parent,x,y) # Llamada recursiva para crear sus hijos



def draw_path(x1, x2, y1, y2):
    """
    Dibuja una linea quebrada que va desde el vertice inferior de una caja de origen (x1,y1) 
    hasta el vertice izquierdo de una caja de destino (x2,y2)
    """
    x_origen = x1 + (BOX_WIDTH / 2)
    y_origen = y1 + BOX_HEIGHT

    desplazamiento_vertical = (y2 + BOX_HEIGHT / 2) - y_origen # vector de desplazamiento vertical
    desplazamiento_horizontal = x2 - x_origen # vector de desplazamiento horizontal

    path = "M {0} {1} v {2} h {3}".format(
        str(x_origen), str(y_origen),
        str(desplazamiento_vertical),
        str(desplazamiento_horizontal)
    )

    write_in_file('<path d="{0}" style="fill:transparent;stroke:black" />'.format(path))


def write_familiar_data(familiar,x,y):
    x = x + 10 # Todos los textos se escriben 10 pixeles a la derecha respecto al borde de la caja
    
    data = familiar.find("./dataFamiliar")
    nacimiento = data.find("./nacimiento")
    fallecimiento = data.find("./fallecimiento")

    nombre_apellido = familiar.attrib.get('nombre') + " " + familiar.attrib.get('apellido')
    
    lugar_nacimiento = nacimiento.find("./lugar").text
    fecha_nacimiento = nacimiento.find("./fecha").text
    coordenadas_nacimiento = "TODO TODO TODO TODO"

    if fallecimiento != None:
        lugar_fallecimiento = fallecimiento.find("./lugar").text
        fecha_fallecimiento = fallecimiento.find("./fecha").text
        coordenadas_fallecimiento = "TODO TODO TODO TODO"
    else:
        lugar_fallecimiento = " - "
        fecha_fallecimiento = " - "
        coordenadas_fallecimiento = " - "


    write_familiar_name(nombre_apellido, x, y + 10)
    write_text("Lugar de nacimiento: " + lugar_nacimiento, x, y + 20)
    write_text("fecha de nacimiento: " + fecha_nacimiento, x, y + 30)
    write_text("c. de nacimiento: " + coordenadas_nacimiento, x, y + 40)

    write_text("Lugar de fallecimiento: " + lugar_fallecimiento, x, y + 50)
    write_text("fecha de fallecimiento: " + fecha_fallecimiento, x, y + 60)
    write_text("c. de fallecimiento: " + coordenadas_fallecimiento, x, y + 70)

    write_photos_box(data, x, y)
    write_videos_box(data, x, y)


def write_photos_box(data_familiar, x_origen, y_origen):
    _x = x_origen + BOX_WIDTH
    _y = y_origen + 10

    box = '<rect x="{0}" y="{1}" width="{2}" height="{3}" style="fill:#a3d2ff;stroke:black;stroke-width:1" />'.format(
            str(_x), str(_y), str(BOX_WIDTH - 70), str(BOX_HEIGHT - 20)
        )
    write_in_file(box)

    _y = _y + 10
    write_text("FOTOS:", _x + 10, _y)

    for retrato in data_familiar.findall("./retrato"):
        _y = _y + 10
        write_text(retrato.text, _x + 10, _y)

def write_videos_box(data_familiar, x_origen, y_origen):
    _x = x_origen + BOX_WIDTH + 130
    _y = y_origen + 10
    if data_familiar.findall("./video"):
        box = '<rect x="{0}" y="{1}" width="{2}" height="{3}" style="fill:#b0ffcf;stroke:black;stroke-width:1" />'.format(
                str(_x), str(_y), str(BOX_WIDTH - 70), str(BOX_HEIGHT - 20)
            )
        write_in_file(box)

        _y = _y + 10
        write_text("VIDEOS:", _x + 10, _y)

        for video in data_familiar.findall("./video"):
            _y = _y + 10
            write_text(video.text, _x + 10, _y)


def write_familiar_name(nombre_apellidos, x, y):
    """
    Funcion dedicada a escribir los nombres de los familiares en el svg
    Incluye un elemento <text>  con el siguiente formato
        <text x="<x>" y="<y>" font-size="10" style="fill:blue"> <nombre_apellidos> </text>
    """
    write_in_file('<text x="{0}" y="{1}" font-size="10" style="fill:blue"> {2} </text>'.format(
        str(x), str(y), nombre_apellidos
    ))


def write_text(text, x, y):
    """
    Incluye un elemento <text>  con el siguiente formato
        <text x="<x>" y="<y>" font-size="8" style="fill:blue"> <paramenter_text> </paramenter_text>
    """
    write_in_file('<text x="{0}" y="{1}" font-size="8" style="fill:black"> {2}</text>'.format(
        str(x), str(y), text
    ))


def write_in_file_svg_head():
    """
    Incluye la cabecera del archivo svg:
        <?xml version="1.0" encoding="utf-8"?>
        <svg width="auto" height="3420" style="overflow:visible " version="1.1" xmlns="http://www.w3.org/2000/svg">
    """
    write_in_file('<?xml version="1.0" encoding="UTF-8"?>')
    write_in_file('<svg width="auto" height="3420" style="overflow:visible " version="1.1" xmlns="http://www.w3.org/2000/svg">')


def main():
    print(xml_2_svg.__doc__)
    
    archivo_XML = "arbolGenealogico.xml"
    xml_2_svg(archivo_XML)

    file.close()
    
    print("Archivo XML convertido con exito!\n")


if __name__ == "__main__":
    main()
