from flask import Flask,render_template,request,flash, request, redirect, url_for
from datetime import datetime 
import json
import os.path
from datetime import date
from collections import defaultdict
from werkzeug.utils import secure_filename

UPLOAD_FOLDER =  os.path.abspath(os.getcwd()) + '\static\imagenes'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Lee el archivo db.json y retorna el array ordenado por fecha
# ordenadaFecha - la los datos  del archivo ordenados por fecha
def recientes():
    if os.path.exists('db.json'):
        with open('db.json') as db:
            ordenadaFecha = json.load(db)
            ordenadaFecha.sort(reverse=True,key = lambda x: datetime.strptime(x['fecha'], '%d/%m/%Y,%H:%M:%S')) 
            for i,data in enumerate(ordenadaFecha):
                ordenadaFecha[i]["contenido"] = (data["contenido"][:100] + '...')
    return ordenadaFecha

#Lee el archivo db.json y retorna la fila espesificada 
#row - la fila que se quiere obtener del archivo
def query (row):
    if os.path.exists('db.json'):
        with open('db.json') as jdb:
            db = json.load(jdb)
    return db[row]

# retorna un nuevo id
#id - nuevo id de bog
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

# Escribe datos en db.json 
def write_json(data, filename='db.json'): 
    with open(filename,'w') as f: 
        json.dump(data, f, indent=4)

#limita las extensiones que se pueden subir
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('index.html',titulo="Bienvenido")


@app.route('/crearBlog', methods=['GET','POST'])
def crearBlog():
    ordenadaFecha = recientes() 
    id = existe()
    now = datetime.now()
    fecha = now.strftime("%d/%m/%Y,%H:%M:%S")
    cuerpo={}    
    if request.method =='POST':
        contenido = request.form["cuerpoBlog"]
        titulo = request.form["titulo"]
        imagen = request.files["subirImagen"]
        if imagen and allowed_file(imagen.filename):
            nombreImagen = secure_filename(str(id)+imagen.filename)
            imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], nombreImagen))
        cuerpo = {"contenido": contenido ,
        "titulo": titulo ,
        "blogId": id,
         "imagen": nombreImagen,
        "fecha": fecha}
        if (id != None and contenido != None):
            with open('db.json') as jdb:
                db = json.load(jdb)
                db.append(cuerpo)
                write_json(db)   
                return redirect('/paginaBlog/'+str(id))
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

@app.route('/editar/',methods=['GET','POST'])
@app.route('/editar/<int:blogId>',methods=['GET','POST'])
def editar(blogId=0):    
    ordenadaFecha = recientes() 
    contenidoBlog = query(blogId)
    now = datetime.now()
    fecha = now.strftime("%d/%m/%Y,%H:%M:%S")
    nombreImagen = contenidoBlog['imagen']
    if request.method =='POST':
        contenido = request.form["cuerpoBlog"]
        titulo = request.form["titulo"]
        if request.files["subirImagen"] != None:
            imagen = request.files["subirImagen"]
            if imagen and allowed_file(imagen.filename):
                nombreImagen = secure_filename(str(id)+imagen.filename)
                imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], nombreImagen))           
        cuerpo = {"contenido": contenido ,
        "titulo": titulo ,
        "blogId": blogId,
         "imagen": nombreImagen,
        "fecha": fecha}
        if (id != None and contenido != None):
            with open('db.json') as jdb:
                db = json.load(jdb)
                db[blogId]=cuerpo
                write_json(db)   
                return redirect('/paginaBlog/'+str(blogId))

    return render_template('editar.html',titulo =  "Editar",ordenadaFecha=ordenadaFecha,contenidoBlog =contenidoBlog)
 