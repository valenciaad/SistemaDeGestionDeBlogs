import json
import os.path
from collections import defaultdict
from datetime import date, datetime
import yagmail as yagmail 
from flask import Flask, flash, redirect, render_template, request, url_for, jsonify
from validate_email import validate_email
from werkzeug.utils import secure_filename
import re
#para alchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer,String, Boolean, DateTime, ForeignKey
import os
from flask_marshmallow import Marshmallow


UPLOAD_FOLDER = os.path.abspath(os.getcwd()) + '\static\imagenes'

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Expresión regular que permite verificar la contraseña.
# Puede contener cualquier letra minúscula y mayúscula
# así como números enteros. Su longitud mínima debe ser de 8
pass_reguex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[^\W_]{8,}$"
# Expresión regular que permite verificar el usuario.
# Debe contener cualquier letra minúscula y mayúscula
# así como números enteros. Su longitud mínima debe ser de 8
user_reguex = "^[a-zA-Z0-9_.-]{8,}$"

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'baseDatos.db')

db  = SQLAlchemy(app)
ma = Marshmallow(app)

@app.cli.command('db_crear')
def db_crear():
    db.create_all()
    print('Base de datos creada')

@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('Base de datos drop')

@app.cli.command('db_seed')
def db_seed():
    admin = Usuario(nombre='Prueba',
                       correo = 'uninortegrupo9b@gmail.com',
                       password = 'Prueba1234',
                       rol= 1,# 0 - usuario,  1 - admin
                       estado = True)

    adrian = Usuario(nombre='AdrianValencia',
                       correo = 'test1@test.com',
                       password = 'Prueba1234',
                       rol= 0, # 0 - usuario,  1 - admin
                       estado = True)

    angelica = Usuario(nombre='AngelicaCamargo',
                       correo = 'test2@test.com',
                       password = 'Prueba1234',
                       rol= 0, # 0 - usuario,  1 - admin
                       estado = True)

    daniel = Usuario(nombre='DanieAcosta',
                       correo = 'test3@test.com',
                       password = 'Prueba1234',
                       rol= 0, # 0 - usuario,  1 - admin
                       estado = True)

    oscar = Usuario(nombre='OscarRomero',
                       correo = 'test4@test.com',
                       password = 'Prueba1234',
                       rol= 0, # 0 - usuario,  1 - admin
                       estado = True)

    willian = Usuario(nombre='WillianQuilismal',
                       correo = 'test5@test.com',
                       password = 'Prueba1234',
                       rol= 0, # 0 - usuario,  1 - admin
                       estado = True)
    db.session.add(admin)
    db.session.add(adrian)
    db.session.add(angelica)
    db.session.add(daniel)
    db.session.add(oscar)
    db.session.add(willian)

    saber = Blog (titulo = 'Saber más',
                 contenido = """¿Quiénes somos? BLUSQUEDA es una aplicación web moderna, dinámica y de fácil acceso que te permitirá administrar, manejar, gestionar escritos (blogs) de interés sobre programación y tecnología. Útil para: Blogueros, profesores, estudiantes, emprendedores y profesionales. Personas que buscan compartir su sabiduría con personas que tienen un modo de pensar similar o curiosos interesados en expandir sus conocimientos en campos tan demandados en la actualidad como lo son el de la programación y la tecnología. ¿Cómo funciona?  Una vez registrado en nuestra plataforma, como usuario autenticado BLUSQUEDA te ofrece la opción de crear, actualizar y borrar blogs escritos por ti, o buscar, leer y comentar blogs públicos escritos por alguien más. Crear contenido es muy fácil, consulta Haz que más personas encuentren tu blog online, Pero si lo que buscas es ampliar tus conocimientos, buscar contenido es aún mucho más sencillo solo tienes que ingresar en el panel de búsqueda una palabra clave y listo se desplegarán todos los blogs con el contenido que estás buscando.¡BIENVENIDO A TU MEJOR EXPERIENCIA WEB!""",
                 categoria = 'noticias',
                 id_usuario = 1,
                 estado = True,
                 imagen = 'imagen0.jpg')

    haz = Blog (titulo = 'HAZ QUE MÁS PERSONAS ENCUENTREN TU BLOG ONLINE',
                 contenido = """ Antes de mencionar algunos de los factores que podrían hacer de tu blog algo exitoso, vamos a definir algunos parámetros estándar que podrían determinar el “éxito” en un blog. Estos son una mezcla de visitas, (especialmente esas visitas que luego de un tiempo se convierten en lectores habituales), calidad de los comentarios recibidos, visibilidad de tu blog y reputación.
Ahora sí, estos son algunos consejos que podrían ayudar al éxito de tu blog.
En la actualidad es muy fácil mantenerte en contacto con los visitantes de tu blog mientras está en construcción. Simplemente agrega tu información de contacto, enlaces de tus cuentas sociales; ¡y listo! mientras estás trabajando en el contenido de tu blog permite a tus visitantes suscribirse y estar actualizados.
Escribe sobre lo que te apasiona y capta la atención de esos visitantes que tengan una manera de pensar muy similar a la tuya.
Usa palabras clave en todo tu blog para contribuir a que se muestre más arriba en los resultados de búsqueda.
El contenido de calidad atraerá buenos comentarios y ayudará a tu blog a hacerse de una reputación.
Ser amable con tus lectores y crear una relación cercana con ellos ayudará a que se conviertan en lectores habituales.
Captar y lograr la fidelización de los lectores dependerá en gran medida de que en verdad encuentren lo que están buscando. Si tienes una idea clara de que es lo que quieres transmitir a tus lectores y cómo traducirlo en contenido y, además, eres capaz de organizarlo de una manera sencilla agradable y fácil de entender, habrás dado un gran paso hacia el éxito de tu blog.
Utiliza un diseño atractivo, muchos curiosos en busca de contenido vendrán y echarán un vistazo rápido a tu blog y si no les gusta el estilo probablemente se irán, pero si por el contrario logras en ellos una primera buena impresión, eso te ayudará a captar su atención.
¡BLUSQUEDA TE DESEA EXITOS!""",
                 categoria = 'noticias',
                 id_usuario = 1,
                 estado = True,
                 imagen = 'imagen1.jpg')
    db.session.add(saber)
    db.session.add(haz)

    comentario1 = Comentario(
                       id_blog = '1',
                       id_usuario = '2',
                       contenido= 'Esta es una prueba de comentarios'
                       )
    db.session.add(comentario1)
    db.session.commit()
    print('Base de datos seeded')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = os.urandom(24)
# Lee el archivo db.json y retorna el array ordenado por fecha
# ordenadaFecha - la los datos  del archivo ordenados por fecha

# modelos de  base de datos
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id_usuario = Column (Integer,  primary_key = True, nullable=False)
    nombre = Column (String, nullable=False)
    correo = Column (String, unique=True, nullable=False)
    password = Column (String, nullable=False)
    rol = Column(Integer, nullable=False)
    estado = Column(Boolean, nullable=False)
    fecha = Column (DateTime, nullable=False,default=datetime.utcnow)

class Blog(db.Model):
    __tablename__ = 'blogs'
    id_blog = Column (Integer,  primary_key = True, nullable=False)
    titulo = Column (String, nullable=False)
    contenido = Column (String, nullable=False)
    fecha = Column (DateTime, nullable=False,default=datetime.utcnow)
    categoria = Column (String, nullable=False)
    id_usuario = Column(Integer,ForeignKey('usuarios.id_usuario') ,nullable=False)
    estado = Column(Boolean, nullable=False)
    imagen = Column (String, unique=True,nullable=False)
    
class Comentario(db.Model):
    __tablename__ = 'comentarios'
    id_comentario = Column (Integer,  primary_key = True, nullable=False)
    id_blog = Column(Integer,ForeignKey('blogs.id_blog') ,nullable=False)
    id_usuario = Column(Integer,ForeignKey('usuarios.id_usuario') ,nullable=False)
    contenido = Column (String, nullable=False)
    fecha = Column (DateTime, nullable=False,default=datetime.utcnow)

class EsquemaUsuario(ma.Schema):
    class Meta:
        campos = ('id_usuario','nombre','correo','password','rol','estado','fecha')


class EsquemaBlog(ma.Schema):
    class Meta:
        fields = ('id_blog','titulo','contenido','fecha','categoria','id_usuario','estado','imagen')

class EsquemaComentario(ma.Schema):
    class Meta:
        fields = ('id_comentario','id_blog','id_usuario','contenido','fecha')

class EsquemaComentarioUS(ma.Schema):
    class Meta:
        fields = ('id_comentario','contenido','nombre',)

esUsuario = EsquemaUsuario()
esUsuarios = EsquemaUsuario(many=True)

esBlog = EsquemaBlog()
esBlogs = EsquemaBlog(many=True)

esComentario = EsquemaComentario()
esComentarios = EsquemaComentario(many=True)
esComenUS = EsquemaComentarioUS(many=True)

def recientes():
    objetos = Blog.query.filter_by(estado = 1)
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

# Lee el archivo db.json y retorna la fila espesificada
# row - la fila que se quiere obtener del archivo



def query(row):
    if os.path.exists('db.json'):
        with open('db.json') as jdb:
            db = json.load(jdb)
    return db[row]


# Lee el archivo db.json y retorna un array de dictionarios que en el titulo tienen la palabra ingresada
# palabra - palabra a buscar
#resultados - array de dict con los matches
def queryBuscar(pablara):
    objetos = Blog.query.filter_by(estado = 1)
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
    #print(type(password))
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
    #id = existe()
    #now = datetime.now()
    #fecha = now.strftime("%d/%m/%Y,%H:%M:%S")
    #cuerpo = {}
    if request.method == 'POST':
        contenido = request.form["cuerpoBlog"]
        titulo = request.form["titulo"]
        imagen = request.files["subirImagen"]
        categoria = request.form["categorias"]
        if imagen and allowed_file(imagen.filename):
            nombreImagen = secure_filename(str(id)+imagen.filename)
            imagen.save(os.path.join(
                app.config['UPLOAD_FOLDER'], nombreImagen))
        blogC = Blog (titulo = titulo,
                 contenido = contenido,
                 categoria = categoria,
                 id_usuario = 1,
                 estado = True,
                 imagen = nombreImagen)
        db.session.add(blogC)
        db.session.commit()        
        return redirect('/paginaBlog/'+str(blogC.id_blog))
        #cuerpo = {"contenido": contenido,
        #          "titulo": titulo,
        #         "blogId": id,
        #         "imagen": nombreImagen,
        #         "fecha": fecha}
        #if (id != None and contenido != None):
        #    with open('db.json') as jdb:
        #        db = json.load(jdb)
         #       db.append(cuerpo)
        #        write_json(db)
                
    return render_template('crearBlog.html', titulo="Crear Blog", ordenadaFecha=ordenadaFecha)


@app.route('/panelBlog', methods=['GET', 'POST'])
def panelBlog():
    ordenadaFecha = recientes()
    blogObj = Blog.query.filter_by(id_usuario = 1, estado = 1)
    blogs = esBlogs.dump(blogObj)
    return render_template('panelBlog.html',blogs = blogs, titulo="Panel de Blog", ordenadaFecha=ordenadaFecha)


@app.route('/verificarCorreo')
def verificarCorreo():
    ordenadaFecha = recientes()
    return render_template('verificarCorreo.html', titulo="verificar Correo", ordenadaFecha=ordenadaFecha)


@app.route('/paginaBlog/', methods=['GET', 'POST'])
@app.route('/paginaBlog/<int:blogId>', methods=['GET', 'POST'])
def paginaBlog(blogId:int):
    blogObj = Blog.query.filter_by(id_blog = blogId).first()
    #blogObj = Blog.query.all()    
    contenidoBlog  = esBlog.dump(blogObj) 
    ordenadaFecha = recientes()
    if request.method == 'POST':
        contenido = request.form["tComentario"]
        id_blog =  blogId
        id_usuario = 1
        comentario1 = Comentario(
                       id_blog = id_blog,
                       id_usuario = id_usuario,
                       contenido= contenido
                       )
        db.session.add(comentario1)
        db.session.commit()        
        return redirect('/paginaBlog/'+str(blogObj.id_blog))
    comentrioOdjetos = db.engine.execute("SELECT id_comentario,  u.nombre ,contenido from comentarios, usuarios as u WHERE id_blog = " + str(blogId) +" and u.id_usuario =1") #Comentario.query.filter_by(id_blog = blogId).all()
    comentarios = esComenUS.dump(comentrioOdjetos)
    #print(comentarios)   
    return render_template('paginaBlog.html', comentarios =comentarios,contenidoBlog=contenidoBlog, titulo=contenidoBlog['titulo'], ordenadaFecha=ordenadaFecha)

# Da la ruta a resultados de busqueda por una palabra ingresada
# Si la palabra no se encuentra en ninguno de los titulos se muestra un mensaje de error
# Muestra la imagen y parte del contenido de los blogs buscados
@app.route('/resultadoBusqueda')
@app.route('/resultadoBusqueda /<palabra>',methods=['GET', 'POST'])
def resultadoBusqueda(palabra ="" ):
    if request.method == "POST":
        palabra =  request.form['Buscar']
    else:
       palabra =  request.args.get('Buscar')        
    ordenadaFecha = recientes()
    resultados = queryBuscar(palabra)    
    if not resultados or palabra == "":
        resultados = []
        flash('No hay resultados!')
    else:  
        for resultado in resultados:      
            resultado['contenido'] = (resultado["contenido"][:200] + '...')
    return render_template('resultadoBusqueda.html', titulo="Resultado de busqueda", ordenadaFecha=ordenadaFecha,resultados=resultados)


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


# Inicio crear cuenta

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

# crearCuenta: función que permite los métodos GET y POST,
# cuando se hace un llamado se ejecuta el método GET y devuelve
# la página principal "crearCuenta.html". Una vez se envíe
# el formulario se ejecuta el método POST y una vez verificado el
# usuario, la contraseña y el correo electrónico
# se envía un mensaje desde la cuenta de Gmail
# configurada al correo suministrado.
# Esta es asignada a la ruta "/crearCuenta/"


@app.route('/crearCuenta/', methods=('GET', 'POST'))
def crearCuenta():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['mail']
        password = request.form['pssw']
        validuser = isUsernameValid1(name)
        nuevoUsuario= Usuario(nombre=name,
                       correo = email,
                       password = password,
                       rol= 0, # 0 - usuario,  1 - admin
                       estado = True)
        db.session.add(nuevoUsuario)
        db.session.commit()
        if validuser == False:
            flash('Usuario inválido')
            return render_template('crearCuenta.html', titulo="Crear Cuenta")
        validpssw = isPasswordValid(password)
        if validpssw == False:
            flash('Contraseña inválida')
            return render_template('crearCuenta.html', titulo="Crear Cuenta")
        valid = isEmailValid(email)
        if valid == True:
            yag = yagmail.SMTP('uninortegrupo9b@gmail.com', 'unigrupob')
            yag.send(to=email, subject='Activa tu cuenta',
                     contents='Bienvenido '+name+', usa este vínculo para activar tu cuenta:')
            return verificarCorreo()
        else:
            flash('Correo inválido')
            return render_template('crearCuenta.html', titulo="Crear Cuenta")
    else:
        return render_template('crearCuenta.html', titulo="Crear cuenta")
# Fin crear cuenta


@app.route('/editar/', methods=['GET','PUT', 'POST'])
@app.route('/editar/<int:blogId>', methods=['GET','PUT', 'POST'])
def editar(blogId=0):
    ordenadaFecha = recientes()
    objeto = Blog.query.filter_by(id_blog = blogId).first()
    contenidoBlog = esBlog.dump(objeto) 
    #now = datetime.now()
    fecha = datetime.utcnow()
    nombreImagen = contenidoBlog['imagen']
    if request.method == 'POST':
        contenido = request.form["cuerpoBlog"]
        titulo = request.form["titulo"]
        categoria = request.form["categorias"]
        if request.files["subirImagen"] != None:
            imagen = request.files["subirImagen"]
            if imagen and allowed_file(imagen.filename):
                nombreImagen = secure_filename(str(id)+imagen.filename)
                imagen.save(os.path.join(
                    app.config['UPLOAD_FOLDER'], nombreImagen))
        objeto.contenido = contenido
        objeto.titulo=titulo
        objeto.imagen=nombreImagen
        objeto.fecha=fecha
        objeto.categoria=categoria
        db.session.commit()
        return redirect('/paginaBlog/'+str(objeto.id_blog))
        #cuerpo = {"contenido": contenido,
        #          "titulo": titulo,
        #          "blogId": blogId,
        #          "imagen": nombreImagen,
        #          "fecha": fecha}
        #if (id != None and contenido != None):
        #    with open('db.json') as jdb:
        #        db = json.load(jdb)
        #        db[blogId] = cuerpo
        #        write_json(db)             

    return render_template('editar.html', titulo="Editar", ordenadaFecha=ordenadaFecha, contenidoBlog=contenidoBlog)

@app.route('/eliminar/', methods=['GET','PUT', 'POST'])
@app.route('/eliminar/<int:blogId>', methods=['GET','PUT', 'POST'])
def eliminar(blogId=0):
    ordenadaFecha = recientes()
    objeto = Blog.query.filter_by(id_blog = blogId).first()
    contenidoBlog = esBlog.dump(objeto)
    if request.method == 'POST':
        estado = False
        objeto.estado=estado
        db.session.commit()
        return redirect('/panelBlog')
    return render_template('eliminar.html', titulo="Eliminar", ordenadaFecha=ordenadaFecha, contenidoBlog=contenidoBlog)
