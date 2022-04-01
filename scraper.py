from asyncio import FIRST_EXCEPTION
from asyncio.windows_events import NULL
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

stop_words = set(stopwords.words('spanish'))

class Receta:
    def __init__(self, nombre, dificultad, duracion, comensales, ingredientes, descripcion, url, imagen):
        self.nombre = nombre
        self.dificultad = dificultad
        self.duracion = duracion
        self.comensales = comensales
        self.ingredientes = ingredientes
        self.descripcion = descripcion
        self.url = url
        self.imagen = imagen
    def __str__(self):
        stringre = "\t"
        for i in self.ingredientes:
            stringre = stringre + '\n\tCantidad: ' + str(i[0][0]) + ', Unidad: ' + str(i[0][1]) + ', Ingrediente: ' + str(i[1])
        return 'Nombre: ' + str(self.nombre) + '\n' + 'Dificultad: ' + str(self.dificultad) + '\n' + 'Duracion: ' + str(self.duracion) + '\n' + 'Comensales: ' + str(self.comensales) + '\n' + 'Ingredientes: ' + stringre + '\nDescripcion: ' + str(self.descripcion) + '\nURL: ' + str(self.url) + '\n'

url = 'https://www.recetasderechupete.com/recetas-faciles/'

response = requests.get(url)
data = response.text
soup = BeautifulSoup(data, 'lxml')
contador_recetas = 1

cred = credentials.Certificate('firebase-sdk.json')

firebase_admin.initialize_app(cred, {

    'databaseURL': 'https://my-app-20856-default-rtdb.europe-west1.firebasedatabase.app/'
})

ref = db.reference('/recetas')

envio_receta_final = {}

for link in soup.find('div', class_='grid').find_all('a'):
    
    link_url = link.get('href')

    try:
        web = link_url
        resultado = requests.get(web)
        sopa = BeautifulSoup(resultado.text, 'lxml')

        receta = (sopa.find('header').find('h1').text).strip()
        try:
            imagen = (sopa.find('img', class_='mainphoto rdr-image wp-post-image').attrs['src'])
        except:
            imagen = 'https://img.icons8.com/ios-glyphs/50/000000/no-image.png'

        print(imagen)

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
            
            tokenize_words = word_tokenize(ingre[1])
            texto_sinSW = []
            for word in tokenize_words:
                if word not in stop_words:
                    texto_sinSW.append(word)
            ingre[1] = ' '.join(texto_sinSW)
            ingredientes.append(ingre)

        descripcion = sopa.find('div', id='description')
        descrip = []
        for ol in descripcion.find_all('ol'):
            for li in ol.find_all('li'):
                descrip.append(' '.join(li.text.split("\xa0")))
        descrip = ' '.join(descrip)


        recetafinal = Receta(receta, dificultad, duracion, comensales, ingredientes, descrip, link_url, imagen)
        envio_ingrediente = {}
        contador_ingrediente = 1
        for ingrediente in ingredientes:
            dict_ingrediente ={
                'ingrediente'+str(contador_ingrediente):{
                    'nombre': ingrediente[1],
                    'cantidad': ingrediente[0][0],
                    'unidad': ingrediente[0][1]
                },
            }
            envio_ingrediente.update(dict_ingrediente)
            contador_ingrediente+=1
        
        envio_receta = {
            'receta'+str(contador_recetas):{
                'nombre': recetafinal.nombre,
                'dificultad': recetafinal.dificultad,
                'duracion': recetafinal.duracion,
                'comensales': recetafinal.comensales,
                'descripcion': recetafinal.descripcion,
                'url': recetafinal.url,
                'ingredientes': envio_ingrediente,
                'receta': 'receta'+str(contador_recetas),
                'imagen': recetafinal.imagen
            }
        }
        envio_receta_final.update(envio_receta)
        if(contador_recetas == 80):
            ref.set(envio_receta_final)
            break
        print("Envio receta " + str(contador_recetas))
        contador_recetas+=1
        print("=======================================================================================================")
    except IndexError:
        print("Receta incorrecta")
        print("=======================================================================================================")
        continue
    except KeyboardInterrupt:
        break
    
