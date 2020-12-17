
import os
import os.path
import random

import pdfkit
from flask import (Blueprint, flash, make_response, redirect, render_template,
                   request)
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.utils import secure_filename

from functions import *

pages = Blueprint('pages',__name__, template_folder='templates')
UPLOAD_FOLDER = os.path.abspath(os.getcwd()) + '\static\imagenes'




#C:\Users\adria\.virtualenvs\SistemaDeGestionDeBlogs-Mr4h8l_d\Lib\site-packages\wkhtmltopdf\bin
path_wkhtmltopdf = os.path.abspath(os.getcwd()) + '\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
wkhtmltopdf_options =  {
    'enable-local-file-access': None,
}

@pages.cli.command('db_crear')
def db_crear():
    db.create_all()
    print('Base de datos creada')

@pages.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('Base de datos drop')

@pages.cli.command('db_seed')
def db_seed():
    admin = Usuario(nombre='Prueba',
                       correo = 'uninortegrupo9b@gmail.com',
                       #password = 'Prueba1234',
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
                 id = 1,
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
                 id = 1,
                 estado = True,
                 imagen = 'imagen1.jpg')
    db.session.add(saber)
    db.session.add(haz)

    comentario1 = Comentario(
                       id_blog = '1',
                       id = '2',
                       contenido= 'Esta es una prueba de comentarios'
                       )
    db.session.add(comentario1)
    db.session.commit()
    print('Base de datos seeded')



# login: función asignada a la ruta "/login" que admite los métodos GET and POST
# de acuerdo a la configuración en index.html, se dejó por defecto el método POST
# para enviar la información al servidor, esta recibe el usuario y contraseña y
# los verfica con las funciones ya descritas anteriormente y devuelve errores si los hay
# Cuando son correctos los datos, redirecciona a "/panelBlog"
# En el caso de encontrar un error diferente, ejecuta el código bajo "except"


@pages.route('/')
@pages.route("/login", methods=('GET', 'POST'))
def login():
    #try:
        
        username = request.form.get('user')
        password = request.form.get('pssw')
        remember = request.form.get('recuerdame')
        if remember != None:
            remember = True
        else:  
            remember = False
        error = None        
        usuario = Usuario.query.filter_by(nombre = username ).first()
        #print(usuario)
        if current_user.is_authenticated:
            print(current_user)
            return redirect('/paginaBlog')        
        if usuario and usuario.get_password(password):
            login_user(usuario,  remember = remember) 
            print(current_user)
            return  redirect("/panelBlog")        
        else:
            error = "Usuario o contraseña incorrecto"
            flash(error)
            return render_template("index.html")
        
        #if not isUsernameValid(username):
         #   error = "Usuario incorrecto"
         #   flash(error)
         #   return render_template("index.html")
        #if not isPasswordValid(password):
         #   error = "Contraseña incorrecta"
          #  flash(error)
           # return render_template("index.html")
        
   # except:
        #flash("Error en el inicio de sesión")
        #return render_template("index.html")
# fin código login

@pages.route("/logout", methods=('GET', 'POST'))
@login_required
def logout():
    logout_user()
    return redirect('/login')


@pages.route('/crearBlog', methods=['GET', 'POST'])
@login_required
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
        publico = publico = request.form.get('publico')
        if publico == None:
            publico = False
        else:
            publico = True
        nombreImagen = ""
        if imagen and allowed_file(imagen.filename):
            nombreImagen = secure_filename(str(current_user.nombre)+imagen.filename)
            print(os.path.join(
                UPLOAD_FOLDER, nombreImagen))
            imagen.save(os.path.join(
                UPLOAD_FOLDER, nombreImagen))
        blogC = Blog (titulo = titulo,
                 contenido = contenido,
                 categoria = categoria,
                 id = current_user.id,
                 estado = True,
                 imagen = nombreImagen,
                 publico = publico)
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


@pages.route('/panelBlog', methods=['GET', 'POST'])
@login_required
def panelBlog():
    ordenadaFecha = recientes()
    categoria = "Todas"
    id = current_user.id
    
    if request.method == 'POST':
        categoria = request.form["categoria"]
        if categoria == None:
            categoria = "Todas"
    if categoria == "Todas":
        blogObj = Blog.query.filter_by(id = id, estado = 1)
    else:
        blogObj = Blog.query.filter_by(id = id, estado = 1,categoria=categoria)
    blogs = esBlogs.dump(blogObj)
    return render_template('panelBlog.html',blogs = blogs, titulo="Panel de Blog", ordenadaFecha=ordenadaFecha)


@pages.route('/verificarCorreo')
def verificarCorreo():
    ordenadaFecha = recientes()
    
    return render_template('verificarCorreo.html', titulo="verificar Correo", ordenadaFecha=ordenadaFecha)

@pages.route('/validacion/<validacion>')
def validacion(validacion=''):
    usuario = Usuario.query.filter_by(validacion =validacion ).first()
    if usuario:
         login_user(usuario)
         return redirect('/panelBlog')
    else:
        return 'Codigo invalido'
        
@pages.route('/descagar/<int:blogId>', methods=['GET', 'POST'])
@login_required
def descagar(blogId:int):
    blogObj = Blog.query.filter_by(id_blog = blogId).first()
    contenidoBlog  = esBlog.dump(blogObj) 
    rendered   = render_template('descarga.html',  contenidoBlog=contenidoBlog, titulo=contenidoBlog['titulo'])
    pdf = pdfkit.from_string(rendered, False, css='static/css/estilos.css', configuration=config,options = wkhtmltopdf_options)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['content-Disposition'] = 'inline; filename=archivo.pdf'
    return response
    #return render_template('descarga.html',  contenidoBlog=contenidoBlog, titulo=contenidoBlog['titulo'])

@pages.route('/paginaBlog/', methods=['GET', 'POST'])
@pages.route('/paginaBlog/<int:blogId>', methods=['GET', 'POST'])
@login_required
def paginaBlog(blogId= None):
    try:
        blogObj = Blog.query.filter_by(id_blog = blogId).first()
        #blogObj = Blog.query.all()    
        usuario = current_user
        if blogObj.publico:
            contenidoBlog  = esBlog.dump(blogObj) 
            ordenadaFecha = recientes()
            propio = False
            if blogObj.id == usuario.id:
                propio = True
            
            if request.method == 'POST':
                contenido = request.form["tComentario"]
                id_blog =  blogId
                id = usuario.id
                comentario1 = Comentario(
                            id_blog = id_blog,
                            id = id,
                            contenido= contenido
                            )
                db.session.add(comentario1)
                db.session.commit()        
                return redirect('/paginaBlog/'+str(blogObj.id_blog))
            comentrioOdjetos = db.engine.execute("SELECT id_comentario,  usuarios.nombre ,contenido, usuarios.id from comentarios c inner join usuarios  on  c.id_blog = " + str(blogId) + " and usuarios.id = c.id")
            comentarios = esComenUS.dump(comentrioOdjetos)
        elif blogObj.publico == False and (usuario.id == blogObj.id):
            flash("Este blog es privado")
            contenidoBlog  = esBlog.dump(blogObj) 
            ordenadaFecha = recientes()
            propio = False
            if blogObj.id == usuario.id:
                propio = True
            
            if request.method == 'POST':
                contenido = request.form["tComentario"]
                id_blog =  blogId
                id = usuario.id
                comentario1 = Comentario(
                            id_blog = id_blog,
                            id = id,
                            contenido= contenido
                            )
                db.session.add(comentario1)
                db.session.commit()        
                return redirect('/paginaBlog/'+str(blogObj.id_blog))
            comentrioOdjetos = db.engine.execute("SELECT id_comentario,  usuarios.nombre ,contenido, usuarios.id from comentarios c inner join usuarios  on  c.id_blog = " + str(blogId) + " and usuarios.id = c.id")
            comentarios = esComenUS.dump(comentrioOdjetos)
        else:
            return "<h1>Este blog no es publico <h1>"
        if blogId == None:
            flash("Ups!! Algo salido mal")
            return redirect('/panelUsuario')
        return render_template('paginaBlog.html', propio = propio, comentarios =comentarios,contenidoBlog=contenidoBlog, titulo=contenidoBlog['titulo'], ordenadaFecha=ordenadaFecha)
    except: 
        flash("Ups!! Algo salido mal")
        return redirect('/panelUsuario')       
    
    #print(comentarios)   

# Da la ruta a resultados de busqueda por una palabra ingresada
# Si la palabra no se encuentra en ninguno de los titulos se muestra un mensaje de error
# Muestra la imagen y parte del contenido de los blogs buscados
@pages.route('/resultadoBusqueda/',methods=['GET', 'POST'])
@pages.route('/resultadoBusqueda /<palabra>',methods=['GET', 'POST'])
@login_required
def resultadoBusqueda(palabra ="" ):
    categoria = "Todas"
    ordenadaFecha = recientes()
    if request.method == "POST":
        palabra =  request.form['Buscar']
        categoria = request.form["categoria"]
    if request.method == "GET":
       palabra =  request.args.get('Buscar')  
       categoria  =  request.args.get('categoria')
       if categoria == None:
           categoria = "Todas"
    print(palabra)
    print(categoria)
    if categoria != "Todas":
        objetos = Blog.query.filter_by(estado = 1, categoria = categoria, publico = True)
    else:
        objetos = Blog.query.filter_by(estado = 1,publico = True)
    db = esBlogs.dump(objetos)
    resultados=[] 
    for diccionario in db:
         if (palabra.upper() in diccionario['titulo'].upper()) or (palabra.upper() in diccionario['contenido'].upper())  and diccionario['estado'] == True:                
             resultados.append(diccionario)
    if not resultados or palabra == "":
        resultados = []
        flash('No hay resultados!')
    else:  
        for resultado in resultados:      
            resultado['contenido'] = (resultado["contenido"][:200] + '...')
    return render_template('resultadoBusqueda.html',palabra=palabra, titulo="Resultado de busqueda", ordenadaFecha=ordenadaFecha,resultados=resultados)


@pages.route('/panelUsuario',methods=['GET', 'POST'])
@login_required
def panelUsuario():
    admin = False    
    if current_user.rol == 1:
        admin = True
    ordenadaFecha = recientes()
    objUsuarios = Usuario.query.filter_by(rol=0, estado = 1)
    usuarios = esUsuarios.dump(objUsuarios)
    

    if request.method == "POST":
        usuario =   request.form['usuario']
        print(usuario)
        objUsuario = Usuario.query.filter_by(id = usuario ).first()
        objUsuario.estado = False
        db.session.commit()                
        redirect('/panelUsario')
        
        
    return render_template('panelUsuario.html', admin=admin,usuarios=usuarios,titulo="Panel de usuario", ordenadaFecha=ordenadaFecha)

# crearCuenta: función que permite los métodos GET y POST,
# cuando se hace un llamado se ejecuta el método GET y devuelve
# la página principal "crearCuenta.html". Una vez se envíe
# el formulario se ejecuta el método POST y una vez verificado el
# usuario, la contraseña y el correo electrónico
# se envía un mensaje desde la cuenta de Gmail
# configurada al correo suministrado.
# Esta es asignada a la ruta "/crearCuenta/"


@pages.route('/crearCuenta/', methods=('GET', 'POST'))
def crearCuenta():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['mail']
        password = request.form['pssw']
        validuser = isUsernameValid1(name)        
        if validuser == False:
            flash('Usuario inválido')
            return render_template('crearCuenta.html', titulo="Crear Cuenta")
        validpssw = isPasswordValid(password)
        if validpssw == False:
            flash('Contraseña inválida')
            return render_template('crearCuenta.html', titulo="Crear Cuenta")
        valid = isEmailValid(email)
        if valid == True:            
            nuevoUsuario= Usuario(nombre=name,
                       correo = email,
                       #password = password,
                       rol= 0, # 0 - usuario,  1 - admin
                       estado = True)
            nuevoUsuario.validacion = random.randint(1000,10000)
            nuevoUsuario.set_password(password)
            db.session.add(nuevoUsuario)
            db.session.commit()
            yag = yagmail.SMTP('uninortegrupo9b@gmail.com', 'unigrupob')
            yag.send(to=email, subject='Activa tu cuenta',
                     contents='Bienvenido '+name+', usa este vínculo para activar tu cuenta: http://127.0.0.1:5000/validacion/'+ str (nuevoUsuario.validacion) )
            return verificarCorreo()
        else:
            flash('Correo inválido')
            return render_template('crearCuenta.html', titulo="Crear Cuenta")
    else:
        return render_template('crearCuenta.html', titulo="Crear cuenta")
# Fin crear cuenta


@pages.route('/editar/', methods=['GET','PUT', 'POST'])
@pages.route('/editar/<int:blogId>', methods=['GET','PUT', 'POST'])
@login_required
def editar(blogId=0):
    ordenadaFecha = recientes()
    objeto = Blog.query.filter_by(id_blog = blogId).first()
    if objeto.id == current_user.id:
        contenidoBlog = esBlog.dump(objeto) 
        #now = datetime.now()
        fecha = datetime.utcnow()
        nombreImagen = contenidoBlog['imagen']
        if request.method == 'POST':
            contenido = request.form["cuerpoBlog"]
            titulo = request.form["titulo"]
            categoria = request.form["categorias"]
            publico = request.form.get('publico')
            if publico == None:
                publico = False
            else:
                publico = True
            if request.files["subirImagen"] != None:
                imagen = request.files["subirImagen"]
                if imagen and allowed_file(imagen.filename):
                    nombreImagen = secure_filename(str(id)+imagen.filename)
                    imagen.save(os.path.join(
                        UPLOAD_FOLDER, nombreImagen))
            objeto.contenido = contenido
            objeto.titulo=titulo
            objeto.imagen=nombreImagen
            objeto.fecha=fecha
            objeto.categoria=categoria
            objeto.publico = publico
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
    else:
        return redirect("/panelBlog")    

    return render_template('editar.html', titulo="Editar", ordenadaFecha=ordenadaFecha, contenidoBlog=contenidoBlog)

@pages.route('/eliminar/', methods=['GET','PUT', 'POST'])
@pages.route('/eliminar/<int:blogId>', methods=['GET','PUT', 'POST'])
@login_required
def eliminar(blogId=0):
    ordenadaFecha = recientes()
    objeto = Blog.query.filter_by(id_blog = blogId).first()
    if objeto.id == current_user.id:
        contenidoBlog = esBlog.dump(objeto)
        if request.method == 'POST':
            estado = False
            objeto.estado=estado
            db.session.commit()
            return redirect('/panelBlog')
    else:
        return redirect('/panelBlog')
    return render_template('eliminar.html', titulo="Eliminar", ordenadaFecha=ordenadaFecha, contenidoBlog=contenidoBlog)

# recuperarPassword: función que permite los métodos GET y POST,
# cuando se hace un llamado se ejecuta el método GET y devuelve
# la página principal "recuperarPassword.html". Una vez se envíe
# el formulario se ejecuta el método POST y una vez verificado el
# correo electrónico se envía un mensaje desde la cuenta de Gmail
# configurada al correo suministrado.
# Esta es asignada a la ruta "/recuperarPassword/"


@pages.route('/recuperarPassword/', methods=('GET', 'POST'))
def recuperarPassword():
    ordenadaFecha = recientes()
    if request.method == 'POST':
        email = request.form['mail']
        valid = isEmailValid(email)
        if valid == True:
            usuario = Usuario.query.filter_by(correo = email).first()
            usuario.validacion = random.randint(1000,10000)
            db.session.commit()
            yag = yagmail.SMTP('uninortegrupo9b@gmail.com', 'unigrupob')
            yag.send(to=email, subject='Activa tu cuenta',
                     contents='Bienvenido, usa este vínculo para recuperar  tu contraseña: http://127.0.0.1:5000/recuperar/'+str(usuario.validacion))
            return verificarCorreo()
        else:
            flash('Correo inválido')
            return render_template('recuperarPassword.html', titulo="Recuperar contraseña", ordenadaFecha=ordenadaFecha)
    else:
        return render_template('recuperarPassword.html', titulo="Recuperar contraseña", ordenadaFecha=ordenadaFecha)

@pages.route('/recuperar/<validacion>', methods=('GET', 'POST'))
def recuperar(validacion=''):
    usuario = Usuario.query.filter_by(validacion = validacion).first()
    print(usuario)
    if usuario:
        if request.method == "POST":
            nueva = request.form['pssw']
            usuario.set_password(nueva)
            db.session.commit()
            return redirect('/login')
    else:
        return "Codigo invalido"
    return render_template('recuperar.html')
