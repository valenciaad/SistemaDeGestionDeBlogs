from flask import Flask, render_template, request, flash, request, redirect, url_for
from datetime import datetime
import json
import os.path
from datetime import date
from collections import defaultdict
from werkzeug.utils import secure_filename
import yagmail as yagmail


UPLOAD_FOLDER = os.path.abspath(os.getcwd()) + '\static\imagenes'

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = os.urandom(24)

# Lee el archivo db.json y retorna el array ordenado por fecha
# ordenadaFecha - la los datos  del archivo ordenados por fecha
def recientes():
    if os.path.exists('db.json'):
        with open('db.json') as db:
            ordenadaFecha = json.load(db)
            ordenadaFecha.sort(reverse=True, key=lambda x: datetime.strptime(
                x['fecha'], '%d/%m/%Y,%H:%M:%S'))
            for i, data in enumerate(ordenadaFecha):
                ordenadaFecha[i]["contenido"] = (
                    data["contenido"][:100] + '...')
    return ordenadaFecha

# Lee el archivo db.json y retorna la fila espesificada
# row - la fila que se quiere obtener del archivo
def query(row):
    if os.path.exists('db.json'):
        with open('db.json') as jdb:
            db = json.load(jdb)
    return db[row]

# retorna un nuevo id
# id - nuevo id de bog
def existe():
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


#rutara la pagina de index
@app.route('/')
def home():
    return render_template('index.html', titulo="Bienvenido")

# Inicio código login


def isUsernameValid(user):
    if user == "Prueba":
        return True
    else:
        return False


def isPasswordValid(password):
    print(type(password))
    if password == "Prueba1234":
        return True
    else:
        return False

# ruta para la pagina de index, es la misma de login
@app.route("/login", methods=('GET', 'POST'))
def login():
    try:

        username = request.args.get('user')
        password = request.args.get('pssw')

        error = None

        if not isUsernameValid(username):
            error = "Usuario incorrecto"
            flash(error)
            return render_template("index.html")
        if not isPasswordValid(password):
            error = "Contraseña incorrecta"
            flash(error)
            return render_template("index.html")
        return panelBlog()
    except:
        flash("Error en el inicio de sesión")
        return render_template("index.html")
# fin código login

#rutara la pagina de Crear blog
#Toma los datos del formulario por get o por post los guarda en un dicionario y luego los escribe en un archivo de json
@app.route('/crearBlog', methods=['GET', 'POST'])
def crearBlog():
    ordenadaFecha = recientes()
    id = existe()
    now = datetime.now()
    fecha = now.strftime("%d/%m/%Y,%H:%M:%S")
    cuerpo = {}
    if request.method == 'POST':
        contenido = request.form["cuerpoBlog"]
        titulo = request.form["titulo"]
        imagen = request.files["subirImagen"]
        if imagen and allowed_file(imagen.filename):
            nombreImagen = secure_filename(str(id)+imagen.filename)
            imagen.save(os.path.join(
                app.config['UPLOAD_FOLDER'], nombreImagen))
        cuerpo = {"contenido": contenido,
                  "titulo": titulo,
                  "blogId": id,
                  "imagen": nombreImagen,
                  "fecha": fecha}
        if (id != None and contenido != None):
            with open('db.json') as jdb:
                db = json.load(jdb)
                db.append(cuerpo)
                write_json(db)
                return redirect('/paginaBlog/'+str(id))
    return render_template('crearBlog.html', titulo="Crear Blog", ordenadaFecha=ordenadaFecha)

#Ruta para panel de blog
@app.route('/panelBlog')
def panelBlog():
    ordenadaFecha = recientes()
    return render_template('panelBlog.html', titulo="Panel de Blog", ordenadaFecha=ordenadaFecha)

#Ruta para verficar correo
@app.route('/verificarCorreo')
def verificarCorreo():
    ordenadaFecha = recientes()     
    return render_template('verificarCorreo.html', titulo="verificar Correo", ordenadaFecha=ordenadaFecha)

#Ruta para pagina de blog
@app.route('/paginaBlog/')
@app.route('/paginaBlog/<int:blogId>')
def paginaBlog(blogId=0):
    contenidoBlog = query(blogId)
    ordenadaFecha = recientes()
    return render_template('paginaBlog.html', contenidoBlog=contenidoBlog, titulo=contenidoBlog["titulo"], ordenadaFecha=ordenadaFecha)

#Ruta para resultados de busqueda
@app.route('/resultadoBusqueda')
def resultadoBusqueda():
    ordenadaFecha = recientes()
    return render_template('resultadoBusqueda.html', titulo="Resultado de busqueda", ordenadaFecha=ordenadaFecha)

#Ruta para panel de usuario
@app.route('/panelUsuario')
def panelUsuario():
    ordenadaFecha = recientes()
    return render_template('panelUsuario.html', titulo="Panel de usuario", ordenadaFecha=ordenadaFecha)

#Ruta para recuperar contaseña
@app.route('/recuperarPassword',methods=["GET","POST"])
def recuperarPassword():    
    try:
        ordenadaFecha = recientes()
        if request.method == 'POST':
            email = request.form['correo']            
        else:
            email = request.args.get('correo')
        error = None
        yag = yagmail.SMTP('uninortegrupo9b@gmail.com','unigrupob')
        yag.send(to=email, subject='Recupera tu contraseña', 
                contents='Con el siguiente link puedes recuperar tu contraseña ('+request.method+')')
        if (email == None):
            error = 'escribe un correo'
            flash(error)            
        else:
            flash('verifica tu correo')
            render_template('recuperarPassword.html', titulo="Recuperar contraseña", ordenadaFecha=ordenadaFecha)
       # return render_template('recuperarPassword.html', titulo="verificar Correo", ordenadaFecha=ordenadaFecha)
    except:
        return render_template('/recuperarPassword.html', titulo="Recuperar contraseña", ordenadaFecha=ordenadaFecha)   
    return render_template('recuperarPassword.html', titulo="Recuperar contraseña", ordenadaFecha=ordenadaFecha)

#Ruta para crear cuenta
@app.route('/crearCuenta')
def crearCuenta():
    return render_template('crearCuenta.html', titulo="Crear cuenta")

#Ruta para editar un blog
#toma el id de blog por get o post y lo manda como parametro a query 
#llena el formulario con la informacion retornada de query y da la opcion de actulizar los datos en el archivo de json
@app.route('/editar/', methods=['GET', 'POST'])
@app.route('/editar/<int:blogId>', methods=['GET', 'POST'])
def editar(blogId=0):
    ordenadaFecha = recientes()
    contenidoBlog = query(blogId)
    now = datetime.now()
    fecha = now.strftime("%d/%m/%Y,%H:%M:%S")
    nombreImagen = contenidoBlog['imagen']
    if request.method == 'POST':
        contenido = request.form["cuerpoBlog"]
        titulo = request.form["titulo"]
        if request.files["subirImagen"] != None:
            imagen = request.files["subirImagen"]
            if imagen and allowed_file(imagen.filename):
                nombreImagen = secure_filename(str(id)+imagen.filename)
                imagen.save(os.path.join(
                    app.config['UPLOAD_FOLDER'], nombreImagen))
        cuerpo = {"contenido": contenido,
                  "titulo": titulo,
                  "blogId": blogId,
                  "imagen": nombreImagen,
                  "fecha": fecha}
        if (id != None and contenido != None):
            with open('db.json') as jdb:
                db = json.load(jdb)
                db[blogId] = cuerpo
                write_json(db)
                return redirect('/paginaBlog/'+str(blogId))

    return render_template('editar.html', titulo="Editar", ordenadaFecha=ordenadaFecha, contenidoBlog=contenidoBlog)
