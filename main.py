from flask import Flask
#from models import User, Tickets, Buy
#from schemas import Users_Schema, User_Schema, Buys_Schema, Buy_Schema, Tickets_Schema,Ticket_Schema
from flask import request, jsonify
#from sqlalchemy.exc import SQLAlchemyError, IntegrityError, NoReferenceError, NoReferencedColumnError, NoReferencedTableError, ArgumentError

#from flask import Flask, request, jsonify
#import os
#from flask_sqlalchemy import SQLAlchemy
#from flask_marshmallow import Marshmallow
from server import app , db , ma
from def_api.tickets import  *
from def_api.user import  *
from def_api.buy import  *

'''app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://ADMIN:Shapochka@127.0.0.1/bd_ticket'

db = SQLAlchemy(app)
ma = Marshmallow(app)'''



'''
Users_Schema = UserSchema(many=True)
User_Schema = UserSchema()

Buys_Schema = BuySchema(many=True)
Buy_Schema = BuySchema()

Tickets_Schema = TicketsSchema(many=True)
Ticket_Schema = TicketsSchema()''''''
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

def tickets_post(json):
    # User
    id = json.get('id')
    row = json.get('row')
    place = json.get('place')
    namefilm = json.get('namefilm')
    datatime = json.get('datatime')
    reservation = json.get('reservation')
    buy = json.get('buy')
    ''''''
    Tickets_add = Tickets(id=id, row=row, place=place, namefilm=namefilm,
                       datatime=datatime, reservation=reservation, buy=buy)
    db.session.add(Tickets_add)
    db.session.commit()
    db.session.rollback()
    return (Ticket_Schema.dump(Tickets_add),200)
    ''''''
    try:
        Tickets_add = Tickets(id=id, row=row, place = place, namefilm = namefilm,
                        datatime = datatime, reservation = reservation, buy = buy)
        db.session.add(Tickets_add)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return ("Ticket with such id already exists", 401)
    except NoReferenceError or NoReferencedColumnError or NoReferencedTableError:
        db.session.rollback()
        return ("There aren`t ticket with such id", 400)
    except ArgumentError:
        db.session.rollback()
        return ("Incorrect datatype", 402)
    except SQLAlchemyError as e:
        print(type(e))
        db.session.rollback()
        return ":(((", 401
    else:
        return (Ticket_Schema.dump(Tickets_add),200)

def tickets_get_id(id):
    # User
    try:
        tickets = Tickets.query.get(id)
    except NoResultFound:
        db.session.rollback()
        return ("A tickets with this id was not found" ,404)
    except SQLAlchemyError as e:
        print(type(e))
        db.session.rollback()
        return ":(((", 401
    else:
        return (Ticket_Schema.dump(tickets),200)

def tickets_put_id(id, json):
    ''''''Ticket = Tickets.query.get(id)
    Ticket.row = json.get('row')
    Ticket.place = json.get('place')
    Ticket.namefilm = json.get('namefilm')
    Ticket.datatime = json.get('datatime')
    Ticket.reservation = json.get('reservation')
    Ticket.buy = json.get('buy')''''''

    db.session.commit()

    return (Ticket_Schema.dump(Ticket), 200)

    ''''''
    try:
        Ticket = Tickets.query.get(id)
    except NoResultFound:
        db.session.rollback()
        return ("A ticket with this id was not found", 404)
    Ticket.row = json.get('row')
    Ticket.place = json.get('place')
    Ticket.namefilm = json.get('namefilm')
    Ticket.datatime = json.get('datatime')
    Ticket.reservation = json.get('reservation')
    Ticket.buy = json.get('buy')

    db.session.commit()
    return (Ticket_Schema.dump(Ticket), 200)''''''

    try:
        try:
            Ticket = Tickets.query.get(id)
        except NoResultFound:
            db.session.rollback()
            return ("A ticket with this id was not found", 404)
        Ticket.row = json.get('row')
        Ticket.place = json.get('place')
        Ticket.namefilm = json.get('namefilm')
        Ticket.datatime = json.get('datatime')
        Ticket.reservation = json.get('reservation')
        Ticket.buy = json.get('buy')

        db.session.commit()


    except ArgumentError:
        db.session.rollback()
        return ("incorrect datatype", 402)
    except SQLAlchemyError as e:
        print(type(e))
        db.session.rollback()
        return ":(((", 401
    else:
        return (Ticket_Schema.dump(Ticket), 200)


def tickets_delet_id(id): #check
    try:
        Ticket = Tickets.query.get(id)
    except NoResultFound:
        db.session.rollback()
        return ("A ticket with this id was not found", 404)
    try:
        Tickets.query.filter_by(id=id).delete()
        db.session.commit()
    except SQLAlchemyError as e:
        print(type(e))
        db.session.rollback()
        return ":(((", 401
    else:
        return ("successful operation. Tickets is updated", 200)

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
    try:
        Buy_add = Buy(id=id, name=name, idticket = idticket)
        db.session.add(Buy_add)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return ("buy with such id already exists", 406)
    except NoReferenceError or NoReferencedColumnError or NoReferencedTableError:
        db.session.rollback()
        return ("There aren`t ticket with such id", 400)
    except ArgumentError:
        db.session.rollback()
        return ("Incorrect datatype", 402)
    except SQLAlchemyError as e:
        print(type(e))
        db.session.rollback()
        return ":(((", 401
    else:
        return (Ticket_Schema.dump(Buy_add),200)

def buy_get_id(id):
    try:
       buy = Buy.query.get(id)
       #print(buy.idticket)
    except NoResultFound:
        db.session.rollback()
        return ("A buy with this id was not found" ,404)
    except SQLAlchemyError as e:
        print(type(e))
        db.session.rollback()
        return ":(((" ,401
    else:
        return (Buy_Schema.dump(buy),200)

def buy_put_id(id, json):
    ''''''
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
    return (Buy_Schema.dump(buy), 200)''''''
    try:
        try:
            buy = Buy.query.get(id)
            # print(buy.idticket)
        except NoResultFound:
            db.session.rollback()
            return ("Buy with such id dosent exists", 404)
        buy.name = json.get('name')
        buy.idticket = json.get('idticket')
        db.session.commit()
    except ArgumentError:
        db.session.rollback()
        return ("Incorrect datatype", 402)
    except IntegrityError:
        db.session.rollback()
        return ("Ticket with such id already exists", 401)
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
        try:
            buy = Buy.query.get(id)
            # print(buy.idticket)
        except NoResultFound:
            db.session.rollback()
            return ("Buy with such id dosent exists", 404)
        db.session.delete(buy)
        db.session.commit()
    except SQLAlchemyError as e:
        print(type(e))
        db.session.rollback()
        return (":(((", 401)
    else:
        return (":)))", 200)

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
    try:
        User_add = User(id=id, name=name, username = username, password = password)
        db.session.add(User_add)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return ("user with such id already exists", 406)
    except NoReferenceError or NoReferencedColumnError or NoReferencedTableError:
        db.session.rollback()
        return ("There aren`t ticket with such id", 400)
    except ArgumentError:
        db.session.rollback()
        return ("Incorrect datatype", 402)
    except exc.SQLAlchemyError as e:
        print(type(e))
        db.session.rollback()
        return (":(((" ,401)
    else:
        return (User_Schema.dump(User_add),200)

def  user_get_id(id):
    # User
    try:
        try:
            user = User.query.get(id)
        except NoResultFound:
            db.session.rollback()
            return ("A user with this id was not found", 404)
    except SQLAlchemyError as e:
        print(type(e))
        return (":(((" ,400)
    else:
        return (User_Schema.dump(user),200)

def user_put_id(id, json):

    try:
        try:
            user = User.query.get(id)
        except NoResultFound:
            db.session.rollback()
            return ("A user with this id was not found", 404)
        user.name = json.get('name')
        user.username = json.get('username')
        user.password = json.get('password')
        #db.session.add(user)
        db.session.commit()
    except (ArgumentError ,IntegrityError):
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
        try:
            user = User.query.get(id)
        except NoResultFound:
            db.session.rollback()
            return ("A user with this id was not found", 404)
        User.query.filter_by(id=id).delete()
        db.session.commit()
    except SQLAlchemyError as e:
        print(type(e))
        db.session.rollback()
        return (":(((",401)
    else:
        return (":)))", 200)
'''
##################################
#tickets
##################################
@app.route('/tickets',methods = ['GET'])
def tickets_api_get():
    # User
    res = tickets_get()
    return jsonify(res[0]), res[1]



@app.route('/tickets',methods = ['POST'])
def tickets_api_post():
    res = tickets_post(request.json)
    return res[0] , res[1]


@app.route('/tickets/<int:id>',methods = ['GET'])
def tickets_api_get_id(id):
#tickets_get_id(id)
    res = tickets_get_id(id)

    return jsonify(res[0]) , res[1]



@app.route('/tickets/<int:id>',methods = ['PUT'])
def tickets_api_put_id(id):
    res = tickets_put_id(id,request.json)
    return jsonify(res[0]) , res[1]

@app.route('/tickets/<int:id>',methods = ['DELETE'])
def tickets_api_delete_id(id):
#tickets_get_id(id)
    res = tickets_delet_id(id)
    return  jsonify(res[0]) , res[1]


##################################
#BUY
##################################
@app.route('/buy',methods = ['GET'])
def buy_api_get():
    res = buy_get()
    return jsonify(res[0]), res[1]


@app.route('/buy',methods = ['POST'])
def buy_api_post():
    res = buy_post(request.json)
    return jsonify(res[0]) , res[1]


@app.route('/buy/<int:id>',methods = ['GET'])
def buy_api_get_id(id):
    res = buy_get_id(id)
    return jsonify(res[0]) , res[1]



@app.route('/buy/<int:id>',methods = ['PUT'])
def buy_api_put_id(id):
#tickets_get_id(id)
    res = buy_put_id(id,request.json)
    return jsonify(res[0]) , res[1]

@app.route('/buy/<int:id>',methods = ['DELETE'])
def buy_api_delete_id(id):
#tickets_get_id(id)
    res = buy_delet_id(id)
    return res[0] , res[1]


##################################
#User
##################################
@app.route('/user',methods = ['GET'])
def user_api_get():
    res = user_get()
    return jsonify(res[0]), res[1]


@app.route('/user',methods = ['POST'])
def user_api_post():
    res = user_post(request.json)
    return res[0] , res[1]


@app.route('/user/<int:id>',methods = ['GET'])
def user_api_post_id(id):
#tickets_get_id(id)
    res = user_get_id(id)

    return jsonify(res[0]) , res[1]



@app.route('/user/<int:id>',methods = ['PUT'])
def user_api_put_id(id):
#tickets_get_id(id)
    res = user_put_id(id,request.json)
    return jsonify(res[0]) , res[1]

@app.route('/user/<int:id>',methods = ['DELETE'])
def user_api_delete_id(id):
    res = user_delet_id(id)
    return res[0] , res[1]

if __name__ == '__main__':
    app.run()