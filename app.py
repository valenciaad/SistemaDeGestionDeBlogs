from flask import Flask,render_template
from datetime import datetime 
import json
import os.path

app = Flask(__name__)


if os.path.exists('db.json'):
    with open('db.json') as db:
        ordenadaFecha = json.load(db)
        ordenadaFecha.sort(key = lambda x: datetime.strptime(x['fecha'], '%d/%m/%Y')) 
        for i,data in enumerate(ordenadaFecha):
            ordenadaFecha[i]["contenido"] = (data["contenido"][:100] + '...')

def query (row):
    if os.path.exists('db.json'):
        with open('db.json') as jdb:
            db = json.load(jdb)
    return db[row]

@app.route('/')
def home():
    return render_template('index.html',titulo="Bienvenido")


@app.route('/crearBlog')
def crearBlog():
    if request.method =='POST'
        contenido = {}
        contenido[resquest.form.get[]]
    return render_template('crearBlog.html',titulo="Crear Blog",ordenadaFecha=ordenadaFecha)

@app.route('/panelBlog')
def panelBlog():
    return render_template('panelBlog.html',titulo="Panel de Blog",ordenadaFecha=ordenadaFecha)

@app.route('/verificarCorreo')
def verificarCorreo():
    return render_template('verificarCorreo.html',titulo="verificar Correo",ordenadaFecha=ordenadaFecha)


@app.route('/paginaBlog/')
@app.route('/paginaBlog/<int:blogId>')
def paginaBlog(blogId=0):
    contenidoBlog = query (blogId)
    return render_template('paginaBlog.html',contenidoBlog=contenidoBlog, titulo=contenidoBlog["titulo"],ordenadaFecha=ordenadaFecha)


@app.route('/resultadoBusqueda')
def resultadoBusqueda():
    return render_template('resultadoBusqueda.html',titulo="Resultado de busqueda",ordenadaFecha=ordenadaFecha)


@app.route('/panelUsuario')
def panelUsuario():
    return render_template('panelUsuario.html',titulo="Panel de usuario",ordenadaFecha=ordenadaFecha)


@app.route('/recuperarPassword')
def recuperarPassword():
    return render_template('recuperarPassword.html',titulo ="Recuperar contraseña",ordenadaFecha=ordenadaFecha)


@app.route('/crearCuenta')
def crearCuenta():
    return render_template('crearCuenta.html',titulo =  "Crear cuenta")
 