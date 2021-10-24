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

    for hijo in raiz.findall("familiar[1]/familiar[1]"):
        print("<h1> "+ hijo.attrib.get('nombre') + " </h1>")




def main():
    print(verXPath.__doc__)
    archivoXML = "arbolGenealogico.xml"
    # expresionXPath = input("Introduzca la expresion xpath: ")
    verXPath2(archivoXML)

if __name__ == "__main__":
    main()