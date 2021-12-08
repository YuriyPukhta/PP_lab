from server import app, db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, NoReferenceError,\
    NoReferencedColumnError, NoReferencedTableError, ArgumentError, OperationalError, DataError
from flask import request, jsonify
from schemas import Users_Schema, User_Schema, Buys_Schema, Buy_Schema, Tickets_Schema,Ticket_Schema
from models import *
from flask_jwt_extended import jwt_required, get_jwt_identity

from sqlalchemy.orm.exc import NoResultFound

##################################
#BUY
##################################
def buy_get():
    try:
        buy = Buy.query.all()
    except SQLAlchemyError as e:
        print(type(e))
        db.session.rollback()
        return "Authentication information is missing or invalid" ,401


    else:
        return (Buys_Schema.dump(buy),200)
@jwt_required()
def buy_post(json):
    id = json.get('id')
    name = json.get('name')
    idticket = json.get('idticket')
    iduser = json.get('iduser')
    logged_in_user_id = get_jwt_identity()
    users = db.session.query(User).filter(User.id == iduser).first()
    if users.id != logged_in_user_id:
        return {'message': 'Access denied'}, 403
    #Buy.query.get(id)
    if not name or idticket is None or iduser is None or id is None:
        return ("Not none value", 400)
    buy = Buy.query.filter(Buy.idticket == json.get('idticket')).first()
    if not buy :

        try:
            Buy_add = Buy(id=id, name=name, idticket = idticket, iduser = iduser)
            db.session.add(Buy_add)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return ("buy with such id already exists or it is wrong FK", 406)
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
            return ":(((", 401
        else:
            return (Buy_Schema.dump(Buy_add),200)
    else:
        return ("only single ticket", 400)

@jwt_required()
def buy_get_id(id):
    logged_in_user_id = get_jwt_identity()
    buys = db.session.query(Buy).filter(Buy.idticket == id).first()
    if buys.iduser != logged_in_user_id:
        return {'message': 'Access denied'}, 403
    try:
       buy = db.session.query(Buy).filter_by(id=id ).first()
       #print(buy.idticket)
       if not buy:
           db.session.rollback()
           return ("A buy with this id was not found" ,404)
    except SQLAlchemyError as e:
        print(type(e))
        db.session.rollback()
        return ":(((", 401
    else:
        return (Buy_Schema.dump(buy),200)

@jwt_required()
def buy_put_id(id, json):
    iduser = json.get('iduser')
    logged_in_user_id = get_jwt_identity()
    users = db.session.query(User).filter(User.id == iduser).first()
    if users.id != logged_in_user_id:
        return {'message': 'Access denied'}, 403
    if id != json.get('id'):
        return buy_post(json)

    try:
        buy = db.session.query(Buy).filter_by(id=id).first()
        # print(buy.idticket)
        if not buy:
            db.session.rollback()
            return ({"message": "A buy with this id was not found"}, 404)

        #if buy.iduser != json.get('iduser'):
            #return ("you cant do it", 401)
        buy.name = json.get('name')
        buy.idticket = json.get('idticket')
        buy.iduser = json.get('iduser')
        if not json.get('name') or json.get('idticket') is None or json.get('iduser') is None:
            return ("Not none value", 400)
        db.session.commit()
    except OperationalError:
        db.session.rollback()
        return ("Incorrect datatype", 402)
    except DataError:
        db.session.rollback()
        return ("Too long", 402)
    except IntegrityError:
        db.session.rollback()
        return ("Ticket or user  with such id doesn`t  exists", 401)
    except NoReferenceError or NoReferencedColumnError or NoReferencedTableError:
        db.session.rollback()
        return ("There aren`t ticket with such id", 400)
    except SQLAlchemyError as e:
        print(type(e))
        db.session.rollback()
        return (":(((",401)

    else:
            return (Buy_Schema.dump(buy), 200)
@jwt_required()
def buy_delet_id(id): #check
    logged_in_user_id = get_jwt_identity()
    buys = db.session.query(Buy).filter(Buy.idticket == id).first()
    if buys.iduser != logged_in_user_id:
        return {'message': 'Access denied'}, 403
    try:
       buy = db.session.query(Buy).filter_by(id=id ).first()
    # print(buy.idticket)
       if not buy:
          return ("A buy with this id was not found", 404)
       db.session.delete(buy)
       db.session.commit()
       return {"message":"ok"},200
    except SQLAlchemyError as e:
        print(type(e))
        db.session.rollback()
        return (":(((", 401)
    else:
        return (":)))", 200)