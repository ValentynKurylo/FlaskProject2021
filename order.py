from flask import Blueprint, request, jsonify, Response
from flask_bcrypt import Bcrypt
from marshmallow import ValidationError
from sqlalchemy.orm import sessionmaker

from config import DATABASE_URI
from validation import OrderSchema
from sqlalchemy import create_engine
from models import Order, User, Product
from user import token_required_user

order = Blueprint('order', __name__)
bcrypt = Bcrypt()
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

session = Session()


@order.route('/orders/', methods=['POST'])
@token_required_user
def creatingOrder(current_user):
    if not current_user.role == 'user':
        return jsonify({'message': 'This is only for workers'})
    data = request.get_json(force=True)
    try:
        OrderSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    userid = session.query(User).filter_by(id=data['user_id']).first()
    if not userid:
        return Response(status=404, response="User_id doesn't exist")
    productid = session.query(Product).filter_by(id=data['product_id']).first()
    if not productid:
        return Response(status=404, response="product id doesn't exist")
    session.query(Order).filter_by(number=data['number']).first()
    users = Order(user_id=data['user_id'], product_id=data['product_id'], number=data['number'])
    session.add(users)
    session.commit()
    session.close()
    return Response(response="Order successfully created")


@order.route('/orders/<id>', methods=['GET'])
@token_required_user
def getWorkerById(current_worker,  id):
    if not current_worker.role == 'worker' or current_worker.role == 'admin':
        return jsonify({'message': 'This is only for workers'})
    id = session.query(Order).filter_by(id=id).first()
    if not id:
        return Response(status=404, response="id doesn't exist")
    biblethump = {'id': id.id, 'user_id': id.user_id,  'product_id': id.product_id, 'number': id.number}
    return jsonify({'user': biblethump})


@order.route('/orders', methods=['GET'])
@token_required_user
def getWorkers(current_user):
    if not current_user.role == 'worker' or current_user.role == 'admin' or current_user.role == 'user':
        return jsonify({'message': 'This is only for workers'})
    limbo = session.query(Order)
    quer = [OrderSchema().dump(i) for i in limbo]
    if not quer:
        return {"message": "No orders available"}, 404
    res = {}
    for i in range(len(quer)):
        res[i + 1] = quer[i]
    return res



@order.route('/orders/<id>', methods=['DELETE'])
@token_required_user
def deleteUser(current_user, id):
    if not current_user.role == 'admin' or current_user.role == 'user':
        return jsonify({'message': 'This is only for workers'})
    id = session.query(Order).filter_by(id=id).first()
    if not id:
        return Response(status=404, response="ID doesn't exist")
    session.delete(id)
    session.commit()
    session.close()
    return Response(response="Order successfully deleted")