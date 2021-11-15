from server import app , db , bcrypt
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, NoReferenceError,\
    NoReferencedColumnError, NoReferencedTableError, ArgumentError, OperationalError, DataError
from flask import request, jsonify
from schemas import Users_Schema, User_Schema, Buys_Schema, Buy_Schema, Tickets_Schema,Ticket_Schema
from models import User, Tickets, Buy
##################################
#User
##################################
def user_get():
    try:
        user = User.query.all()
    except:
        return ("Authentication information is missing or invalid", 401)
    else:
        return (Users_Schema.dump(user),200)

def user_post(json):
    # User
    id = json.get('id')
    name = json.get('name')
    username = json.get('username')
    password = json.get('password')
    if not username or not password or id is None:
        return ("Not none value", 400)
    hash_password = bcrypt.generate_password_hash(password).decode('utf-8')
    try:
        User_add = User(id=id, name=name, username = username, password = hash_password)
        db.session.add(User_add)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return ("user with such id already exists", 406)
    except NoReferenceError or NoReferencedColumnError or NoReferencedTableError:
        db.session.rollback()
        return ("There aren`t ticket with such id", 400)
    except OperationalError:
        db.session.rollback()
        return ("Incorrect datatype", 402)
    except DataError:
        db.session.rollback()
        return ("Too long", 402)
    except SQLAlchemyError as e:
        print(type(e))
        db.session.rollback()
        return (":(((" ,401)
    else:
        return (User_Schema.dump(User_add),200)

def  user_get_id(id):
    # User
    try:
        user = User.query.get(id)
        # print(buy.idticket)
        if not user:
            db.session.rollback()
            return ("A user with this id was not found", 404)
    except SQLAlchemyError as e:
        print(type(e))
        return (":(((" ,400)
    else:
        return (User_Schema.dump(user),200)

def user_put_id(id, json):
    if id != json.get('id'):
        return user_post(json)




    if not json.get('username') or not json.get('password'):
        return ("Not none value", 400)

    try:
        user = User.query.get(id)
        # print(buy.idticket)
        if not user:
            db.session.rollback()
            return ("A user with this id was not found", 404)
        user.name = json.get('name')
        user.username = json.get('username')
        user.password = json.get('password')
        print(bcrypt.generate_password_hash(json.get('password'), 10).decode('utf-8'))
        #db.session.add(user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return ("user with such id already exists", 406)
    except DataError:
        db.session.rollback()
        return ("Too long", 402)
    except (ArgumentError ,OperationalError):
        db.session.rollback()
        return ("Incorrect datatype", 402)
    except SQLAlchemyError as e:
        print(type(e))
        db.session.rollback()
        return (":(((", 401)
    else:
        #db.session.add(user)
        #db.session.commit()
        return (User_Schema.dump(user),200)

def user_delet_id(id): #check

    try:
        user = User.query.get(id)
        # print(buy.idticket)
        if not user:
            db.session.rollback()
            return ("A user with this id was not found", 404)
        db.session.delete(user)
        db.session.commit()
    except SQLAlchemyError as e:
        print(type(e))
        db.session.rollback()
        return (":(((",401)
    else:
        return (":)))", 200)

