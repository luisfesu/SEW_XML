from typing import Text
import xml.etree.ElementTree as ET

# Automatically clears all the file content
file = open("sample.html", "w")

def write(line):
    file.write(line)
    file.write("\n")

def verXPath(archivo_XML, expresion_XPath):
    try:
        arbol = ET.parse(archivo_XML)
    except IOError:
        print("No se encuentra el archivo ", archivo_XML);
        exit()

    except ET.ET.ParseError:
        print("Error procesando el archivo XML ", archivo_XML)
        exit()
    
    raiz = arbol.getroot()

    for hijo in raiz.findall(expresion_XPath):
        print("\nElemento = ", hijo.tag)
        if hijo.text != None:
            print("Contenido = ", hijo.text.strip('\n'))
        else:
            print("contenido = ", hijo.text)
        
        print("Atributos = ", hijo.attrib)



def xml_2_HTML(archivo_XML):
    try:
        arbol = ET.parse(archivo_XML)
    except IOError:
        print("No se encuentra el archivo ", archivo_XML)
        exit()

    except ET.ET.ParseError:
        print("Error procesando el archivo XML ", archivo_XML)
        exit()
    
    raiz = arbol.getroot()

    write('<!DOCTYPE HTML>')
    write('<html lang="es">')
    write_HTML_head()

    write('<body>')
    # ## Raiz del arbol ############################################################
    write('<h2> La Raiz </h2>')
 
    familiarRaiz =  raiz.find("familiar[1]") 
    
    parse_familiar_data(familiarRaiz)
    # ###############################################################################

    write("<h2> Los Padres </h2>")
    for padre in familiarRaiz.findall("./familiar"):
        parse_familiar_data(padre)

    write('</body>')
    write('</html>')
    
def write_HTML_head():
    write('<head>')
    # charset
    write('\t<meta charset="UTF-8"/>')
    
    # author
    write('\t<meta name="author" content="Luis A. Fernandez Suarez"/>')

    # description
    write('\t<meta name="description" content="Pagina auto-generada a partir de un ' + 
        'archivo XML dedicada a mostrar el arbol genealogico del Alumno"/>')

    write('\t<link rel="stylesheet" type="text/css" href="estilos.css" />')
    write('\t<title>Arbol Genealogico - Inicio</title>')
    write('</head>')

def parse_familiar_data(familiar):

    write("<h3>"+ familiar.attrib.get('nombre') + " " + familiar.attrib.get('apellido') + "</h3>")

    data = familiar.find("./dataFamiliar[1]") 
    # print(data.tag) data = dataFamiliar
    nacimiento = data.find("./nacimiento[1]")

    fecha = nacimiento.find("./fecha").text
    lugar =  nacimiento.find("./lugar").text 
    coordenadas = "{0},{1},{2}".format(str(nacimiento.find("./coordenadas").attrib.get("latitud")),
                                        str(nacimiento.find("./coordenadas").attrib.get("longitud")),
                                        str(nacimiento.find("./coordenadas").attrib.get("altitud")))

    write("<ul>")
    write("\t<li><b>fecha de nacimiento: </b>" + fecha + "</li>")
    write("\t<li><b>lugar de nacimiento: </b>" + lugar + "</li>")
    write("\t<li><b>coordenadas: </b>" + coordenadas + "</li>")
    write("</ul>")

    parse_fotos(data, familiar)
    parse_videos(data, familiar)


def parse_fotos(data, familiar):
    foto_index = 1
    for retrato in data.findall("./retrato"):
        alt = "foto " + str(foto_index) +" de " + str(familiar.attrib.get("nombre"))
        write('<img src="{0}" alt="{1}"/><br />'.format(retrato.text, alt))
        foto_index = foto_index + 1

def parse_videos(data, familiar):
    for video in data.findall("./video"):
        write('<video controls>')
        write('\t<source src="{0}" type="video/mp4"/><br />'.format(video.text))
        write('</video>')

def main():
    print(verXPath.__doc__)
    archivoXML = "arbolGenealogico.xml"
    # expresionXPath = input("Introduzca la expresion xpath: ")
    xml_2_HTML(archivoXML)

    file.close()

if __name__ == "__main__":
    main()