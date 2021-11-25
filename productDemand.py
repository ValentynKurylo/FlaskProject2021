from flask import Blueprint, request, jsonify, Response
from flask_bcrypt import Bcrypt
from marshmallow import ValidationError
from sqlalchemy.orm import sessionmaker

from config import DATABASE_URI
from validation import ProductDemandSchema
from sqlalchemy import create_engine
from models import ProductDemand, User, Product
from user import token_required_user


productDemand = Blueprint('productDemand', __name__)
bcrypt = Bcrypt()
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

session = Session()


@productDemand.route('/productDemands/', methods=['POST'])
@token_required_user
def creatingOrder(current_user):
    if not  current_user.role == 'admin' or current_user.role == 'user':
        return jsonify({'message': 'This is only for workers'})
    data = request.get_json(force=True)
    try:
        ProductDemandSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    userid = session.query(User).filter_by(id=data['user_id']).first()
    if not userid:
        return Response(status=404, response="User_id doesn't exist")
    productid = session.query(Product).filter_by(id=data['product_id']).first()
    if not productid:
        return Response(status=404, response="product id doesn't exist")
    session.query(ProductDemand).filter_by(nameProduct=data['nameProduct']).first()
    users = ProductDemand(user_id=data['user_id'], product_id=data['product_id'], nameProduct=data['nameProduct'])
    session.add(users)
    session.commit()
    session.close()
    return Response(response="Product Demand successfully created")


@productDemand.route('/productDemands/<id>', methods=['GET'])
@token_required_user
def getWorkerById(current_user, id):
    if not current_user.role == 'worker' or current_user.role == 'admin':
        return jsonify({'message': 'This is only for workers'})
    id = session.query(ProductDemand).filter_by(id=id).first()
    if not id:
        return Response(status=404, response="id doesn't exist")
    biblethump = {'id': id.id, 'user_id': id.user_id,  'product_id': id.product_id, 'name': id.name}
    return jsonify({'user': biblethump})

@productDemand.route('/productDemandsUser/<user_id>', methods=['GET'])
@token_required_user
def getWorkerByIdUser(current_user, user_id):
    if not current_user.role == 'worker' or current_user.role == 'admin':
        return jsonify({'message': 'This is only for workers'})
    id = session.query(ProductDemand).filter_by(user_id=user_id).first()
    if not id:
        return Response(status=404, response="id doesn't exist")
    biblethump = {'id': id.id, 'user_id': id.user_id,  'product_id': id.product_id, 'name': id.name}
    return jsonify({'user': biblethump})

@productDemand.route('/productDemands', methods=['GET'])
@token_required_user
def getWorkers(current_user):
    if not current_user.role == 'worker' or current_user.role == 'admin':
        return jsonify({'message': 'This is only for workers'})
    limbo = session.query(ProductDemand)
    quer = [ProductDemandSchema().dump(i) for i in limbo]
    if not quer:
        return {"message": "No product demand available"}, 404
    res = {}
    for i in range(len(quer)):
        res[i + 1] = quer[i]
    return res


@productDemand.route('/productDemandsProduct/<product_id>', methods=['GET'])
@token_required_user
def getWorkerByIdProduct(current_user, product_id):
    if not current_user.role == 'worker' or current_user.role == 'admin':
        return jsonify({'message': 'This is only for workers'})
    id = session.query(ProductDemand).filter_by(product_id=product_id).first()
    if not id:
        return Response(status=404, response="id doesn't exist")
    biblethump = {'id': id.id, 'user_id': id.user_id,  'product_id': id.product_id, 'name': id.name}
    return jsonify({'user': biblethump})




@productDemand.route('/productDemands/<id>', methods=['DELETE'])
@token_required_user
def deleteUser(current_user, id):
    if not current_user.role == 'worker' or current_user.role == 'admin':
        return jsonify({'message': 'This is only for workers'})
    id = session.query(ProductDemand).filter_by(id=id).first()
    if not id:
        return Response(status=404, response="ID doesn't exist")
    session.delete(id)
    session.commit()
    session.close()
    return Response(response="Product Demand successfully deleted")