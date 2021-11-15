
from models import User, Tickets, Buy
from flask import Flask
from flask_marshmallow import Marshmallow
from server import  ma

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        # Fields to expose
        model = User


Users_Schema = UserSchema(many=True)
User_Schema = UserSchema()


class TicketsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Tickets

Tickets_Schema = TicketsSchema(many=True)
Ticket_Schema = TicketsSchema()


class BuySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Buy
        load_instance = True  # Optional: deserialize to model instances

    id = ma.auto_field()
    name = ma.auto_field()
    idticket = ma.auto_field()
    iduser = ma.auto_field()



Buys_Schema = BuySchema(many=True)
Buy_Schema = BuySchema()

#user_schema = UserSchema()
#users_schema = UserSchema(many=True)