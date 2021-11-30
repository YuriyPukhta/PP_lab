from typing import List
from flask_sqlalchemy import SQLAlchemy
from server import db

db = SQLAlchemy()
from passlib.hash import bcrypt
from datetime import timedelta
from flask_jwt_extended import create_access_token


class User(db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    username = db.Column(db.String(45))
    password = db.Column(db.String(70))
    rang = db.Column(db.String(70))
    user = db.relationship("Tickets")

    def __init__(self, id, name, username, password,rang):
        self.id = id
        self.name = name
        self.username = username
        self.password = password
        self.rang = rang

    def get_token(self, expire_time=1):
        expire_delta = timedelta(expire_time)
        token = create_access_token(identity=self.id, expires_delta=expire_delta)
        return token

    @classmethod
    def authenticate(cls, username, password):
        user = db.session.query(User).filter_by(username=username).first()
        if not bcrypt.verify(password, user.password):
            return False
        return user

    def __repr__(self):
        return 'ItemModel(name=%s, price=%s,store_id=%s)' % (self.id,
                                                             self.name,
                                                             self.username,
                                                             self.password,
                                                             self.rang)

    # def json(self):
    # return {'name': self.name, 'price': self.price}


''''
    @classmethod
    def find_by_name(cls, name) -> "User":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id) -> "ItemModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["ItemModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
'''


class Tickets(db.Model):
    __tablename__ = "Tickets"
    id = db.Column(db.Integer, primary_key=True)
    row = db.Column(db.Integer)
    place = db.Column(db.Integer)
    namefilm = db.Column(db.String(45))
    datatime = db.Column(db.DATETIME)
    reservation = db.Column(db.String(45))
    buy = db.Column(db.String(45))
    id_user_create = db.Column(db.Integer, db.ForeignKey('User.id'))

    def __init__(self, id, row, place, namefilm, datatime, reservation, buy, id_user_create):
        self.id = id
        self.row = row
        self.place = place
        self.namefilm = namefilm
        self.datatime = datatime
        self.reservation = reservation
        self.buy = buy
        self.id_user_create = id_user_create


class Buy(db.Model):
    __tablename__ = "Buy"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))
    idticket = db.Column(db.Integer, db.ForeignKey('Tickets.id'))
    tickets = db.relationship("Tickets")
    iduser = db.Column(db.Integer, db.ForeignKey('User.id'))
    user = db.relationship("User")

    def __init__(self, id, name, idticket, iduser):
        self.id = id
        self.name = name
        self.idticket = idticket
        self.iduser = iduser

    def __repr__(self):
        return {"id": self.id, "name": self.name, "idticket": self.idticket}


class TokenBlockList(db.Model):
    __tablename__ = "token_block_list"
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)


