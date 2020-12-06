from flask import Flask,render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/crearBlog')
def crearBlog():
    return render_template('crearBlog.html')

@app.route('/panelBlog')
def panelBlog():
    return render_template('panelBlog.html')


@app.route('/paginaBlog/')
@app.route('/paginaBlog/<blogId>')
def paginaBlog():
    contenidoBlog = [{"contenido":"Contenido del blog...Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
                    "titulo":"Titulo del blog"}]
    print(contenidoBlog[0]["titulo"])
    return render_template('paginaBlog.html',contenidoBlog=contenidoBlog)


@app.route('/resultadoBusqueda')
def resultadoBusqueda():
    return render_template('resultadoBusqueda.html')


@app.route('/panelUsuario')
def panelUsuario():
    return render_template('panelUsuario.html')


@app.route('/recuperarPassword')
def recuperarPassword():
    return render_template('recuperarPassword.html')


@app.route('/crearCuenta')
def crearCuenta():
    return render_template('crearCuenta.html')
 