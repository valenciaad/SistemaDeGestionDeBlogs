import os

import flask


from classes import db,ma,login_manager

from views import pages

basedir = os.path.abspath(os.path.dirname(__file__))
app = flask.Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'baseDatos.db')



login_manager.init_app(app)
db.init_app(app)
ma.init_app(app)
app.register_blueprint(pages)


