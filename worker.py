
from flask import Blueprint, request, jsonify, Response
from flask_bcrypt import Bcrypt
from marshmallow import ValidationError
from sqlalchemy.orm import sessionmaker

from config import DATABASE_URI
from validation import WorkerSchema
from sqlalchemy import create_engine
from models import Worker

worker = Blueprint('worker', __name__)
bcrypt = Bcrypt()
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

session = Session()


@worker.route('/workers/', methods=['POST'])
def creatingWorker():
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
def getWorkerById(id):
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
def updateWorker(id):
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
def patchWorker(id):
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
def deleteUser(id):
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
