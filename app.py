import json
import os.path
from collections import defaultdict
from datetime import date, datetime

import yagmail as yagmail
from flask import Flask, flash, redirect, render_template, request, url_for
from validate_email import validate_email
from werkzeug.utils import secure_filename

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


@app.route('/')
def home():
    return render_template('index.html', titulo="Bienvenido")

# Inicio código login

# isUsernameValid: función que verifica que el usuario sea correcto. Por defecto se usó "Prueba"


def isUsernameValid(user):
    if user == "Prueba":
        return True
    else:
        return False

# isPasswordValid: función que verifica que la contraseña sea correcta. Por defecto se usó "Prueba1234"


def isPasswordValid(password):
    print(type(password))
    if password == "Prueba1234":
        return True
    else:
        return False

# login: función asignada a la ruta "/login" que admite los métodos GET and POST
# de acuerdo a la configuración en index.html, se dejó por defecto el método POST
# para enviar la información al servidor, esta recibe el usuario y contraseña y
# los verfica con las funciones ya descritas anteriormente y devuelve errores si los hay
# Cuando son correctos los datos, redirecciona a "/panelBlog"
# En el caso de encontrar un error diferente, ejecuta el código bajo "except"


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


@app.route('/panelBlog')
def panelBlog():
    ordenadaFecha = recientes()
    return render_template('panelBlog.html', titulo="Panel de Blog", ordenadaFecha=ordenadaFecha)


@app.route('/verificarCorreo')
def verificarCorreo():
    ordenadaFecha = recientes()
    return render_template('verificarCorreo.html', titulo="verificar Correo", ordenadaFecha=ordenadaFecha)


@app.route('/paginaBlog/')
@app.route('/paginaBlog/<int:blogId>')
def paginaBlog(blogId=0):
    contenidoBlog = query(blogId)
    ordenadaFecha = recientes()
    return render_template('paginaBlog.html', contenidoBlog=contenidoBlog, titulo=contenidoBlog["titulo"], ordenadaFecha=ordenadaFecha)


@app.route('/resultadoBusqueda')
def resultadoBusqueda():
    ordenadaFecha = recientes()
    return render_template('resultadoBusqueda.html', titulo="Resultado de busqueda", ordenadaFecha=ordenadaFecha)


@app.route('/panelUsuario')
def panelUsuario():
    ordenadaFecha = recientes()
    return render_template('panelUsuario.html', titulo="Panel de usuario", ordenadaFecha=ordenadaFecha)

# isEmailValid: Función que valida si es correcto un email usando el paquete validate_email


def isEmailValid(email):
    is_valid = validate_email(email)
    return is_valid

# recuperarPassword: función que permite los métodos GET y POST,
# cuando se hace un llamado se ejecuta el método GET y devuelve
# la página principal "recuperarPassword.html". Una vez se envíe
# el formulario se ejecuta el método POST y una vez verificado el
# correo electrónico se envía un mensaje desde la cuenta de Gmail
# configurada al correo suministrado.
# Esta es asignada a la ruta "/recuperarPassword/"


@app.route('/recuperarPassword/', methods=('GET', 'POST'))
def recuperarPassword():
    ordenadaFecha = recientes()
    if request.method == 'POST':
        email = request.form['mail']
        valid = isEmailValid(email)
        if valid == True:
            yag = yagmail.SMTP('uninortegrupo9b@gmail.com', 'unigrupob')
            yag.send(to=email, subject='Activa tu cuenta',
                     contents='Bienvenido, usa este vínculo para activar tu cuenta ('+request.method+')')
            return verificarCorreo()
        else:
            flash('Correo inválido')
            return render_template('recuperarPassword.html', titulo="Recuperar contraseña", ordenadaFecha=ordenadaFecha)
    else:
        return render_template('recuperarPassword.html', titulo="Recuperar contraseña", ordenadaFecha=ordenadaFecha)


@app.route('/crearCuenta')
def crearCuenta():
    return render_template('crearCuenta.html', titulo="Crear cuenta")


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
