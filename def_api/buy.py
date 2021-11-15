from server import app , db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, NoReferenceError,\
    NoReferencedColumnError, NoReferencedTableError, ArgumentError, OperationalError, DataError
from flask import request, jsonify
from schemas import Users_Schema, User_Schema, Buys_Schema, Buy_Schema, Tickets_Schema,Ticket_Schema
from models import User, Tickets, Buy
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

def buy_post(json):
    # User
    id = json.get('id')
    name = json.get('name')
    idticket = json.get('idticket')
    iduser = json.get('iduser')
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


def buy_get_id(id):
    try:
       buy = Buy.query.get(id)
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

def buy_put_id(id, json):
    '''
    try:
        buy = Buy.query.get(id)
        # print(buy.idticket)
    except NoResultFound:
        db.session.rollback()
        return ("Buy with such id dosent exists", 404)
    buy.name = json.get('name')
    buy.idticket = json.get('idticket')
    db.session.commit()''''''
    buy = Buy.query.get(id)
    buy.name = json.get('name')
    print(json.get('name'), buy.name)
    buy.idticket = json.get('idticket')
    db.session.commit()
    print(Buy_Schema.dump(buy))
    return (Buy_Schema.dump(buy), 200)'''
    if id != json.get('id'):
        return buy_post(json)

    try:
        buy = Buy.query.get(id)
        # print(buy.idticket)
        if not buy:
            db.session.rollback()
            return ({"message": "A buy with this id was not found"}, 404)

        if Buy.query.filter(Buy.idticket == json.get('idticket')).first() and buy.iduser != json.get('iduser'):
            return ("only single tickets", 400)

        if Buy.query.filter(Buy.idticket == json.get('idticket')).first().idticket != buy.idticket:
            return ("booked", 400)
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

def buy_delet_id(id): #check

    try:
        buy = Buy.query.get(id)
        # print(buy.idticket)
        if not buy:
            db.session.rollback()
            return ("A buy with this id was not found", 404)
        db.session.delete(buy)
        db.session.commit()
    except SQLAlchemyError as e:
        print(type(e))
        db.session.rollback()
        return (":(((", 401)
    else:
        return (":)))", 200)