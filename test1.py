from typing import Text
import xml.etree.ElementTree as ET

def verXPath(archivoXML, expresionXPath):
    try:
        arbol = ET.parse(archivoXML)
    except IOError:
        print("No se encuentra el archivo ", archivoXML);
        exit()

    except ET.ET.ParseError:
        print("Error procesando el archivo XML ", archivoXML)
        exit()
    
    raiz = arbol.getroot()

    for hijo in raiz.findall(expresionXPath):
        print("\nElemento = ", hijo.tag)
        if hijo.text != None:
            print("Contenido = ", hijo.text.strip('\n'))
        else:
            print("contenido = ", hijo.text)
        
        print("Atributos = ", hijo.attrib)



def verXPath2(archivoXML):
    try:
        arbol = ET.parse(archivoXML)
    except IOError:
        print("No se encuentra el archivo ", archivoXML);
        exit()

    except ET.ET.ParseError:
        print("Error procesando el archivo XML ", archivoXML)
        exit()
    
    raiz = arbol.getroot()

    # ## Raiz del arbol ############################################################
    print("<h2> La Raiz </h2>")
 
    familiarRaiz =  raiz.find("familiar[1]") 
    
    parseFamiliarData(familiarRaiz)
    # ###############################################################################

    print("<h2> Los Padres </h2>")
    for padre in familiarRaiz.findall("./familiar"):
        parseFamiliarData(padre)



def parseFamiliarData(familiar):

    print("<h3>"+ familiar.attrib.get('nombre') + " " + familiar.attrib.get('apellido') + "</h3>")

    data = familiar.find("./dataFamiliar[1]") 
    # print(data.tag) data = dataFamiliar
    nacimiento = data.find("./nacimiento[1]")

    fecha = nacimiento.find("./fecha").text
    lugar =  nacimiento.find("./lugar").text 
    coordenadas = "{0},{1},{2}".format(str(nacimiento.find("./coordenadas").attrib.get("latitud")),
                                        str(nacimiento.find("./coordenadas").attrib.get("longitud")),
                                        str(nacimiento.find("./coordenadas").attrib.get("altitud")))

    print("<ul>")
    print("\t<li> fecha de nacimiento: " + fecha + "</li>")
    print("\t<li> lugar de nacimiento: " + lugar + "</li>")
    print("\t<li> coordenadas: " + coordenadas + "</li>")
    print("</ul>")

    parseFotos(data, familiar)
    parseVideos(data, familiar)


def parseFotos(data, familiar):
    foto_index = 1
    for retrato in data.findall("./retrato"):
        alt = "foto " + str(foto_index) +" de " + str(familiar.attrib.get("nombre"))
        print('<img src="{0}" alt="{1}"/>'.format(retrato.text, alt))
        foto_index = foto_index + 1

def parseVideos(data, familiar):
    for video in data.findall("./video"):
        print('<video controls>')
        print('\t<source src="{0}" type="video/mp4"/>'.format(video.text))
        print('</video>')

def main():
    print(verXPath.__doc__)
    archivoXML = "arbolGenealogico.xml"
    # expresionXPath = input("Introduzca la expresion xpath: ")
    verXPath2(archivoXML)

if __name__ == "__main__":
    main()