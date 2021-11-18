
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Enum, Float, ForeignKey, engine
from sqlalchemy.orm import sessionmaker
from marshmallow import fields, Schema

app = Flask(__name__)
Base = declarative_base()
db = SQLAlchemy(app)
#role = Enum['user', 'worker', 'admin']
session = sessionmaker(bind=engine)
s = session()
ma = Marshmallow(engine)


class Worker(Base):
    __tablename__ = 'worker'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(255))
    login = Column(String(255))
    password = Column(String(255))
    role = Column(String(255))


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String)
    login = Column(String)
    password = Column(String)
    role = Column(String)


class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String)
    price = Column(Float)
    number = Column(Integer())



class Order(Base):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    product_id = Column(Integer, ForeignKey('product.id'))
    number = Column(Integer)


class ProductDemand(Base):
    __tablename__ = 'ProductDemand'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    product_id = Column(Integer, ForeignKey('product.id'))
    nameProduct = Column(String())




