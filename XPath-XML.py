# # -*- coding: utf-8 -*-
""""
Trasformar Codigo XML a HTML usando XPath
@author: Luis Antonio Fernandez Suarez
"""

from typing import Text
import xml.etree.ElementTree as ET

# Variable Global file
file = open("sample.html", "w") # Abre y borra automaticamente el contenido del archivo

def write_in_file(line):
    """"""
    file.write(line)
    file.write("\n")

def xml_2_HTML(archivo_XML):
    """Función xml_2_HTML(archivo_XML):
    Transforma el contenido de un archivo XML basado
    en el XML Schema arbolGenealogico en un documento HTML

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
    
    raiz = arbol.getroot()

    write_in_file('<!DOCTYPE HTML>')
    write_in_file('<html lang="es">')
    write_in_file_HTML_head()

    write_in_file('<body>')

    nombre = raiz.find("familiar[1]").attrib.get('nombre')
    apellido = raiz.find("familiar[1]").attrib.get('apellido')
    write_in_file('<h1>Arbol genealogico de {0} {1}</h1>'.format(nombre, apellido))

    ### Raiz del arbol ##############################################################
    write_in_file('<h2> La Raiz </h2>')
 
    familiarRaiz =  raiz.find("familiar[1]") 
    
    parse_familiar_data(familiarRaiz)
    #################################################################################

    ### Padres ######################################################################
    write_in_file("<h2> Los Padres </h2>")
    for padre in familiarRaiz.findall("./familiar"):
        parse_familiar_data(padre)
    #################################################################################

    ### Abuelos ######################################################################
    write_in_file("<h2> Abuelos Paternos</h2>")
    for abuelo in familiarRaiz.findall("./familiar[1]/familiar"):
        parse_familiar_data(abuelo)
    
    write_in_file("<h2> Abuelos Maternos</h2>")
    for abuelo in familiarRaiz.findall("./familiar[2]/familiar"):
        parse_familiar_data(abuelo)
    #################################################################################

    ### Bisabuelos ###################################################################
    write_in_file("<h2> Bisabuelos Paternos</h2>")
    for bis_abuelo in familiarRaiz.findall("./familiar[1]/familiar[1]/familiar"):
        parse_familiar_data(bis_abuelo)

    write_in_file("<h2> Bisabuelos Maternos</h2>")
    bisabuelos_maternos = familiarRaiz.findall("./familiar[2]/familiar[1]/familiar") + familiarRaiz.findall("./familiar[2]/familiar[2]/familiar")

    for bis_abuelo in bisabuelos_maternos:
        parse_familiar_data(bis_abuelo)
    #################################################################################
    write_in_file('</body>')
    write_in_file('</html>')
    
def write_in_file_HTML_head():
    write_in_file('<head>')
    # charset
    write_in_file('\t<meta charset="UTF-8"/>')
    
    # author
    write_in_file('\t<meta name="author" content="Luis A. Fernandez Suarez"/>')

    # description
    write_in_file('\t<meta name="description" content="Pagina auto-generada a partir de un ' + 
        'archivo XML dedicada a mostrar el arbol genealogico del Alumno"/>')

    write_in_file('\t<link rel="stylesheet" type="text/css" href="estilos.css" />')
    write_in_file('\t<title>Arbol Genealogico - Inicio</title>')
    write_in_file('</head>')

def parse_familiar_data(familiar):
    """Convertir el contenido del elemento xs:dataFamiliar a codigo HTML, incluyendo las fotos y videos"""

    write_in_file("<h3>"+ familiar.attrib.get('nombre') + " " + familiar.attrib.get('apellido') + "</h3>")

    data = familiar.find("./dataFamiliar[1]") 
    # print(data.tag) data = dataFamiliar
    nacimiento = data.find("./nacimiento[1]")

    fecha = nacimiento.find("./fecha").text
    lugar =  nacimiento.find("./lugar").text 
    coordenadas = "{0},{1},{2}".format(str(nacimiento.find("./coordenadas").attrib.get("latitud")),
                                        str(nacimiento.find("./coordenadas").attrib.get("longitud")),
                                        str(nacimiento.find("./coordenadas").attrib.get("altitud")))

    write_in_file("<ul>")
    write_in_file("\t<li><b>fecha de nacimiento: </b>" + fecha + "</li>")
    write_in_file("\t<li><b>lugar de nacimiento: </b>" + lugar + "</li>")
    write_in_file("\t<li><b>coordenadas: </b>" + coordenadas + "</li>")
    write_in_file("</ul>")

    fallecimiento = data.find("./fallecimiento[1]")
    if fallecimiento != None:
        fecha_f = fallecimiento.find("./fecha").text
        lugar_f =  fallecimiento.find("./lugar").text 
        coordenadas_f = "{0},{1},{2}".format(str(fallecimiento.find("./coordenadas").attrib.get("latitud")),
                                        str(fallecimiento.find("./coordenadas").attrib.get("longitud")),
                                        str(fallecimiento.find("./coordenadas").attrib.get("altitud")))

        write_in_file("<ul>")
        write_in_file("\t<li><b>fecha de fallecimiento: </b>" + fecha_f + "</li>")
        write_in_file("\t<li><b>lugar de fallecimiento: </b>" + lugar_f + "</li>")
        write_in_file("\t<li><b>coordenadas: </b>" + coordenadas_f + "</li>")
        write_in_file("</ul>")

    parse_fotos(data, familiar)
    parse_videos(data, familiar)


def parse_fotos(data, familiar):
    """ Convertir elemento xs:retrato a HTML <img>"""
    _foto_index = 1
    for retrato in data.findall("./retrato"):
        alt = "foto " + str(_foto_index) +" de " + str(familiar.attrib.get("nombre"))
        write_in_file('<img src="{0}" alt="{1}"/><br />'.format(retrato.text, alt))
        _foto_index = _foto_index + 1

def parse_videos(data, familiar):
    """ Convertir elemento xs:video a HTML <video>"""
    for video in data.findall("./video"):
        write_in_file('<video controls>')
        write_in_file('\t<source src="{0}" type="video/mp4"/><br />'.format(video.text))
        write_in_file('</video>')

def main():
    print(xml_2_HTML.__doc__)
    archivoXML = "arbolGenealogico.xml"
    xml_2_HTML(archivoXML)

    file.close()
    print

if __name__ == "__main__":
    main()