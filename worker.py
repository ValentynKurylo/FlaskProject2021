import datetime
from functools import wraps

import jwt
from flask import Blueprint, request, jsonify, Response, make_response
from flask_bcrypt import Bcrypt
from marshmallow import ValidationError
from sqlalchemy.orm import sessionmaker

from config import DATABASE_URI, SECRET_KEY
from validation import WorkerSchema
from sqlalchemy import create_engine
from models import Worker


worker = Blueprint('worker', __name__)
bcrypt = Bcrypt()
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

session = Session()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        print(token)

        if not token:
            return jsonify({'message': 'token is missing'}), 401
        print(jwt.decode(token, SECRET_KEY, algorithms=["HS256"]))
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = session.query(Worker).filter_by(id=data['public_id']).first()
        except:
            return jsonify({'message': 'token is not valid!'}), 401

        return f(current_user, *args, **kwargs)
    return decorated


@worker.route('/workers/', methods=['POST'])
def creatingWorker(current_user):
    data = request.get_json(force=True)
    try:
        WorkerSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    session.query(Worker).filter_by(name=data['name']).first()
    exist = session.query(Worker).filter_by(login=data['login']).first()
    if exist:
        return Response(status=400, response="Email already exists")
    hashpassword = bcrypt.generate_password_hash(data['password'])
    workers = Worker(name=data['name'], login=data['login'], password=hashpassword, role=data['role'])
    session.add(workers)
    session.commit()
    session.close()
    return Response(response="Worker successfully created")


@worker.route('/workers/<id>', methods=['GET'])
@token_required
def getWorkerById(current_user, id):
    if not current_user.role == current_user.role == 'worker' or current_user.role == 'admin':
        return jsonify({'message': 'This is only for workers'})
    if 500:
        return jsonify({'message': 'This is only for workers'})
    id = session.query(Worker).filter_by(id=id).first()
    if not id:
        return Response(status=404, response="id doesn't exist")
    biblethump = {'id': id.id, 'name': id.name,  'login': id.login}
    return jsonify({'worker': biblethump})


@worker.route('/workers', methods=['GET'])
def getWorkers():
    limbo = session.query(Worker)
    quer = [WorkerSchema().dump(i) for i in limbo]
    if not quer:
        return {"message": "No workers available"}, 404
    res = {}
    for i in range(len(quer)):
        res[i + 1] = quer[i]
    return res


@worker.route('/workers/<id>', methods=['PUT'])
@token_required
def updateWorker(current_user, id):
    if not current_user.role == 'worker' or current_user.role == 'admin':
        return jsonify({'message': 'This is only for workers'})
    if 500:
        return jsonify({'message': 'This is only for workers'})
    data = request.get_json(force=True)
    try:
        WorkerSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    user_data = session.query(Worker).filter_by(id=id).first()
    if not user_data:
        return Response(status=404, response="Id doesn't exist")
    if 'name' in data.keys():
        session.query(Worker).filter_by(name=data['name']).first()

        user_data.name = data['name']

    if 'login' in data.keys():
        session.query(Worker).filter_by(login=data['login']).first()

        user_data.login = data['login']

    if 'password' in data.keys():
        hashpassword = bcrypt.generate_password_hash(data['password'])
        user_data.password = hashpassword

    if 'role' in data.keys():
        user_data.role = data['role']

    session.commit()
    session.close()
    return Response(response="Worker successfully updated")


@worker.route('/workers/<id>', methods=['PATCH'])
@token_required
def patchWorker(current_user, id):
    if not current_user.role == 'worker' or current_user.role == 'admin':
        return jsonify({'message': 'This is only for workers'})
    if 500:
        return jsonify({'message': 'This is only for workers'})
    data = request.get_json(force=True)
    try:
        WorkerSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    user_data = session.query(Worker).filter_by(id=id).first()
    if not user_data:
        return Response(status=404, response="Id doesn't exist")
    if 'name' in data.keys():
        session.query(Worker).filter_by(name=data['name']).first()

        user_data.name = data['name']

    if 'login' in data.keys():
        session.query(Worker).filter_by(login=data['login']).first()

        user_data.login = data['login']

    if 'password' in data.keys():
        hashpassword = bcrypt.generate_password_hash(data['password'])
        user_data.password = hashpassword

    if 'role' in data.keys():
        user_data.role = data['role']

    session.commit()
    session.close()
    return Response(response="Worker successfully updated")

@worker.route('/workers/<id>', methods=['DELETE'])
@token_required
def deleteUser(current_user, id):
    if not current_user.role == 'worker' or current_user.role == 'admin':
        return jsonify({'message': 'This is only for workers'})
    if 500:
        return jsonify({'message': 'This is only for workers'})
    id = session.query(Worker).filter_by(id=id).first()
    if not id:
        return Response(status=404, response="ID doesn't exist")
    #exist = session.query(Worker).filter_by(user_id=id.id).first()
    #if exist:
       # return Response(status=400, response="This user is a foreign key")
    session.delete(id)
    session.commit()
    session.close()
    return Response(response="Worker successfully deleted")


@worker.route('/workers/login', methods=['GET'])
def loginUser():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401)

    user = session.query(Worker).filter_by(login=auth.username).first()

    if not user:
        return make_response('Not user', 401)

    if user:
        token = jwt.encode({'public_id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, SECRET_KEY)
        return jsonify({'token': token})

    return make_response('problem', 401)