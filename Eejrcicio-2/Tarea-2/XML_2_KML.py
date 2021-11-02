# # -*- coding: utf-8 -*-
""""
Trasformar Codigo XML a KML usando XPath
@author: Luis Antonio Fernandez Suarez
"""

from typing import Text
import xml.etree.ElementTree as ET

# Variable Global file
file = open("coordenadasFamilia.kml", "w") # Abre y borra automaticamente el contenido del archivo

def write_in_file(line):
    """ Funcion que escribe la linea en el archivo y agrega un salto de linea"""
    file.write(line)
    file.write("\n")


def xml_2_kml(archivo_XML):
    """
    Función xml_2_kml(archivo_XML):
    Transforma el contenido de un archivo XML basado
    en el XML Schema arbolGenealogico en un documento KML que pueda ser interpretado por Google Earth

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
    write_in_file_kml_head()

    write_in_file('<Document>')
    write_name_tag('coordenadas de familiares')
    
    familiar_raiz = raiz.find("familiar[1]")
    parse_coordenadas_familiar(familiar_raiz) # Adaptar elemento <Familiar> de XML a elemento <Placemark> de KML

    write_in_file('</Document>')
    write_in_file('</kml>')


def parse_coordenadas_familiar(familiar):
    ''' Funcion que adapta un elemento <Familiar> de XML Schema 'arbolGenealogico.xsd' a elemento <Placemark> de KML'''    
    data = familiar.find("./dataFamiliar[1]") # consigue el elemento <dataFamiliar>

    nacimiento = data.find("./nacimiento")
    parse_lugar_nacimiento(nacimiento, familiar)

    fallecimiento = data.find("./fallecimiento")
    if fallecimiento != None: # Añade un placemark para el lugar de muerte en caso de haberlo
        parse_lugar_fallecimiento(fallecimiento,familiar)

    for parent in familiar.findall('./familiar'): # Padres del familiar
        parse_coordenadas_familiar(parent) # Llamada recursiva que recorre todo el arbol de "arbolGenealogico.xml"


def parse_lugar_nacimiento(nacimiento, familiar):
    '''
        Añade un elemento <Placemark> para la ubicacion de nacimiento de un familiar
    '''
    nombre = familiar.attrib.get('nombre')
    apellido = familiar.attrib.get('apellido')
    lugar = nacimiento.find('./lugar').text

    coordenadas = nacimiento.find('./coordenadas') # Elemento <Coordenadas> perteneciente a XML Schema "arbolGenealogico.xsd"

    longitud = coordenadas.attrib.get('longitud')
    latitud = coordenadas.attrib.get('latitud')
    altitud = coordenadas.attrib.get('altitud')

    write_in_file('<Placemark>') # Placemark de nacimiento

    write_name_tag('Lugar de nacimiento de ' + nombre + ' ' + apellido) # Nombre de la placemark

    write_in_file('<Point>')
    write_coordinates_tag('{0},{1},{2}'.format(str(longitud), str(latitud), str(altitud))) # String with Format: <long>,<lat>,<alt>
    write_in_file('</Point>')

    write_in_file('</Placemark>')


def parse_lugar_fallecimiento(fallecimiento, familiar):
    '''
        Añade un elemento <Placemark> para la ubicacion de fallecimiento de un familiar
    '''
    nombre = familiar.attrib.get('nombre')
    apellido = familiar.attrib.get('apellido')
    lugar = fallecimiento.find('./lugar').text

    coordenadas = fallecimiento.find('./coordenadas') # Elemento <Coordenadas> perteneciente a XML Schema "arbolGenealogico.xsd"

    longitud = coordenadas.attrib.get('longitud')
    latitud = coordenadas.attrib.get('latitud')
    altitud = coordenadas.attrib.get('altitud')

    write_in_file('<Placemark>') # Placemark de fallecimiento

    write_name_tag('Lugar de fallecimiento de ' + nombre + ' ' + apellido) # Nombre de la placemark

    write_in_file('<Point>')
    write_coordinates_tag('{0},{1},{2}'.format(str(longitud), str(latitud), str(altitud))) # String with Format: <long>,<lat>,<alt>
    write_in_file('</Point>')
    
    write_in_file('</Placemark>')


def write_in_file_kml_head():
    '''
    Incluye la cabecera del archivo kml:
        <?xml version="1.0" encoding="UTF-8"?>
        <kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">
    '''
    write_in_file('<?xml version="1.0" encoding="UTF-8"?>')
    write_in_file('<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">')


def write_name_tag(name):
    '''
    Incluye un tag <name>  con el siguiente formato
        <name> 'nombre indicado como parametro' </name>
    '''
    write_in_file('<name> ' + name + ' </name>')


def write_coordinates_tag(coordinates):
    '''
    Incluye un elemento <coordinates>  con el siguiente formato
        <coordinates> 'Coordenadas separadas por comas dadas como parametro' </coordinates>
    '''
    write_in_file('<coordinates>' + coordinates + '</coordinates>')


def main():
    print(xml_2_kml.__doc__)
    
    archivo_XML = "arbolGenealogico.xml"
    xml_2_kml(archivo_XML)

    file.close()
    print


if __name__ == "__main__":
    main()
