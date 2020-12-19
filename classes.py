
from datetime import datetime

from flask_login import LoginManager, UserMixin
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from werkzeug.security import check_password_hash, generate_password_hash
import warnings


db  = SQLAlchemy()
ma = Marshmallow()
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.filter_by(id=user_id).first()

# modelos de  base de datos
class Usuario(db.Model,UserMixin):
    __tablename__ = 'usuarios'
    id = Column (Integer,  primary_key = True, nullable=False)
    nombre = Column (String, nullable=False)
    correo = Column (String, unique=True, nullable=False)
    password = Column (String, nullable=False)
    rol = Column(Integer, nullable=False)
    estado = Column(Boolean, nullable=False)
    fecha = Column (DateTime, nullable=False,default=datetime.utcnow)
    validacion = Column(String)
    def set_password(self,password):
        self.password = generate_password_hash(password)    
    def get_password(self,password):
        return check_password_hash(self.password, password)

class Blog(db.Model):
    __tablename__ = 'blogs'
    id_blog = Column (Integer,  primary_key = True, nullable=False)
    titulo = Column (String, nullable=False)
    contenido = Column (String, nullable=False)
    fecha = Column (DateTime, nullable=False,default=datetime.utcnow)
    categoria = Column (String, nullable=False)
    id = Column(Integer,ForeignKey('usuarios.id') ,nullable=False)
    estado = Column(Boolean, nullable=False)
    imagen = Column (String, unique=True,nullable=False)
    publico = Column(Boolean)
    
class Comentario(db.Model):
    __tablename__ = 'comentarios'
    id_comentario = Column (Integer,  primary_key = True, nullable=False)
    id_blog = Column(Integer,ForeignKey('blogs.id_blog') ,nullable=False)
    id = Column(Integer,ForeignKey('usuarios.id') ,nullable=False)
    contenido = Column (String, nullable=False)
    fecha = Column (DateTime, nullable=False,default=datetime.utcnow)

class EsquemaUsuario(ma.Schema):
    class Meta:
        fields = ('id','nombre','correo','password','rol','estado','fecha')


class EsquemaBlog(ma.Schema):
    class Meta:
        fields = ('id_blog','titulo','contenido','fecha','categoria','id','estado','imagen')

class EsquemaComentario(ma.Schema):
    class Meta:
        fields = ('id_comentario','id_blog','id','contenido','fecha')

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
