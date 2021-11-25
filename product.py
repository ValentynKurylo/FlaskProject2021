from flask import Blueprint, request, jsonify, Response
from flask_bcrypt import Bcrypt
from marshmallow import ValidationError
from sqlalchemy.orm import sessionmaker

from config import DATABASE_URI
from validation import ProductSchema
from sqlalchemy import create_engine
from models import Product
from user import token_required_user

product = Blueprint('product', __name__)
bcrypt = Bcrypt()
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

session = Session()


@product.route('/products/', methods=['POST'])
@token_required_user
def creatingProduct(current_user):
    if not current_user.role == 'worker' or current_user.role == 'admin':
        return jsonify({'message': 'This is only for workers'})

    data = request.get_json(force=True)
    try:
        ProductSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    session.query(Product).filter_by(name=data['name']).first()
    session.query(Product).filter_by(price=data['price']).first()
    session.query(Product).filter_by(number=data['number']).first()
    users = Product(name=data['name'], price=data['price'], number=data['number'])
    session.add(users)
    session.commit()
    session.close()
    return Response(response="Product successfully created")


@product.route('/products/<id>', methods=['GET'])
def getWorkerById(id):
    id = session.query(Product).filter_by(id=id).first()
    if not id:
        return Response(status=404, response="id doesn't exist")
    biblethump = {'id': id.id, 'name': id.name,  'price': id.price, 'number': id.number}
    return jsonify({'user': biblethump})


@product.route('/productsName/<string:name>', methods=['GET'])
def getWorkerByName(name):
    id = session.query(Product).filter_by(name=name).first()
    if not id:
        return Response(status=404, response="id doesn't exist")
    biblethump = {'id': id.id, 'name': id.name,  'price': id.price, 'number': id.number}
    return jsonify({'user': biblethump})

@product.route('/products', methods=['GET'])
def getWorkers():
    limbo = session.query(Product)
    quer = [ProductSchema().dump(i) for i in limbo]
    if not quer:
        return {"message": "No products available"}, 404
    res = {}
    for i in range(len(quer)):
        res[i + 1] = quer[i]
    return res


@product.route('/products/<id>', methods=['PUT'])
@token_required_user
def updateWorker(current_user, id):
    if not current_user.role == 'worker' or current_user.role == 'admin':
        return jsonify({'message': 'This is only for workers'})

    data = request.get_json(force=True)
    try:
        ProductSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    user_data = session.query(Product).filter_by(id=id).first()
    if not user_data:
        return Response(status=404, response="Id doesn't exist")
    if 'name' in data.keys():
        session.query(Product).filter_by(name=data['name']).first()

        user_data.name = data['name']

    if 'login' in data.keys():
        session.query(Product).filter_by(price=data['price']).first()
        user_data.login = data['price']


    if 'number' in data.keys():
        user_data.number = data['number']

    session.commit()
    session.close()
    return Response(response="Product successfully updated")


@product.route('/products/<id>', methods=['PATCH'])
@token_required_user
def patchProduct(current_user, id):
    if not current_user.role == 'worker' or current_user.role == 'admin':
        return jsonify({'message': 'This is only for workers'})

    data = request.get_json(force=True)
    try:
        ProductSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    user_data = session.query(Product).filter_by(id=id).first()
    if not user_data:
        return Response(status=404, response="Id doesn't exist")
    if 'name' in data.keys():
        session.query(Product).filter_by(name=data['name']).first()

        user_data.name = data['name']

    if 'login' in data.keys():
        session.query(Product).filter_by(price=data['price']).first()
        user_data.login = data['price']


    if 'number' in data.keys():
        user_data.number = data['number']

    session.commit()
    session.close()
    return Response(response="Product successfully updated")

@product.route('/products/<id>', methods=['DELETE'])
@token_required_user
def deleteUser(current_user, id):
    if not current_user.role == 'worker' or current_user.role == 'admin':
        return jsonify({'message': 'This is only for workers'})
    id = session.query(Product).filter_by(id=id).first()
    if not id:
        return Response(status=404, response="ID doesn't exist")
    session.delete(id)
    session.commit()
    session.close()
    return Response(response="Product successfully deleted")