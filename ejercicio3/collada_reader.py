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
    return Format.STATEMENT + line + Format.RESET


def get_arbol_ET(archivo_DAE):
    try:
        arbol = ET.parse(archivo_DAE)
    except IOError:
        print("No se encuentra el archivo ", archivo_DAE)
        sys.exit()

    except ET.ET.ParseError:
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


def main():

    opt = 0
    end = False
    
    print(__doc__)

    archivo_DAE = "espada.dae"

    while end == False:
        print(Format.UNDERLINE + "Opciones del programa:" + Format.RESET) 
        print(statement("\t1. Mostar Informacion del archivo Collada."))
        print(statement("\t2. Mostar Informacion de las librerias del archivo Collada."))
        print(statement("\t3. Mostar las geometrias (meshes)."))
        print(statement("\t4. Salir"))

        opt = input("Por favor, seleccione una Opcion: ")
        
        if opt == "1":
            print(SEPARATOR)
            print(show_collada_info.__doc__)
            show_collada_info(archivo_DAE)
            print("\n"+ SEPARATOR)
        if opt == "2":
            end = True
        if opt == "3":
            end = True
        if opt == "4":
            end = True

    print(label("Gracias por usar collada_reader!"))      


if __name__ == "__main__":
    main()
