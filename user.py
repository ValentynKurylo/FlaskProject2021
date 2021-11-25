import datetime
import jwt
from flask import Blueprint, request, jsonify, Response, make_response
from flask_bcrypt import Bcrypt
from marshmallow import ValidationError
from sqlalchemy.orm import sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from flask_httpauth import HTTPBasicAuth

from config import DATABASE_URI, SECRET_KEY
from validation import UserSchema
from sqlalchemy import create_engine
from models import User, Product

user = Blueprint('user', __name__)
bcrypt = Bcrypt()
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

session = Session()



def token_required_user(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'token is missing'}), 401
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = session.query(User).filter_by(id=data['public_id']).first()
        except:
            return jsonify({'message': 'token is not valid!'}), 401

        return f(current_user, *args, **kwargs)
    return decorated


@user.route('/users/', methods=['POST'])
def creatingUser():
    data = request.get_json(force=True)
    try:
        UserSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    session.query(User).filter_by(name=data['name']).first()

    exist = session.query(User).filter_by(login=data['login']).first()
    if exist:
        return Response(status=400, response="Email already exists")
    hashpassword = generate_password_hash(data['password'])
    users = User(name=data['name'], login=data['login'], password=hashpassword, role=data['role'])
    session.add(users)
    session.commit()
    session.close()
    return Response(response="User successfully created")


@user.route('/users/<id>', methods=['GET'])
def getUserById(current_user, id):
    id = session.query(User).filter_by(id=id).first()
    if not id:
        return Response(status=404, response="id doesn't exist")
    biblethump = {'id': id.id, 'name': id.name,  'login': id.login}
    return jsonify({'user': biblethump})


@user.route('/users', methods=['GET'])
def getUsers():
    limbo = session.query(User)
    quer = [UserSchema().dump(i) for i in limbo]
    if not quer:
        return {"message": "No workers available"}, 404
    res = {}
    for i in range(len(quer)):
        res[i + 1] = quer[i]
    return res


@user.route('/users/<id>', methods=['PUT'])
@token_required_user
def updateUser(current_user, id):
    if not current_user.role == 'user' or current_user.role == 'admin':
        return jsonify({'message': 'This is only for users'})
    if 500:
        return jsonify({'message': 'This is only for workers'})
    data = request.get_json(force=True)
    try:
        UserSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    user_data = session.query(User).filter_by(id=id).first()
    if not user_data:
        return Response(status=404, response="Id doesn't exist")
    if 'name' in data.keys():
        session.query(User).filter_by(name=data['name']).first()

        user_data.name = data['name']

    if 'login' in data.keys():
        session.query(User).filter_by(login=data['login']).first()

        user_data.login = data['login']

    if 'password' in data.keys():
        hashpassword = bcrypt.generate_password_hash(data['password'])
        user_data.password = hashpassword

    if 'role' in data.keys():
        user_data.role = data['role']

    session.commit()
    session.close()
    return Response(response="User successfully updated")


@user.route('/users/<id>', methods=['PATCH'])
@token_required_user
def patchUser(current_user, id):
    if not current_user.role == 'user' or current_user.role == 'admin':
        return jsonify({'message': 'This is only for users'})
    if 500:
        return jsonify({'message': 'This is only for workers'})

    data = request.get_json(force=True)
    try:
        UserSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    user_data = session.query(User).filter_by(id=id).first()
    if not user_data:
        return Response(status=404, response="Id doesn't exist")
    if 'name' in data.keys():
        session.query(User).filter_by(name=data['name']).first()

        user_data.name = data['name']

    if 'login' in data.keys():
        session.query(User).filter_by(login=data['login']).first()

        user_data.login = data['login']

    if 'password' in data.keys():
        hashpassword = bcrypt.generate_password_hash(data['password'])
        user_data.password = hashpassword

    if 'role' in data.keys():
        user_data.role = data['role']

    session.commit()
    session.close()
    return Response(response="User successfully updated")

@user.route('/users/<id>', methods=['DELETE'])
@token_required_user
def deleteUser(current_user, id):
    if not current_user.role == 'user' or current_user.role == 'admin':
        return jsonify({'message': 'This is only for users'})
    if 500:
        return jsonify({'message': 'This is only for workers'})

    id = session.query(User).filter_by(id=id).first()
    if not id:
        return Response(status=404, response="ID doesn't exist")
    exist = session.query(Product).filter_by(user_id=id.id).first()
    if exist:
        return Response(status=400, response="This user is a foreign key")
    session.delete(id)
    session.commit()
    session.close()
    return Response(response="Worker successfully deleted")



@user.route('/users/login', methods=['GET'])
def loginUser():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401)

    user = session.query(User).filter_by(login=auth.username).first()

    if not check_password_hash(user.password, auth.password):
        return make_response('Wrong password', 401)

    if user:
        token = jwt.encode({'public_id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, SECRET_KEY)
        return jsonify({'token': token})

    return make_response('problem', 401)



