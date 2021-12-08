from server import app, db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, NoReferenceError, NoReferencedColumnError, \
    NoReferencedTableError, ArgumentError, OperationalError, DataError
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request, jsonify
from schemas import Users_Schema, User_Schema, Buys_Schema, Buy_Schema, Tickets_Schema,Ticket_Schema
from models import *

##################################
#tickets
##################################
def tickets_get():
    try:
        tickets = Tickets.query.all()
    except:
        db.session.rollback()
        return ("Authentication information is missing or invalid", 401)
    else:
        return (Tickets_Schema.dump(tickets),200)
@jwt_required()
def tickets_post(json):
    id = json.get('id')
    row = json.get('row')
    place = json.get('place')
    namefilm = json.get('namefilm')
    datatime = json.get('datatime')
    reservation = json.get('reservation')
    buy = json.get('buy')
    id_user_create = json.get('id_user_create')
    if User.rang == 'Admin':
        return {"message": "This user is not an Admin."}, 406
    admin = db.session.query(User).filter(User.id == id_user_create).first()
    if admin.rang != 'Admin':
        return {'message': 'Access denied'}, 403
    if json.get('id') is None or json.get('row') is None or json.get('place') \
            is None or not json.get('namefilm') or not json.get('datatime') \
            or not json.get('reservation') or not json.get('buy'):
        return ("Not none value", 400)


    try:
        Tickets_add = Tickets(id=id, row=row, place = place, namefilm = namefilm,
                        datatime = datatime, reservation = reservation, buy = buy,id_user_create =id_user_create)
        db.session.add(Tickets_add)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return ("Ticket with such id already exists", 401)
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
        return (Ticket_Schema.dump(Tickets_add),200)
@jwt_required()
def tickets_get_id(id):
    logged_in_user_id = get_jwt_identity()
    tickets = db.session.query(Tickets).filter(Tickets.id == id).first()
    if tickets.id_user_create != logged_in_user_id:
        return {'message': 'Access denied'}, 403
    try:
        Ticket = Tickets.query.get(id)
        # print(buy.idticket)
        if not Ticket:
            db.session.rollback()
            return ("A ticket with this id was not found", 404)
    except SQLAlchemyError as e:
        print(type(e))
        db.session.rollback()
        return ":(((", 401
    else:
        return (Ticket_Schema.dump(Ticket),200)

@jwt_required()
def tickets_put_id(id, json):
    id_user_create = json.get('id_user_create')
    admin = db.session.query(User).filter(User.id == id_user_create).first()
    if admin.rang != 'Admin':
        return {'message': 'Access denied'}, 403
    if id != json.get('id'):
        return tickets_post(json)
    if json.get('row') is None or json.get('place') is None or not json.get(
            'namefilm') or not json.get('datatime') or not json.get('reservation') or not json.get('buy') \
            or not json.get('id_user_create'):
        return ("Not none value", 400)
    try:
        Ticket = db.session.query(Tickets).filter_by(id=id ).first()
        # print(buy.idticket)
        if not Ticket:
            db.session.rollback()
            return ("A ticket with this id was not found", 404)
        Ticket.row = json.get('row')
        Ticket.place = json.get('place')
        Ticket.namefilm = json.get('namefilm')
        Ticket.datatime = json.get('datatime')
        Ticket.reservation = json.get('reservation')
        Ticket.buy = json.get('buy')
        Ticket.id_user_create = json.get('id_user_create')

        db.session.commit()


    except OperationalError:
        db.session.rollback()
        return ("incorrect datatype", 402)
    except DataError:
        db.session.rollback()
        return ("Too long", 402)
    except SQLAlchemyError as e:
        print(type(e))
        db.session.rollback()
        return ":(((", 401
    else:
        return (Ticket_Schema.dump(Ticket), 200)

@jwt_required()
def tickets_delet_id(id): #check
    logged_in_user_id = get_jwt_identity()
    tickets = db.session.query(Tickets).filter(Tickets.id == id).first()
    if tickets.id_user_create != logged_in_user_id:
        return {'message': 'Access denied'}, 403
    Ticket = db.session.query(Tickets).filter_by(id=id ).first()
    # print(buy.idticket)
    if not Ticket:
        db.session.rollback()
        return ("A ticket with this id was not found", 404)
    try:
        db.session.query(Tickets).filter_by(id=id ).delete()
        db.session.commit()
    except SQLAlchemyError as e:
        print(type(e))
        db.session.rollback()
        return ":(((", 401
    else:
        return ("successful operation. Tickets is updated", 200)
