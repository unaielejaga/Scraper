from bs4 import BeautifulSoup
import requests
import json

web = 'https://www.recetasderechupete.com/zaatar-la-mezcla-de-especias-que-dara-un-toque-arabe-a-tus-recetas/44836/'
resultado = requests.get(web)
sopa = BeautifulSoup(resultado.text, 'lxml')

receta = (sopa.find('header').find('h1').text).strip()
print(receta)

spans = [] 
tag = sopa.find('div', class_='rdr-eat')
for span in tag.find_all('span', class_='rdr-tag'):
    spans.append(span.text)
dificultad = spans[0]
duracion = spans[1]
comensales = spans[2]
print(dificultad)
print(duracion)
print(comensales)

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
print(ingredientes)

descripcion = sopa.find('div', id='description')

descrip = []
for ol in descripcion.find_all('ol'):
    for li in ol.find_all('li'):
        descrip.append(' '.join(li.text.split("\xa0")))
descrip = ' '.join(descrip)
print(descrip)

