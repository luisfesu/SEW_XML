# # -*- coding: utf-8 -*-
""""
Este programa permite visulizar infomacion relevante de un archivo
collada *.dae, asi como informacion relacionada con sus librerias 
internas y sus geometrias.

@author: Luis Antonio Fernandez Suarez
@version: 1.1
"""

from typing import Text
import xml.etree.ElementTree as ET
import sys

import os
# Utilizado para que la consolo de windows (cmd o powershell) habiliten los colores ANSI
# durante la ejecucion de este programa
os.system("color") 

SEPARATOR = "--------------------------------------------------------------------------------------------------------"

class Format:
    LABEL = "\033[1;33m"
    STATEMENT = "\033[1;34m"
    UNDERLINE = "\033[4m"
    RESET = "\033[0m"

# Variable Global file
file = open("arbolFamiliar.svg", "w") # Abre y borra automaticamente el contenido del archivo
ns = {'collada' : 'http://www.collada.org/2005/11/COLLADASchema'}   # diccionario usado para facilitar la sintaxis de las consultas


def label(line):
    ''' 
    Funcion usada para dar el formato de label a una linea,
    este consiste en un texto amarillo y en negrita
    '''
    return Format.LABEL + line + Format.RESET


def statement(line):
    ''' 
    Funcion usada para dar el formato de label a una linea,
    este consiste en un texto azul y en negrita
    '''
    return Format.STATEMENT + line + Format.RESET


def get_arbol_ET(archivo_DAE):
    try:
        arbol = ET.parse(archivo_DAE)
    except IOError:
        print("No se encuentra el archivo ", archivo_DAE)
        sys.exit()

    except ET.ParseError:
        print("Error procesando el archivo XML ", archivo_DAE)
        sys.exit()

    return arbol

def show_collada_info(archivo_DAE):
    """
    Funcion que mostrará Informacion relevante del archivo collada tales como autor, 
    fecha de creacion, modificacion , etc.
    """
    arbol = get_arbol_ET(archivo_DAE)
    raiz = arbol.getroot() # Raiz del documento

    print(statement("Informacion relevante del archivo {0}:".format(archivo_DAE)))

    contributor = raiz.find("collada:asset/collada:contributor", ns)
    print(label("\tAutor del documento: ") + contributor.find("collada:author", ns).text)
    print(label("\tHerramienta de autoria: ") + contributor.find("collada:authoring_tool", ns).text)
    
    fecha_creacion = raiz.find("collada:asset/collada:created", ns)
    print(label("\tFecha de creacion: ") + fecha_creacion.text)

    for mod in raiz.findall("collada:asset/collada:modified", ns):
        print(label("\t\tModificacion: ") + mod.text)


def show_elements_in_library(raiz,library, element):
    """
    Funcion que muestra el numero de elementos de una ibreria
    interna collada junto al ID y Nombre de los elementos que contiene.
    """
    elements = raiz.findall("collada:{0}[1]/collada:{1}".format(library,element), ns) 
    print(label("\n{0}: ".format(library)) + "numero de elementos " + label(str(len(elements))))
    for elem in elements:
        print(label("\tElement ID: ") + elem.attrib.get("id") + label(" Element Name: ") + elem.attrib.get("name"))


def show_elements_in_library_no_name(raiz,library, element):
    """
    Funcion que muestra el numero de elementos de una ibreria
    interna collada junto al ID de los elementos que contiene.

    Esta funcion sirve para analizar dichas librerias cuyos elementos no contienen el atributo
    nombre.
    """
    elements = raiz.findall("collada:{0}[1]/collada:{1}".format(library,element), ns) 
    print(label("\n{0}: ".format(library)) + "numero de elementos " + label(str(len(elements))))
    for elem in elements:
        print(label("\tElement ID: ") + elem.attrib.get("id"))


def show_collada_libraries(archivo_DAE):
    """
    Funcion que da una informacion detallada de las librerias internas que utiliza el
    archivo collada *.dae, junto a los elementos que contiene
    """
    arbol = get_arbol_ET(archivo_DAE)
    raiz = arbol.getroot()

    print(statement("Informacion de las librerias del archivo {0}:".format(archivo_DAE)))
    show_elements_in_library(raiz, "library_cameras", "camera") # Muestra las camaras
    show_elements_in_library(raiz, "library_images", "image") # Muestra las imagenes
    show_elements_in_library_no_name(raiz, "library_effects", "effect") # Muestra los efectos
    show_elements_in_library(raiz, "library_materials", "material") # Muestra los materiales
    show_elements_in_library(raiz, "library_geometries", "geometry") # Muestra las geometrias
    show_elements_in_library(raiz, "library_controllers", "controller") # Muestra os controladores
    show_elements_in_library(raiz, "library_visual_scenes", "visual_scene") # Muestra las escenas visuales


def show_geometry_info(geometry):
    """
    Funcion que Muestra informacion de una geometria dada.
    """
    print(label("\tID de la geomtria: ") + geometry.attrib.get("id") +
        label(" Nombre de la geometria: ") + geometry.attrib.get("name"))    


def show_node_info_and_meshes(raiz, node):
    """
    Funcion que muestra la informacion de cada nodo de la escena visual
    junto a las gemotrias que lo componen
    """
    print(label("\nID Nodo: ") + node.attrib.get('id') + 
        label(" Nombre del Nodo: ") + node.attrib.get('name'))

    for geometry_instance in node.findall("./collada:instance_geometry", ns):
        geomtry_id = geometry_instance.attrib.get('url')[1:] # Id de la geomtria
        geomtry = raiz.find("collada:library_geometries[1]/collada:geometry[@id='{0}']".format(
            geomtry_id
        ), ns) # Elemento Geomtria perteneciente al arbol
        
        show_geometry_info(geomtry) # Mostrar la informacion de la geometria


def show_collada_meshes(archivo_DAE):
    """
    Muestra los nodos que componen la escena visual actual junto a las geometrias que lo componen
    """
    arbol = get_arbol_ET(archivo_DAE)
    raiz = arbol.getroot()

    # Variable que nos indica la escena visual que valla a usar el archivo.
    # Esto se hace porque un archivo puede contener multiples escenas visuales
    # pero se usa la que se instancia en el elemento <scene>
    instance_visual_scene = raiz.find("collada:scene[1]/collada:instance_visual_scene[1]", ns)
    
    # La id se obinen de la URL quitando el primer caracter '#'
    visual_scene_ID = instance_visual_scene.attrib.get("url")[1:] 

    # La visual scene utilizada
    visual_scene = raiz.find("collada:library_visual_scenes[1]/collada:visual_scene[@id='{0}']".format(
        visual_scene_ID
    ), ns)

    for node in visual_scene.findall("./collada:node", ns):
        show_node_info_and_meshes(raiz, node)

def main():

    opt = 0
    end = False
    
    print(__doc__)

    archivo_DAE = "espada.dae"

    while end == False:
        print(Format.UNDERLINE + "Opciones del programa:" + Format.RESET) 
        print(statement("\t1. Mostar Informacion del archivo Collada."))
        print(statement("\t2. Mostar Informacion de las librerias del archivo Collada."))
        print(statement("\t3. Mostar las nodos y su geometrias(mesh) en al escena actual."))
        print(statement("\t4. Salir"))

        opt = input("Por favor, seleccione una Opcion: ")
        
        if opt == "1":
            print(SEPARATOR)
            print(show_collada_info.__doc__)
            show_collada_info(archivo_DAE)
            print("\n"+ SEPARATOR)
        if opt == "2":
            print(SEPARATOR)
            print(show_collada_libraries.__doc__)
            show_collada_libraries(archivo_DAE)
            print("\n"+ SEPARATOR)
        if opt == "3":
            print(SEPARATOR)
            print(show_collada_libraries.__doc__)
            show_collada_meshes(archivo_DAE)
            print("\n"+ SEPARATOR)
        if opt == "4":
            end = True

    print(label("Gracias por usar collada_reader!"))      


if __name__ == "__main__":
    main()
