from flask import Blueprint, request, jsonify, Response
from flask_bcrypt import Bcrypt
from marshmallow import ValidationError
from sqlalchemy.orm import sessionmaker

from config import DATABASE_URI
from validation import UserSchema
from sqlalchemy import create_engine
from models import User, Product

user = Blueprint('user', __name__)
bcrypt = Bcrypt()
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

session = Session()


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
    hashpassword = bcrypt.generate_password_hash(data['password'])
    users = User(name=data['name'], login=data['login'], password=hashpassword, role=data['role'])
    session.add(users)
    session.commit()
    session.close()
    return Response(response="User successfully created")


@user.route('/users/<id>', methods=['GET'])
def getUserById(id):
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
def updateUser(id):
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
def updateUser(id):
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
def deleteUser(id):
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

