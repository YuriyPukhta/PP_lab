from flask import Flask
from flask import request,jsonify,make_response
from server import *
from def_api.tickets import  *
from def_api.user import  *
from def_api.buy import  *
from datetime import datetime, timezone
from def_api.user_login import  *
from flask_jwt import current_identity
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity,JWTManager, get_jwt
from bcrypt import checkpw
from models import User
from schemas import *



##################################
#tickets
##################################
@app.route('/tickets',methods = ['GET'])
@jwt_required()
def tickets_api_get():
    # User
    res = tickets_get()
    return jsonify(res[0]), res[1]


@jwt_required()
@app.route('/tickets',methods = ['POST'])
def tickets_api_post():
    res = tickets_post(request.json)
    return res[0] , res[1]


@app.route('/tickets/<int:id>',methods = ['GET'])
@jwt_required()
def tickets_api_get_id(id):
#tickets_get_id(id)
    res = tickets_get_id(id)
    return jsonify(res[0]) , res[1]


@app.route('/tickets/<int:id>',methods = ['PUT'])
@jwt_required()
def tickets_api_put_id(id):
    res = tickets_put_id(id,request.json)
    return jsonify(res[0]) , res[1]


@app.route('/tickets/<int:id>',methods = ['DELETE'])
@jwt_required()
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
@jwt_required()
def buy_api_post():
    res = buy_post(request.json)
    return jsonify(res[0]) , res[1]

@app.route('/buy/<int:id>',methods = ['GET'])
@jwt_required()
def buy_api_get_id(id):
    res = buy_get_id(id)
    return jsonify(res[0]) , res[1]


@app.route('/buy/<int:id>',methods = ['PUT'])
@jwt_required()
def buy_api_put_id(id):
#tickets_get_id(id)
    res = buy_put_id(id,request.json)
    return jsonify(res[0]), res[1]

@app.route('/buy/<int:id>',methods = ['DELETE'])
@jwt_required()
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


@staticmethod
@app.route('/user', methods=['POST'])
def user_api_post():
    token = user_post(request.json)
    return {'access_token': token}

@staticmethod
@app.route('/login', methods=['POST'])
def login():
    info = request.authorization
    user = User.authenticate(**info)
    if not user:
        return {'message': 'Invalid password'}, 406
    token = user.get_token()
    return {'access_token': token}

@app.route('/logout', methods=['DELETE'])
@jwt_required()
def logout():
        jti = get_jwt()["jti"]
        now = datetime.now(timezone.utc)
        db.session.add(TokenBlockList(jti=jti, created_at=now))
        db.session.commit()
        return jsonify(msg="JWT revoked")

@app.route('/user/<int:id>',methods = ['GET'])
@jwt_required()
def user_api_post_id(id):
#tickets_get_id(id)
    token = user_get_id(id)
    return {'access_token': token}


@app.route('/user/<int:id>',methods = ['PUT'])
@jwt_required()
def user_api_put_id(id):
#tickets_get_id(id)
    res = user_put_id(id,request.json)
    return jsonify(res[0]) , res[1]

@app.route('/user/<int:id>',methods = ['DELETE'])
@jwt_required()
def user_api_delete_id(id):
    res = user_delet_id(id)
    return res[0] , res[1]

jwt = JWTManager(app)


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlockList.id).filter_by(jti=jti).first()
    return token is not None

if __name__ == '__main__':
    app.run()