from bs4 import BeautifulSoup
import requests

class Receta:
    def __init__(self, nombre, dificultad, duracion, comensales, ingredientes, descripcion):
        self.nombre = nombre
        self.dificultad = dificultad
        self.duracion = duracion
        self.comensales = comensales
        self.ingredientes = ingredientes
        self.descripcion = descripcion
    def __str__(self):
        stringre = "\t"
        for i in self.ingredientes:
            stringre = stringre + '\n\tCantidad: ' + str(i[0][0]) + ', Unidad: ' + str(i[0][1]) + ', Ingrediente: ' + str(i[1])
        return 'Nombre: ' + str(self.nombre) + '\n' + 'Dificultad: ' + str(self.dificultad) + '\n' + 'Duracion: ' + str(self.duracion) + '\n' + 'Comensales: ' + str(self.comensales) + '\n' + 'Ingredientes: ' + stringre + '\nDescripcion: ' + str(self.descripcion) + '\n'


f = open('recetas.txt','r')
with open('recetas.txt') as f:
    lines = f.readlines()
f.close()

for recetaslist in lines:
    web = recetaslist
    resultado = requests.get(web)
    sopa = BeautifulSoup(resultado.text, 'lxml')

    receta = (sopa.find('header').find('h1').text).strip()

    spans = [] 
    tag = sopa.find('div', class_='rdr-eat')
    for span in tag.find_all('span', class_='rdr-tag'):
        spans.append(span.text)
    dificultad = spans[0]
    duracion = spans[1]
    comensales = spans[2]

    ingredientes = []
    ingresopa = sopa.find('div', id='ingredients').find('ul')
    for li in ingresopa.find_all('li'):
        ingre = li.text.split(". ")
        if len(ingre) == 1:
            if ingre[0][0].isdigit():
                ingre = li.text.split(" " , 1)
                ingre[0] = [ingre[0], 'und']
            else:
                ingre = [['1', 'und'], ingre[0]]
        else:
            if ingre[0][0].isdigit():
                ingre[0] = ingre[0].split(" ")
            else:
                ingre[0] = (ingre[0].split(": "))[1]
                ingre[0] = ingre[0].split(" ")
        ingredientes.append(ingre)

    descripcion = sopa.find('div', id='description')
    descrip = []
    for ol in descripcion.find_all('ol'):
        for li in ol.find_all('li'):
            descrip.append(' '.join(li.text.split("\xa0")))
    descrip = ' '.join(descrip)


    recetafinal = Receta(receta, dificultad, duracion, comensales, ingredientes, descrip)
    print(str(recetafinal))
    print("=======================================================================================================")

