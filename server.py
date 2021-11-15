from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://ADMIN:Shapochka@127.0.0.1/bd_ticket'

bcrypt = Bcrypt(app)


db = SQLAlchemy(app)
ma = Marshmallow(app)