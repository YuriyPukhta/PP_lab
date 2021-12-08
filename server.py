from flask import Flask
import os
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt

from config import Config

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:chornobai2002@localhost:3306/bd'
app.config.from_object(Config)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

print("waitress")
db = SQLAlchemy(app)
ma = Marshmallow(app)