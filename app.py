import os
import flask
from classes import db,ma,login_manager
from datetime import timedelta
from views import pages

basedir = os.path.abspath(os.path.dirname(__file__))
app = flask.Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'baseDatos.db')
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=10)
SQLALCHEMY_TRACK_MODIFICATIONS = False


login_manager.init_app(app)
db.init_app(app)
ma.init_app(app)
app.register_blueprint(pages)

if __name__ == '__main__':
    #app.run(port=80,debug=True)
    app.run(host='0.0.0.0', port=443, ssl_context=('micertificado.cer', 'llaveprivada.pem'))

