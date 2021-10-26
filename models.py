from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Enum, Float, ForeignKey

Base = declarative_base()

#role = Enum['user', 'worker', 'admin']


class Worker(Base):
    __tablename__ = 'worker'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    login = Column(String)
    password = Column(String)
    role = Column(String)

    def __repr__(self):
        return "<Worker(name='{}')>" \
            .format(self.name)


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String)
    login = Column(String)
    password = Column(String)
    role = Column(String)

    def __repr__(self):
        return "<User(name='{}')>" \
            .format(self.name)


class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String)
    price = Column(Float)
    number = Column(Integer)

    def __repr__(self):
        return "<Product(name='{}', price='{}', number={})>" \
            .format(self.name, self.price, self.number)


class Order(Base):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    product_id = Column(Integer, ForeignKey('product.id'))
    number = Column(Integer)

    def __repr__(self):
        return "<Order(user='{}', product='{}', number={})>" \
            .format(self.user_id, self.product_id, self.number)


class ProductDemand(Base):
    __tablename__ = 'ProductDemand'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    product_id = Column(Integer, ForeignKey('product.id'))
    name = Column(Integer)

    def __repr__(self):
        return "<Order(user='{}', product='{}', name={})>" \
            .format(self.user_id, self.product_id, self.name)

