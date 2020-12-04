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


@app.route('/paginaBlog')
def paginaBlog():
    return render_template('paginaBlog.html')


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
 