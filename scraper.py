from bs4 import BeautifulSoup
import requests
import json

web = 'https://www.recetasderechupete.com/como-preparar-pollo-teriyaki-de-manera-facil-y-rapida/9848/'
resultado = requests.get(web)
sopa = BeautifulSoup(resultado.text, 'lxml')
ingredientes = sopa.find('div', id='ingredients').find('ul')

for li in ingredientes.find_all('li'):
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
    print(ingre)