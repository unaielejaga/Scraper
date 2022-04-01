import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('firebase-sdk.json')

firebase_admin.initialize_app(cred, {

    'databaseURL': 'https://my-app-20856-default-rtdb.europe-west1.firebasedatabase.app/'
})

ref = db.reference('/recetas')


ref.set({
    'receta1':{
        'nombre': 'Pan',
        'ingredientes': {
            'ingrediente3': {
                'nombre': 'Levadura',
                'cantidad': 200,
                'unidad': 'g'
            },
        },
        'duracion': 10
    }
})


