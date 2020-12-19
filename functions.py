import json
import os
import re
import yagmail as yagmail
from sqlalchemy.sql.elements import Null
from validate_email import validate_email

from classes import *


# Expresión regular que permite verificar la contraseña.
# Puede contener cualquier letra minúscula y mayúscula
# así como números enteros. Su longitud mínima debe ser de 8
pass_reguex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[^\W_]{8,}$"
# Expresión regular que permite verificar el usuario.
# Debe contener cualquier letra minúscula y mayúscula
# así como números enteros. Su longitud mínima debe ser de 8
user_reguex = "^[a-zA-Z0-9_.-]{8,}$"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def recientes():
    objetos = Blog.query.filter_by(estado = 1,publico = True).limit(5)
    ordenadaFecha = esBlogs.dump(objetos)
    ordenadaFecha.sort(reverse=True, key=lambda x: datetime.strptime(
                x['fecha'], '%Y-%m-%dT%H:%M:%S.%f'))
    #if os.path.exists('db.json'):
      #  with open('db.json') as db:
      #     ordenadaFecha = json.load(db)
       #     ordenadaFecha.sort(reverse=True, key=lambda x: datetime.strptime(
       #         x['fecha'], '%d/%m/%Y,%H:%M:%S'))
    for i, data in enumerate(ordenadaFecha):
        ordenadaFecha[i]["contenido"] = (
            data["contenido"][:100] + '...')
    return ordenadaFecha


def query(row):
    db = Null
    if os.path.exists('db.json'):
        with open('db.json') as jdb:
            db = json.load(jdb)
    return db[row]


# Lee el archivo db.json y retorna un array de dictionarios que en el titulo tienen la palabra ingresada
# palabra - palabra a buscar
#resultados - array de dict con los matches
def queryBuscar(pablara):
    objetos = Blog.query.filter_by(estado = 1, publico = True)
    db = esBlogs.dump(objetos)
    resultados=[]
    #if os.path.exists('db.json'):
     #   resultados=[]
      #  with open('db.json') as jdb:
       #     db = json.load(jdb)
    for diccionario in db:
         if pablara.upper() in diccionario['titulo'].upper()  and diccionario['estado'] == True:                
             resultados.append(diccionario)
    return resultados   

# retorna un nuevo id
# id - nuevo id de bog


def existe():
    db = Null
    if os.path.exists('db.json'):
        with open('db.json') as jdb:
            db = json.load(jdb)
    id = 0
    for datos in db:
        if id == datos['blogId']:
            id = id + 1
            print(datos['blogId'])
        else:
            break
    return id

# Escribe datos en db.json


def write_json(data, filename='db.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

# limita las extensiones que se pueden subir


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# isUsernameValid: función que verifica que el usuario sea correcto. Por defecto se usó "Prueba"


def isUsernameValid(user):
    if user == "Prueba":
        return True
    else:
        return False

# isPasswordValid: función que verifica que la contraseña sea correcta. Por defecto se usó "Prueba1234"


def isPasswordValid(password):
    #print(type(password))
    if password == "Prueba1234":
        return True
    else:
        return False

# isEmailValid: Función que valida si es correcto un email usando el paquete validate_email
def isEmailValid(email):
    is_valid = validate_email(email)
    return is_valid

# isUsernameValid1: función que verifica basados
# en la expresión regular definida anteriormente
# que el usuario tenga caracteres permitidos


def isUsernameValid1(user):
    if re.search(user_reguex, user):
        return True
    else:
        return False

# isPasswordValid: función que verifica basados
# en la expresión regular definida anteriormente
# que la contraseña tenga caracteres permitidos


def isPasswordValid(password):
    if re.search(pass_reguex, password):
        return True
    else:
        return False
