from flask import Flask,render_template,request
from datetime import datetime 
import json
import os.path
from datetime import date
from collections import defaultdict

app = Flask(__name__)

def recientes():
    if os.path.exists('db.json'):
        with open('db.json') as db:
            ordenadaFecha = json.load(db)
            ordenadaFecha.sort(reverse=True,key = lambda x: datetime.strptime(x['fecha'], '%d/%m/%Y')) 
            for i,data in enumerate(ordenadaFecha):
                ordenadaFecha[i]["contenido"] = (data["contenido"][:100] + '...')
            print(ordenadaFecha)
    return ordenadaFecha

def query (row):
    if os.path.exists('db.json'):
        with open('db.json') as jdb:
            db = json.load(jdb)
    return db[row]

def existe():
    if os.path.exists('db.json'):
        with open('db.json') as jdb:
            db = json.load(jdb)
    id = 0
    for datos in db:       
        if id == datos['blogId'] :
            id = id + 1
            print(datos['blogId'])
        else:
            break
    return id

def write_json(data, filename='db.json'): 
    with open(filename,'w') as f: 
        json.dump(data, f, indent=4)

@app.route('/')
def home():
    return render_template('index.html',titulo="Bienvenido")


@app.route('/crearBlog', methods=['GET','POST'])
def crearBlog():
    ordenadaFecha = recientes() 
    id = existe()
    today = date.today()
    fecha = today.strftime("%d/%m/%Y")
    cuerpo={}    
    if request.method =='POST':
        contenido = request.form["cuerpoBlog"]
        titulo = request.form["titulo"]
        cuerpo = {"contenido": contenido ,
        "titulo": titulo ,
        "blogId": id,
         "imagen": "imagen0.jpg",
        "fecha": fecha}
        if (id != None and contenido != None):
            with open('db.json') as jdb:
                db = json.load(jdb)
                db.append(cuerpo)
                write_json(db)       
    return render_template('crearBlog.html',titulo="Crear Blog",ordenadaFecha=ordenadaFecha)

@app.route('/panelBlog')
def panelBlog():
    ordenadaFecha = recientes() 
    return render_template('panelBlog.html',titulo="Panel de Blog",ordenadaFecha=ordenadaFecha)

@app.route('/verificarCorreo')
def verificarCorreo():
    ordenadaFecha = recientes() 
    return render_template('verificarCorreo.html',titulo="verificar Correo",ordenadaFecha=ordenadaFecha)


@app.route('/paginaBlog/')
@app.route('/paginaBlog/<int:blogId>')
def paginaBlog(blogId=0):
    contenidoBlog = query (blogId)
    ordenadaFecha = recientes() 
    return render_template('paginaBlog.html',contenidoBlog=contenidoBlog, titulo=contenidoBlog["titulo"],ordenadaFecha=ordenadaFecha)


@app.route('/resultadoBusqueda')
def resultadoBusqueda():
    ordenadaFecha = recientes() 
    return render_template('resultadoBusqueda.html',titulo="Resultado de busqueda",ordenadaFecha=ordenadaFecha)


@app.route('/panelUsuario')
def panelUsuario():
    ordenadaFecha = recientes() 
    return render_template('panelUsuario.html',titulo="Panel de usuario",ordenadaFecha=ordenadaFecha)


@app.route('/recuperarPassword')
def recuperarPassword():
    ordenadaFecha = recientes() 
    return render_template('recuperarPassword.html',titulo ="Recuperar contraseña",ordenadaFecha=ordenadaFecha)


@app.route('/crearCuenta')
def crearCuenta():    
    return render_template('crearCuenta.html',titulo =  "Crear cuenta")
 